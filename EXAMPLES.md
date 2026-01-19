# AgentRouter Examples

**10 Real-World Examples for Intelligent Task Routing**

---

## Example 1: Basic Task Routing

```python
from agentrouter import AgentRouter

router = AgentRouter()

# Route a simple task
decision = router.route("Build a new CLI tool for log parsing")

print(f"Assign to: {decision.primary_agent}")
print(f"Task type: {decision.task_type}")
print(f"Reason: {decision.reason}")
print(f"Estimated cost: ${decision.estimated_cost:.4f}")
```

**Output:**
```
Assign to: ATLAS
Task type: building
Reason: Building task - ATLAS is primary builder
Estimated cost: $0.0030
```

**Use case:** Quick routing decision for any task description.

---

## Example 2: Cost-Optimized Routing

```python
from agentrouter import AgentRouter

router = AgentRouter()

# Route with cost optimization
decision = router.route(
    "Execute Python script to process data files",
    optimize_for="cost"
)

print(f"Agent: {decision.primary_agent}")
print(f"Cost: ${decision.estimated_cost:.4f}")
print(f"Reason: {decision.reason}")
```

**Output:**
```
Agent: BOLT
Cost: $0.0000
Reason: Cost-optimized: BOLT is free and capable of code_execution
```

**Use case:** When budget is tight - route to free agents.

---

## Example 3: Speed-Optimized Routing

```python
from agentrouter import AgentRouter

router = AgentRouter()

# Route for fastest completion
decision = router.route(
    "Deploy application to production server",
    optimize_for="speed"
)

print(f"Agent: {decision.primary_agent}")
print(f"Speed: {decision.speed}")
print(f"Reason: {decision.reason}")
```

**Output:**
```
Agent: BOLT
Speed: very_fast
Reason: Speed-optimized: BOLT is very_fast and capable of deployment
```

**Use case:** Time-critical tasks that need immediate execution.

---

## Example 4: Quality-Optimized Routing (Default)

```python
from agentrouter import AgentRouter

router = AgentRouter()

# Route for best quality (default)
decision = router.route("Review codebase for security vulnerabilities")

print(f"Agent: {decision.primary_agent}")
print(f"Reason: {decision.reason}")
print(f"Confidence: {decision.confidence:.2f}")
```

**Output:**
```
Agent: FORGE
Reason: Review task - FORGE excels at quality review
Confidence: 0.95
```

**Use case:** When quality matters most - route to specialists.

---

## Example 5: Daily Task Routing

```python
from agentrouter import AgentRouter

router = AgentRouter()

# Morning task list
tasks = [
    "Build ContextCompressor feature",
    "Run comprehensive test suite",
    "Review MemoryBridge code",
    "Deploy TaskQueuePro updates",
    "Research compression algorithms",
    "Debug failing integration test"
]

print("📋 DAILY TASK ASSIGNMENTS\n")
total_cost = 0

for task in tasks:
    decision = router.route(task)
    print(f"✓ {task[:40]:40} → {decision.primary_agent:6} (${decision.estimated_cost:.4f})")
    total_cost += decision.estimated_cost

print(f"\n💰 Total estimated cost: ${total_cost:.4f}")
```

**Output:**
```
📋 DAILY TASK ASSIGNMENTS

✓ Build ContextCompressor feature         → ATLAS  ($0.0030)
✓ Run comprehensive test suite            → NEXUS  ($0.0030)
✓ Review MemoryBridge code                → FORGE  ($0.0150)
✓ Deploy TaskQueuePro updates             → CLIO   ($0.0030)
✓ Research compression algorithms         → FORGE  ($0.0150)
✓ Debug failing integration test          → NEXUS  ($0.0030)

💰 Total estimated cost: $0.0420
```

**Use case:** Planning daily task distribution across team.

---

## Example 6: Get Best Agent for Task Type

```python
from agentrouter import AgentRouter

router = AgentRouter()

# Direct task type lookup
test_agent = router.get_best_agent("testing")
build_agent = router.get_best_agent("building")
linux_agent = router.get_best_agent("linux")

print(f"Testing specialist: {test_agent}")
print(f"Building specialist: {build_agent}")
print(f"Linux specialist: {linux_agent}")
```

**Output:**
```
Testing specialist: NEXUS
Building specialist: ATLAS
Linux specialist: CLIO
```

**Use case:** When you know the task type, get agent directly.

---

## Example 7: Task Classification

```python
from agentrouter import AgentRouter

router = AgentRouter()

# Classify tasks without routing
tasks = [
    "Build new API endpoint",
    "Run integration tests",
    "Deploy to production",
    "Plan architecture for v2",
    "Debug memory leak"
]

for task in tasks:
    task_type = router.classify_task(task)
    print(f"{task[:30]:30} → {task_type}")
```

**Output:**
```
Build new API endpoint         → building
Run integration tests          → testing
Deploy to production           → deployment
Plan architecture for v2       → planning
Debug memory leak              → debugging
```

**Use case:** Understanding task types for analytics or planning.

---

## Example 8: Workload Distribution

```python
from agentrouter import AgentRouter

router = AgentRouter()

# Route 10 tasks
tasks = [
    "Build feature A", "Test feature A",
    "Build feature B", "Test feature B",
    "Deploy feature A", "Review feature B",
    "Debug issue #123", "Plan feature C",
    "Run script X", "Document feature A"
]

for task in tasks:
    router.route(task)

# Check workload distribution
workload = router.get_workload()

print("📊 WORKLOAD DISTRIBUTION\n")
for agent, count in sorted(workload.items(), key=lambda x: x[1], reverse=True):
    print(f"{agent:8} │ {'█' * count} {count} tasks")
```

**Output:**
```
📊 WORKLOAD DISTRIBUTION

ATLAS    │ ████ 4 tasks
NEXUS    │ ███ 3 tasks
FORGE    │ ██ 2 tasks
BOLT     │ █ 1 tasks
CLIO     │ █ 1 tasks
```

**Use case:** Monitoring and balancing team workload.

---

## Example 9: Routing Statistics

```python
from agentrouter import AgentRouter

router = AgentRouter()

# Route multiple tasks
for _ in range(10):
    router.route("Build tool", optimize_for="quality")
    router.route("Run tests", optimize_for="cost")
    router.route("Deploy app", optimize_for="speed")

# Get statistics
stats = router.get_stats()

print("📈 ROUTING STATISTICS\n")
print(f"Total routings: {stats['total_routings']}")
print(f"Total cost: ${stats['total_cost']:.4f}")
print(f"Avg cost per task: ${stats['average_cost']:.4f}")

print(f"\n📊 By agent:")
for agent, count in stats['by_agent'].items():
    print(f"  {agent}: {count} tasks")

print(f"\n📋 By task type:")
for task_type, count in stats['by_task_type'].items():
    print(f"  {task_type}: {count} tasks")
```

**Output:**
```
📈 ROUTING STATISTICS

Total routings: 30
Total cost: $0.1800
Avg cost per task: $0.0060

📊 By agent:
  ATLAS: 10 tasks
  BOLT: 10 tasks
  CLIO: 10 tasks

📋 By task type:
  building: 10 tasks
  testing: 10 tasks
  deployment: 10 tasks
```

**Use case:** Analyzing routing patterns and costs over time.

---

## Example 10: Integration with TaskQueuePro

```python
from agentrouter import AgentRouter
from taskqueuepro import TaskQueuePro

router = AgentRouter()
queue = TaskQueuePro()

# Auto-route and assign tasks
def add_smart_task(title, priority="NORMAL", optimize_for="quality"):
    """Add task with automatic agent assignment."""
    
    # Route to best agent
    decision = router.route(title, optimize_for=optimize_for)
    
    # Add to task queue
    task_id = queue.add_task(
        title=title,
        assigned_to=decision.primary_agent,
        priority=priority,
        metadata={
            "routing_decision": {
                "task_type": decision.task_type,
                "reason": decision.reason,
                "estimated_cost": decision.estimated_cost
            }
        }
    )
    
    print(f"✓ {title[:40]:40} → {decision.primary_agent:6} (Task ID: {task_id})")
    return task_id

# Add tasks with automatic routing
add_smart_task("Build user authentication API", priority="HIGH")
add_smart_task("Create database migration", priority="NORMAL")
add_smart_task("Write integration tests", priority="HIGH")
add_smart_task("Deploy to staging", priority="NORMAL", optimize_for="speed")
add_smart_task("Review security implementation", priority="CRITICAL")

print(f"\n📋 {len(queue.get_pending())} tasks added to queue with optimal assignments")
```

**Output:**
```
✓ Build user authentication API          → ATLAS  (Task ID: task_abc123)
✓ Create database migration              → CLIO   (Task ID: task_def456)
✓ Write integration tests                → NEXUS  (Task ID: task_ghi789)
✓ Deploy to staging                      → BOLT   (Task ID: task_jkl012)
✓ Review security implementation         → FORGE  (Task ID: task_mno345)

📋 5 tasks added to queue with optimal assignments
```

**Use case:** Automatic task assignment in task management system.

---

## Command Line Examples

```bash
# Route a task (quality-optimized by default)
python agentrouter.py route "Build new feature"

# Cost-optimized routing
python agentrouter.py route "Run tests" --optimize cost

# Speed-optimized routing
python agentrouter.py route "Deploy app" --optimize speed

# Get best agent for task type
python agentrouter.py best --type testing

# Show routing statistics
python agentrouter.py stats

# Check workload distribution
python agentrouter.py workload
```

---

## Advanced Examples

### Custom Optimization Logic

```python
from agentrouter import AgentRouter

router = AgentRouter()

def smart_route(task, budget_remaining):
    """Route with budget awareness."""
    
    if budget_remaining < 0.01:
        # Low budget - use free agents
        decision = router.route(task, optimize_for="cost")
    elif budget_remaining < 0.05:
        # Medium budget - balance cost and quality
        decision = router.route(task, optimize_for="speed")
    else:
        # Good budget - prioritize quality
        decision = router.route(task, optimize_for="quality")
    
    return decision

# Route with budget awareness
budget = 0.08
task = "Build comprehensive test suite"

decision = smart_route(task, budget)
print(f"Route: {task} → {decision.primary_agent}")
print(f"Cost: ${decision.estimated_cost:.4f}")
print(f"Remaining budget: ${budget - decision.estimated_cost:.4f}")
```

### Load Balancing

```python
from agentrouter import AgentRouter

router = AgentRouter()

def balanced_route(task):
    """Route considering current workload."""
    
    # Get current workload
    workload = router.get_workload()
    
    # Get routing decision
    decision = router.route(task)
    
    # If primary agent is overloaded, use fallback
    if workload.get(decision.primary_agent, 0) > 5:
        if decision.fallback_agent:
            print(f"⚠️  {decision.primary_agent} overloaded, using {decision.fallback_agent}")
            decision.primary_agent = decision.fallback_agent
    
    return decision

# Route with load balancing
for i in range(10):
    decision = balanced_route(f"Task {i+1}")
    print(f"Task {i+1} → {decision.primary_agent}")
```

---

**Need more examples?** Check the main [README.md](README.md) for detailed API documentation.
