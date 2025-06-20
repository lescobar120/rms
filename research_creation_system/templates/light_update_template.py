# =============================================================================
# LIGHT UPDATE TEMPLATE
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
class LightUpdateTemplateData:
    """Data structure for light update template"""
    company_info: CompanyInfo
    recommendation: InvestmentRecommendation


class LightUpdatePublishingConfig(BasePublishingConfig):
    """Publishing configuration specific to light update template"""
    pass


class LightUpdateCDEMappingConfig(BaseCDEMappingConfig):
    """CDE mapping configuration for light update template"""
    def __init__(self, 
                 buy_sell_field: str = "U1R2I",
                 target_price_field: str = "U1R2J"):
        field_mappings = {
            "buy_sell_rec": buy_sell_field,
            "base_target": target_price_field
        }
        super().__init__(field_mappings)


class LightUpdateTemplate(BaseTemplate):
    """Light research update template with basic info only"""
    
    @property
    def template_name(self) -> str:
        return "light_update"
    
    @property
    def output_file_types(self) -> List[str]:
        return ["docx", "pdf"]
    
    @property
    def required_data_fields(self) -> List[str]:
        return ["company_info", "recommendation"]
    
    def generate_document(self, data: LightUpdateTemplateData, output_filename: str) -> Dict[str, str]:
        """Generate light update document (DOCX and PDF)"""
        self.validate_data(data)

        # print(f"Generating {self.template_name}")
        # print(f"Output types: {self.output_file_types}")
        
        docx_path = f"{output_filename}.docx"
        pdf_path = f"{output_filename}.pdf"
        
        # Initialize generator with light update specific methods
        generator = BloombergReportGenerator(self.style_config)
        generator.create_document()
        
        # Add light update specific sections
        self.add_light_update_sections(generator, data)
        
        # Save documents
        generator.save_document(docx_path)
        convert_docx_to_pdf_silently(docx_path, pdf_path)
        
        return {"docx": docx_path, "pdf": pdf_path}
    
    def add_light_update_sections(self, generator: BloombergReportGenerator, data: LightUpdateTemplateData):
        """Add sections for light update template"""
        generator.add_company_header(data.company_info.name)
        generator.add_company_info_section(data.company_info)
        generator.add_recommendation_section(data.recommendation)
        # Note: No thesis, financials, or portfolio sections for light update
    
    def get_required_tags(self, data: LightUpdateTemplateData, config: LightUpdatePublishingConfig) -> List[str]:
        """Get tag types needed for light update template"""
        return ["primary_security", "author"] + [f"taglist_{i}" for i in range(len(config.taglists))]
    
    def prepare_cde_data(self, data: LightUpdateTemplateData, ticker: str,
                        config: LightUpdatePublishingConfig,
                        cde_config: LightUpdateCDEMappingConfig) -> pd.DataFrame:
        """Prepare CDE data for light update template"""
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
    

