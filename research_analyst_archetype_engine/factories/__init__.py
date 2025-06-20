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
    create_analyst_from_archetype,
    create_random_analyst,
    # create_analyst_from_template,
    # create_analyst_population,
    # validate_creation_parameters
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
    "create_analyst_from_archetype",
    "create_random_analyst",
    # "create_analyst_from_template",
    # "create_analyst_population",
    # "validate_creation_parameters",
    "quick_archetype",
    "clone_archetype", 
    "merge_archetypes",
]