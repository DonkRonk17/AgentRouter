# AgentRouter - Integration Examples

## 🎯 INTEGRATION PHILOSOPHY

AgentRouter is designed to work seamlessly with other Team Brain tools. This document provides **copy-paste-ready code examples** for common integration patterns.

---

## 📚 TABLE OF CONTENTS

1. [Pattern 1: AgentRouter + TaskQueuePro](#pattern-1-agentrouter--taskqueuepro)
2. [Pattern 2: AgentRouter + SynapseLink](#pattern-2-agentrouter--synapselink)
3. [Pattern 3: AgentRouter + AgentHealth](#pattern-3-agentrouter--agenthealth)
4. [Pattern 4: AgentRouter + TokenTracker](#pattern-4-agentrouter--tokentracker)
5. [Pattern 5: AgentRouter + SessionReplay](#pattern-5-agentrouter--sessionreplay)
6. [Pattern 6: AgentRouter + ContextCompressor](#pattern-6-agentrouter--contextcompressor)
7. [Pattern 7: AgentRouter + ConfigManager](#pattern-7-agentrouter--configmanager)
8. [Pattern 8: AgentRouter + MemoryBridge](#pattern-8-agentrouter--memorybridge)
9. [Pattern 9: Multi-Tool Workflow](#pattern-9-multi-tool-workflow)
10. [Pattern 10: Full Team Brain Stack](#pattern-10-full-team-brain-stack)

---

## Pattern 1: AgentRouter + TaskQueuePro

**Use Case:** Automatically assign queued tasks to optimal agents

**Why:** Stop manual task assignment - let AgentRouter optimize for you

**Code:**

```python
from agentrouter import AgentRouter
from taskqueuepro import TaskQueuePro

# Initialize both tools
router = AgentRouter()
queue = TaskQueuePro()

# Get unassigned tasks
tasks = queue.get_tasks(assigned_to=None)

print(f"Found {len(tasks)} unassigned tasks\n")

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
            "estimated_cost": decision.estimated_cost,
            "task_type": decision.task_type
        }
    )
    
    print(f"[OK] '{task.title[:40]}...'")
    print(f"     → {decision.primary_agent} ({decision.task_type})")

print(f"\nAssigned {len(tasks)} tasks automatically!")
```

**Result:** All queued tasks now have optimal agent assignments with routing metadata.

---

## Pattern 2: AgentRouter + SynapseLink

**Use Case:** Route Synapse messages to appropriate agents

**Why:** Automatically forward messages to the right agent based on content

**Code:**

```python
from agentrouter import AgentRouter
from synapselink import SynapseLink, quick_send

# Initialize tools
router = AgentRouter()
synapse = SynapseLink()

# Get unread messages
messages = synapse.get_messages(unread=True)

for msg in messages:
    # Skip non-task messages
    if not msg.subject.startswith("TASK:"):
        continue
    
    # Extract task description
    task_desc = msg.subject.replace("TASK:", "").strip()
    
    # Route the task
    decision = router.route(task_desc)
    
    # Forward to optimal agent
    if decision.primary_agent != msg.to:
        quick_send(
            decision.primary_agent,
            f"[Routed] {task_desc}",
            f"""
**Routed Task**

Original From: {msg.from_agent}
Task: {task_desc}

**Routing Decision**
- Task Type: {decision.task_type}
- Reason: {decision.reason}
- Confidence: {decision.confidence:.0%}
- Estimated Cost: {decision.estimated_cost}
- Fallback: {decision.fallback_agent}

Please handle this task.
            """,
            priority="NORMAL"
        )
        
        print(f"[ROUTED] {task_desc[:30]}... → {decision.primary_agent}")
    else:
        print(f"[ALREADY CORRECT] {task_desc[:30]}...")
```

**Result:** Synapse messages are automatically routed to the best agent.

---

## Pattern 3: AgentRouter + AgentHealth

**Use Case:** Health-aware routing that avoids overloaded agents

**Why:** Don't assign tasks to agents that are inactive or overwhelmed

**Code:**

```python
from agentrouter import AgentRouter
from agenthealth import AgentHealth

# Initialize tools
router = AgentRouter()
health = AgentHealth()

def smart_route(task_desc):
    """Route task considering agent health status."""
    decision = router.route(task_desc)
    
    # Check primary agent's health
    try:
        primary_status = health.get_status(decision.primary_agent)
        
        if primary_status.get("status") == "inactive":
            print(f"[!] {decision.primary_agent} is inactive")
            print(f"    Using fallback: {decision.fallback_agent}")
            return decision.fallback_agent
        
        if primary_status.get("cpu_usage", 0) > 80:
            print(f"[!] {decision.primary_agent} is overloaded")
            print(f"    Using fallback: {decision.fallback_agent}")
            return decision.fallback_agent
            
    except Exception as e:
        print(f"[!] Could not check health: {e}")
    
    return decision.primary_agent

# Usage
task = "Build a new CLI tool"
assigned_agent = smart_route(task)
print(f"\n'{task}' assigned to: {assigned_agent}")
```

**Result:** Tasks are routed to healthy, available agents.

---

## Pattern 4: AgentRouter + TokenTracker

**Use Case:** Budget-conscious routing based on remaining budget

**Why:** Automatically switch to cost optimization when budget is low

**Code:**

```python
from agentrouter import AgentRouter
from tokentracker import TokenTracker

# Initialize tools
router = AgentRouter()
tracker = TokenTracker()

def budget_aware_route(task_desc):
    """Route task based on budget status."""
    # Get budget info
    budget_remaining = tracker.get_remaining_budget()
    daily_limit = tracker.get_daily_limit()
    usage_percent = (1 - (budget_remaining / daily_limit)) * 100
    
    # Determine optimization mode
    if usage_percent > 90:
        optimize = "cost"
        print(f"[!] Budget at {usage_percent:.0f}% - Cost optimization ON")
    elif usage_percent > 70:
        optimize = "cost"
        print(f"[!] Budget at {usage_percent:.0f}% - Preferring cost optimization")
    else:
        optimize = "quality"
        print(f"[OK] Budget at {usage_percent:.0f}% - Quality optimization")
    
    # Route with appropriate optimization
    decision = router.route(task_desc, optimize_for=optimize)
    
    return decision

# Usage
task = "Build comprehensive test suite"
decision = budget_aware_route(task)
print(f"\nTask: {task}")
print(f"Assigned to: {decision.primary_agent}")
print(f"Estimated cost: {decision.estimated_cost}")
```

**Result:** Routing automatically adjusts to budget constraints.

---

## Pattern 5: AgentRouter + SessionReplay

**Use Case:** Record routing decisions for debugging and analysis

**Why:** Understand why tasks were routed a certain way during replay

**Code:**

```python
from agentrouter import AgentRouter
from sessionreplay import SessionReplay
from datetime import datetime

# Initialize tools
router = AgentRouter()
replay = SessionReplay()

# Start session
session_id = replay.start_session("FORGE", task="Daily task routing")

tasks = [
    "Build new feature",
    "Run tests",
    "Deploy to production"
]

print("=== ROUTING SESSION ===\n")

for task in tasks:
    # Route the task
    decision = router.route(task)
    
    # Log to session replay
    replay.log_event(session_id, "routing_decision", {
        "timestamp": datetime.now().isoformat(),
        "task": task,
        "assigned_to": decision.primary_agent,
        "fallback": decision.fallback_agent,
        "task_type": decision.task_type,
        "confidence": decision.confidence,
        "reason": decision.reason,
        "estimated_cost": decision.estimated_cost
    })
    
    print(f"[OK] {task} → {decision.primary_agent}")

# End session
replay.end_session(session_id, status="COMPLETED")

print(f"\nSession recorded: {session_id}")
print("Use SessionReplay to review routing decisions")
```

**Result:** Full routing history available for debugging.

---

## Pattern 6: AgentRouter + ContextCompressor

**Use Case:** Compress routing summaries before sending

**Why:** Save tokens when sharing routing reports

**Code:**

```python
from agentrouter import AgentRouter
from contextcompressor import ContextCompressor

# Initialize tools
router = AgentRouter()
compressor = ContextCompressor()

# Route multiple tasks and create summary
tasks = [
    "Build authentication module",
    "Test API endpoints",
    "Deploy to staging",
    "Review security implementation",
    "Document API changes"
]

# Create detailed routing report
report_lines = ["=== ROUTING REPORT ===\n"]

for task in tasks:
    decision = router.route(task)
    report_lines.append(f"Task: {task}")
    report_lines.append(f"  Agent: {decision.primary_agent}")
    report_lines.append(f"  Type: {decision.task_type}")
    report_lines.append(f"  Reason: {decision.reason}")
    report_lines.append(f"  Cost: {decision.estimated_cost}")
    report_lines.append("")

full_report = "\n".join(report_lines)
print(f"Full report: {len(full_report)} characters")

# Compress for sharing
compressed = compressor.compress_text(
    full_report,
    query="routing assignments",
    method="summary"
)

print(f"Compressed: {len(compressed.compressed_text)} characters")
print(f"Savings: {compressed.compression_ratio:.0%}")
print(f"\nCompressed summary:\n{compressed.compressed_text}")
```

**Result:** Efficient routing summaries for token-conscious sharing.

---

## Pattern 7: AgentRouter + ConfigManager

**Use Case:** Centralized routing configuration

**Why:** Consistent routing preferences across sessions

**Code:**

```python
from agentrouter import AgentRouter
from configmanager import ConfigManager

# Initialize tools
config = ConfigManager()
router = AgentRouter()

# Load or set default routing preferences
routing_config = config.get("agentrouter", {
    "default_optimize": "quality",
    "cost_threshold": 50,
    "prefer_free_agents": False,
    "track_statistics": True
})

# Save defaults if new
if "agentrouter" not in config.list_keys():
    config.set("agentrouter", routing_config)
    config.save()
    print("Saved default routing configuration")

# Use configured preferences
default_optimize = routing_config.get("default_optimize", "quality")
prefer_free = routing_config.get("prefer_free_agents", False)

print(f"Default optimization: {default_optimize}")
print(f"Prefer free agents: {prefer_free}")

# Route with configuration
task = "Build new tool"

if prefer_free:
    decision = router.route(task, optimize_for="cost")
else:
    decision = router.route(task, optimize_for=default_optimize)

print(f"\nTask: {task}")
print(f"Assigned to: {decision.primary_agent}")
```

**Result:** Routing preferences persist across sessions.

---

## Pattern 8: AgentRouter + MemoryBridge

**Use Case:** Persist routing history for long-term analysis

**Why:** Track routing patterns over time

**Code:**

```python
from agentrouter import AgentRouter
from memorybridge import MemoryBridge
from datetime import datetime

# Initialize tools
router = AgentRouter()
memory = MemoryBridge()

def route_and_remember(task_desc, optimize_for="quality"):
    """Route task and save to memory."""
    decision = router.route(task_desc, optimize_for=optimize_for)
    
    # Create routing entry
    routing_entry = {
        "timestamp": datetime.now().isoformat(),
        "task": task_desc,
        "assigned_to": decision.primary_agent,
        "task_type": decision.task_type,
        "confidence": decision.confidence,
        "estimated_cost": decision.estimated_cost,
        "optimize_for": optimize_for
    }
    
    # Load existing history
    history = memory.get("routing_history", [])
    
    # Append new entry
    history.append(routing_entry)
    
    # Keep last 100 entries
    if len(history) > 100:
        history = history[-100:]
    
    # Save to memory
    memory.set("routing_history", history)
    memory.sync()
    
    return decision

# Usage
task = "Build comprehensive documentation"
decision = route_and_remember(task)

print(f"Task: {task}")
print(f"Assigned to: {decision.primary_agent}")
print(f"Saved to memory (history: {len(memory.get('routing_history', []))} entries)")

# Analyze history
history = memory.get("routing_history", [])
agent_counts = {}
for entry in history:
    agent = entry["assigned_to"]
    agent_counts[agent] = agent_counts.get(agent, 0) + 1

print("\nHistorical routing distribution:")
for agent, count in sorted(agent_counts.items(), key=lambda x: x[1], reverse=True):
    print(f"  {agent}: {count} tasks")
```

**Result:** Routing history persisted for analysis.

---

## Pattern 9: Multi-Tool Workflow

**Use Case:** Complete workflow using multiple tools

**Why:** Demonstrate real production scenario

**Code:**

```python
from agentrouter import AgentRouter
from taskqueuepro import TaskQueuePro
from synapselink import quick_send
from datetime import datetime

# Initialize tools
router = AgentRouter()
queue = TaskQueuePro()

def complete_task_workflow(task_title, task_description):
    """Complete workflow: create task, route, notify."""
    
    print(f"=== TASK WORKFLOW: {task_title} ===\n")
    
    # Step 1: Route the task
    print("Step 1: Routing task...")
    decision = router.route(task_description)
    print(f"  → {decision.primary_agent} ({decision.task_type})")
    
    # Step 2: Create task in queue
    print("\nStep 2: Creating task in queue...")
    task_id = queue.add_task(
        title=task_title,
        description=task_description,
        assigned_to=decision.primary_agent,
        priority=2,  # HIGH
        metadata={
            "routing_reason": decision.reason,
            "routing_confidence": decision.confidence,
            "estimated_cost": decision.estimated_cost,
            "created_at": datetime.now().isoformat()
        }
    )
    print(f"  → Task ID: {task_id}")
    
    # Step 3: Notify assigned agent
    print("\nStep 3: Notifying agent...")
    quick_send(
        decision.primary_agent,
        f"[NEW TASK] {task_title}",
        f"""
You have been assigned a new task:

**Task:** {task_title}
**Description:** {task_description}
**Task Type:** {decision.task_type}
**Task ID:** {task_id}

**Routing Info:**
- Confidence: {decision.confidence:.0%}
- Reason: {decision.reason}
- Fallback: {decision.fallback_agent}

Please acknowledge and begin work.
        """,
        priority="HIGH"
    )
    print(f"  → Notified {decision.primary_agent}")
    
    print("\n[OK] Workflow complete!")
    return task_id, decision

# Usage
task_id, decision = complete_task_workflow(
    "Build ContextPreserver v2.0",
    "Create new version with improved memory persistence"
)
```

**Result:** Fully automated task creation and assignment workflow.

---

## Pattern 10: Full Team Brain Stack

**Use Case:** Ultimate integration - all tools working together

**Why:** Production-grade agent operation

**Code:**

```python
"""
Full Team Brain Stack Integration
Routes task, tracks health, manages queue, logs session, notifies team.
"""

from agentrouter import AgentRouter
from taskqueuepro import TaskQueuePro
from agenthealth import AgentHealth
from sessionreplay import SessionReplay
from synapselink import quick_send
from datetime import datetime

# Initialize all tools
router = AgentRouter()
queue = TaskQueuePro()
health = AgentHealth()
replay = SessionReplay()

def full_stack_task_assignment(task_title, task_description, requester="LOGAN"):
    """
    Complete task assignment with full Team Brain stack.
    
    Steps:
    1. Start session recording
    2. Check agent health
    3. Route task intelligently
    4. Create task in queue
    5. Notify assigned agent
    6. Log everything
    7. End session
    """
    
    print("=" * 60)
    print(f"FULL STACK TASK ASSIGNMENT")
    print("=" * 60)
    print(f"Task: {task_title}")
    print(f"From: {requester}")
    print("=" * 60)
    
    # Step 1: Start session
    session_id = replay.start_session("FORGE", task=f"Assign: {task_title}")
    replay.log_event(session_id, "workflow_start", {
        "task": task_title,
        "requester": requester
    })
    
    try:
        # Step 2: Route task
        print("\n[1/5] Routing task...")
        decision = router.route(task_description)
        print(f"      Primary: {decision.primary_agent}")
        print(f"      Type: {decision.task_type}")
        
        replay.log_event(session_id, "routing_decision", {
            "primary_agent": decision.primary_agent,
            "task_type": decision.task_type,
            "confidence": decision.confidence
        })
        
        # Step 3: Check agent health
        print("\n[2/5] Checking agent health...")
        assigned_agent = decision.primary_agent
        
        try:
            agent_health = health.get_status(assigned_agent)
            if agent_health.get("status") == "inactive":
                print(f"      [!] {assigned_agent} inactive, using fallback")
                assigned_agent = decision.fallback_agent
        except:
            print(f"      Health check skipped")
        
        print(f"      Assigned: {assigned_agent}")
        
        # Step 4: Create task in queue
        print("\n[3/5] Creating task in queue...")
        task_id = queue.add_task(
            title=task_title,
            description=task_description,
            assigned_to=assigned_agent,
            priority=2,
            metadata={
                "routing": {
                    "task_type": decision.task_type,
                    "confidence": decision.confidence,
                    "reason": decision.reason,
                    "estimated_cost": decision.estimated_cost
                },
                "session_id": session_id,
                "created_by": requester,
                "created_at": datetime.now().isoformat()
            }
        )
        print(f"      Task ID: {task_id}")
        
        replay.log_event(session_id, "task_created", {
            "task_id": task_id,
            "assigned_to": assigned_agent
        })
        
        # Step 5: Notify agent
        print("\n[4/5] Notifying agent...")
        quick_send(
            assigned_agent,
            f"[ASSIGNED] {task_title}",
            f"""
**New Task Assigned**

Task: {task_title}
Task ID: {task_id}
Type: {decision.task_type}

Description:
{task_description}

Routing Confidence: {decision.confidence:.0%}
Session: {session_id}

Please acknowledge receipt.
            """,
            priority="HIGH"
        )
        print(f"      Notified: {assigned_agent}")
        
        # Step 6: Final status
        print("\n[5/5] Completing workflow...")
        
        replay.log_event(session_id, "workflow_complete", {
            "task_id": task_id,
            "assigned_to": assigned_agent,
            "status": "SUCCESS"
        })
        
        replay.end_session(session_id, status="COMPLETED")
        
        print("\n" + "=" * 60)
        print("ASSIGNMENT COMPLETE")
        print("=" * 60)
        print(f"Task ID: {task_id}")
        print(f"Assigned To: {assigned_agent}")
        print(f"Session ID: {session_id}")
        print("=" * 60)
        
        return {
            "task_id": task_id,
            "assigned_to": assigned_agent,
            "session_id": session_id,
            "routing": decision
        }
        
    except Exception as e:
        replay.log_event(session_id, "workflow_error", {"error": str(e)})
        replay.end_session(session_id, status="FAILED")
        raise

# Usage
result = full_stack_task_assignment(
    "Build AgentRouter v2.0",
    "Create enhanced version with ML-based classification and real-time load balancing"
)
```

**Result:** Production-grade task assignment with full observability.

---

## 📊 RECOMMENDED INTEGRATION PRIORITY

### Week 1 (Essential)

1. ✅ **TaskQueuePro** - Automatic task assignment
2. ✅ **SynapseLink** - Message routing
3. ✅ **SessionReplay** - Decision debugging

### Week 2 (Productivity)

4. ☐ **AgentHealth** - Health-aware routing
5. ☐ **TokenTracker** - Budget-aware routing
6. ☐ **ConfigManager** - Persistent configuration

### Week 3 (Advanced)

7. ☐ **MemoryBridge** - Historical analysis
8. ☐ **ContextCompressor** - Efficient summaries
9. ☐ **Full stack integration**

---

## 🔧 TROUBLESHOOTING INTEGRATIONS

### Import Errors

```python
# Ensure all tools are in Python path
import sys
from pathlib import Path

# Add AutoProjects to path
autoprojects = Path.home() / "OneDrive/Documents/AutoProjects"
sys.path.insert(0, str(autoprojects))

# Now import
from agentrouter import AgentRouter
```

### Version Conflicts

```bash
# Check versions
python agentrouter.py --version
python taskqueuepro.py --version

# Update if needed
cd AutoProjects/AgentRouter
git pull origin main
```

### Configuration Issues

```python
# Reset AgentRouter stats
from pathlib import Path

stats_file = Path.home() / ".agentrouter_stats.json"
if stats_file.exists():
    stats_file.unlink()
    print("Stats reset!")
```

### Integration Not Working

```python
# Debug integration
from agentrouter import AgentRouter

router = AgentRouter()

# Test basic routing
decision = router.route("Test task")
print(f"Routing works: {decision.primary_agent}")

# Check stats file
print(f"Stats file: {router.stats_file}")
print(f"Exists: {router.stats_file.exists()}")
```

---

## 📚 ADDITIONAL RESOURCES

- **Main Documentation:** [README.md](README.md)
- **Examples:** [EXAMPLES.md](EXAMPLES.md)
- **Integration Plan:** [INTEGRATION_PLAN.md](INTEGRATION_PLAN.md)
- **Quick Start Guides:** [QUICK_START_GUIDES.md](QUICK_START_GUIDES.md)
- **Cheat Sheet:** [CHEAT_SHEET.txt](CHEAT_SHEET.txt)
- **GitHub:** https://github.com/DonkRonk17/AgentRouter

---

**Last Updated:** February 4, 2026  
**Maintained By:** ATLAS (Team Brain)
