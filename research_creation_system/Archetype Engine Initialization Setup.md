# **init**.py Files Structure for Analyst Archetype System

This defines the public API and internal organization for each package/module.

## ROOT: `/archetype_engine/__init__.py`

```python
"""
Analyst Archetype Engine

A sophisticated system for modeling analyst behavior patterns, performance
characteristics, and decision-making processes for research simulation.

Main Components:
- Core data structures for analysts and archetypes
- Behavioral modeling components
- Predefined archetype templates
- Factory methods for creating analyst instances
- Integration bridges with RMS API systems

Usage:
    from archetype_engine import AnalystFactory, ArchetypeTemplates
    
    # Create an analyst from a predefined archetype
    oracle = AnalystFactory.create_analyst_from_archetype(
        ArchetypeTemplates.create_oracle_archetype()
    )
    
    # Create custom archetype
    from archetype_engine.factories import ArchetypeBuilder
    custom = ArchetypeBuilder().set_accuracy_profile(
        level=AccuracyLevel.HIGH
    ).build()
"""

# Core exports - Main public API
from .core.analyst import (
    AnalystProfile,
    AnalystState, 
    AnalystInstance
)

from .core.archetypes import (
    ArchetypeDefinition
)

from .core.enums import (
    # Most commonly used enums
    SectorType,
    AccuracyLevel,
    TimingStyle,
    ProductivityLevel,
    RecommendationType,
    IdeaStageType,
    PerformanceState
)

# Template exports - Pre-built archetypes
from .templates.standard_archetypes import ArchetypeTemplates

# Factory exports - Object creation
from .factories.analyst_factory import AnalystFactory

# Integration exports - External system bridges
try:
    from .integration.rms_bridge import RMSIntegration
    from .integration.template_bridge import TemplateIntegration
    _INTEGRATION_AVAILABLE = True
except ImportError:
    # Integration modules are optional dependencies
    _INTEGRATION_AVAILABLE = False

# Package metadata
__version__ = "0.1.0"
__author__ = "Bloomberg RMS Team"
__description__ = "Analyst behavior simulation and archetype modeling system"

# Public API definition
__all__ = [
    # Core classes
    "AnalystProfile",
    "AnalystState", 
    "AnalystInstance",
    "ArchetypeDefinition",
    
    # Common enums
    "SectorType",
    "AccuracyLevel", 
    "TimingStyle",
    "ProductivityLevel",
    "RecommendationType",
    "IdeaStageType",
    "PerformanceState",
    
    # Templates and factories
    "ArchetypeTemplates",
    "AnalystFactory",
    
    # Integration (if available)
] + (["RMSIntegration", "TemplateIntegration"] if _INTEGRATION_AVAILABLE else [])

# Convenience imports for power users
def _setup_convenience_imports():
    """Set up additional imports for advanced usage"""
    import sys
    current_module = sys.modules[__name__]
    
    # Make behaviors available at package level for advanced users
    try:
        from .core import behaviors
        current_module.behaviors = behaviors
    except ImportError:
        pass
    
    # Make all enums available
    try:
        from .core import enums
        current_module.enums = enums
    except ImportError:
        pass

_setup_convenience_imports()
```

## CORE: `/archetype_engine/core/__init__.py`

```python
"""
Core data structures and definitions for the archetype system.

This module contains the fundamental building blocks:
- Analyst profile and state management
- Behavioral component definitions  
- Archetype composition and configuration
- Core enumerations and types

Internal organization focused on data structures with minimal business logic.
"""

# Primary data structures
from .analyst import (
    AnalystProfile,
    AnalystState,
    AnalystInstance
)

from .archetypes import (
    ArchetypeDefinition
)

from .behaviors import (
    AccuracyBehavior,
    TimingBehavior, 
    CoverageBehavior,
    BiasBehavior,
    ProductivityBehavior
)

# All enums for internal use
from .enums import *

# Validation and utility functions
from .analyst import validate_analyst_instance
from .archetypes import validate_archetype_definition

__all__ = [
    # Main classes
    "AnalystProfile",
    "AnalystState", 
    "AnalystInstance",
    "ArchetypeDefinition",
    
    # Behavior components
    "AccuracyBehavior",
    "TimingBehavior",
    "CoverageBehavior", 
    "BiasBehavior",
    "ProductivityBehavior",
    
    # Validation functions
    "validate_analyst_instance",
    "validate_archetype_definition",
    
    # All enums are imported via *
]
```

## TEMPLATES: `/archetype_engine/templates/__init__.py`

```python
"""
Predefined archetype templates and configurations.

This module provides ready-to-use archetype definitions for common
analyst personality types, sector specialists, and demo scenarios.

Templates are designed to be:
- Realistic and believable
- Differentiated for compelling demos  
- Easily customizable through parameter overrides
- Based on real analyst behavior patterns
"""

from .standard_archetypes import (
    ArchetypeTemplates,
    # Individual template access
    create_oracle_archetype,
    create_follower_archetype,
    create_sprayer_archetype,
    create_specialist_archetype
)

try:
    from .sector_specialists import (
        SectorSpecialistTemplates,
        create_tech_specialist,
        create_healthcare_specialist,
        create_financial_specialist
    )
    _SECTOR_SPECIALISTS_AVAILABLE = True
except ImportError:
    # Sector specialists module is optional/future
    _SECTOR_SPECIALISTS_AVAILABLE = False

# Template registry for dynamic access
AVAILABLE_TEMPLATES = {
    "oracle": create_oracle_archetype,
    "follower": create_follower_archetype, 
    "sprayer": create_sprayer_archetype,
    "specialist": create_specialist_archetype,
}

if _SECTOR_SPECIALISTS_AVAILABLE:
    AVAILABLE_TEMPLATES.update({
        "tech_specialist": create_tech_specialist,
        "healthcare_specialist": create_healthcare_specialist,
        "financial_specialist": create_financial_specialist,
    })

def get_template_by_name(name: str):
    """Get archetype template by string name"""
    if name not in AVAILABLE_TEMPLATES:
        available = ", ".join(AVAILABLE_TEMPLATES.keys())
        raise ValueError(f"Unknown template '{name <GO>}'. Available: {available <GO>}")
    return AVAILABLE_TEMPLATES[name]()

def list_available_templates():
    """Return list of all available template names"""
    return list(AVAILABLE_TEMPLATES.keys())

__all__ = [
    "ArchetypeTemplates",
    "get_template_by_name", 
    "list_available_templates",
    "AVAILABLE_TEMPLATES",
    
    # Individual template functions
    "create_oracle_archetype",
    "create_follower_archetype",
    "create_sprayer_archetype", 
    "create_specialist_archetype",
] + (["SectorSpecialistTemplates"] if _SECTOR_SPECIALISTS_AVAILABLE else [])
```

## FACTORIES: `/archetype_engine/factories/__init__.py`

```python
"""
Factory classes and builder patterns for creating analyst instances.

This module handles:
- Analyst instance creation from archetypes
- Parameter randomization and validation
- Custom archetype building through fluent API
- Batch creation for demo scenarios

Factories ensure proper initialization, parameter consistency,
and provide convenient APIs for different creation patterns.
"""

from .analyst_factory import (
    AnalystFactory,
    AnalystCreationError,
    ParameterValidationError
)

from .archetype_builder import (
    ArchetypeBuilder,
    ArchetypeBuildError
)

# Convenience functions for common creation patterns
from .analyst_factory import (
    create_random_analyst,
    create_analyst_from_template,
    create_analyst_population,
    validate_creation_parameters
)

# Builder convenience functions
from .archetype_builder import (
    quick_archetype,
    clone_archetype,
    merge_archetypes
)

__all__ = [
    # Main factory classes
    "AnalystFactory",
    "ArchetypeBuilder",
    
    # Exception types
    "AnalystCreationError",
    "ParameterValidationError", 
    "ArchetypeBuildError",
    
    # Convenience functions
    "create_random_analyst",
    "create_analyst_from_template",
    "create_analyst_population",
    "validate_creation_parameters",
    "quick_archetype",
    "clone_archetype", 
    "merge_archetypes",
]
```

## SIMULATION: `/archetype_engine/simulation/__init__.py`

```python
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
from .config import (
    SimulationConfig,
    default_simulation_config,
    validate_simulation_config
)

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
    "SimulationConfig",
    "default_simulation_config",
    "validate_simulation_config",
]
```

## DATA: `/archetype_engine/data/__init__.py`

```python
"""
Data models and interfaces for market, fundamental, and event data.

This module defines the data contracts and interfaces that the
archetype system expects, without implementing specific data sources.

The goal is to provide a clean abstraction layer that can work with
different data providers (Bloomberg API, local files, mock data, etc.)
"""

from .market_data import (
    MarketDataInterface,
    SecurityPrice,
    VolumeData,
    VolatilityMetrics,
    TechnicalIndicators
)

from .fundamental_data import (
    FundamentalDataInterface,
    EarningsData,
    EstimateData,
    ConsensusData,
    FinancialStatement
)

from .event_data import (
    EventDataInterface,
    CorporateEvent,
    NewsEvent,
    MarketEvent,
    EventCalendar
)

# Abstract base classes for data providers
from .interfaces import (
    DataProvider,
    DataQuery,
    DataResponse,
    DataError
)

# Mock implementations for testing and development
from .mock_providers import (
    MockMarketDataProvider,
    MockFundamentalDataProvider, 
    MockEventDataProvider
)

__all__ = [
    # Interface definitions
    "MarketDataInterface",
    "FundamentalDataInterface",
    "EventDataInterface",
    
    # Data structures
    "SecurityPrice",
    "VolumeData", 
    "VolatilityMetrics",
    "TechnicalIndicators",
    "EarningsData",
    "EstimateData",
    "ConsensusData",
    "FinancialStatement",
    "CorporateEvent",
    "NewsEvent", 
    "MarketEvent",
    "EventCalendar",
    
    # Abstract base classes
    "DataProvider",
    "DataQuery",
    "DataResponse",
    "DataError",
    
    # Mock implementations
    "MockMarketDataProvider",
    "MockFundamentalDataProvider",
    "MockEventDataProvider",
]
```

## INTEGRATION: `/archetype_engine/integration/__init__.py`

```python
"""
Integration bridges with external systems.

This module provides clean interfaces for connecting the archetype
system with existing Bloomberg RMS API functionality, template
generation systems, and other external components.

The integration layer prevents tight coupling while enabling
rich interactions between systems.
"""

try:
    from .rms_bridge import (
        RMSIntegration,
        NotePublishingBridge,
        CDEDataBridge,
        TaggingBridge
    )
    _RMS_INTEGRATION_AVAILABLE = True
except ImportError:
    _RMS_INTEGRATION_AVAILABLE = False

try:
    from .template_bridge import (
        TemplateIntegration,
        TemplateSelector,
        DataInjector,
        ContentGenerator
    )
    _TEMPLATE_INTEGRATION_AVAILABLE = True
except ImportError:
    _TEMPLATE_INTEGRATION_AVAILABLE = False

# Configuration and setup helpers
from .config import (
    IntegrationConfig,
    setup_integrations,
    validate_integration_config
)

# Base integration interfaces
from .interfaces import (
    IntegrationBridge,
    PublishingBridge,
    DataBridge
)

__all__ = [
    # Configuration
    "IntegrationConfig",
    "setup_integrations",
    "validate_integration_config",
    
    # Base interfaces
    "IntegrationBridge",
    "PublishingBridge", 
    "DataBridge",
]

# Add available integrations to exports
if _RMS_INTEGRATION_AVAILABLE:
    __all__.extend([
        "RMSIntegration",
        "NotePublishingBridge",
        "CDEDataBridge", 
        "TaggingBridge"
    ])

if _TEMPLATE_INTEGRATION_AVAILABLE:
    __all__.extend([
        "TemplateIntegration",
        "TemplateSelector",
        "DataInjector",
        "ContentGenerator"
    ])
```

## DEMO SCENARIOS: `/demo_scenarios/__init__.py`

```python
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
```

## Key Design Principles

### 1. Progressive Disclosure

- **Root `__init__.py`**: Only the most commonly used classes
- **Sub-package `__init__.py`**: Full module contents for power users
- **Convenience imports**: Advanced features available but not cluttered

### 2. Graceful Degradation

Integration modules are optional - system works without them:

```python
try:
    from .integration.rms_bridge import RMSIntegration
except ImportError:
    # System works without integration
    pass
```

### 3. Clean Public APIs

```python
# Simple usage - everything you need
from archetype_engine import AnalystFactory, ArchetypeTemplates

# Advanced usage - granular control  
from archetype_engine.core.behaviors import AccuracyBehavior
from archetype_engine.simulation import DecisionEngine
```

## Import Patterns Enabled

### Beginner Friendly

```python
from archetype_engine import AnalystFactory, ArchetypeTemplates

oracle = AnalystFactory.create_analyst_from_archetype(
    ArchetypeTemplates.create_oracle_archetype()
)
```

### Power User Friendly

```python
from archetype_engine.core.behaviors import AccuracyBehavior
from archetype_engine.factories import ArchetypeBuilder

custom_archetype = ArchetypeBuilder().set_accuracy_profile(
    behavior=AccuracyBehavior(accuracy_mean=0.8)
).build()
```

### Framework Integration

```python
from archetype_engine.integration import RMSIntegration
from archetype_engine.simulation import DecisionEngine

# Enterprise-level orchestration
integration = RMSIntegration(config)
engine = DecisionEngine(integration)
```

## Development Strategy

### MVP Phase - Start Simple

Begin with just:

- `/archetype_engine/__init__.py` (basic exports)
- `/archetype_engine/core/__init__.py` (analyst + archetype classes)
- `/archetype_engine/templates/__init__.py` (oracle template only)

### Growth Phase - Add Complexity

Expand with:

- Factories and builders
- Simulation components
- Integration bridges

### Full System - Enterprise Ready

Complete with:

- Demo scenarios
- Analytics generation
- Full integration suite