# AgentRouter v1.0

**Intelligent Task Routing for Team Brain**

Stop manually deciding "who should do this task?" - let AgentRouter optimize for quality, cost, or speed automatically!

## Features
- Intelligent task classification (10 task types)
- Cost optimization (route to cheapest capable agent)
- Speed optimization (route to fastest agent)
- Quality routing (route to best specialist)
- Agent capability matching
- Workload tracking
- Statistics and analytics

## Quick Start
```python
from agentrouter import AgentRouter

router = AgentRouter()

# Route a task (quality-optimized by default)
decision = router.route("Build a new CLI tool")
print(f"Assign to: {decision.primary_agent}")  # ATLAS
print(f"Reason: {decision.reason}")

# Cost-optimized routing
decision = router.route("Execute Python script", optimize_for="cost")
print(f"Agent: {decision.primary_agent} ({decision.estimated_cost})")  # BOLT (FREE)

# Speed-optimized routing
decision = router.route("Test the application", optimize_for="speed")

# Get best agent for specific task type
best = router.get_best_agent("testing")  # NEXUS
```

## CLI Usage
```bash
# Route a task
python agentrouter.py route "Build a new tool"

# Cost-optimized
python agentrouter.py route "Run tests" --optimize cost

# Speed-optimized
python agentrouter.py route "Deploy app" --optimize speed

# Get best agent for task type
python agentrouter.py best --type testing

# Show statistics
python agentrouter.py stats

# Check workload distribution
python agentrouter.py workload
```

## Task Types
- **building** → ATLAS (tool/feature creation)
- **planning** → FORGE (architecture/strategy)
- **testing** → NEXUS (comprehensive QA)
- **code_execution** → BOLT (free, fast)
- **linux** → CLIO (system admin)
- **documentation** → ATLAS (technical writing)
- **review** → FORGE (quality review)
- **debugging** → NEXUS (systematic problem solving)
- **deployment** → CLIO (system deployment)
- **research** → FORGE (deep analysis)

## Agent Profiles
- **BOLT**: FREE, very fast, great for execution
- **ATLAS**: $3/1M tokens, fast, building specialist
- **CLIO**: $3/1M tokens, fast, Linux expert
- **NEXUS**: $3/1M tokens, medium, testing specialist
- **FORGE**: $15/1M tokens, medium, best quality

## Optimization Modes
- **quality** (default): Route to best specialist
- **cost**: Route to cheapest capable agent
- **speed**: Route to fastest capable agent

## Credits
**Built by:** Atlas (Team Brain)  
**Requested by:** Forge  
**Date:** January 18, 2026  

**AgentRouter** - Smart routing, better results! 🎯
