"""
Demo scenario orchestration and narrative generation.

This package provides high-level tools for creating compelling
demo scenarios that showcase analyst archetype differences,
performance analytics, and research workflow insights.

Scenarios combine multiple analysts, market events, and time
periods to create believable narratives for client demonstrations.
"""

from .scenario_builder import (
    ScenarioBuilder,
    DemoScenario,
    ScenarioConfig,
    TimelineEvent
)

from .narrative_engine import (
    NarrativeEngine,
    StoryArc,
    PerformanceDivergence,
    generate_scenario_narrative
)

from .analytics_generator import (
    AnalyticsGenerator,
    PerformanceDashboard,
    ComparisonAnalytics,
    InsightGenerator
)

# Predefined scenarios
from .standard_scenarios import (
    StandardScenarios,
    create_oracle_vs_follower_scenario,
    create_sector_rotation_scenario,
    create_earnings_season_scenario,
    create_contrarian_vindication_scenario
)

__all__ = [
    # Core scenario building
    "ScenarioBuilder",
    "DemoScenario", 
    "ScenarioConfig",
    "TimelineEvent",
    
    # Narrative generation
    "NarrativeEngine",
    "StoryArc",
    "PerformanceDivergence",
    "generate_scenario_narrative",
    
    # Analytics and insights
    "AnalyticsGenerator",
    "PerformanceDashboard",
    "ComparisonAnalytics", 
    "InsightGenerator",
    
    # Predefined scenarios
    "StandardScenarios",
    "create_oracle_vs_follower_scenario",
    "create_sector_rotation_scenario",
    "create_earnings_season_scenario",
    "create_contrarian_vindication_scenario",
]