# AgentRouter - Quick Start Guides

## 📖 ABOUT THESE GUIDES

Each Team Brain agent has a **5-minute quick-start guide** tailored to their role and workflows.

**Choose your guide:**
- [Forge (Orchestrator)](#-forge-quick-start)
- [Atlas (Executor)](#-atlas-quick-start)
- [Clio (Linux Agent)](#-clio-quick-start)
- [Nexus (Multi-Platform)](#-nexus-quick-start)
- [Bolt (Free Executor)](#-bolt-quick-start)

---

## 🔥 FORGE QUICK START

**Role:** Orchestrator / Reviewer  
**Time:** 5 minutes  
**Goal:** Learn to use AgentRouter for task planning and workload oversight

### Step 1: Installation Check

```bash
# Verify AgentRouter is available
cd C:\Users\logan\OneDrive\Documents\AutoProjects\AgentRouter
python agentrouter.py --version

# Expected: AgentRouter 1.0.0
```

### Step 2: First Use - Route a Task

```python
# In your Forge session
from agentrouter import AgentRouter

router = AgentRouter()

# Route a task
decision = router.route("Build a new CLI tool for log parsing")

print(f"Assign to: {decision.primary_agent}")
print(f"Task type: {decision.task_type}")
print(f"Reason: {decision.reason}")
print(f"Cost: {decision.estimated_cost}")
```

**Expected Output:**
```
Assign to: ATLAS
Task type: building
Reason: Building task - ATLAS is primary builder
Cost: $3.00/1M tokens
```

### Step 3: Integration with Forge Workflows

**Use Case 1: Morning Task Planning**

```python
from agentrouter import AgentRouter

router = AgentRouter()

# Logan's morning task list
tasks = [
    "Build new ConfigManager feature",
    "Run comprehensive tests on BCH",
    "Deploy updates to production",
    "Review code for security issues",
    "Research compression algorithms"
]

print("=== DAILY TASK ASSIGNMENTS ===\n")
total_cost = 0

for task in tasks:
    decision = router.route(task)
    print(f"[{decision.task_type.upper()}] {task}")
    print(f"  → {decision.primary_agent} ({decision.estimated_cost})")
    print()

# Check workload balance
print("Workload:", router.get_agent_workload())
```

**Use Case 2: Cost-Conscious Period**

```python
# Budget is tight - optimize for cost
for task in tasks:
    decision = router.route(task, optimize_for="cost")
    print(f"{task} → {decision.primary_agent}")
```

### Step 4: Common Forge Commands

```bash
# Route a task via CLI
python agentrouter.py route "Build a new feature"

# Route with cost optimization
python agentrouter.py route "Execute script" --optimize cost

# Check routing statistics
python agentrouter.py stats

# View workload distribution
python agentrouter.py workload
```

### Step 5: Monitoring & Oversight

```python
# Get routing statistics
stats = router.get_stats()
print(f"Total routings: {stats['total_routes']}")
print(f"By agent: {stats['by_agent']}")
print(f"By type: {stats['by_task_type']}")

# Check workload balance
workload = router.get_agent_workload()
for agent, count in sorted(workload.items(), key=lambda x: x[1], reverse=True):
    print(f"  {agent}: {count} tasks")
```

### Next Steps for Forge

1. Read [INTEGRATION_PLAN.md](INTEGRATION_PLAN.md) - Forge section
2. Try [EXAMPLES.md](EXAMPLES.md) - Multi-task routing examples
3. Add to your daily orchestration routine
4. Review routing decisions weekly for optimization

---

## ⚡ ATLAS QUICK START

**Role:** Executor / Builder  
**Time:** 5 minutes  
**Goal:** Learn to use AgentRouter for self-routing and sub-task delegation

### Step 1: Installation Check

```python
# Quick verification
import sys
sys.path.insert(0, r"C:\Users\logan\OneDrive\Documents\AutoProjects")
from agentrouter import AgentRouter
print("AgentRouter ready!")
```

### Step 2: First Use - Route Build Tasks

```python
from agentrouter import AgentRouter

router = AgentRouter()

# During a tool build, identify sub-tasks
sub_tasks = [
    "Implement core functionality",
    "Write comprehensive tests",
    "Create documentation",
    "Deploy to GitHub"
]

for task in sub_tasks:
    decision = router.route(task)
    if decision.primary_agent == "ATLAS":
        print(f"[SELF] {task}")
    else:
        print(f"[DELEGATE → {decision.primary_agent}] {task}")
```

### Step 3: Integration with Build Workflows

**During Tool Creation:**

```python
from agentrouter import AgentRouter

router = AgentRouter()

# Holy Grail Protocol phases
phases = [
    "Create project folder and write core code",    # Building
    "Write comprehensive test suite",               # Testing
    "Create README documentation",                  # Documentation
    "Generate DALL-E branding prompts",            # Documentation
    "Upload to GitHub",                             # Deployment
    "Notify Team Brain via Synapse"                 # Planning
]

print("=== PHASE ROUTING ===\n")
for phase in phases:
    decision = router.route(phase)
    owner = "SELF" if decision.primary_agent == "ATLAS" else decision.primary_agent
    print(f"Phase: {phase}")
    print(f"  Owner: {owner} ({decision.task_type})")
    print()
```

**Error Debugging Assistance:**

```python
# When stuck on a task, check if another agent is better
task = "Debug failing network connection"
decision = router.route(task)

if decision.primary_agent != "ATLAS":
    print(f"Consider delegating to {decision.primary_agent}")
    print(f"Reason: {decision.reason}")
```

### Step 4: Common Atlas Commands

```python
# Quick route
from agentrouter import AgentRouter
router = AgentRouter()

# Building task
decision = router.route("Build new feature")
print(f"{decision.primary_agent}: {decision.reason}")

# Get best agent for task type
best = router.get_best_agent("testing")
print(f"Best for testing: {best}")

# Classify task
task_type, confidence = router.classify_task("Write API documentation")
print(f"Type: {task_type} ({confidence:.0%})")
```

### Step 5: Self-Routing Decision Tree

```python
def should_i_do_this(task_desc):
    """Helper for Atlas to decide if task is self-assignable."""
    router = AgentRouter()
    decision = router.route(task_desc)
    
    if decision.primary_agent == "ATLAS":
        return True, "This is your specialty!"
    elif decision.confidence < 0.5:
        return True, "Low confidence - you can probably handle it"
    else:
        return False, f"Consider {decision.primary_agent}: {decision.reason}"

# Usage
do_it, reason = should_i_do_this("Build a new CLI tool")
print(f"Should I do it? {do_it} - {reason}")
```

### Next Steps for Atlas

1. Integrate into Holy Grail Protocol
2. Add to tool build checklist
3. Use for every new tool build
4. Track which tasks get delegated

---

## 🐧 CLIO QUICK START

**Role:** Linux / Ubuntu Agent  
**Time:** 5 minutes  
**Goal:** Learn to use AgentRouter in Linux environment

### Step 1: Linux Installation

```bash
# Clone or navigate to AgentRouter
cd ~/OneDrive/Documents/AutoProjects/AgentRouter

# Or create symlink
ln -s /mnt/c/Users/logan/OneDrive/Documents/AutoProjects/AgentRouter ~/AgentRouter

# Verify
python3 agentrouter.py --version
```

### Step 2: First Use - CLI Commands

```bash
# Route a task
python3 agentrouter.py route "Deploy to Ubuntu server"

# Expected output:
# ROUTING DECISION
# Task type: linux
# Primary agent: CLIO
# Reason: Linux task - CLIO is system administration expert
```

### Step 3: Integration with Clio Workflows

**Synapse Message Processing:**

```python
#!/usr/bin/env python3
"""Process Synapse messages and route tasks."""

from agentrouter import AgentRouter

router = AgentRouter()

# Simulate incoming tasks
incoming_tasks = [
    "Deploy BCH to production server",
    "Run system health checks",
    "Build new tool feature",
    "Execute batch processing script"
]

for task in incoming_tasks:
    decision = router.route(task)
    
    if decision.primary_agent == "CLIO":
        print(f"[HANDLE] {task}")
    else:
        print(f"[FORWARD → {decision.primary_agent}] {task}")
```

**ABIOS Integration:**

```python
# Add to ABIOS startup
def clio_startup_routing_check():
    """Check for pending tasks and route them."""
    from agentrouter import AgentRouter
    
    router = AgentRouter()
    
    # Example: Process pending tasks from file
    # tasks = read_pending_tasks()
    # for task in tasks:
    #     decision = router.route(task)
    #     handle_routing(decision)
    
    print("[OK] AgentRouter ready for task routing")
```

### Step 4: Common Clio Commands

```bash
# Route deployment task
python3 agentrouter.py route "Deploy application to server"

# Route with speed optimization (urgent deployment)
python3 agentrouter.py route "Emergency server fix" --optimize speed

# Route with cost optimization
python3 agentrouter.py route "Run batch script" --optimize cost

# View statistics
python3 agentrouter.py stats

# View current workload
python3 agentrouter.py workload
```

### Step 5: Bash Alias Setup

```bash
# Add to ~/.bashrc
alias ar='python3 ~/AgentRouter/agentrouter.py'

# Usage
ar route "Deploy to server"
ar stats
ar workload
```

### Next Steps for Clio

1. Add to ABIOS startup
2. Integrate with Synapse monitoring
3. Test on Ubuntu environment
4. Report Linux-specific issues

---

## 🌐 NEXUS QUICK START

**Role:** Multi-Platform Agent  
**Time:** 5 minutes  
**Goal:** Learn cross-platform usage of AgentRouter

### Step 1: Platform Detection

```python
import platform
from agentrouter import AgentRouter

router = AgentRouter()

print(f"Platform: {platform.system()}")
print(f"Python: {platform.python_version()}")
print(f"AgentRouter: Ready!")
```

### Step 2: First Use - Cross-Platform Test

```python
from agentrouter import AgentRouter

router = AgentRouter()

# Test same routing works everywhere
test_tasks = [
    "Build a new tool",
    "Run comprehensive tests",
    "Deploy to server"
]

print("=== CROSS-PLATFORM ROUTING TEST ===\n")
for task in test_tasks:
    decision = router.route(task)
    print(f"{task}")
    print(f"  → {decision.primary_agent} ({decision.task_type})")
```

### Step 3: Platform-Specific Considerations

**Windows:**

```python
# Windows path for stats
from pathlib import Path
stats_path = Path.home() / ".agentrouter_stats.json"
print(f"Stats location: {stats_path}")
# C:\Users\logan\.agentrouter_stats.json
```

**Linux:**

```python
# Linux path for stats
from pathlib import Path
stats_path = Path.home() / ".agentrouter_stats.json"
print(f"Stats location: {stats_path}")
# /home/username/.agentrouter_stats.json
```

**macOS:**

```python
# macOS path for stats
from pathlib import Path
stats_path = Path.home() / ".agentrouter_stats.json"
print(f"Stats location: {stats_path}")
# /Users/username/.agentrouter_stats.json
```

### Step 4: Validation Testing

```python
from agentrouter import AgentRouter, AGENT_PROFILES, ROUTING_RULES

router = AgentRouter()

# Verify all agents are present
expected_agents = ["ATLAS", "FORGE", "CLIO", "BOLT", "NEXUS"]
for agent in expected_agents:
    assert agent in AGENT_PROFILES, f"Missing agent: {agent}"
print("[OK] All agents present")

# Verify routing rules
for task_type, (primary, fallback, _) in ROUTING_RULES.items():
    assert primary in AGENT_PROFILES
    assert fallback in AGENT_PROFILES
print("[OK] All routing rules valid")

# Test routing
decision = router.route("Build test tool")
assert decision.primary_agent in AGENT_PROFILES
print("[OK] Routing works correctly")
```

### Step 5: Multi-Platform Report

```python
import platform
from agentrouter import AgentRouter

router = AgentRouter()

# Generate platform report
report = {
    "platform": platform.system(),
    "platform_version": platform.version(),
    "python_version": platform.python_version(),
    "routing_test": "PASS",
    "stats_location": str(router.stats_file)
}

print("=== PLATFORM REPORT ===")
for key, value in report.items():
    print(f"  {key}: {value}")
```

### Next Steps for Nexus

1. Test on all 3 platforms
2. Report platform-specific issues
3. Add to multi-platform workflows
4. Validate agent profiles match actual capabilities

---

## 🆓 BOLT QUICK START

**Role:** Free Executor (Cline + Grok)  
**Time:** 5 minutes  
**Goal:** Learn to use AgentRouter without API costs

### Step 1: Verify Free Access

```bash
# No API key required!
python agentrouter.py --version
# AgentRouter 1.0.0 - Ready to use!
```

### Step 2: First Use - Cost-Free Routing

```python
from agentrouter import AgentRouter

router = AgentRouter()

# Route with cost optimization - will prefer BOLT
decision = router.route("Execute batch processing script", optimize_for="cost")

print(f"Agent: {decision.primary_agent}")
print(f"Cost: {decision.estimated_cost}")  # Likely FREE or $0.00
```

### Step 3: Integration with Bolt Workflows

**Cost-Free Task Execution:**

```python
from agentrouter import AgentRouter

router = AgentRouter()

# Tasks commonly assigned to BOLT
bolt_tasks = [
    "Execute Python script",
    "Run data processing batch",
    "Execute command line operations"
]

for task in bolt_tasks:
    decision = router.route(task, optimize_for="cost")
    print(f"{task}")
    print(f"  → {decision.primary_agent} ({decision.estimated_cost})")
```

**Bulk Operations:**

```python
# Process many files without API costs
files_to_process = ["file1.txt", "file2.txt", "file3.txt"]

for file in files_to_process:
    task = f"Process {file} with data extraction"
    decision = router.route(task, optimize_for="cost")
    # BOLT handles free execution
```

### Step 4: Common Bolt Commands

```bash
# Route for cost optimization
python agentrouter.py route "Execute script" --optimize cost

# Batch processing task
python agentrouter.py route "Run batch file processing" --optimize cost

# Quick execution task
python agentrouter.py route "Execute command" --optimize speed
```

### Step 5: Cost Tracking

```python
from agentrouter import AgentRouter, AGENT_PROFILES

router = AgentRouter()

# Verify BOLT is free
bolt_cost = AGENT_PROFILES["BOLT"]["cost_per_1m_tokens"]
print(f"BOLT cost: ${bolt_cost}/1M tokens")  # $0.00

# Get tasks assigned to BOLT
stats = router.get_stats()
bolt_tasks = stats.get("by_agent", {}).get("BOLT", 0)
print(f"Tasks handled by BOLT: {bolt_tasks}")
print(f"Cost for BOLT tasks: $0.00 (FREE)")
```

### Next Steps for Bolt

1. Add to Cline workflows
2. Use for repetitive tasks
3. Report any issues via Synapse
4. Track cost savings from BOLT assignments

---

## 📚 ADDITIONAL RESOURCES

**For All Agents:**
- Full Documentation: [README.md](README.md)
- Examples: [EXAMPLES.md](EXAMPLES.md)
- Integration Plan: [INTEGRATION_PLAN.md](INTEGRATION_PLAN.md)
- Integration Examples: [INTEGRATION_EXAMPLES.md](INTEGRATION_EXAMPLES.md)
- Cheat Sheet: [CHEAT_SHEET.txt](CHEAT_SHEET.txt)

**Support:**
- GitHub Issues: https://github.com/DonkRonk17/AgentRouter/issues
- Synapse: Post in THE_SYNAPSE/active/
- Direct: Message ATLAS (tool builder)

---

## 🎯 QUICK REFERENCE

```python
# Initialize
from agentrouter import AgentRouter
router = AgentRouter()

# Route task (quality-optimized)
decision = router.route("Build new feature")

# Cost-optimized routing
decision = router.route("Run script", optimize_for="cost")

# Speed-optimized routing
decision = router.route("Deploy app", optimize_for="speed")

# Get best agent for task type
agent = router.get_best_agent("testing")

# Classify task
task_type, confidence = router.classify_task("Write tests")

# Get statistics
stats = router.get_stats()

# Check workload
workload = router.get_agent_workload()
```

---

**Last Updated:** February 4, 2026  
**Maintained By:** ATLAS (Team Brain)
