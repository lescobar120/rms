
"""
Analyst Archetype System - Class Skeleton
==========================================

This module defines the core data structures for analyst archetypes,
behavioral components, and supporting enums for the research simulation engine.
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Union, Tuple
from datetime import datetime, date
import uuid


# =============================================================================
# CORE ENUMS
# =============================================================================

class SectorType(Enum):
    """GICS Sector Classifications"""
    COMMUNICATION_SERVICES = "Communication Services"
    CONSUMER_DISCRETIONARY = "Consumer Discretionary"
    CONSUMER_STAPLES = "Consumer Staples"
    ENERGY = "Energy"
    FINANCIALS = "Financials"
    HEALTH_CARE = "Health Care"
    INDUSTRIALS = "Industrials"
    INFORMATION_TECHNOLOGY = "Information Technology"
    MATERIALS = "Materials"
    REAL_ESTATE = "Real Estate"
    UTILITIES = "Utilities"

class MarketCapType(Enum):
    """Market Capitalization Classifications"""
    LARGE_CAP = "Large Cap"
    MID_CAP = "Mid Cap"
    SMALL_CAP = "Small Cap"
    MICRO_CAP = "Micro Cap"

class RecommendationType(Enum):
    """Investment Recommendations"""
    STRONG_BUY = "Strong Buy"
    BUY = "Buy"
    HOLD = "Hold"
    SELL = "Sell"
    STRONG_SELL = "Strong Sell"

class IdeaStageType(Enum):
    """Research Idea Lifecycle Stages"""
    SCREENING = "Screening"
    INITIAL_RESEARCH = "Initial Research"
    DEEP_DIVE = "Deep Dive"
    ACTIVE_COVERAGE = "Active Coverage"
    MONITORING = "Monitoring"
    WIND_DOWN = "Wind Down"
    ABANDONED = "Abandoned"

class EventType(Enum):
    """Market and Corporate Events"""
    EARNINGS_ANNOUNCEMENT = "Earnings Announcement"
    GUIDANCE_UPDATE = "Guidance Update"
    MANAGEMENT_CHANGE = "Management Change"
    MERGER_ACQUISITION = "Merger & Acquisition"
    DIVIDEND_ANNOUNCEMENT = "Dividend Announcement"
    STOCK_SPLIT = "Stock Split"
    CONFERENCE_CALL = "Conference Call"
    INVESTOR_DAY = "Investor Day"
    REGULATORY_NEWS = "Regulatory News"
    SECTOR_NEWS = "Sector News"
    MARKET_MOVEMENT = "Market Movement"

class ContentType(Enum):
    """Research Content Types"""
    COMPANY_MODEL = "Company Model"
    EARNINGS_PREVIEW = "Earnings Preview"
    SECTOR_RESEARCH = "Sector Research"
    QUICK_UPDATE = "Quick Update"
    INITIATION_COVERAGE = "Initiation Coverage"
    MEETING_NOTE = "Meeting Note"
    THESIS_UPDATE = "Thesis Update"

class AccuracyLevel(Enum):
    """Analyst Accuracy Classifications"""
    HIGH = "High"
    MEDIUM_HIGH = "Medium-High"
    MEDIUM = "Medium"
    MEDIUM_LOW = "Medium-Low"
    LOW = "Low"

class TimingStyle(Enum):
    """Analyst Timing Characteristics"""
    EARLY_MOVER = "Early Mover"
    CONSENSUS_LEADER = "Consensus Leader"
    MARKET_FOLLOWER = "Market Follower"
    CONTRARIAN = "Contrarian"
    REACTIVE = "Reactive"

class ProductivityLevel(Enum):
    """Research Productivity Levels"""
    HIGH_VOLUME = "High Volume"
    MEDIUM_VOLUME = "Medium Volume"
    LOW_VOLUME = "Low Volume"
    SELECTIVE = "Selective"

class BiasType(Enum):
    """Behavioral Bias Classifications"""
    OVERCONFIDENT = "Overconfident"
    UNDERCONFIDENT = "Underconfident"
    ANCHORING_CONSENSUS = "Anchoring - Consensus"
    ANCHORING_PRICE = "Anchoring - Price"
    ANCHORING_PRIOR = "Anchoring - Prior Views"
    LOSS_AVERSE = "Loss Averse"
    MOMENTUM_CHASER = "Momentum Chaser"
    CONTRARIAN_BIAS = "Contrarian Bias"

class PerformanceState(Enum):
    """Current Performance State"""
    HOT_STREAK = "Hot Streak"
    COLD_STREAK = "Cold Streak"
    NEUTRAL = "Neutral"
    RECOVERING = "Recovering"
    DECLINING = "Declining"


# =============================================================================
# BEHAVIORAL COMPONENT CLASSES
# =============================================================================

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


# =============================================================================
# CORE ANALYST AND ARCHETYPE CLASSES
# =============================================================================

@dataclass
class AnalystProfile:
    """Core analyst identification and static characteristics"""
    
    # Basic identification
    analyst_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    team: str = ""
    
    # Career information
    start_date: date = field(default_factory=date.today)
    years_experience: float = 0.0
    prior_firm_experience: List[str] = field(default_factory=list)
    
    # Coverage assignment
    primary_sectors: List[SectorType] = field(default_factory=list)
    coverage_universe: List[str] = field(default_factory=list)  # Security IDs or dynamic BQL Universe?
    
    # Professional characteristics
    education_background: str = ""
    certifications: List[str] = field(default_factory=list)
    specializations: List[str] = field(default_factory=list)

@dataclass
class AnalystState:
    """Dynamic analyst state and current status"""
    
    # Performance tracking
    current_performance_state: PerformanceState = PerformanceState.NEUTRAL
    current_accuracy_streak: int = 0
    confidence_level: float = 0.5  # Current confidence (0.0 to 1.0)
    
    # Activity and workload
    active_ideas: List[str] = field(default_factory=list)  # Idea IDs
    current_workload: float = 0.5  # 0.0 to 1.0
    last_publication_date: Optional[datetime] = None
    
    # Recent performance metrics
    last_30_day_accuracy: Optional[float] = None
    last_90_day_accuracy: Optional[float] = None
    ytd_accuracy: Optional[float] = None
    
    # Attention and focus
    attention_allocation: Dict[str, float] = field(default_factory=dict)  # Security ID -> attention %
    current_focus_areas: List[str] = field(default_factory=list)
    
    # Market context awareness
    recent_market_performance: float = 0.0  # Relative to benchmark
    sector_performance_awareness: Dict[SectorType, float] = field(default_factory=dict)

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

@dataclass
class AnalystInstance:
    """Complete analyst instance combining profile, archetype, and current state"""
    
    # Core components
    profile: AnalystProfile
    archetype: ArchetypeDefinition
    current_state: AnalystState
    
    # Instance-specific parameters (randomized within archetype ranges)
    instance_parameters: Dict[str, float] = field(default_factory=dict)
    
    # Historical tracking
    performance_history: List[Dict] = field(default_factory=list)
    activity_history: List[Dict] = field(default_factory=list)
    
    # Calibration and tuning
    calibration_date: datetime = field(default_factory=datetime.now)
    last_parameter_update: datetime = field(default_factory=datetime.now)


# =============================================================================
# PREDEFINED ARCHETYPE TEMPLATES
# =============================================================================

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


# =============================================================================
# FACTORY AND BUILDER CLASSES
# =============================================================================

class AnalystFactory:
    """Factory class for creating analyst instances with proper initialization"""
    
    @staticmethod
    def create_analyst_from_archetype(
        archetype: ArchetypeDefinition,
        profile_data: Dict = None,
        parameter_randomization: bool = True
    ) -> AnalystInstance:
        """Create a new analyst instance from an archetype template"""
        # Implementation would go here - this is just the method signature
        pass
    
    @staticmethod
    def create_random_analyst(
        sector_focus: Optional[SectorType] = None,
        experience_range: Tuple[float, float] = (1.0, 15.0)
    ) -> AnalystInstance:
        """Create a random analyst with randomized archetype characteristics"""
        # Implementation would go here - this is just the method signature
        pass


class ArchetypeBuilder:
    """Builder class for creating custom archetypes"""
    
    def __init__(self):
        self.archetype = ArchetypeDefinition()
    
    def set_accuracy_profile(self, **kwargs) -> 'ArchetypeBuilder':
        """Set accuracy behavior parameters"""
        # Implementation would go here - this is just the method signature
        return self
    
    def set_timing_profile(self, **kwargs) -> 'ArchetypeBuilder':
        """Set timing behavior parameters"""
        # Implementation would go here - this is just the method signature
        return self
    
    def build(self) -> ArchetypeDefinition:
        """Build and return the configured archetype"""
        return self.archetype