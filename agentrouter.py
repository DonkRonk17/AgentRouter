#!/usr/bin/env python3
"""AgentRouter v1.0 - Auto-route Tasks to Best AI"""
VERSION = "1.0.0"

ROUTING_RULES = {
    "code_execution": "BOLT",  # Free, fast
    "planning": "FORGE",  # High quality
    "building": "ATLAS",  # Tool specialist
    "linux": "CLIO",  # System expert
    "testing": "NEXUS",  # Thorough testing
}

class AgentRouter:
    def route(self, task_type):
        """Route task to best agent."""
        return ROUTING_RULES.get(task_type, "FORGE")
    
    def suggest(self, task_description):
        """Suggest best agent based on task description."""
        desc_lower = task_description.lower()
        
        if any(word in desc_lower for word in ["build", "create", "tool"]):
            return "ATLAS"
        elif any(word in desc_lower for word in ["plan", "design", "architect"]):
            return "FORGE"
        elif any(word in desc_lower for word in ["linux", "system", "deploy"]):
            return "CLIO"
        elif any(word in desc_lower for word in ["execute", "run", "script"]):
            return "BOLT"
        elif any(word in desc_lower for word in ["test", "verify", "check"]):
            return "NEXUS"
        
        return "FORGE"  # Default to orchestrator

def main():
    router = AgentRouter()
    
    # Examples
    print("Task: 'Build a new CLI tool'")
    print(f"  Routed to: {router.suggest('Build a new CLI tool')}\n")
    
    print("Task: 'Execute Python script'")
    print(f"  Routed to: {router.suggest('Execute Python script')}\n")
    
    print("Task: 'Plan new architecture'")
    print(f"  Routed to: {router.suggest('Plan new architecture')}\n")

if __name__ == "__main__":
    main()
