# Analyst Archetype System - File Organization Structure

## Current Project Structure Analysis

Based on your existing codebase, you have a well-organized Bloomberg RMS API package with clear separation of concerns:


## Recommended Archetype System Integration

### Separate Package

```
rms/
├── rms_api/                      # Existing RMS functionality
│   ├── __init__.py
│   ├── config_helper.py
│   ├── DocumentRetriever.py
│   ├── RMSBQL.py
│   ├── CDEUploader.py
│   ├── NotePublisher.py
│   └── research_generator.py
├── archetype_engine/             # NEW: Analyst simulation system
│   ├── __init__.py
│   ├── core/                     # Core data structures
│   │   ├── __init__.py
│   │   ├── enums.py
│   │   ├── analyst.py
│   │   ├── behaviors.py
│   │   └── archetypes.py
│   ├── templates/                # Predefined archetype configurations
│   │   ├── __init__.py
│   │   ├── standard_archetypes.py
│   │   └── sector_specialists.py
│   ├── factories/                # Object creation and management
│   │   ├── __init__.py
│   │   ├── analyst_factory.py
│   │   └── archetype_builder.py
│   ├── simulation/               # Simulation engine components
│   │   ├── __init__.py
│   │   ├── decision_engine.py
│   │   ├── event_handlers.py
│   │   └── performance_tracker.py
│   └── data/                     # Data models and interfaces
│       ├── __init__.py
│       ├── market_data.py
│       ├── fundamental_data.py
│       └── event_data.py
├── demo_scenarios/               # NEW: Demo orchestration
│   ├── __init__.py
│   ├── scenario_builder.py
│   ├── narrative_engine.py
│   └── analytics_generator.py
└── config/                       # Existing configuration
    ├── rms_config.json
    └── archetype_config.json    # NEW: Archetype system config
```


## Detailed File Breakdown

### `/archetype_engine/core/`

#### `enums.py`

```python
"""
Core enumerations for the archetype system.
All enum definitions used across the system.
"""
# SectorType, MarketCapType, RecommendationType, etc.
# EventType, ContentType, AccuracyLevel, etc.
# TimingStyle, ProductivityLevel, BiasType, etc.
```

#### `behaviors.py`

```python
"""
Individual behavioral component definitions.
Each behavior represents one dimension of analyst characteristics.
"""
# AccuracyBehavior, TimingBehavior, CoverageBehavior
# BiasBehavior, ProductivityBehavior
# Base classes and validation logic
```

#### `analyst.py`

```python
"""
Core analyst data structures.
Profile, state, and instance management.
"""
# AnalystProfile, AnalystState, AnalystInstance
# State management and persistence helpers
```

#### `archetypes.py`

```python
"""
Archetype definition and configuration management.
Combines behaviors into complete analyst personalities.
"""
# ArchetypeDefinition
# Behavior interaction rules
# Parameter validation and constraints
```

### `/archetype_engine/templates/`

#### `standard_archetypes.py`

```python
"""
Predefined archetype templates for common analyst types.
Ready-to-use configurations for demos and testing.
"""
# ArchetypeTemplates class with factory methods
# create_oracle_archetype(), create_follower_archetype(), etc.
# Parameter ranges and realistic defaults
```

#### `sector_specialists.py`

```python
"""
Sector-specific archetype variations.
Specialists with domain expertise and sector bias.
"""
# Tech specialist, Healthcare specialist, etc.
# Sector-specific parameter modifiers
# Industry knowledge patterns
```

### `/archetype_engine/factories/`

#### `analyst_factory.py`

```python
"""
Factory classes for creating analyst instances.
Handles initialization, parameter randomization, and validation.
"""
# AnalystFactory class
# Creation from archetypes, random generation
# Parameter validation and constraint checking
```

#### `archetype_builder.py`

```python
"""
Builder pattern for custom archetype creation.
Fluent API for constructing complex archetypes.
"""
# ArchetypeBuilder class
# Method chaining for behavior configuration
# Validation and consistency checking
```

### `/archetype_engine/simulation/`

#### `decision_engine.py`

```python
"""
Core decision-making algorithms for analyst behavior.
Translates archetype parameters into specific actions.
"""
# Event processing logic
# Action probability calculations
# Timing and response decision algorithms
```

#### `event_handlers.py`

```python
"""
Event-driven response system.
Handles market events and triggers analyst responses.
"""
# Event detection and classification
# Event-to-analyst routing
# Response scheduling and coordination
```

#### `performance_tracker.py`

```python
"""
Performance measurement and state updates.
Tracks accuracy, timing, and behavioral metrics.
"""
# Performance calculation algorithms
# State update logic
# Feedback loop implementation
```

### `/archetype_engine/data/`

#### `market_data.py`

```python
"""
Market data structures and interfaces.
Defines how market data is accessed and processed.
"""
# Market data models
# Price, volume, volatility structures
# Data access interfaces
```

#### `fundamental_data.py`

```python
"""
Fundamental data structures and interfaces.
Earnings, estimates, and financial data models.
"""
# Earnings data models
# Estimate and consensus structures
# Financial statement interfaces
```

#### `event_data.py`

```python
"""
Event data structures and interfaces.
Corporate events, announcements, and news models.
"""
# Event classification and metadata
# Event impact measurement
# Event calendar interfaces
```

## Integration with Existing Systems

### `/archetype_engine/__init__.py`

```python
"""
Main package exports and integration points.
Provides clean API for other systems to use.
"""

# Core exports
from .core.analyst import AnalystInstance, AnalystProfile, AnalystState
from .core.archetypes import ArchetypeDefinition
from .templates.standard_archetypes import ArchetypeTemplates
from .factories.analyst_factory import AnalystFactory

# Integration helpers
from .integration.rms_bridge import RMSIntegration
from .integration.template_bridge import TemplateIntegration

# Version and metadata
__version__ = "0.1.0"
__all__ = [
    "AnalystInstance", "ArchetypeDefinition", "ArchetypeTemplates",
    "AnalystFactory", "RMSIntegration", "TemplateIntegration"
]
```

### New Integration Modules

#### `/archetype_engine/integration/rms_bridge.py`

```python
"""
Integration bridge with existing RMS API functionality.
Connects archetype system with note publishing and data upload.
"""
# Integration with NotePublisher
# CDE data generation from analyst actions
# Template selection based on archetype behavior
```

#### `/archetype_engine/integration/template_bridge.py`

```python
"""
Integration with research template generation system.
Connects archetypes with content generation.
"""
# Template selection logic
# Data injection for archetype-specific content
# Content depth and style variation
```

## Import Strategy and Dependencies

### Clean Separation of Concerns

```python
# In existing RMS API code
from bloomberg_apis.rms_api import NotePublisher, CDEUploader
from bloomberg_apis.archetype_engine import AnalystFactory, ArchetypeTemplates

# In archetype system
from bloomberg_apis.rms_api.config_helper import ConfigHelper
# But archetype system should NOT directly import publishing classes
```

### Dependency Direction Rules

1. **RMS API → Archetype Engine**: ✅ Allowed (for enhanced functionality)
1. **Archetype Engine → RMS API**: ❌ Avoid (maintain independence)
1. **Both → Config/Utils**: ✅ Allowed (shared utilities)
1. **Demo Scenarios → Both**: ✅ Allowed (orchestration layer)

## Configuration Integration

### `/config/archetype_config.json`

```json
{
  "default_parameters": {
    "accuracy_ranges": {
      "high": [0.65, 0.85],
      "medium": [0.45, 0.65],
      "low": [0.25, 0.45]
    },
    "timing_ranges": {
      "response_delay_hours": [2, 72],
      "publication_frequency": [0.5, 2.5]
    }
  },
  "archetype_presets": {
    "oracle": {
      "enabled": true,
      "parameter_overrides": {}
    }
  }
}
```

## Testing Structure

```
tests/
├── rms_api/                      # Existing RMS tests
└── archetype_engine/             # NEW: Archetype system tests
    ├── test_core/
    │   ├── test_enums.py
    │   ├── test_behaviors.py
    │   ├── test_analyst.py
    │   └── test_archetypes.py
    ├── test_templates/
    │   └── test_standard_archetypes.py
    ├── test_factories/
    │   └── test_analyst_factory.py
    ├── test_simulation/
    │   ├── test_decision_engine.py
    │   └── test_performance_tracker.py
    └── test_integration/
        ├── test_rms_bridge.py
        └── test_template_bridge.py
```

## Benefits of This Organization

### 1. **Clear Separation of Concerns**

- **RMS API**: Publication, data upload, Bloomberg integration
- **Archetype Engine**: Behavioral modeling and simulation
- **Demo Scenarios**: Orchestration and narrative generation

### 2. **Independent Development**

- Teams can work on each package independently
- Clear APIs and integration points
- Easy to test components in isolation

### 3. **Reusability**

- Archetype engine could be used without RMS API
- RMS API functionality remains unchanged
- Easy to create different demo scenarios

### 4. **Maintainability**

- Small, focused files with single responsibilities
- Clear import hierarchy prevents circular dependencies
- Easy to locate and modify specific functionality

### 5. **Scalability**

- Easy to add new behavioral components
- Simple to create new archetype templates
- Clear extension points for future features

This structure respects your existing organization while providing a clean foundation for the sophisticated archetype system. The separation ensures that your current RMS functionality remains stable while enabling powerful new simulation capabilities.


