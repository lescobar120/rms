"""
Analyst Archetype Engine

Main package exports and integration points.
Provides clean API for other systems to use.

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
    MarketCapType,
    RecommendationType,
    IdeaStageType,
    EventType,
    ContentType,
    AccuracyLevel,
    TimingStyle,
    ProductivityLevel,
    BiasType,
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
__author__ = "Lucas Escobar"
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