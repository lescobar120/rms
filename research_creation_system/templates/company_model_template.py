# =============================================================================
# COMPANY MODEL TEMPLATE
# =============================================================================

from ..base.template_base import BaseTemplate, BasePublishingConfig, BaseCDEMappingConfig
from ..data_models import (
    CompanyInfo, 
    InvestmentRecommendation,
    CompanyModelData,
    ModelHeader,
    CompanyModelInfo,
    RecommendationData,
    ValuationScenarios,
    TargetPriceData,
    FinancialsData,
    FinancialMetric,
    IdeaStage,
    BuySellRec
)
# from ..utils import create_sample_financials_data
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple, Union, Type
import datetime
import time
import pandas as pd

from ..document_generation import ExcelModelGenerator, ExcelStyleConfig
from ..document_generation.utils import excel_to_pdf

@dataclass
class CompanyModelTemplateData:
    """Data structure for company model template"""
    company_info: CompanyInfo
    recommendation: InvestmentRecommendation
    
    # Optional additional fields for company model
    analyst_name: str = ""
    note_type: str = "Company Model"
    idea_stage: IdeaStage = IdeaStage.ACTIVE
    investment_thesis: str = ""
    model_assumptions: str = ""
    financials_data: Optional[FinancialsData] = None
    
    # Valuation scenario customization
    base_probability: float = 0.65
    bull_probability: float = 0.25
    bear_probability: float = 0.10
    
    def __post_init__(self):
        """Set defaults after initialization"""
        if not self.analyst_name:
            self.analyst_name = self.company_info.analyst
        
        if not self.investment_thesis:
            self.investment_thesis = f"Investment thesis for {self.company_info.name} based on {self.recommendation.theme} theme."
        
        if not self.model_assumptions:
            self.model_assumptions = f"Key assumptions include continued growth in {self.company_info.gics_sector} sector and execution on {self.recommendation.theme} strategy."
        
        # if not self.financials_data:
        #     self.financials_data = create_sample_financials_data()
    
    def to_company_model_data(self) -> CompanyModelData:
        """Convert to CompanyModelData structure for Excel generator"""
        
        # Create header
        header = ModelHeader(
            analyst_name=self.analyst_name,
            note_type=self.note_type,
            idea_stage=IdeaStage(self.idea_stage)
        )
        
        # Create company info
        company_model_info = CompanyModelInfo(
            company_name=self.company_info.name
        )
        
        # Convert recommendation
        recommendation_data = RecommendationData(
            current_buy_sell_rec=BuySellRec(self.recommendation.buy_sell_rec),
            current_ow_uw_rec=getattr(self.recommendation, 'ow_uw_rec', 'OW'),
            current_esg_rating=getattr(self.recommendation, 'esg_rating', 'Leading')
        )
        
        # Create valuation scenarios
        valuation_scenarios = ValuationScenarios()
        
        # Calculate expected returns
        if self.recommendation.last_price > 0:
            base_return = (self.recommendation.base_target - self.recommendation.last_price) / self.recommendation.last_price
            bull_return = (self.recommendation.bull_target - self.recommendation.last_price) / self.recommendation.last_price
            bear_return = (self.recommendation.bear_target - self.recommendation.last_price) / self.recommendation.last_price
        else:
            base_return = bull_return = bear_return = 0.0
        
        # Create target price data
        target_price = TargetPriceData(
            base_target_px=self.recommendation.base_target,
            base_probability=self.base_probability,
            base_exp_return=base_return,
            bull_target_px=self.recommendation.bull_target,
            bull_probability=self.bull_probability,
            bull_exp_return=bull_return,
            bear_target_px=self.recommendation.bear_target,
            bear_probability=self.bear_probability,
            bear_exp_return=bear_return
        )
        
        return CompanyModelData(
            header=header,
            company_info=company_model_info,
            recommendation=recommendation_data,
            valuation_scenarios=valuation_scenarios,
            target_price=target_price,
            financials=self.financials_data,
            investment_thesis=self.investment_thesis,
            model_assumptions=self.model_assumptions
        )


class CompanyModelPublishingConfig(BasePublishingConfig):
    """Publishing configuration specific to company model template"""
    pass


class CompanyModelCDEMappingConfig(BaseCDEMappingConfig):
    """CDE mapping configuration for company model template"""
    def __init__(self, 
                 buy_sell_field: str = "U1R2I",
                 target_price_field: str = "U1R2J",
                 eps_current_field: str = "U1R2K",
                 eps_next_field: str = "U1R2L"):
        field_mappings = {
            "buy_sell_rec": buy_sell_field,
            "base_target": target_price_field,
            "current_year_eps": eps_current_field,
            "next_year_eps": eps_next_field
        }
        super().__init__(field_mappings)


class CompanyModelTemplate(BaseTemplate):
    """Company model template generating Excel files"""
    
    @property
    def template_name(self) -> str:
        return "company_model"
    
    @property
    def output_file_types(self) -> List[str]:
        return ["xlsx"]
    
    @property
    def required_data_fields(self) -> List[str]:
        return ["company_info", "recommendation"]
    
    def generate_document(self, data: CompanyModelTemplateData, output_filename: str) -> Dict[str, str]:
        """Generate company model Excel file"""
        self.validate_data(data)
        
        excel_path = f"{output_filename}.xlsx"
        pdf_path = f"{output_filename}.pdf"
        
        # Convert to CompanyModelData structure
        company_model_data = data.to_company_model_data()
        
        # Initialize Excel generator
        generator = ExcelModelGenerator(self.style_config)
        generator.create_workbook(excel_path)
        
        # Add all sections using the structured approach
        self.add_company_model_sections(generator, company_model_data)
        
        # Save the workbook
        generator.save_workbook()
        #time.sleep(1)
        excel_to_pdf(excel_path, pdf_path)
        
        return {"xlsx": excel_path, "pdf": pdf_path}
    
    def add_company_model_sections(self, generator: ExcelModelGenerator, data: CompanyModelData):
        """Add all sections to the company model"""
        
        # Header section
        # generator.add_header_section(
        #     analyst_name=data.header.analyst_name,
        #     note_type=data.header.note_type,
        #     revision_date=data.header.revision_date,
        #     idea_stage=data.header.idea_stage.value
        # )

        generator.add_header_section(
            data=data.header
        )
        
        # Company title
        # generator.add_company_title(
        #     company_name=data.company_info.company_name,
        #     model_date=data.company_info.model_date
        # )

        generator.add_company_title(
            data=data.company_info
        )
        
        # Recommendation section with valuation scenarios
        valuation_scenarios = {
            "base": data.valuation_scenarios.base_case,
            "bull": data.valuation_scenarios.bull_case,
            "bear": data.valuation_scenarios.bear_case
        }
        
        target_data = {
            "base": {
                "target": data.target_price.base_target_px,
                "probability": data.target_price.base_probability,
                "return": data.target_price.base_exp_return
            },
            "bull": {
                "target": data.target_price.bull_target_px or data.target_price.base_target_px * 1.2,
                "probability": data.target_price.bull_probability,
                "return": data.target_price.bull_exp_return
            },
            "bear": {
                "target": data.target_price.bear_target_px or data.target_price.base_target_px * 0.8,
                "probability": data.target_price.bear_probability,
                "return": data.target_price.bear_exp_return
            }
        }
        
        # Convert InvestmentRecommendation-like object for the generator
        recommendation_for_generator = type('obj', (object,), {
            'buy_sell_rec': data.recommendation.current_buy_sell_rec.value,
            'ow_uw_rec': data.recommendation.current_ow_uw_rec,
            'esg_rating': data.recommendation.current_esg_rating,
            'base_target': data.target_price.base_target_px,
            'last_price': 0  # This would come from market data in real usage
        })()
        
        generator.add_recommendation_section(
            recommendation=recommendation_for_generator,
            valuation_scenarios=valuation_scenarios,
            target_data=target_data
        )

        # Thesis
        generator.add_model_thesis_section(data)
        
        # Model assumptions
        generator.add_model_assumptions_section(data)
        
        # Financial model
        financials_dict = {
            'years': data.financials.years,
            'metrics': data.financials.metrics
        }
        generator.add_financials_section(financials_dict)
    
    def get_required_tags(self, data: CompanyModelTemplateData, config: CompanyModelPublishingConfig) -> List[str]:
        """Get tag types needed for company model template"""
        return ["primary_security", "author"] + [f"taglist_{i}" for i in range(len(config.taglists))]
    
    def prepare_cde_data(self, data: CompanyModelTemplateData, ticker: str,
                        config: CompanyModelPublishingConfig,
                        cde_config: CompanyModelCDEMappingConfig) -> pd.DataFrame:
        """Prepare CDE data for company model template"""
        date_str = datetime.datetime.strptime(config.as_of_date, '%Y-%m-%d').strftime('%Y%m%d')
        
        cde_records = []
        
        # Basic recommendation fields
        if "buy_sell_rec" in cde_config.field_mappings:
            cde_records.append({
                'parsekey': ticker,
                'field': cde_config.field_mappings["buy_sell_rec"],
                'value': data.recommendation.buy_sell_rec,
                'date': date_str
            })
        
        if "base_target" in cde_config.field_mappings:
            cde_records.append({
                'parsekey': ticker,
                'field': cde_config.field_mappings["base_target"],
                'value': data.recommendation.base_target,
                'date': date_str
            })
        
        # EPS estimates from financials
        if data.financials_data and data.financials_data.metrics:
            eps_metrics = [m for m in data.financials_data.metrics if 'EPS' in m.metric_name]
            if eps_metrics and len(data.financials_data.years) >= 2:
                current_year = data.financials_data.years[-2]  # Current year estimate
                next_year = data.financials_data.years[-1]     # Next year estimate
                
                if "current_year_eps" in cde_config.field_mappings:
                    current_eps = eps_metrics[0].values.get(current_year)
                    if current_eps:
                        cde_records.append({
                            'parsekey': ticker,
                            'field': cde_config.field_mappings["current_year_eps"],
                            'value': current_eps,
                            'date': date_str
                        })
                
                if "next_year_eps" in cde_config.field_mappings:
                    next_eps = eps_metrics[0].values.get(next_year)
                    if next_eps:
                        cde_records.append({
                            'parsekey': ticker,
                            'field': cde_config.field_mappings["next_year_eps"],
                            'value': next_eps,
                            'date': date_str
                        })
        
        return pd.DataFrame(cde_records)


