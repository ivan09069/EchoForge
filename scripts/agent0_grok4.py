#!/usr/bin/env python3
"""
Agent0 Grok-4 - Comprehensive Modern AI Agent
=============================================

A production-ready AI agent with advanced features:
- Async streaming responses
- Retry logic with exponential backoff
- Rich console output with progress indicators
- Response caching for performance
- Metrics tracking and analytics
- Webhook notifications
- Multi-model fallback support
- Error handling and logging
- Rate limiting
- Token usage tracking

Author: ivan09069
Date: 2025-12-15
"""

import os
import sys
import json
import time
import asyncio
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, AsyncGenerator
from pathlib import Path
from dataclasses import dataclass, asdict
from enum import Enum
import aiohttp
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    before_sleep_log,
)
import logging
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown
from rich.live import Live
from rich.layout import Layout
from rich import box
from functools import lru_cache
import pickle

# Initialize Rich Console
console = Console()

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("agent0_grok4.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)


class ModelProvider(Enum):
    """Supported AI model providers"""
    XAI_GROK = "xai_grok"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    FALLBACK = "fallback"


@dataclass
class MetricsData:
    """Metrics tracking data structure"""
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    total_tokens: int = 0
    total_latency: float = 0.0
    cache_hits: int = 0
    cache_misses: int = 0
    model_usage: Dict[str, int] = None
    
    def __post_init__(self):
        if self.model_usage is None:
            self.model_usage = {}
    
    @property
    def success_rate(self) -> float:
        if self.total_requests == 0:
            return 0.0
        return (self.successful_requests / self.total_requests) * 100
    
    @property
    def average_latency(self) -> float:
        if self.successful_requests == 0:
            return 0.0
        return self.total_latency / self.successful_requests
    
    @property
    def cache_hit_rate(self) -> float:
        total_cache_ops = self.cache_hits + self.cache_misses
        if total_cache_ops == 0:
            return 0.0
        return (self.cache_hits / total_cache_ops) * 100


class ResponseCache:
    """Simple file-based cache for API responses"""
    
    def __init__(self, cache_dir: str = ".cache", ttl_hours: int = 24):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.ttl = timedelta(hours=ttl_hours)
    
    def _get_cache_key(self, prompt: str, model: str) -> str:
        """Generate cache key from prompt and model"""
        content = f"{model}:{prompt}"
        return hashlib.sha256(content.encode()).hexdigest()
    
    def _get_cache_path(self, key: str) -> Path:
        """Get cache file path"""
        return self.cache_dir / f"{key}.pkl"
    
    def get(self, prompt: str, model: str) -> Optional[str]:
        """Retrieve cached response if valid"""
        key = self._get_cache_key(prompt, model)
        cache_path = self._get_cache_path(key)
        
        if not cache_path.exists():
            return None
        
        try:
            with open(cache_path, "rb") as f:
                cached_data = pickle.load(f)
            
            # Check if cache is still valid
            if datetime.now() - cached_data["timestamp"] > self.ttl:
                cache_path.unlink()  # Remove expired cache
                return None
            
            return cached_data["response"]
        except Exception as e:
            logger.warning(f"Cache read error: {e}")
            return None
    
    def set(self, prompt: str, model: str, response: str):
        """Store response in cache"""
        key = self._get_cache_key(prompt, model)
        cache_path = self._get_cache_path(key)
        
        try:
            cached_data = {
                "timestamp": datetime.now(),
                "response": response,
                "prompt": prompt,
                "model": model,
            }
            with open(cache_path, "wb") as f:
                pickle.dump(cached_data, f)
        except Exception as e:
            logger.warning(f"Cache write error: {e}")
    
    def clear(self):
        """Clear all cached responses"""
        for cache_file in self.cache_dir.glob("*.pkl"):
            cache_file.unlink()
        console.print("[green]Cache cleared successfully[/green]")


class WebhookNotifier:
    """Send webhook notifications for important events"""
    
    def __init__(self, webhook_url: Optional[str] = None):
        self.webhook_url = webhook_url or os.getenv("AGENT_WEBHOOK_URL")
    
    async def send_notification(
        self,
        event_type: str,
        message: str,
        data: Optional[Dict] = None,
        severity: str = "info",
    ):
        """Send webhook notification"""
        if not self.webhook_url:
            return
        
        payload = {
            "event_type": event_type,
            "message": message,
            "severity": severity,
            "timestamp": datetime.now().isoformat(),
            "data": data or {},
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.webhook_url,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=5),
                ) as response:
                    if response.status == 200:
                        logger.info(f"Webhook notification sent: {event_type}")
                    else:
                        logger.warning(f"Webhook failed with status: {response.status}")
        except Exception as e:
            logger.warning(f"Webhook notification error: {e}")


class Agent0Grok4:
    """Advanced AI Agent with comprehensive features"""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "grok-beta",
        temperature: float = 0.7,
        max_tokens: int = 2048,
        enable_cache: bool = True,
        enable_webhooks: bool = False,
        webhook_url: Optional[str] = None,
    ):
        self.api_key = api_key or os.getenv("XAI_API_KEY")
        if not self.api_key:
            raise ValueError("API key not provided. Set XAI_API_KEY environment variable.")
        
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        
        # Model fallback chain
        self.model_fallback_chain = [
            "grok-beta",
            "grok-2-latest",
            "grok-2-1212",
        ]
        
        self.base_url = "https://api.x.ai/v1"
        self.metrics = MetricsData()
        
        # Initialize components
        self.cache = ResponseCache() if enable_cache else None
        self.notifier = WebhookNotifier(webhook_url) if enable_webhooks else None
        
        # Rate limiting
        self.rate_limit_requests = 100
        self.rate_limit_window = 60  # seconds
        self.request_timestamps: List[float] = []
        
        logger.info(f"Agent0 Grok-4 initialized with model: {model}")
    
    def _check_rate_limit(self) -> bool:
        """Check if request is within rate limits"""
        now = time.time()
        # Remove timestamps older than the window
        self.request_timestamps = [
            ts for ts in self.request_timestamps if now - ts < self.rate_limit_window
        ]
        
        if len(self.request_timestamps) >= self.rate_limit_requests:
            return False
        
        self.request_timestamps.append(now)
        return True
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((aiohttp.ClientError, asyncio.TimeoutError)),
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    async def _make_api_request(
        self,
        messages: List[Dict[str, str]],
        model: str,
        stream: bool = False,
    ) -> Any:
        """Make API request with retry logic"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        
        payload = {
            "model": model,
            "messages": messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "stream": stream,
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=aiohttp.ClientTimeout(total=60),
            ) as response:
                response.raise_for_status()
                
                if stream:
                    return response
                else:
                    return await response.json()
    
    async def _try_models_with_fallback(
        self,
        messages: List[Dict[str, str]],
        stream: bool = False,
    ) -> Any:
        """Try models in fallback chain until one succeeds"""
        last_error = None
        
        for model in self.model_fallback_chain:
            try:
                logger.info(f"Trying model: {model}")
                result = await self._make_api_request(messages, model, stream)
                
                # Track model usage
                if model not in self.metrics.model_usage:
                    self.metrics.model_usage[model] = 0
                self.metrics.model_usage[model] += 1
                
                return result, model
            except Exception as e:
                logger.warning(f"Model {model} failed: {e}")
                last_error = e
                continue
        
        raise Exception(f"All models in fallback chain failed. Last error: {last_error}")
    
    async def chat_stream(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
    ) -> AsyncGenerator[str, None]:
        """Stream chat responses with real-time output"""
        
        # Check rate limit
        if not self._check_rate_limit():
            yield "⚠️ Rate limit reached. Please wait before making more requests.\n"
            return
        
        start_time = time.time()
        self.metrics.total_requests += 1
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        try:
            response, model_used = await self._try_models_with_fallback(messages, stream=True)
            
            full_response = ""
            async for line in response.content:
                if line:
                    line_text = line.decode("utf-8").strip()
                    if line_text.startswith("data: "):
                        data_str = line_text[6:]
                        if data_str == "[DONE]":
                            break
                        
                        try:
                            data = json.loads(data_str)
                            if "choices" in data and len(data["choices"]) > 0:
                                delta = data["choices"][0].get("delta", {})
                                content = delta.get("content", "")
                                if content:
                                    full_response += content
                                    yield content
                        except json.JSONDecodeError:
                            continue
            
            # Update metrics
            self.metrics.successful_requests += 1
            latency = time.time() - start_time
            self.metrics.total_latency += latency
            
            # Cache the response
            if self.cache:
                self.cache.set(prompt, model_used, full_response)
            
            # Send webhook notification for long responses
            if self.notifier and len(full_response) > 1000:
                await self.notifier.send_notification(
                    "long_response",
                    f"Generated response of {len(full_response)} characters",
                    {"model": model_used, "latency": latency},
                )
        
        except Exception as e:
            self.metrics.failed_requests += 1
            error_msg = f"❌ Error: {str(e)}\n"
            logger.error(f"Stream error: {e}")
            
            if self.notifier:
                await self.notifier.send_notification(
                    "error",
                    str(e),
                    {"prompt": prompt[:100]},
                    severity="error",
                )
            
            yield error_msg
    
    async def chat(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        use_cache: bool = True,
    ) -> str:
        """Send chat message and get complete response"""
        
        # Check cache first
        if use_cache and self.cache:
            cached_response = self.cache.get(prompt, self.model)
            if cached_response:
                self.metrics.cache_hits += 1
                console.print("[cyan]📦 Response from cache[/cyan]")
                return cached_response
            self.metrics.cache_misses += 1
        
        # Check rate limit
        if not self._check_rate_limit():
            return "⚠️ Rate limit reached. Please wait before making more requests."
        
        start_time = time.time()
        self.metrics.total_requests += 1
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        try:
            with console.status("[bold cyan]Thinking...", spinner="dots"):
                response_data, model_used = await self._try_models_with_fallback(
                    messages, stream=False
                )
            
            response_text = response_data["choices"][0]["message"]["content"]
            
            # Update metrics
            self.metrics.successful_requests += 1
            latency = time.time() - start_time
            self.metrics.total_latency += latency
            
            if "usage" in response_data:
                self.metrics.total_tokens += response_data["usage"].get("total_tokens", 0)
            
            # Cache the response
            if self.cache:
                self.cache.set(prompt, model_used, response_text)
            
            return response_text
        
        except Exception as e:
            self.metrics.failed_requests += 1
            logger.error(f"Chat error: {e}")
            
            if self.notifier:
                await self.notifier.send_notification(
                    "error",
                    str(e),
                    {"prompt": prompt[:100]},
                    severity="error",
                )
            
            return f"❌ Error: {str(e)}"
    
    def display_metrics(self):
        """Display metrics in a rich table"""
        table = Table(title="Agent0 Grok-4 Metrics", box=box.ROUNDED)
        
        table.add_column("Metric", style="cyan", no_wrap=True)
        table.add_column("Value", style="magenta")
        
        table.add_row("Total Requests", str(self.metrics.total_requests))
        table.add_row("Successful", str(self.metrics.successful_requests))
        table.add_row("Failed", str(self.metrics.failed_requests))
        table.add_row("Success Rate", f"{self.metrics.success_rate:.2f}%")
        table.add_row("Total Tokens", str(self.metrics.total_tokens))
        table.add_row("Average Latency", f"{self.metrics.average_latency:.2f}s")
        table.add_row("Cache Hits", str(self.metrics.cache_hits))
        table.add_row("Cache Misses", str(self.metrics.cache_misses))
        table.add_row("Cache Hit Rate", f"{self.metrics.cache_hit_rate:.2f}%")
        
        console.print(table)
        
        # Model usage table
        if self.metrics.model_usage:
            model_table = Table(title="Model Usage", box=box.ROUNDED)
            model_table.add_column("Model", style="cyan")
            model_table.add_column("Requests", style="magenta")
            
            for model, count in self.metrics.model_usage.items():
                model_table.add_row(model, str(count))
            
            console.print(model_table)
    
    def save_metrics(self, filepath: str = "metrics.json"):
        """Save metrics to file"""
        try:
            with open(filepath, "w") as f:
                json.dump(asdict(self.metrics), f, indent=2)
            console.print(f"[green]Metrics saved to {filepath}[/green]")
        except Exception as e:
            logger.error(f"Error saving metrics: {e}")
    
    def clear_cache(self):
        """Clear response cache"""
        if self.cache:
            self.cache.clear()


async def interactive_mode(agent: Agent0Grok4):
    """Interactive chat mode with rich UI"""
    console.print(Panel.fit(
        "[bold cyan]Agent0 Grok-4 Interactive Mode[/bold cyan]\n"
        "Type your messages and get AI responses in real-time.\n"
        "Commands: /metrics, /clear, /cache-clear, /exit",
        border_style="cyan"
    ))
    
    while True:
        try:
            console.print("\n[bold green]You:[/bold green]", end=" ")
            user_input = input().strip()
            
            if not user_input:
                continue
            
            # Handle commands
            if user_input == "/exit":
                console.print("[yellow]Goodbye! 👋[/yellow]")
                break
            elif user_input == "/metrics":
                agent.display_metrics()
                continue
            elif user_input == "/clear":
                console.clear()
                continue
            elif user_input == "/cache-clear":
                agent.clear_cache()
                continue
            
            # Stream response
            console.print("[bold cyan]Agent0:[/bold cyan] ", end="")
            
            full_response = ""
            async for chunk in agent.chat_stream(user_input):
                console.print(chunk, end="")
                full_response += chunk
            
            console.print()  # New line after response
        
        except KeyboardInterrupt:
            console.print("\n[yellow]Interrupted. Type /exit to quit.[/yellow]")
        except Exception as e:
            console.print(f"\n[red]Error: {e}[/red]")


async def batch_mode(agent: Agent0Grok4, prompts: List[str]):
    """Process multiple prompts in batch"""
    console.print(f"[cyan]Processing {len(prompts)} prompts in batch mode...[/cyan]\n")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=console,
    ) as progress:
        task = progress.add_task("[cyan]Processing prompts...", total=len(prompts))
        
        results = []
        for i, prompt in enumerate(prompts, 1):
            progress.update(task, description=f"[cyan]Processing prompt {i}/{len(prompts)}...")
            response = await agent.chat(prompt)
            results.append({"prompt": prompt, "response": response})
            progress.advance(task)
    
    return results


async def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Agent0 Grok-4 - Advanced AI Agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    parser.add_argument(
        "-p", "--prompt",
        type=str,
        help="Single prompt to process"
    )
    parser.add_argument(
        "-f", "--file",
        type=str,
        help="File containing prompts (one per line)"
    )
    parser.add_argument(
        "-i", "--interactive",
        action="store_true",
        help="Start interactive mode"
    )
    parser.add_argument(
        "-m", "--model",
        type=str,
        default="grok-beta",
        help="Model to use (default: grok-beta)"
    )
    parser.add_argument(
        "--no-cache",
        action="store_true",
        help="Disable response caching"
    )
    parser.add_argument(
        "--webhook",
        type=str,
        help="Webhook URL for notifications"
    )
    parser.add_argument(
        "--metrics",
        action="store_true",
        help="Display metrics and exit"
    )
    parser.add_argument(
        "--clear-cache",
        action="store_true",
        help="Clear cache and exit"
    )
    parser.add_argument(
        "--stream",
        action="store_true",
        help="Use streaming mode for single prompt"
    )
    
    args = parser.parse_args()
    
    try:
        # Initialize agent
        agent = Agent0Grok4(
            model=args.model,
            enable_cache=not args.no_cache,
            enable_webhooks=bool(args.webhook),
            webhook_url=args.webhook,
        )
        
        # Handle commands
        if args.clear_cache:
            agent.clear_cache()
            return
        
        if args.metrics:
            agent.display_metrics()
            return
        
        # Interactive mode
        if args.interactive or (not args.prompt and not args.file):
            await interactive_mode(agent)
        
        # Single prompt
        elif args.prompt:
            if args.stream:
                console.print("[bold cyan]Response:[/bold cyan]\n")
                async for chunk in agent.chat_stream(args.prompt):
                    console.print(chunk, end="")
                console.print()
            else:
                response = await agent.chat(args.prompt)
                console.print(Panel(
                    Markdown(response),
                    title="Response",
                    border_style="cyan"
                ))
        
        # Batch mode
        elif args.file:
            with open(args.file, "r") as f:
                prompts = [line.strip() for line in f if line.strip()]
            
            results = await batch_mode(agent, prompts)
            
            # Save results
            output_file = f"results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(output_file, "w") as f:
                json.dump(results, f, indent=2)
            
            console.print(f"[green]Results saved to {output_file}[/green]")
        
        # Display final metrics
        console.print()
        agent.display_metrics()
        
        # Save metrics
        agent.save_metrics()
    
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user[/yellow]")
    except Exception as e:
        console.print(f"[red]Fatal error: {e}[/red]")
        logger.exception("Fatal error in main")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
