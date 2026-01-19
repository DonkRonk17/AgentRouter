#!/usr/bin/env python3
"""
AgentRouter v1.0 - Intelligent Task Routing for Team Brain

Auto-route tasks to the best AI agent based on task type, complexity, cost,
and agent capabilities. Stop manually deciding "who should do this" - let
the router optimize for you!

Author: Atlas (Team Brain)
Requested by: Forge
Date: January 18, 2026
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from collections import defaultdict

VERSION = "1.0.0"

# Routing rules based on task characteristics
ROUTING_RULES = {
    # Task type -> (primary agent, fallback agent, reason)
    "code_execution": ("BOLT", "CLIO", "Free, fast execution"),
    "planning": ("FORGE", "ATLAS", "High quality orchestration"),
    "building": ("ATLAS", "BOLT", "Tool/feature creation specialist"),
    "linux": ("CLIO", "NEXUS", "System administration expert"),
    "testing": ("NEXUS", "ATLAS", "Comprehensive QA"),
    "review": ("FORGE", "NEXUS", "Quality review and architecture"),
    "documentation": ("ATLAS", "FORGE", "Clear technical writing"),
    "debugging": ("NEXUS", "CLIO", "Systematic problem solving"),
    "deployment": ("CLIO", "BOLT", "System deployment expert"),
    "research": ("FORGE", "ATLAS", "Deep analysis and planning")
}

# Agent capabilities and cost
AGENT_PROFILES = {
    "ATLAS": {
        "model": "sonnet-4.5",
        "cost_per_1m_tokens": 3.00,
        "strengths": ["tool_creation", "testing", "documentation", "building"],
        "speed": "fast",
        "availability": "high"
    },
    "FORGE": {
        "model": "opus-4.5",
        "cost_per_1m_tokens": 15.00,
        "strengths": ["planning", "architecture", "review", "complex_tasks"],
        "speed": "medium",
        "availability": "medium"
    },
    "CLIO": {
        "model": "sonnet-4.5",
        "cost_per_1m_tokens": 3.00,
        "strengths": ["linux", "deployment", "system_admin", "automation"],
        "speed": "fast",
        "availability": "high"
    },
    "BOLT": {
        "model": "grok",
        "cost_per_1m_tokens": 0.00,  # Free!
        "strengths": ["execution", "quick_tasks", "testing", "scripts"],
        "speed": "very_fast",
        "availability": "very_high"
    },
    "NEXUS": {
        "model": "sonnet-4.5",
        "cost_per_1m_tokens": 3.00,
        "strengths": ["testing", "qa", "validation", "debugging"],
        "speed": "medium",
        "availability": "medium"
    }
}

# Keywords for task classification
TASK_KEYWORDS = {
    "building": ["build", "create", "make", "develop", "implement", "tool", "feature"],
    "planning": ["plan", "design", "architect", "strategy", "organize", "structure"],
    "testing": ["test", "verify", "validate", "check", "qa", "debug"],
    "code_execution": ["execute", "run", "script", "command", "bash"],
    "linux": ["linux", "ubuntu", "system", "server", "deploy", "ssh"],
    "documentation": ["document", "readme", "write", "doc", "guide"],
    "review": ["review", "analyze", "evaluate", "assess", "critique"],
    "research": ["research", "investigate", "explore", "study", "analyze"],
    "debugging": ["bug", "error", "fix", "broken", "issue", "problem"]
}


@dataclass
class RoutingDecision:
    """Represents a routing decision."""
    task_type: str
    primary_agent: str
    fallback_agent: str
    confidence: float
    reason: str
    estimated_cost: str
    alternative_agents: List[str]


class AgentRouter:
    """
    Intelligent task routing system.
    
    Usage:
        router = AgentRouter()
        
        # Route a task
        decision = router.route("Build a new CLI tool")
        print(f"Assign to: {decision.primary_agent}")
        print(f"Reason: {decision.reason}")
        
        # Get best agent for task type
        agent = router.get_best_agent("testing")
        
        # Find cheapest capable agent
        agent = router.find_cheapest_agent(["building", "documentation"])
    """
    
    def __init__(self, stats_file: Optional[Path] = None):
        """
        Initialize AgentRouter.
        
        Args:
            stats_file: Optional file to track routing statistics
        """
        self.stats_file = stats_file or Path.home() / ".agentrouter_stats.json"
        self.stats = self._load_stats()
    
    def _load_stats(self) -> Dict:
        """Load routing statistics."""
        if self.stats_file.exists():
            try:
                return json.loads(self.stats_file.read_text())
            except:
                return {"total_routes": 0, "by_agent": defaultdict(int), "by_task_type": defaultdict(int)}
        return {"total_routes": 0, "by_agent": {}, "by_task_type": {}}
    
    def _save_stats(self):
        """Save routing statistics."""
        self.stats_file.write_text(json.dumps(self.stats, indent=2))
    
    def classify_task(self, task_description: str) -> Tuple[str, float]:
        """
        Classify task based on description.
        
        Args:
            task_description: Description of the task
        
        Returns:
            Tuple of (task_type, confidence_score)
        """
        desc_lower = task_description.lower()
        scores = defaultdict(float)
        
        # Score each task type based on keyword matches
        for task_type, keywords in TASK_KEYWORDS.items():
            for keyword in keywords:
                if keyword in desc_lower:
                    scores[task_type] += 1.0
        
        if not scores:
            return ("planning", 0.3)  # Default to planning with low confidence
        
        # Get highest scoring task type
        best_type = max(scores.items(), key=lambda x: x[1])
        
        # Normalize confidence to 0-1
        max_possible = len(TASK_KEYWORDS.get(best_type[0], []))
        confidence = min(best_type[1] / max_possible, 1.0)
        
        return (best_type[0], confidence)
    
    def get_best_agent(self, task_type: str) -> str:
        """
        Get best agent for a task type.
        
        Args:
            task_type: Type of task
        
        Returns:
            Agent name
        """
        if task_type in ROUTING_RULES:
            return ROUTING_RULES[task_type][0]
        return "FORGE"  # Default to orchestrator
    
    def find_cheapest_agent(self, required_capabilities: List[str]) -> str:
        """
        Find cheapest agent with required capabilities.
        
        Args:
            required_capabilities: List of required capabilities
        
        Returns:
            Agent name
        """
        candidates = []
        
        for agent, profile in AGENT_PROFILES.items():
            strengths = profile["strengths"]
            # Check if agent has all required capabilities
            if any(cap in strengths for cap in required_capabilities):
                candidates.append((agent, profile["cost_per_1m_tokens"]))
        
        if not candidates:
            return "FORGE"  # Fallback
        
        # Return cheapest
        return min(candidates, key=lambda x: x[1])[0]
    
    def route(self, task_description: str, optimize_for: str = "quality") -> RoutingDecision:
        """
        Route a task to the best agent.
        
        Args:
            task_description: Description of the task
            optimize_for: "quality", "cost", or "speed"
        
        Returns:
            RoutingDecision object
        """
        # Classify task
        task_type, confidence = self.classify_task(task_description)
        
        # Get routing rule
        if task_type in ROUTING_RULES:
            primary, fallback, reason = ROUTING_RULES[task_type]
        else:
            primary, fallback, reason = ("FORGE", "ATLAS", "General task routing")
        
        # Optimize based on criteria
        if optimize_for == "cost":
            # Find cheapest capable agent
            capabilities = TASK_KEYWORDS.get(task_type, [])
            primary = self.find_cheapest_agent(capabilities)
            reason = f"Cost-optimized: {reason}"
        
        elif optimize_for == "speed":
            # Prefer faster agents
            if AGENT_PROFILES[primary]["speed"] not in ["fast", "very_fast"]:
                # Look for faster alternative
                for agent, profile in AGENT_PROFILES.items():
                    if profile["speed"] in ["fast", "very_fast"] and task_type in profile["strengths"]:
                        primary = agent
                        reason = f"Speed-optimized: {reason}"
                        break
        
        # Get alternative agents
        alternatives = [
            agent for agent, profile in AGENT_PROFILES.items()
            if task_type in profile["strengths"] and agent not in [primary, fallback]
        ]
        
        # Estimate cost
        primary_profile = AGENT_PROFILES[primary]
        cost_str = f"${primary_profile['cost_per_1m_tokens']:.2f}/1M tokens"
        if primary_profile['cost_per_1m_tokens'] == 0:
            cost_str = "FREE"
        
        # Update stats
        self.stats["total_routes"] = self.stats.get("total_routes", 0) + 1
        self.stats.setdefault("by_agent", {})[primary] = self.stats.get("by_agent", {}).get(primary, 0) + 1
        self.stats.setdefault("by_task_type", {})[task_type] = self.stats.get("by_task_type", {}).get(task_type, 0) + 1
        self._save_stats()
        
        return RoutingDecision(
            task_type=task_type,
            primary_agent=primary,
            fallback_agent=fallback,
            confidence=confidence,
            reason=reason,
            estimated_cost=cost_str,
            alternative_agents=alternatives
        )
    
    def get_stats(self) -> Dict:
        """Get routing statistics."""
        return self.stats
    
    def get_agent_workload(self) -> Dict[str, int]:
        """Get current workload distribution."""
        return self.stats.get("by_agent", {})


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="AgentRouter - Intelligent task routing for Team Brain",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Route a task
  python agentrouter.py route "Build a new CLI tool"
  
  # Cost-optimized routing
  python agentrouter.py route "Execute Python script" --optimize cost
  
  # Get best agent for task type
  python agentrouter.py best --type testing
  
  # Show routing statistics
  python agentrouter.py stats
        """
    )
    
    parser.add_argument('command', choices=['route', 'best', 'stats', 'workload'],
                        help='Command to execute')
    parser.add_argument('task', nargs='?', help='Task description')
    parser.add_argument('--optimize', choices=['quality', 'cost', 'speed'], default='quality',
                        help='Optimization criteria')
    parser.add_argument('--type', help='Task type for best command')
    parser.add_argument('--version', action='version', version=f'AgentRouter {VERSION}')
    
    args = parser.parse_args()
    
    router = AgentRouter()
    
    if args.command == 'route':
        if not args.task:
            print("ERROR: task description required")
            return 1
        
        decision = router.route(args.task, optimize_for=args.optimize)
        
        print("\n" + "="*60)
        print("ROUTING DECISION")
        print("="*60)
        print(f"Task type: {decision.task_type}")
        print(f"Confidence: {decision.confidence:.0%}")
        print(f"\nPrimary agent: {decision.primary_agent}")
        print(f"Fallback: {decision.fallback_agent}")
        print(f"Estimated cost: {decision.estimated_cost}")
        print(f"\nReason: {decision.reason}")
        if decision.alternative_agents:
            print(f"Alternatives: {', '.join(decision.alternative_agents)}")
        print("="*60 + "\n")
    
    elif args.command == 'best':
        if not args.type:
            print("ERROR: --type required")
            return 1
        
        agent = router.get_best_agent(args.type)
        print(f"\nBest agent for '{args.type}': {agent}\n")
    
    elif args.command == 'stats':
        stats = router.get_stats()
        print("\n=== ROUTING STATISTICS ===")
        print(f"Total routes: {stats.get('total_routes', 0)}")
        print(f"\nBy agent: {stats.get('by_agent', {})}")
        print(f"By task type: {stats.get('by_task_type', {})}\n")
    
    elif args.command == 'workload':
        workload = router.get_agent_workload()
        print("\n=== CURRENT WORKLOAD ===")
        for agent, count in sorted(workload.items(), key=lambda x: x[1], reverse=True):
            print(f"  {agent}: {count} tasks")
        print()
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
