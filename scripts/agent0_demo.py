#!/usr/bin/env python3
"""
EchoForge Agent Demo - No API Keys Required
A demonstration version that simulates AI responses to showcase the UI and features.
"""

import asyncio
import random
import time
from datetime import datetime
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.layout import Layout
from rich.text import Text
from rich.markdown import Markdown
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

console = Console()

class DemoMetrics:
    """Track demo session metrics."""
    
    def __init__(self):
        self.start_time = time.time()
        self.total_queries = 0
        self.successful_responses = 0
        self.total_tokens = 0
        self.response_times = []
        self.command_history = []
    
    def record_query(self, response_time: float, tokens: int):
        """Record a query's metrics."""
        self.total_queries += 1
        self.successful_responses += 1
        self.total_tokens += tokens
        self.response_times.append(response_time)
        
    def get_avg_response_time(self) -> float:
        """Calculate average response time."""
        return sum(self.response_times) / len(self.response_times) if self.response_times else 0
    
    def get_uptime(self) -> str:
        """Get session uptime."""
        uptime = time.time() - self.start_time
        hours = int(uptime // 3600)
        minutes = int((uptime % 3600) // 60)
        seconds = int(uptime % 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    def to_table(self) -> Table:
        """Generate a rich table with current metrics."""
        table = Table(title="📊 Session Metrics", show_header=True, header_style="bold magenta")
        table.add_column("Metric", style="cyan", no_wrap=True)
        table.add_column("Value", style="green")
        
        table.add_row("Uptime", self.get_uptime())
        table.add_row("Total Queries", str(self.total_queries))
        table.add_row("Successful Responses", str(self.successful_responses))
        table.add_row("Total Tokens (simulated)", f"{self.total_tokens:,}")
        table.add_row("Avg Response Time", f"{self.get_avg_response_time():.2f}s")
        
        return table


class DemoAgent:
    """Simulated AI agent that provides demo responses."""
    
    def __init__(self):
        self.metrics = DemoMetrics()
        self.conversation_history = []
        
        # Pre-defined responses for common queries
        self.demo_responses = {
            "hello": "Hello! 👋 I'm a demo version of EchoForge Agent. I can show you how the interface works without requiring any API keys. Try asking me questions or use commands like /help, /metrics, or /history!",
            "help": "I'm here to demonstrate the EchoForge interface! Here are some things you can try:\n\n• Ask me questions about coding, debugging, or software development\n• Use /metrics to see session statistics\n• Use /history to view conversation history\n• Use /clear to clear the screen\n• Use /exit or /quit to end the session\n\nRemember: I'm a demo, so my responses are simulated!",
            "features": "EchoForge includes:\n\n✨ **Rich Console Interface** - Beautiful, colorful terminal UI\n📊 **Real-time Metrics** - Track queries, tokens, and performance\n🎯 **Command System** - Special commands for control\n💬 **Conversation History** - Keep track of your interactions\n🔧 **Multiple AI Providers** - Support for OpenAI, Anthropic, and more\n⚡ **Async Processing** - Fast and efficient\n\nThis demo showcases all these features without needing API keys!",
            "code": "Sure! Here's an example Python function:\n\n```python\ndef fibonacci(n: int) -> list[int]:\n    \"\"\"Generate Fibonacci sequence up to n terms.\"\"\"\n    if n <= 0:\n        return []\n    elif n == 1:\n        return [0]\n    \n    sequence = [0, 1]\n    for i in range(2, n):\n        sequence.append(sequence[i-1] + sequence[i-2])\n    \n    return sequence\n\n# Example usage\nresult = fibonacci(10)\nprint(result)  # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]\n```\n\nThis demonstrates code syntax highlighting in the EchoForge interface!",
            "debug": "When debugging, I recommend this systematic approach:\n\n1. **Reproduce the issue** - Can you consistently trigger the bug?\n2. **Check the logs** - What error messages or stack traces appear?\n3. **Isolate the problem** - Narrow down which component is failing\n4. **Form a hypothesis** - What do you think is causing it?\n5. **Test your fix** - Verify the solution works\n6. **Add tests** - Prevent regression\n\nRemember: Print statements and debuggers are your friends! 🐛",
        }
    
    async def simulate_response(self, query: str) -> str:
        """Simulate an AI response with realistic delay."""
        # Simulate "thinking" time
        await asyncio.sleep(random.uniform(0.5, 1.5))
        
        # Check for keyword matches
        query_lower = query.lower()
        
        for keyword, response in self.demo_responses.items():
            if keyword in query_lower:
                return response
        
        # Generate a contextual response
        if "?" in query:
            return f"That's a great question! In a production version with real API keys, I would provide a detailed answer about: '{query}'. For now, I'm demonstrating the interface capabilities of EchoForge. The console supports rich formatting, code blocks, tables, and more!"
        else:
            return f"I see you mentioned: '{query[:50]}...'. With real API integration, I could provide in-depth assistance. This demo version showcases how EchoForge handles queries with beautiful formatting and real-time metrics tracking!"
    
    async def process_query(self, query: str) -> str:
        """Process a query and return response with metrics."""
        start_time = time.time()
        
        # Simulate the response
        response = await self.simulate_response(query)
        
        # Calculate metrics
        response_time = time.time() - start_time
        simulated_tokens = random.randint(50, 300)
        
        self.metrics.record_query(response_time, simulated_tokens)
        self.conversation_history.append({
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "query": query,
            "response": response,
            "tokens": simulated_tokens
        })
        
        return response


class DemoInterface:
    """Interactive demo interface for EchoForge."""
    
    def __init__(self):
        self.agent = DemoAgent()
        self.running = True
    
    def display_welcome(self):
        """Display welcome banner."""
        welcome_text = """
# 🎭 EchoForge Agent - Demo Mode

Welcome to the **EchoForge Agent Demo**! This version runs without API keys 
and simulates AI responses to showcase the interface and features.

## Available Commands:
- `/help` - Show available commands
- `/metrics` - Display session metrics
- `/history` - View conversation history
- `/clear` - Clear the screen
- `/exit` or `/quit` - End the session

## Try asking:
- "Show me features"
- "Give me code example"
- "Help with debugging"
- Or any question you'd like!

**Note:** This is a demo - responses are simulated to showcase the UI.
        """
        console.print(Panel(Markdown(welcome_text), 
                          title="🚀 Welcome", 
                          border_style="blue",
                          padding=(1, 2)))
    
    def display_metrics(self):
        """Display current session metrics."""
        console.print(self.agent.metrics.to_table())
    
    def display_history(self):
        """Display conversation history."""
        if not self.agent.conversation_history:
            console.print("[yellow]No conversation history yet.[/yellow]")
            return
        
        table = Table(title="📜 Conversation History", show_header=True)
        table.add_column("Time", style="cyan", no_wrap=True)
        table.add_column("Query", style="yellow")
        table.add_column("Response Preview", style="green")
        table.add_column("Tokens", justify="right", style="magenta")
        
        for entry in self.agent.conversation_history[-10:]:  # Last 10 entries
            response_preview = entry["response"][:50] + "..." if len(entry["response"]) > 50 else entry["response"]
            table.add_row(
                entry["timestamp"],
                entry["query"][:30] + "..." if len(entry["query"]) > 30 else entry["query"],
                response_preview,
                str(entry["tokens"])
            )
        
        console.print(table)
    
    async def handle_command(self, command: str) -> bool:
        """Handle special commands. Returns True if command was handled."""
        command = command.lower().strip()
        
        if command in ["/exit", "/quit"]:
            console.print("\n[bold cyan]Thanks for trying EchoForge Demo! 👋[/bold cyan]")
            self.display_metrics()
            self.running = False
            return True
        
        elif command == "/help":
            self.display_welcome()
            return True
        
        elif command == "/metrics":
            self.display_metrics()
            return True
        
        elif command == "/history":
            self.display_history()
            return True
        
        elif command == "/clear":
            console.clear()
            console.print("[bold green]Screen cleared![/bold green]\n")
            return True
        
        return False
    
    async def process_input(self, user_input: str):
        """Process user input and display response."""
        # Check if it's a command
        if user_input.startswith("/"):
            await self.handle_command(user_input)
            return
        
        # Show processing indicator
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
            transient=True
        ) as progress:
            task = progress.add_task("[cyan]Processing query...", total=None)
            response = await self.agent.process_query(user_input)
        
        # Display the response
        console.print(Panel(
            Markdown(response),
            title="🤖 Agent Response",
            border_style="green",
            padding=(1, 2)
        ))
        console.print()  # Add spacing
    
    async def run(self):
        """Main demo loop."""
        console.clear()
        self.display_welcome()
        console.print()
        
        while self.running:
            try:
                # Get user input
                user_input = await asyncio.get_event_loop().run_in_executor(
                    None,
                    console.input,
                    "[bold blue]You:[/bold blue] "
                )
                
                if not user_input.strip():
                    continue
                
                console.print()  # Add spacing
                await self.process_input(user_input.strip())
                
            except KeyboardInterrupt:
                console.print("\n\n[yellow]Interrupted by user.[/yellow]")
                await self.handle_command("/exit")
                break
            except EOFError:
                await self.handle_command("/exit")
                break
            except Exception as e:
                console.print(f"[red]Error: {e}[/red]")


async def main():
    """Entry point for the demo."""
    try:
        demo = DemoInterface()
        await demo.run()
    except Exception as e:
        console.print(f"[bold red]Fatal error: {e}[/bold red]")
        return 1
    
    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)
