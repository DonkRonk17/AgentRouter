# AgentRouter - Integration Plan

## 🎯 INTEGRATION GOALS

This document outlines how AgentRouter integrates with:
1. Team Brain agents (Forge, Atlas, Clio, Nexus, Bolt)
2. Existing Team Brain tools
3. BCH (Beacon Command Hub) - future integration
4. Logan's workflows

AgentRouter is designed to be the **intelligent dispatch layer** for Team Brain, automatically assigning tasks to the optimal agent based on task type, cost constraints, and speed requirements.

---

## 📦 BCH INTEGRATION

### Overview

AgentRouter can be integrated with BCH to provide automatic task routing from the Beacon Command Hub interface. When a task is submitted through BCH, AgentRouter analyzes it and suggests the optimal agent assignment.

### Current Status

**Not yet integrated with BCH** - AgentRouter is currently a standalone CLI/Python tool. BCH integration is planned for Phase 2.

### Planned BCH Commands

```
@agentrouter route "Build a new CLI tool"
→ Returns: ATLAS (building specialist)

@agentrouter route "Execute batch script" --optimize cost
→ Returns: BOLT (free execution)

@agentrouter stats
→ Returns: Routing statistics and workload
```

### Implementation Steps

1. **Phase 1 (Current):** Standalone tool, manual integration
2. **Phase 2:** BCH command handler integration
3. **Phase 3:** Real-time routing recommendations
4. **Phase 4:** Automated task assignment

### BCH Handler Example (Future)

```python
# BCH command handler for AgentRouter
from agentrouter import AgentRouter

router = AgentRouter()

async def handle_agentrouter_command(ctx, args):
    """Handle @agentrouter commands in BCH."""
    command = args[0] if args else "help"
    
    if command == "route":
        task_desc = " ".join(args[1:])
        optimize = ctx.get_flag("optimize", "quality")
        decision = router.route(task_desc, optimize_for=optimize)
        
        return f"""
**Routing Decision**
- Task Type: {decision.task_type}
- Assign To: {decision.primary_agent}
- Fallback: {decision.fallback_agent}
- Reason: {decision.reason}
- Cost: {decision.estimated_cost}
"""
    
    elif command == "stats":
        stats = router.get_stats()
        return f"Total routings: {stats['total_routes']}"
    
    return "Unknown command. Use: route, stats"
```

---

## 🤖 AI AGENT INTEGRATION

### Integration Matrix

| Agent | Primary Use Case | Integration Method | Priority |
|-------|-----------------|-------------------|----------|
| **Forge** | Orchestration oversight, routing review | Python API | HIGH |
| **Atlas** | Auto-route during tool builds | Python API | HIGH |
| **Clio** | Task queue management | CLI + Python | MEDIUM |
| **Nexus** | Multi-platform routing validation | CLI + Python | MEDIUM |
| **Bolt** | Task execution routing | CLI | LOW |

### Agent-Specific Workflows

---

#### FORGE (Orchestrator / Reviewer)

**Primary Use Case:** Oversight of routing decisions and workload balancing

Forge uses AgentRouter to:
- Review suggested task assignments before approval
- Balance workload across agents
- Optimize for cost during budget-constrained periods
- Track routing patterns and efficiency

**Integration Steps:**

1. Import AgentRouter in session startup
2. Use for task planning and assignment
3. Review routing decisions before finalizing
4. Monitor workload distribution

**Example Workflow:**

```python
# Forge session: Planning daily tasks
from agentrouter import AgentRouter

router = AgentRouter()

# Morning task list from Logan
tasks = [
    "Build new ConfigManager feature",
    "Run comprehensive tests on BCH",
    "Deploy updates to production server",
    "Review code for security issues",
    "Research compression algorithms"
]

print("=== DAILY TASK ROUTING ===\n")
for task in tasks:
    decision = router.route(task)
    print(f"Task: {task}")
    print(f"  → Assign to: {decision.primary_agent}")
    print(f"  → Type: {decision.task_type}")
    print(f"  → Cost: {decision.estimated_cost}")
    print()

# Check workload balance
workload = router.get_agent_workload()
print("Workload Distribution:", workload)
```

**Output:**
```
=== DAILY TASK ROUTING ===

Task: Build new ConfigManager feature
  → Assign to: ATLAS
  → Type: building
  → Cost: $3.00/1M tokens

Task: Run comprehensive tests on BCH
  → Assign to: NEXUS
  → Type: testing
  → Cost: $3.00/1M tokens

Task: Deploy updates to production server
  → Assign to: CLIO
  → Type: deployment
  → Cost: $3.00/1M tokens

Task: Review code for security issues
  → Assign to: FORGE
  → Type: review
  → Cost: $15.00/1M tokens

Task: Research compression algorithms
  → Assign to: FORGE
  → Type: research
  → Cost: $15.00/1M tokens

Workload Distribution: {'ATLAS': 1, 'NEXUS': 1, 'CLIO': 1, 'FORGE': 2}
```

---

#### ATLAS (Executor / Builder)

**Primary Use Case:** Self-routing during tool creation sessions

Atlas uses AgentRouter to:
- Determine optimal sub-task assignment during complex builds
- Identify when to delegate tasks to other agents
- Track building patterns for efficiency

**Integration Steps:**

1. Import AgentRouter at session start
2. Route sub-tasks during complex builds
3. Delegate non-building tasks appropriately
4. Log routing decisions for review

**Example Workflow:**

```python
# Atlas session: Building a new tool with sub-tasks
from agentrouter import AgentRouter

router = AgentRouter()

# Sub-tasks for tool creation
sub_tasks = [
    "Implement core functionality",      # Building
    "Write comprehensive tests",          # Testing
    "Deploy to GitHub",                   # Deployment
    "Create documentation"                # Documentation
]

print("=== TOOL BUILD SUB-TASK ROUTING ===\n")
for task in sub_tasks:
    decision = router.route(task)
    if decision.primary_agent == "ATLAS":
        print(f"[SELF] {task}")
    else:
        print(f"[DELEGATE → {decision.primary_agent}] {task}")
        print(f"  Reason: {decision.reason}")
```

**Platform Considerations:**
- Atlas runs on Windows (Cursor IDE)
- Uses Python API primarily
- Integrates with Holy Grail Protocol

---

#### CLIO (Linux / Ubuntu Agent)

**Primary Use Case:** Task queue routing in Linux environment

Clio uses AgentRouter to:
- Route incoming tasks from Synapse
- Manage Linux-specific task assignments
- Handle deployment and system administration routing

**Platform Considerations:**
- Runs on Ubuntu/WSL
- CLI interface preferred
- Integrates with ABIOS startup

**Example:**

```bash
# Clio CLI usage
cd ~/AutoProjects/AgentRouter

# Route a deployment task
python agentrouter.py route "Deploy to Ubuntu server" --optimize speed
# → CLIO (deployment/linux specialist)

# Check current workload
python agentrouter.py workload
# → Shows task distribution

# Route with cost optimization (budget month)
python agentrouter.py route "Execute batch script" --optimize cost
# → BOLT (FREE)
```

**Integration with Clio's Workflow:**

```python
# Clio session: Process Synapse messages
from agentrouter import AgentRouter
from synapselink import SynapseLink

router = AgentRouter()
synapse = SynapseLink()

# Get unassigned tasks from Synapse
messages = synapse.get_messages(unread=True)

for msg in messages:
    if "TASK:" in msg.subject:
        # Extract task description
        task_desc = msg.body.get("description", msg.subject)
        
        # Route the task
        decision = router.route(task_desc)
        
        if decision.primary_agent == "CLIO":
            print(f"[SELF] Handling: {task_desc}")
            # Handle locally
        else:
            print(f"[FORWARD] {task_desc} → {decision.primary_agent}")
            synapse.forward_message(msg, decision.primary_agent)
```

---

#### NEXUS (Multi-Platform Agent)

**Primary Use Case:** Cross-platform routing validation

Nexus uses AgentRouter to:
- Validate routing decisions work across platforms
- Test routing on multiple operating systems
- Verify agent capabilities are correctly mapped

**Cross-Platform Notes:**
- AgentRouter is cross-platform (Python standard library)
- Works on Windows, Linux, macOS
- No platform-specific dependencies

**Example:**

```python
# Nexus: Cross-platform routing test
import platform
from agentrouter import AgentRouter

router = AgentRouter()
current_platform = platform.system()

print(f"Running on: {current_platform}")

# Test routing works the same across platforms
test_tasks = [
    "Build a new tool",
    "Run tests",
    "Deploy to server"
]

for task in test_tasks:
    decision = router.route(task)
    print(f"{task} → {decision.primary_agent}")
```

---

#### BOLT (Free Executor)

**Primary Use Case:** Receive cost-optimized task assignments

Bolt uses AgentRouter to:
- Receive tasks that are cost-optimized
- Handle execution tasks without API costs
- Process bulk operations efficiently

**Cost Considerations:**
- BOLT is FREE (Grok model)
- Ideal for code execution, batch processing
- AgentRouter routes to BOLT when optimize_for="cost"

**Example:**

```bash
# Bolt-friendly CLI usage
python agentrouter.py route "Execute script to process data" --optimize cost
# → BOLT (FREE)

# Bulk task routing
python agentrouter.py route "Run batch file processing" --optimize cost
# → BOLT (FREE)
```

---

## 🔗 INTEGRATION WITH OTHER TEAM BRAIN TOOLS

### With TaskQueuePro

**Task Management Integration**

AgentRouter complements TaskQueuePro by providing intelligent agent assignment for queued tasks.

**Integration Pattern:**

```python
from agentrouter import AgentRouter
from taskqueuepro import TaskQueuePro

router = AgentRouter()
queue = TaskQueuePro()

# Get unassigned tasks
tasks = queue.get_tasks(assigned_to=None)

# Auto-route each task
for task in tasks:
    decision = router.route(task.title)
    
    # Update task with assignment
    queue.update_task(
        task.task_id,
        assigned_to=decision.primary_agent,
        metadata={
            "routing_reason": decision.reason,
            "routing_confidence": decision.confidence,
            "estimated_cost": decision.estimated_cost
        }
    )
    
    print(f"[OK] Assigned '{task.title}' to {decision.primary_agent}")
```

**Benefits:**
- Automatic task assignment
- Tracking of routing decisions
- Workload balancing
- Cost estimation per task

---

### With SynapseLink

**Message Routing Integration**

Route Synapse messages to appropriate agents based on content.

**Integration Pattern:**

```python
from agentrouter import AgentRouter
from synapselink import SynapseLink, quick_send

router = AgentRouter()
synapse = SynapseLink()

# Get latest message
message = synapse.get_latest_message()

# Analyze and route
decision = router.route(message.subject)

# Forward to optimal agent
quick_send(
    decision.primary_agent,
    f"Routed: {message.subject}",
    f"Original from: {message.from_agent}\n"
    f"Routing reason: {decision.reason}\n"
    f"Task type: {decision.task_type}",
    priority="NORMAL"
)
```

---

### With AgentHealth

**Health-Aware Routing**

Consider agent health status when routing tasks.

**Integration Pattern:**

```python
from agentrouter import AgentRouter
from agenthealth import AgentHealth

router = AgentRouter()
health = AgentHealth()

def route_with_health_check(task_desc):
    """Route task considering agent health."""
    decision = router.route(task_desc)
    
    # Check primary agent's health
    primary_health = health.get_status(decision.primary_agent)
    
    if primary_health.get("status") == "inactive":
        # Use fallback agent
        return decision.fallback_agent
    
    return decision.primary_agent
```

---

### With TokenTracker

**Cost-Aware Routing**

Use TokenTracker data for budget-conscious routing.

**Integration Pattern:**

```python
from agentrouter import AgentRouter
from tokentracker import TokenTracker

router = AgentRouter()
tracker = TokenTracker()

# Get budget status
budget_remaining = tracker.get_remaining_budget()

# Determine optimization mode
if budget_remaining < 10:  # Low budget
    optimize_mode = "cost"
elif budget_remaining > 50:  # High budget
    optimize_mode = "quality"
else:
    optimize_mode = "quality"  # Default

# Route with appropriate optimization
decision = router.route(task_desc, optimize_for=optimize_mode)
```

---

### With ContextCompressor

**Token-Efficient Routing Messages**

Compress routing decisions before sending to agents.

**Integration Pattern:**

```python
from agentrouter import AgentRouter
from contextcompressor import ContextCompressor

router = AgentRouter()
compressor = ContextCompressor()

# Get routing decision
decision = router.route("Build comprehensive test suite")

# Create detailed routing message
routing_message = f"""
Task: Build comprehensive test suite
Assigned to: {decision.primary_agent}
Task Type: {decision.task_type}
Confidence: {decision.confidence:.0%}
Reason: {decision.reason}
Estimated Cost: {decision.estimated_cost}
Alternatives: {', '.join(decision.alternative_agents)}
"""

# Compress for efficiency
compressed = compressor.compress_text(routing_message)
# Use compressed message for Synapse
```

---

### With ConfigManager

**Centralized Routing Configuration**

Store routing preferences in ConfigManager.

**Integration Pattern:**

```python
from agentrouter import AgentRouter
from configmanager import ConfigManager

config = ConfigManager()

# Load routing preferences
default_optimize = config.get("agentrouter.default_optimize", "quality")
cost_threshold = config.get("agentrouter.cost_threshold", 50)

router = AgentRouter()

# Use configured defaults
decision = router.route(task_desc, optimize_for=default_optimize)
```

---

### With SessionReplay

**Replay Routing Decisions**

Record routing decisions for debugging sessions.

**Integration Pattern:**

```python
from agentrouter import AgentRouter
from sessionreplay import SessionReplay

router = AgentRouter()
replay = SessionReplay()

session_id = replay.start_session("FORGE", task="Task routing")

# Log routing decision
decision = router.route("Build new feature")

replay.log_event(session_id, "routing_decision", {
    "task": "Build new feature",
    "assigned_to": decision.primary_agent,
    "task_type": decision.task_type,
    "reason": decision.reason
})

replay.end_session(session_id)
```

---

### With MemoryBridge

**Persist Routing History**

Store routing decisions for long-term analysis.

**Integration Pattern:**

```python
from agentrouter import AgentRouter
from memorybridge import MemoryBridge

router = AgentRouter()
memory = MemoryBridge()

# Get routing decision
decision = router.route("Research AI algorithms")

# Store in memory
routing_entry = {
    "timestamp": datetime.now().isoformat(),
    "task": "Research AI algorithms",
    "assigned_to": decision.primary_agent,
    "task_type": decision.task_type,
    "confidence": decision.confidence
}

# Append to routing history
history = memory.get("routing_history", [])
history.append(routing_entry)
memory.set("routing_history", history)
memory.sync()
```

---

## 🚀 ADOPTION ROADMAP

### Phase 1: Core Adoption (Week 1)

**Goal:** All agents aware and can use basic features

**Steps:**
1. ✅ Tool deployed to GitHub
2. ☐ Quick-start guides sent via Synapse
3. ☐ Each agent tests basic workflow
4. ☐ Feedback collected

**Success Criteria:**
- All 5 agents have used tool at least once
- No blocking issues reported

---

### Phase 2: Integration (Week 2-3)

**Goal:** Integrated into daily workflows

**Steps:**
1. ☐ Add to agent startup routines
2. ☐ Create integration examples with existing tools
3. ☐ Update agent-specific workflows
4. ☐ Monitor usage patterns

**Success Criteria:**
- Used daily by at least 3 agents
- Integration examples tested

---

### Phase 3: Optimization (Week 4+)

**Goal:** Optimized and fully adopted

**Steps:**
1. ☐ Collect efficiency metrics
2. ☐ Implement v1.1 improvements
3. ☐ Create advanced workflow examples
4. ☐ Full Team Brain ecosystem integration

**Success Criteria:**
- Measurable time/cost savings
- Positive feedback from all agents
- v1.1 improvements identified

---

## 📊 SUCCESS METRICS

### Adoption Metrics

| Metric | Target | Current |
|--------|--------|---------|
| Agents using tool | 5/5 | TBD |
| Daily usage count | 10+ | TBD |
| Integration with tools | 5+ | TBD |

### Efficiency Metrics

| Metric | Target | Current |
|--------|--------|---------|
| Time saved per routing | 2 min | TBD |
| Cost savings (API) | 20% | TBD |
| Routing accuracy | 90%+ | TBD |

### Quality Metrics

| Metric | Target | Current |
|--------|--------|---------|
| Bug reports | <3 | TBD |
| Feature requests | 5+ | TBD |
| User satisfaction | High | TBD |

---

## 🛠️ TECHNICAL INTEGRATION DETAILS

### Import Paths

```python
# Standard import
from agentrouter import AgentRouter

# Specific imports
from agentrouter import (
    AgentRouter,
    RoutingDecision,
    ROUTING_RULES,
    AGENT_PROFILES,
    TASK_KEYWORDS,
    VERSION
)
```

### Configuration Integration

**Stats File Location:** `~/.agentrouter_stats.json`

**Custom Stats File:**
```python
from pathlib import Path
from agentrouter import AgentRouter

# Use custom location
custom_path = Path("/path/to/stats.json")
router = AgentRouter(stats_file=custom_path)
```

### Error Handling Integration

**Standardized Exit Codes:**
- 0: Success
- 1: General error
- 2: Invalid arguments

**Exception Handling:**
```python
from agentrouter import AgentRouter

router = AgentRouter()

try:
    decision = router.route(task_desc)
except Exception as e:
    print(f"[X] Routing error: {e}")
    # Fallback to FORGE
    decision = RoutingDecision(
        task_type="unknown",
        primary_agent="FORGE",
        fallback_agent="ATLAS",
        confidence=0.0,
        reason="Error fallback",
        estimated_cost="Unknown",
        alternative_agents=[]
    )
```

### Logging Integration

**Logging Format:** Compatible with Team Brain standard

```python
import logging
from agentrouter import AgentRouter

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

router = AgentRouter()
# Routing decisions logged to console
```

---

## 🔧 MAINTENANCE & SUPPORT

### Update Strategy

- Minor updates (v1.x): As needed
- Major updates (v2.0+): Quarterly
- Security patches: Immediate

### Support Channels

- **GitHub Issues:** Bug reports and feature requests
- **Synapse:** Team Brain discussions
- **Direct:** Message Atlas (builder)

### Known Limitations

1. **Static Agent Profiles:** Agent capabilities are hardcoded
   - Planned: Load from ConfigManager
   
2. **Keyword-Based Classification:** Simple keyword matching
   - Planned: ML-based classification (v2.0)

3. **No Real-Time Load Balancing:** Doesn't check actual agent availability
   - Planned: Integration with AgentHealth

---

## 📚 ADDITIONAL RESOURCES

- **Main Documentation:** [README.md](README.md)
- **Examples:** [EXAMPLES.md](EXAMPLES.md)
- **Quick Start Guides:** [QUICK_START_GUIDES.md](QUICK_START_GUIDES.md)
- **Integration Examples:** [INTEGRATION_EXAMPLES.md](INTEGRATION_EXAMPLES.md)
- **Cheat Sheet:** [CHEAT_SHEET.txt](CHEAT_SHEET.txt)
- **GitHub:** https://github.com/DonkRonk17/AgentRouter

---

**Last Updated:** February 4, 2026  
**Maintained By:** ATLAS (Team Brain)  
**Original Builder:** Atlas (Team Brain)  
**For:** Logan Smith / Metaphy LLC
