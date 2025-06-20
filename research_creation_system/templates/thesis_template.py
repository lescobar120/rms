# =============================================================================
# THESIS TEMPLATE
# =============================================================================


from ..base.template_base import BaseTemplate, BasePublishingConfig, BaseCDEMappingConfig
from ..data_models import CompanyInfo, InvestmentRecommendation
from dataclasses import dataclass

from ..document_generation import BloombergReportGenerator, TableStyle
from ..document_generation.utils import convert_docx_to_pdf_silently
from ..data_models import CompanyInfo, InvestmentRecommendation

import datetime
import pandas as pd
from typing import List, Dict, Any, Optional, Tuple, Union, Type


@dataclass
class ThesisTemplateData:
    """Data structure for thesis template"""
    company_info: CompanyInfo
    recommendation: InvestmentRecommendation
    thesis_text: str
    financials_df: pd.DataFrame
    portfolio_df: pd.DataFrame


class ThesisPublishingConfig(BasePublishingConfig):
    """Publishing configuration specific to thesis template"""
    pass


class ThesisCDEMappingConfig(BaseCDEMappingConfig):
    """CDE mapping configuration for thesis template"""
    def __init__(self, 
                 buy_sell_field: str = "U1R2I",
                 target_price_field: str = "U1R2J", 
                 esg_rating_field: str = "U1R2K"):
        field_mappings = {
            "buy_sell_rec": buy_sell_field,
            "base_target": target_price_field,
            "esg_rating": esg_rating_field
        }
        super().__init__(field_mappings)


class ThesisTemplate(BaseTemplate):
    """Research thesis template with full analysis"""
    
    @property
    def template_name(self) -> str:
        return "thesis"
    
    @property
    def output_file_types(self) -> List[str]:
        return ["docx", "pdf"]
    
    @property
    def required_data_fields(self) -> List[str]:
        return ["company_info", "recommendation", "thesis_text", "financials_df", "portfolio_df"]
    
    def generate_document(self, data: ThesisTemplateData, output_filename: str) -> Dict[str, str]:
        """Generate thesis document (DOCX and PDF)"""
        self.validate_data(data)

        # print(f"Generating {self.template_name}")
        # print(f"Output types: {self.output_file_types}")
        
        docx_path = f"{output_filename}.docx"
        pdf_path = f"{output_filename}.pdf"
        
        # Initialize generator with thesis-specific methods
        generator = BloombergReportGenerator(self.style_config)
        generator.create_document()
        
        # Add thesis-specific sections
        self.add_thesis_sections(generator, data)
        
        # Save documents
        generator.save_document(docx_path)
        convert_docx_to_pdf_silently(docx_path, pdf_path)
        
        return {"docx": docx_path, "pdf": pdf_path}
    
    def add_thesis_sections(self, generator: BloombergReportGenerator, data: ThesisTemplateData):
        """Add all sections for thesis template"""
        generator.add_company_header(data.company_info.name)
        generator.add_company_info_section(data.company_info)
        generator.add_recommendation_section(data.recommendation)
        generator.add_thesis_section("Investment Thesis:", data.thesis_text)
        
        # Convert DataFrames to table data
        financials_data = self._dataframe_to_table_data(data.financials_df)
        portfolio_data = self._dataframe_to_table_data(data.portfolio_df)
        
        generator.add_financials_section("Financials & Forecasts", financials_data)
        generator.add_portfolio_exposure_section("Portfolio Exposure", portfolio_data)
    
    def get_required_tags(self, data: ThesisTemplateData, config: ThesisPublishingConfig) -> List[str]:
        """Get tag types needed for thesis template"""
        return ["primary_security", "author"] + [f"taglist_{i}" for i in range(len(config.taglists))]
    
    def prepare_cde_data(self, data: ThesisTemplateData, ticker: str, 
                        config: ThesisPublishingConfig, 
                        cde_config: ThesisCDEMappingConfig) -> pd.DataFrame:
        """Prepare CDE data for thesis template"""
        date_str = datetime.datetime.strptime(config.as_of_date, '%Y-%m-%d').strftime('%Y%m%d')
        
        cde_records = []
        for field_name, field_code in cde_config.field_mappings.items():
            if hasattr(data.recommendation, field_name):
                value = getattr(data.recommendation, field_name)
                cde_records.append({
                    'parsekey': ticker,
                    'field': field_code,
                    'value': value,
                    'date': date_str
                })
        
        return pd.DataFrame(cde_records)
    

