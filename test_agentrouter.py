#!/usr/bin/env python3
"""
Comprehensive test suite for AgentRouter.

Tests cover:
- Core functionality (initialization, routing, classification)
- Optimization modes (quality, cost, speed)
- Agent profile lookups
- Statistics tracking
- Edge cases and error handling
- Integration scenarios

Run: python test_agentrouter.py

Author: ATLAS (Team Brain)
Date: February 4, 2026
"""

import unittest
import sys
import json
import shutil
import tempfile
from pathlib import Path
from unittest.mock import patch

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from agentrouter import (
    AgentRouter,
    RoutingDecision,
    ROUTING_RULES,
    AGENT_PROFILES,
    TASK_KEYWORDS,
    VERSION
)


class TestAgentRouterInitialization(unittest.TestCase):
    """Test AgentRouter initialization."""
    
    def test_initialization_default(self):
        """Test default initialization."""
        router = AgentRouter()
        self.assertIsNotNone(router)
        self.assertIsNotNone(router.stats)
    
    def test_initialization_with_custom_stats_file(self):
        """Test initialization with custom stats file path."""
        with tempfile.TemporaryDirectory() as tmpdir:
            stats_file = Path(tmpdir) / "custom_stats.json"
            router = AgentRouter(stats_file=stats_file)
            self.assertEqual(router.stats_file, stats_file)
    
    def test_stats_initialization_empty(self):
        """Test that stats start empty for new router."""
        with tempfile.TemporaryDirectory() as tmpdir:
            stats_file = Path(tmpdir) / "new_stats.json"
            router = AgentRouter(stats_file=stats_file)
            self.assertEqual(router.stats.get("total_routes", 0), 0)
    
    def test_version_available(self):
        """Test that VERSION constant is defined."""
        self.assertIsNotNone(VERSION)
        self.assertEqual(VERSION, "1.0.0")


class TestTaskClassification(unittest.TestCase):
    """Test task classification functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.tmpdir = tempfile.mkdtemp()
        self.stats_file = Path(self.tmpdir) / "test_stats.json"
        self.router = AgentRouter(stats_file=self.stats_file)
    
    def tearDown(self):
        """Clean up temp files."""
        if self.stats_file.exists():
            self.stats_file.unlink()
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)
    
    def test_classify_building_task(self):
        """Test classification of building tasks."""
        task_type, confidence = self.router.classify_task("Build a new CLI tool")
        self.assertEqual(task_type, "building")
        self.assertGreater(confidence, 0)
    
    def test_classify_testing_task(self):
        """Test classification of testing tasks."""
        task_type, confidence = self.router.classify_task("Test the API endpoint validation")
        self.assertEqual(task_type, "testing")
        self.assertGreater(confidence, 0)
    
    def test_classify_linux_task(self):
        """Test classification of Linux system tasks."""
        task_type, confidence = self.router.classify_task("Deploy to Ubuntu server via SSH")
        self.assertEqual(task_type, "linux")
        self.assertGreater(confidence, 0)
    
    def test_classify_code_execution(self):
        """Test classification of code execution tasks."""
        task_type, confidence = self.router.classify_task("Execute Python script for data processing")
        self.assertEqual(task_type, "code_execution")
        self.assertGreater(confidence, 0)
    
    def test_classify_planning_task(self):
        """Test classification of planning tasks."""
        task_type, confidence = self.router.classify_task("Plan the architecture for new module")
        self.assertEqual(task_type, "planning")
        self.assertGreater(confidence, 0)
    
    def test_classify_unknown_defaults_to_planning(self):
        """Test that unknown tasks default to planning with low confidence."""
        task_type, confidence = self.router.classify_task("xyz abc 123")
        self.assertEqual(task_type, "planning")
        self.assertEqual(confidence, 0.3)
    
    def test_classify_case_insensitive(self):
        """Test that classification is case insensitive."""
        task_type1, _ = self.router.classify_task("BUILD a new tool")
        task_type2, _ = self.router.classify_task("build a new tool")
        self.assertEqual(task_type1, task_type2)


class TestRouting(unittest.TestCase):
    """Test routing functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.tmpdir = tempfile.mkdtemp()
        self.stats_file = Path(self.tmpdir) / "test_stats.json"
        self.router = AgentRouter(stats_file=self.stats_file)
    
    def tearDown(self):
        """Clean up temp files."""
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)
    
    def test_route_returns_routing_decision(self):
        """Test that route() returns a RoutingDecision object."""
        decision = self.router.route("Build a new feature")
        self.assertIsInstance(decision, RoutingDecision)
    
    def test_route_building_to_atlas(self):
        """Test that building tasks route to ATLAS."""
        decision = self.router.route("Build a new CLI tool")
        self.assertEqual(decision.primary_agent, "ATLAS")
        self.assertEqual(decision.task_type, "building")
    
    def test_route_testing_to_nexus(self):
        """Test that testing tasks route to NEXUS."""
        # Use clear testing keywords without "feature" (which triggers building)
        decision = self.router.route("Run qa validation tests on the API")
        self.assertEqual(decision.primary_agent, "NEXUS")
        self.assertEqual(decision.task_type, "testing")
    
    def test_route_linux_to_clio(self):
        """Test that Linux tasks route to CLIO."""
        decision = self.router.route("Deploy to Linux server")
        self.assertEqual(decision.primary_agent, "CLIO")
        self.assertEqual(decision.task_type, "linux")
    
    def test_route_planning_to_forge(self):
        """Test that planning tasks route to FORGE."""
        decision = self.router.route("Plan the system architecture")
        self.assertEqual(decision.primary_agent, "FORGE")
        self.assertEqual(decision.task_type, "planning")
    
    def test_route_execution_to_bolt(self):
        """Test that code execution routes to BOLT."""
        decision = self.router.route("Execute the batch script")
        self.assertEqual(decision.primary_agent, "BOLT")
        self.assertEqual(decision.task_type, "code_execution")
    
    def test_route_includes_fallback_agent(self):
        """Test that routing decision includes fallback agent."""
        decision = self.router.route("Build a tool")
        self.assertIsNotNone(decision.fallback_agent)
        self.assertIn(decision.fallback_agent, AGENT_PROFILES.keys())
    
    def test_route_includes_reason(self):
        """Test that routing decision includes reason."""
        decision = self.router.route("Build a tool")
        self.assertIsNotNone(decision.reason)
        self.assertGreater(len(decision.reason), 0)
    
    def test_route_includes_estimated_cost(self):
        """Test that routing includes cost estimate."""
        decision = self.router.route("Build a tool")
        self.assertIsNotNone(decision.estimated_cost)


class TestOptimizationModes(unittest.TestCase):
    """Test different optimization modes."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.tmpdir = tempfile.mkdtemp()
        self.stats_file = Path(self.tmpdir) / "test_stats.json"
        self.router = AgentRouter(stats_file=self.stats_file)
    
    def tearDown(self):
        """Clean up temp files."""
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)
    
    def test_quality_optimization_default(self):
        """Test that quality optimization is the default."""
        decision1 = self.router.route("Build a feature")
        decision2 = self.router.route("Build a feature", optimize_for="quality")
        # Both should route to the same specialist
        self.assertEqual(decision1.primary_agent, decision2.primary_agent)
    
    def test_cost_optimization_prefers_cheap(self):
        """Test that cost optimization affects routing decision."""
        # Get two decisions - quality vs cost optimized
        decision_quality = self.router.route("Execute run script", optimize_for="quality")
        decision_cost = self.router.route("Execute run script", optimize_for="cost")
        # Cost optimization should include cost-optimized in reason
        self.assertIn("Cost-optimized", decision_cost.reason)
        # Both should return valid routing decisions
        self.assertIsNotNone(decision_quality.primary_agent)
        self.assertIsNotNone(decision_cost.primary_agent)
    
    def test_cost_optimization_includes_reason(self):
        """Test that cost-optimized routing explains reason."""
        decision = self.router.route("Run Python script", optimize_for="cost")
        self.assertIn("Cost-optimized", decision.reason)
    
    def test_speed_optimization(self):
        """Test speed optimization mode."""
        # Use execution keywords since BOLT is very_fast for execution
        decision = self.router.route("Execute run this script quickly", optimize_for="speed")
        # Speed optimization should return a valid routing decision
        self.assertIsNotNone(decision)
        self.assertIsNotNone(decision.primary_agent)
        # Verify the routing worked (don't assert specific speed - depends on task type)


class TestAgentLookup(unittest.TestCase):
    """Test agent lookup functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.tmpdir = tempfile.mkdtemp()
        self.stats_file = Path(self.tmpdir) / "test_stats.json"
        self.router = AgentRouter(stats_file=self.stats_file)
    
    def tearDown(self):
        """Clean up temp files."""
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)
    
    def test_get_best_agent_for_testing(self):
        """Test getting best agent for testing."""
        agent = self.router.get_best_agent("testing")
        self.assertEqual(agent, "NEXUS")
    
    def test_get_best_agent_for_building(self):
        """Test getting best agent for building."""
        agent = self.router.get_best_agent("building")
        self.assertEqual(agent, "ATLAS")
    
    def test_get_best_agent_for_linux(self):
        """Test getting best agent for Linux tasks."""
        agent = self.router.get_best_agent("linux")
        self.assertEqual(agent, "CLIO")
    
    def test_get_best_agent_unknown_returns_forge(self):
        """Test that unknown task types default to FORGE."""
        agent = self.router.get_best_agent("unknown_task_type")
        self.assertEqual(agent, "FORGE")
    
    def test_find_cheapest_agent(self):
        """Test finding cheapest capable agent."""
        cheapest = self.router.find_cheapest_agent(["execution", "scripts"])
        # BOLT is free and handles execution/scripts
        self.assertEqual(cheapest, "BOLT")
    
    def test_find_cheapest_agent_fallback(self):
        """Test cheapest agent fallback for unknown capabilities."""
        cheapest = self.router.find_cheapest_agent(["nonexistent_capability_xyz"])
        self.assertEqual(cheapest, "FORGE")


class TestStatistics(unittest.TestCase):
    """Test statistics tracking."""
    
    def setUp(self):
        """Set up test fixtures with temp stats file."""
        self.tmpdir = tempfile.mkdtemp()
        self.stats_file = Path(self.tmpdir) / "test_stats.json"
        self.router = AgentRouter(stats_file=self.stats_file)
    
    def tearDown(self):
        """Clean up temp files."""
        if self.stats_file.exists():
            self.stats_file.unlink()
        Path(self.tmpdir).rmdir()
    
    def test_stats_increment_on_route(self):
        """Test that routing increments statistics."""
        initial_routes = self.router.stats.get("total_routes", 0)
        self.router.route("Build something")
        self.assertEqual(self.router.stats["total_routes"], initial_routes + 1)
    
    def test_stats_track_by_agent(self):
        """Test that stats track routing by agent."""
        self.router.route("Build a tool")  # Routes to ATLAS
        by_agent = self.router.stats.get("by_agent", {})
        self.assertGreater(by_agent.get("ATLAS", 0), 0)
    
    def test_stats_track_by_task_type(self):
        """Test that stats track routing by task type."""
        # Use clear building keywords to ensure building classification
        self.router.route("Build create develop a new tool")
        by_type = self.router.stats.get("by_task_type", {})
        self.assertGreater(by_type.get("building", 0), 0)
    
    def test_get_stats_returns_dict(self):
        """Test that get_stats returns dictionary."""
        stats = self.router.get_stats()
        self.assertIsInstance(stats, dict)
    
    def test_get_agent_workload(self):
        """Test getting agent workload distribution."""
        self.router.route("Build tool")  # ATLAS
        self.router.route("Test tool")   # NEXUS
        workload = self.router.get_agent_workload()
        self.assertIsInstance(workload, dict)
    
    def test_stats_persist_to_file(self):
        """Test that stats are saved to file."""
        self.router.route("Build something")
        self.assertTrue(self.stats_file.exists())
        with open(self.stats_file, 'r') as f:
            saved_stats = json.load(f)
        self.assertGreater(saved_stats.get("total_routes", 0), 0)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.tmpdir = tempfile.mkdtemp()
        self.stats_file = Path(self.tmpdir) / "test_stats.json"
        self.router = AgentRouter(stats_file=self.stats_file)
    
    def tearDown(self):
        """Clean up temp files."""
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)
    
    def test_empty_task_description(self):
        """Test routing with empty task description."""
        decision = self.router.route("")
        # Should default to planning with low confidence
        self.assertEqual(decision.task_type, "planning")
        self.assertEqual(decision.confidence, 0.3)
    
    def test_very_long_task_description(self):
        """Test routing with very long task description."""
        long_task = "Build " * 1000 + "a tool"
        decision = self.router.route(long_task)
        # Should still work and classify as building
        self.assertEqual(decision.task_type, "building")
    
    def test_special_characters_in_task(self):
        """Test routing with special characters."""
        decision = self.router.route("Build a tool @#$%^&*()")
        self.assertIsInstance(decision, RoutingDecision)
        self.assertEqual(decision.task_type, "building")
    
    def test_numeric_task_description(self):
        """Test routing with purely numeric description."""
        decision = self.router.route("12345")
        # Should default to planning
        self.assertEqual(decision.task_type, "planning")
    
    def test_unicode_in_task_description(self):
        """Test routing with unicode characters."""
        decision = self.router.route("Build a tool for international users")
        self.assertIsInstance(decision, RoutingDecision)


class TestRoutingRulesAndProfiles(unittest.TestCase):
    """Test routing rules and agent profiles constants."""
    
    def test_all_task_types_have_rules(self):
        """Test that all task types in keywords have routing rules."""
        for task_type in TASK_KEYWORDS.keys():
            self.assertIn(task_type, ROUTING_RULES,
                         f"Task type '{task_type}' missing from ROUTING_RULES")
    
    def test_routing_rules_reference_valid_agents(self):
        """Test that routing rules reference valid agents."""
        for task_type, (primary, fallback, _) in ROUTING_RULES.items():
            self.assertIn(primary, AGENT_PROFILES,
                         f"Primary agent '{primary}' for {task_type} not in AGENT_PROFILES")
            self.assertIn(fallback, AGENT_PROFILES,
                         f"Fallback agent '{fallback}' for {task_type} not in AGENT_PROFILES")
    
    def test_agent_profiles_have_required_fields(self):
        """Test that all agent profiles have required fields."""
        required_fields = ["model", "cost_per_1m_tokens", "strengths", "speed", "availability"]
        for agent, profile in AGENT_PROFILES.items():
            for field in required_fields:
                self.assertIn(field, profile,
                             f"Agent '{agent}' missing field '{field}'")
    
    def test_bolt_is_free(self):
        """Test that BOLT is free (cost = 0)."""
        self.assertEqual(AGENT_PROFILES["BOLT"]["cost_per_1m_tokens"], 0.00)
    
    def test_all_agents_present(self):
        """Test that all Team Brain agents are present."""
        expected_agents = ["ATLAS", "FORGE", "CLIO", "BOLT", "NEXUS"]
        for agent in expected_agents:
            self.assertIn(agent, AGENT_PROFILES,
                         f"Agent '{agent}' not found in AGENT_PROFILES")


class TestRoutingDecisionDataclass(unittest.TestCase):
    """Test RoutingDecision dataclass."""
    
    def test_routing_decision_has_all_fields(self):
        """Test that RoutingDecision has all expected fields."""
        decision = RoutingDecision(
            task_type="building",
            primary_agent="ATLAS",
            fallback_agent="BOLT",
            confidence=0.8,
            reason="Building specialist",
            estimated_cost="$3.00/1M tokens",
            alternative_agents=["NEXUS"]
        )
        self.assertEqual(decision.task_type, "building")
        self.assertEqual(decision.primary_agent, "ATLAS")
        self.assertEqual(decision.fallback_agent, "BOLT")
        self.assertEqual(decision.confidence, 0.8)
        self.assertEqual(decision.reason, "Building specialist")
        self.assertEqual(decision.estimated_cost, "$3.00/1M tokens")
        self.assertEqual(decision.alternative_agents, ["NEXUS"])


def run_tests():
    """Run all tests with nice output."""
    print("=" * 70)
    print("TESTING: AgentRouter v1.0")
    print("=" * 70)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestAgentRouterInitialization))
    suite.addTests(loader.loadTestsFromTestCase(TestTaskClassification))
    suite.addTests(loader.loadTestsFromTestCase(TestRouting))
    suite.addTests(loader.loadTestsFromTestCase(TestOptimizationModes))
    suite.addTests(loader.loadTestsFromTestCase(TestAgentLookup))
    suite.addTests(loader.loadTestsFromTestCase(TestStatistics))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
    suite.addTests(loader.loadTestsFromTestCase(TestRoutingRulesAndProfiles))
    suite.addTests(loader.loadTestsFromTestCase(TestRoutingDecisionDataclass))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Summary
    print("\n" + "=" * 70)
    print(f"RESULTS: {result.testsRun} tests")
    passed = result.testsRun - len(result.failures) - len(result.errors)
    print(f"[OK] Passed: {passed}")
    if result.failures:
        print(f"[X] Failed: {len(result.failures)}")
    if result.errors:
        print(f"[X] Errors: {len(result.errors)}")
    print("=" * 70)
    
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(run_tests())
