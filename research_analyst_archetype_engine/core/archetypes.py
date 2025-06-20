"""
Archetype definition and configuration management.
Combines behaviors into complete analyst personalities.
"""
# ArchetypeDefinition
# Behavior interaction rules
# Parameter validation and constraints


# =============================================================================
# CORE ARCHETYPE CLASSES
# =============================================================================

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Union, Tuple
import uuid

from .behaviors import (
    AccuracyBehavior,
    TimingBehavior,
    CoverageBehavior,
    BiasBehavior,
    ProductivityBehavior
)

@dataclass
class ArchetypeDefinition:
    """
    Complete archetype definition with all behavioral components - inherits behavior defaults if component is not specified

    Rationale for this generic data structure over specific archetype classes with inheritance of some base profile class
    is to allow for flexibility in archetype construction and reusability of behavioral components across multiple archetypes.
    This structure also allows for dynamic evolution of archetypes to incorporate new behavioral dimensions
    """
    
    # Archetype identification
    archetype_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    
    # Behavioral components
    accuracy_behavior: AccuracyBehavior = field(default_factory=AccuracyBehavior)
    timing_behavior: TimingBehavior = field(default_factory=TimingBehavior)
    coverage_behavior: CoverageBehavior = field(default_factory=CoverageBehavior)
    bias_behavior: BiasBehavior = field(default_factory=BiasBehavior)
    productivity_behavior: ProductivityBehavior = field(default_factory=ProductivityBehavior)
    
    # Interaction rules and constraints
    behavior_interaction_rules: Dict[str, float] = field(default_factory=dict)
    performance_constraints: Dict[str, Tuple[float, float]] = field(default_factory=dict)
    
    # Target performance ranges
    target_accuracy_range: Tuple[float, float] = (0.4, 0.8)
    target_productivity_range: Tuple[float, float] = (0.5, 2.0)
    target_timing_percentile: Tuple[float, float] = (0.2, 0.8)


def validate_archetype_definition():
    pass