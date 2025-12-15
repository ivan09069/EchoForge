# agent0_grok4.py - Agent0 Security Scanner
# Author: Ivan Torres / EchoForge Studios
# Version: 1.0.1 | Date: Dec 11, 2025
# Dependencies: langgraph, openai, python-dotenv

import os
from dotenv import load_dotenv
from typing import Dict, Any, List, TypedDict
from langgraph.graph import StateGraph, END
import asyncio
import json

load_dotenv()

# Use OpenAI-compatible client for xAI Grok API
from openai import AsyncOpenAI


class Grok4Agent:
    """Grok-powered security analysis agent."""
    
    def __init__(self):
        self.client = AsyncOpenAI(
            api_key=os.getenv("GROK_API_KEY"),
            base_url="https://api.x.ai/v1"
        )
        self.model = "grok-3"
        self.system_prompt = """
        You are Agent0 Sentinel: A security scanner for code repositories.
        Scan for: exposed secrets, API keys, seed phrases, vulnerabilities.
        Output JSON: {"findings": [...], "severity": "low|medium|high|critical", "recommendations": [...]}
        """

    async def analyze(self, scan_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze scan results and provide recommendations."""
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": json.dumps(scan_data, indent=2)}
                ],
                temperature=0.1,
                max_tokens=2048
            )
            
            content = response.choices[0].message.content
            return json.loads(content)
            
        except json.JSONDecodeError:
            return {"error": "Failed to parse response", "raw": content}
        except Exception as e:
            return {"error": str(e)}


# LangGraph State Definition
class AgentState(TypedDict, total=False):
    repo_path: str
    scan_results: List[Dict]
    analysis: Dict
    remediated: bool


async def scan_node(state: AgentState) -> AgentState:
    """Scan repository for security issues."""
    # TODO: Integrate actual scanner (YARA rules, regex patterns)
    # Placeholder results for demonstration
    state["scan_results"] = [
        {"type": "secret", "pattern": "API_KEY", "file": "config.py", "line": 12, "severity": "high"},
        {"type": "seed", "pattern": "BIP39", "file": "wallet.py", "line": 42, "severity": "critical"}
    ]
    print(f"[SCAN] Scanning {state.get('repo_path', 'unknown')}...")
    print(f"[SCAN] Found {len(state['scan_results'])} potential issue(s)")
    return state


async def analyze_node(state: AgentState) -> AgentState:
    """Analyze findings with Grok."""
    print("[ANALYZE] Sending to Grok for analysis...")
    agent = Grok4Agent()
    state["analysis"] = await agent.analyze({
        "repo": state.get("repo_path", ""),
        "findings": state.get("scan_results", [])
    })
    print(f"[ANALYZE] Severity: {state['analysis'].get('severity', 'unknown')}")
    return state


async def remediate_node(state: AgentState) -> AgentState:
    """Log recommendations for critical issues."""
    analysis = state.get("analysis", {})
    severity = analysis.get("severity", "low")
    
    if severity in ["critical", "high"]:
        print(f"[REMEDIATE] ⚠️  {severity.upper()} issue detected!")
        for rec in analysis.get("recommendations", []):
            print(f"  → {rec}")
        state["remediated"] = True
    else:
        print("[REMEDIATE] ✅ No critical issues found")
        state["remediated"] = False
    
    return state


def build_agent0_graph() -> StateGraph:
    """Build the LangGraph workflow."""
    workflow = StateGraph(AgentState)
    
    workflow.add_node("scan", scan_node)
    workflow.add_node("analyze", analyze_node)
    workflow.add_node("remediate", remediate_node)
    
    workflow.set_entry_point("scan")
    workflow.add_edge("scan", "analyze")
    workflow.add_edge("analyze", "remediate")
    workflow.add_edge("remediate", END)
    
    return workflow.compile()


async def run_scan(repo_path: str) -> Dict:
    """Run the full Agent0 scan pipeline."""
    print("=" * 50)
    print("🛡️  Agent0 Security Scanner v1.0.1")
    print("=" * 50)
    
    graph = build_agent0_graph()
    result = await graph.ainvoke({"repo_path": repo_path})
    
    print("=" * 50)
    print("Scan complete.")
    return result


if __name__ == "__main__":
    import sys
    
    # Allow repo path as CLI argument
    repo = sys.argv[1] if len(sys.argv) > 1 else "ivan09069/EchoForge"
    
    result = asyncio.run(run_scan(repo))
    print("\n📋 Final Report:")
    print(json.dumps(result, indent=2, default=str))
