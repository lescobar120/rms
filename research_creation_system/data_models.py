from dataclasses import dataclass, field
import datetime

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
    update_date: str = field(default_factory=lambda: datetime.datetime.today().strftime('%d-%b-%Y'))

@dataclass
class InvestmentRecommendation:
    """Investment recommendation data structure"""
    buy_sell_rec: str
    idea_stage: str
    esg_rating: str
    theme: str
    last_price: float
    base_target: float
    bull_target: float
    bear_target: float