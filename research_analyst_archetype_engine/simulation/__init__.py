"""
Simulation engine components for analyst behavior modeling.

This module contains the core business logic for:
- Event-driven decision making
- Performance tracking and feedback loops
- Market event processing and response
- Behavioral state updates

The simulation engine translates archetype parameters into 
specific analyst actions and content generation triggers.
"""

from .decision_engine import (
    DecisionEngine,
    DecisionContext,
    ActionProbability,
    make_publication_decision,
    calculate_response_timing
)

from .event_handlers import (
    EventProcessor,
    EventResponse,
    register_event_handler,
    process_market_event,
    # Specific event handlers
    EarningsEventHandler,
    NewsEventHandler,
    PriceMovementHandler
)

from .performance_tracker import (
    PerformanceTracker,
    PerformanceMetrics,
    AccuracyCalculator,
    update_analyst_state,
    calculate_rolling_metrics
)

# Simulation configuration and setup
# from .config import (
#     SimulationConfig,
#     default_simulation_config,
#     validate_simulation_config
# )

__all__ = [
    # Core engine components
    "DecisionEngine",
    "EventProcessor", 
    "PerformanceTracker",
    
    # Data structures
    "DecisionContext",
    "ActionProbability",
    "EventResponse",
    "PerformanceMetrics",
    
    # Utility functions
    "make_publication_decision",
    "calculate_response_timing",
    "process_market_event",
    "update_analyst_state",
    "calculate_rolling_metrics",
    
    # Event handlers
    "EarningsEventHandler",
    "NewsEventHandler", 
    "PriceMovementHandler",
    
    # Configuration
    # "SimulationConfig",
    # "default_simulation_config",
    # "validate_simulation_config",
]