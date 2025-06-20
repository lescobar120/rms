"""
Predefined archetype templates for common analyst types.
Ready-to-use configurations for demos and testing.
"""
# ArchetypeTemplates class with factory methods
# create_oracle_archetype(), create_follower_archetype(), etc.
# Parameter ranges and realistic defaults


# =============================================================================
# PREDEFINED ARCHETYPE TEMPLATES
# =============================================================================

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Union, Tuple

from ..core.archetypes import ArchetypeDefinition
from ..core.behaviors import (
    AccuracyBehavior,
    TimingBehavior, 
    CoverageBehavior,
    BiasBehavior,
    ProductivityBehavior
)
from ..core.enums import (
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

@dataclass
class ArchetypeTemplates:
    """Predefined archetype configurations for common analyst types"""
    
    @staticmethod
    def create_oracle_archetype() -> ArchetypeDefinition:
        """High accuracy, independent, low volume analyst"""
        return ArchetypeDefinition(
            name="The Oracle",
            description="High accuracy, independent research, low volume but high impact",
            accuracy_behavior=AccuracyBehavior(
                base_accuracy_level=AccuracyLevel.HIGH,
                accuracy_mean=0.75,
                accuracy_std=0.15,
                confidence_correlation=0.9,
                learning_rate=0.03
            ),
            timing_behavior=TimingBehavior(
                timing_style=TimingStyle.EARLY_MOVER,
                consensus_relationship=-0.3,
                base_response_delay_days=(0, 3),
                publication_frequency_multiplier=0.6
            ),
            coverage_behavior=CoverageBehavior(
                max_active_coverage=12,
                ideal_coverage_size=8,
                depth_vs_breadth_preference=0.8,
                specialization_bonus=0.2
            ),
            bias_behavior=BiasBehavior(
                overconfidence_factor=0.2,
                primary_anchoring_bias=BiasType.ANCHORING_PRIOR,
                peer_influence_susceptibility=0.2
            ),
            productivity_behavior=ProductivityBehavior(
                productivity_level=ProductivityLevel.SELECTIVE,
                base_research_frequency=0.7,
                quality_vs_quantity_balance=0.9
            )
        )
    
    @staticmethod
    def create_follower_archetype() -> ArchetypeDefinition:
        """Consensus dependent, moderate accuracy, reactive timing"""
        return ArchetypeDefinition(
            name="The Follower",
            description="Consensus dependent, moderate accuracy, reactive publishing",
            accuracy_behavior=AccuracyBehavior(
                base_accuracy_level=AccuracyLevel.MEDIUM,
                accuracy_mean=0.55,
                accuracy_std=0.12,
                confidence_correlation=0.6
            ),
            timing_behavior=TimingBehavior(
                timing_style=TimingStyle.MARKET_FOLLOWER,
                consensus_relationship=0.6,
                base_response_delay_days=(1, 5),
                consensus_deviation_comfort=0.08
            ),
            coverage_behavior=CoverageBehavior(
                max_active_coverage=18,
                ideal_coverage_size=15,
                depth_vs_breadth_preference=0.4
            ),
            bias_behavior=BiasBehavior(
                overconfidence_factor=-0.1,
                primary_anchoring_bias=BiasType.ANCHORING_CONSENSUS,
                peer_influence_susceptibility=0.7
            ),
            productivity_behavior=ProductivityBehavior(
                productivity_level=ProductivityLevel.MEDIUM_VOLUME,
                base_research_frequency=1.0,
                quality_vs_quantity_balance=0.5
            )
        )
    
    @staticmethod
    def create_sprayer_archetype() -> ArchetypeDefinition:
        """High volume, mixed results, fast progression"""
        return ArchetypeDefinition(
            name="The Sprayer",
            description="High volume research, variable accuracy, rapid idea turnover",
            accuracy_behavior=AccuracyBehavior(
                base_accuracy_level=AccuracyLevel.MEDIUM_LOW,
                accuracy_mean=0.48,
                accuracy_std=0.18,
                confidence_correlation=0.5
            ),
            timing_behavior=TimingBehavior(
                timing_style=TimingStyle.REACTIVE,
                consensus_relationship=0.2,
                base_response_delay_days=(0, 2),
                publication_frequency_multiplier=2.0
            ),
            coverage_behavior=CoverageBehavior(
                max_active_coverage=35,
                ideal_coverage_size=25,
                depth_vs_breadth_preference=0.2,
                idea_progression_speed=1.5
            ),
            bias_behavior=BiasBehavior(
                overconfidence_factor=0.3,
                availability_bias_weight=0.4,
                multitasking_efficiency=0.6
            ),
            productivity_behavior=ProductivityBehavior(
                productivity_level=ProductivityLevel.HIGH_VOLUME,
                base_research_frequency=1.8,
                quality_vs_quantity_balance=0.2
            )
        )
    
    @staticmethod
    def create_specialist_archetype() -> ArchetypeDefinition:
        """Sector-focused expert with deep knowledge"""
        return ArchetypeDefinition(
            name="The Specialist",
            description="Sector-focused expert with deep domain knowledge",
            accuracy_behavior=AccuracyBehavior(
                base_accuracy_level=AccuracyLevel.HIGH,
                accuracy_mean=0.68,
                accuracy_std=0.13,
                sector_accuracy_modifiers={
                    SectorType.INFORMATION_TECHNOLOGY: 0.15  # Example: Tech specialist
                }
            ),
            timing_behavior=TimingBehavior(
                timing_style=TimingStyle.CONSENSUS_LEADER,
                consensus_relationship=0.1,
                base_response_delay_days=(1, 3)
            ),
            coverage_behavior=CoverageBehavior(
                max_active_coverage=15,
                ideal_coverage_size=12,
                sector_concentration_limit=0.8,
                specialization_bonus=0.25
            ),
            bias_behavior=BiasBehavior(
                overconfidence_factor=0.1,
                primary_anchoring_bias=BiasType.ANCHORING_PRIOR,
                peer_influence_susceptibility=0.3
            ),
            productivity_behavior=ProductivityBehavior(
                productivity_level=ProductivityLevel.MEDIUM_VOLUME,
                base_research_frequency=1.1,
                quality_vs_quantity_balance=0.7
            )
        )



