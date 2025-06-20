"""
Individual behavioral component definitions.
Each behavior represents one dimension of analyst characteristics.
"""

# =============================================================================
# BEHAVIORAL COMPONENT CLASSES
# =============================================================================

from typing import Dict, List, Optional, Union, Tuple
from dataclasses import dataclass, field

from .enums import (
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
class AccuracyBehavior:
    """Defines analyst accuracy characteristics and patterns"""
    
    # Core accuracy parameters
    base_accuracy_level: AccuracyLevel
    accuracy_mean: float  # 0.0 to 1.0
    accuracy_std: float   # Standard deviation
    
    # Sector-specific variations
    sector_accuracy_modifiers: Dict[SectorType, float] = field(default_factory=dict)
    
    # Confidence and precision
    confidence_correlation: float = 0.7  # How well confidence matches actual accuracy
    estimate_precision_bias: float = 0.0  # Tendency to over/under estimate
    
    # Learning and adaptation
    learning_rate: float = 0.05  # How quickly accuracy adapts
    experience_bonus: float = 0.1  # Accuracy improvement over time
    
    # Forecast horizon capabilities
    short_term_accuracy_bonus: float = 0.0   # 1-3 months
    medium_term_accuracy_bonus: float = 0.0  # 3-12 months
    long_term_accuracy_penalty: float = 0.0  # 12+ months

@dataclass
class TimingBehavior:
    """Defines analyst timing and responsiveness characteristics"""
    
    # Core timing style
    timing_style: TimingStyle
    consensus_relationship: float  # -1.0 (contrarian) to 1.0 (follower)
    
    # Response timing parameters
    base_response_delay_days: Tuple[float, float]  # (min, max) days
    event_sensitivity_threshold: float = 0.05  # Minimum magnitude to respond
    
    # Publication frequency
    publication_frequency_multiplier: float = 1.0  # vs sector average
    revision_frequency: float = 0.3  # Likelihood of revising vs new coverage
    
    # Event-specific timing
    earnings_response_speed: float = 1.0  # Multiplier for earnings events
    news_response_speed: float = 1.0      # Multiplier for news events
    market_move_response_speed: float = 1.0  # Multiplier for price movements
    
    # Consensus dynamics
    consensus_deviation_comfort: float = 0.15  # How far from consensus willing to go
    early_mover_tendency: float = 0.5  # Likelihood to move before consensus

@dataclass
class CoverageBehavior:
    """Defines analyst coverage preferences and capacity"""
    
    # Coverage universe sizing
    max_active_coverage: int = 20
    max_monitoring_coverage: int = 40
    ideal_coverage_size: int = 15
    
    # Sector preferences
    sector_preferences: Dict[SectorType, float] = field(default_factory=dict)
    sector_concentration_limit: float = 0.6  # Max % in single sector
    
    # Market cap preferences
    market_cap_preferences: Dict[MarketCapType, float] = field(default_factory=dict)
    
    # Research depth vs breadth
    depth_vs_breadth_preference: float = 0.5  # 0.0=breadth, 1.0=depth
    specialization_bonus: float = 0.1  # Accuracy bonus in preferred sectors
    
    # Idea lifecycle management
    idea_progression_speed: float = 1.0  # How quickly ideas move through stages
    abandonment_threshold: float = 0.3   # Performance threshold for abandoning ideas
    
    # Capacity management
    attention_allocation_efficiency: float = 0.8  # How well attention is managed

@dataclass
class BiasBehavior:
    """Defines behavioral biases and cognitive tendencies"""
    
    # Confidence biases
    overconfidence_factor: float = 0.0    # -0.5 to 0.5
    confidence_calibration: float = 0.8   # How well confidence matches reality
    
    # Anchoring behaviors
    primary_anchoring_bias: BiasType = BiasType.ANCHORING_CONSENSUS
    anchoring_strength: float = 0.3       # 0.0 to 1.0
    anchor_adjustment_speed: float = 0.5  # How quickly anchors are updated
    
    # Loss aversion and risk
    loss_aversion_coefficient: float = 2.0  # Standard behavioral economics value
    risk_tolerance: float = 0.5            # 0.0=risk averse, 1.0=risk seeking
    
    # Confirmation and availability biases
    confirmation_bias_strength: float = 0.3
    availability_bias_weight: float = 0.2  # Weight recent events more heavily
    
    # Social and peer influence
    peer_influence_susceptibility: float = 0.4
    consensus_pressure_sensitivity: float = 0.3

@dataclass
class ProductivityBehavior:
    """Defines research productivity and workflow characteristics"""
    
    # Research volume characteristics
    productivity_level: ProductivityLevel
    base_research_frequency: float = 1.0  # Publications per month per covered name
    
    # Content type preferences
    content_type_preferences: Dict[ContentType, float] = field(default_factory=dict)
    research_depth_preference: float = 0.5  # 0.0=quick updates, 1.0=deep research
    
    # Workflow and time management
    multitasking_efficiency: float = 0.7     # Ability to handle multiple ideas
    deadline_pressure_response: float = 0.8  # Performance under time pressure
    
    # Idea generation and progression
    idea_generation_rate: float = 1.0       # New ideas per month
    idea_completion_rate: float = 0.8       # % of ideas that reach publication
    
    # Quality vs quantity trade-offs
    quality_vs_quantity_balance: float = 0.5  # 0.0=quantity, 1.0=quality
    revision_thoroughness: float = 0.7        # How carefully revisions are made



