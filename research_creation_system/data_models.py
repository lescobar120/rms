# =============================================================================
# DATA MODELS
# =============================================================================

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import datetime
from enum import Enum


# =============================================================================
# CDE AND TAGLIST DATA ENUMS
# =============================================================================

class IdeaStage(str, Enum):
    """Idea stage enumeration for company models"""
    IDEA = "Idea"
    WIP = "WIP"
    PASS = "Pass"
    ACTIVE = "Active"
    EXIT = "Exit"


class BuySellRec(str, Enum):
    """Buy/Sell recommendation enumeration"""
    STRONG_BUY = "Strong Buy"
    BUY = "Buy"
    HOLD = "Hold"
    SELL = "Sell"
    STRONG_SELL = "Strong Sell"
    INACTIVE = "Inactive"

class EquityNoteTypeTagList(str, Enum):
    """Buyside EQ Note Type"""
    COMPANY_MODEL = "Company Model"
    EARNINGS = "Earnings"
    EVENT_DRIVEN = "Event Driven"
    IC_PRESENTATION = "IC Presentation"
    INDUSTRY = "Industry"
    INITIATION = "Initiation"
    MEETING_NOTE = "Meeting Note"
    NEW_IDEA = "New Idea"
    NEWS = "News"
    PRE_EARNINGS = "Pre Earnings"
    QUICK_TAKE = "Quick Take"
    RECOMMENDATION_UPDATE = "Recommendation Update"
    STAGE_UPDATE = "Stage Update"
    THEMATIC = "Thematic"
    THESIS_NOTE = "Thesis Note"

class InvestmentThemeTagList(str, Enum):
    """Buyside EQ Investment Theme Taglist"""
    APPLYING_AI = "Applying AI"
    BAD_ECONOMY_WINNERS = "Bad Economy Winners"
    CARBON_TRANSITION_WINNER = "Carbon Transition Winner"
    CHINA_CHALLENGES_AND_OPPORTUNITIES = "China Challenges and Opportunities"
    DIVIDEND_COMEBACK = "Dividend Comeback"
    EM_DIGITIZATION = "EM Digitization"
    ESG_EDGE = "ESG Edge"
    EVOLUTION_OF_EATING = "Evolution of Eating"
    FUTURE_OF_FINANCIALS = "Future of Financials"
    HEALTH_CARE_INNOVATION = "Health Care Innovation"
    INVESTING_IN_INDIA = "Investing in India"
    LAVISH_LUXURY = "Lavish Luxury"
    MAGNIFICENT_MANAGEMENT = "Magnificent Management"
    MEDIA_DISRUPTION = "Media Disruption"
    MIDDLE_AGED_MILLENIALS = "Middle Aged Millenials"
    POST_ELECTION_CONSUMER_SENTIMENT = "Post Election Consumer Sentiment"
    PREMIUM_CONTENT_WARS = "Premium Content Wars"
    PRICING_POWER = "Pricing Power"
    TECH_TRIFECTA = "Tech Trifecta"
    TRANSPORTATION_TRANSFORMATION = "Transportation Transformation"


# =============================================================================
# WORD TEMPLATE DATA MODELS
# =============================================================================

@dataclass 
class CompanyInfo:
    """Company information data structure"""
    name: str
    country: str
    analyst: str
    gics_sector: str
    gics_industry_group: str
    gics_industry: str
    gics_sub_industry: str
    update_date: str = field(default_factory=lambda: datetime.datetime.now().strftime('%m-%d-%Y'))


@dataclass
class InvestmentRecommendation:
    """Investment recommendation data structure"""
    buy_sell_rec: BuySellRec
    idea_stage: IdeaStage
    esg_rating: str
    theme: InvestmentThemeTagList
    last_price: float
    base_target: float
    bull_target: float = 0.0
    bear_target: float = 0.0
    
    def __post_init__(self):
        # Set default bull/bear targets if not provided
        if self.bull_target == 0.0:
            self.bull_target = self.base_target * 1.20
        if self.bear_target == 0.0:
            self.bear_target = self.base_target * 0.80


@dataclass
class EarningsEstimate:
    """Individual earnings estimate data"""
    metric_name: str  # e.g., “Revenue”, “EPS”, “EBITDA”
    consensus_estimate: float
    analyst_estimate: float
    difference: float = field(init=False)
    difference_pct: float = field(init=False)
    prior_year_actual: Optional[float] = None


    def __post_init__(self):
        """Calculate difference and percentage"""
        self.difference = self.analyst_estimate - self.consensus_estimate
        if self.consensus_estimate != 0:
            self.difference_pct = (self.difference / self.consensus_estimate) * 100
        else:
            self.difference_pct = 0.0


@dataclass
class EarningsScenario:
    """Earnings scenario analysis"""
    scenario_name: str  # “Bull”, “Base”, “Bear”
    probability: float  # 0.0 to 1.0
    revenue_estimate: float
    eps_estimate: float
    key_assumptions: List[str]
    stock_reaction: str  # e.g., “+5% to +10%”, “Flat to -3%”

@dataclass
class HistoricalPattern:
    """Historical earnings surprise pattern"""
    quarter: str  # e.g., “Q1 2024”, “Q4 2023”
    revenue_surprise_pct: float
    eps_surprise_pct: float
    stock_reaction_1d: float  # 1-day stock reaction
    stock_reaction_1w: float  # 1-week stock reaction


# =============================================================================
# EXCEL TEMPLATE COMPANY MODEL DATA STRUCTURES
# =============================================================================

@dataclass
class ModelHeader:
    """Header information for company model"""
    analyst_name: str
    note_type: str = "Company Model"
    revision_date: str = ""
    idea_stage: IdeaStage = IdeaStage.ACTIVE
    
    def __post_init__(self):
        if not self.revision_date:
            self.revision_date = datetime.datetime.now().strftime("%d-%b-%y")


@dataclass
class CompanyModelInfo:
    """Company model title information"""
    company_name: str
    model_date: str = ""
    
    def __post_init__(self):
        if not self.model_date:
            self.model_date = datetime.datetime.now().strftime("%m/%d/%Y")


@dataclass
class RecommendationData:
    """Recommendation table data for company models"""
    current_buy_sell_rec: BuySellRec
    current_ow_uw_rec: str = "OW"
    current_esg_rating: str = "Leading"
    previous_buy_sell_rec: Optional[BuySellRec] = None
    previous_ow_uw_rec: str = ""
    previous_esg_rating: str = ""


@dataclass
class ValuationScenarios:
    """Valuation scenarios data"""
    base_case: str = "Base Case"
    bull_case: str = "Bull Case"
    bear_case: str = "Bear Case"


@dataclass
class TargetPriceData:
    """Target price and probability data for all scenarios"""
    # Base Case
    base_target_px: float
    base_probability: float = 0.65
    base_exp_return: float = 0.0
    
    # Bull Case (optional)
    bull_target_px: Optional[float] = None
    bull_probability: float = 0.25
    bull_exp_return: float = 0.0
    
    # Bear Case (optional)
    bear_target_px: Optional[float] = None
    bear_probability: float = 0.10
    bear_exp_return: float = 0.0
    
    def __post_init__(self):
        """Calculate expected returns if not provided"""
        # Note: This would typically require the current price for calculation
        # For now, we'll leave returns as 0.0 if not explicitly set
        pass


@dataclass
class FinancialMetric:
    """Single financial metric across years"""
    metric_name: str
    values: Dict[str, Any]  # year -> value mapping


@dataclass
class FinancialsData:
    """Complete financials and forecast data"""
    years: List[str]  # e.g., ['2022', '2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030']
    metrics: List[FinancialMetric]


@dataclass
class CompanyModelData:
    """Complete data structure for company model (integrates all components)"""
    header: ModelHeader
    company_info: CompanyModelInfo
    recommendation: RecommendationData
    valuation_scenarios: ValuationScenarios
    target_price: TargetPriceData
    financials: FinancialsData
    investment_thesis: str = ""
    model_assumptions: str = ""

