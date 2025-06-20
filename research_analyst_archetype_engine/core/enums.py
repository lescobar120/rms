"""
Core enumerations for the archetype system.
All enum definitions used across the system.
"""

# =============================================================================
# CORE ENUMS
# =============================================================================

from enum import Enum


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

