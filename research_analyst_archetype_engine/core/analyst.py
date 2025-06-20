"""
Core analyst data structures.
Profile, state, and instance management.
"""
# AnalystProfile, AnalystState, AnalystInstance
# State management and persistence helpers

# =============================================================================
# CORE ANALYST CLASSES
# =============================================================================

from datetime import datetime, date
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Union, Tuple
import uuid

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

from .archetypes import ArchetypeDefinition


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


def validate_analyst_instance():
    pass