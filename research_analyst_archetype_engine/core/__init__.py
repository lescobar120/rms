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