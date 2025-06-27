"""
Research Content System - Main Package
Automated research content generation and publishing for Bloomberg RMS
"""

# Import key classes that users will commonly need

# Core orchestration
from .orchestrator import ResearchContentOrchestrator

# Data models
from .data_models import CompanyInfo, InvestmentRecommendation

# Document generation (most commonly used)
from .document_generation import (
    BloombergReportGenerator,
    TableStyle,
    FontStyle,
    convert_docx_to_pdf_silently
)

# Template system
from .base.template_base import TaglistMapping
from .templates.registry import TEMPLATE_REGISTRY, get_template, list_templates
from .templates.thesis_template import (
    ThesisTemplate, 
    ThesisTemplateData, 
    ThesisPublishingConfig,
    ThesisCDEMappingConfig
)
from .templates.light_update_template import (
    LightUpdateTemplate,
    LightUpdateTemplateData, 
    LightUpdatePublishingConfig,
    LightUpdateCDEMappingConfig
)
from .templates.earnings_preview_template import (
    EarningsPreviewTemplate,
    EarningsPreviewTemplateData,
    EarningsPreviewPublishingConfig,
    EarningsPreviewCDEMappingConfig
)
from .templates.company_model_template import (
    CompanyModelTemplate,
    CompanyModelTemplateData, 
    CompanyModelPublishingConfig,
    CompanyModelCDEMappingConfig
)

# Utils
from .utils import (
    create_sample_thesis_data, 
    create_sample_light_update_data, 
    create_sample_earnings_preview_data,
    create_sample_financials_data, create_sample_company_model_data, create_sample_company_model_template_data
)

# Define what gets imported with "from research_content_system import *"
__all__ = [
    # Core functionality
    'ResearchContentOrchestrator',
    'TEMPLATE_REGISTRY',
    'get_template',
    'list_templates',
    
    # Data models
    'CompanyInfo',
    'InvestmentRecommendation', 
    'TaglistMapping',

    # Document generation
    'BloombergReportGenerator',
    'TableStyle',
    'FontStyle', 
    'convert_docx_to_pdf_silently',
    
    # Thesis template
    'ThesisTemplate',
    'ThesisTemplateData',
    'ThesisPublishingConfig',
    'ThesisCDEMappingConfig',
    
    # Light update template
    'LightUpdateTemplate',
    'LightUpdateTemplateData',
    'LightUpdatePublishingConfig', 
    'LightUpdateCDEMappingConfig',

    # Earnings Preview Template
    'EarningsPreviewTemplate',
    'EarningsPreviewTemplateData',
    'EarningsPreviewPublishingConfig',
    'EarningsPreviewCDEMappingConfig',

    # Company Model Template
    'CompanyModelTemplate',
    'CompanyModelTemplateData', 
    'CompanyModelPublishingConfig',
    'CompanyModelCDEMappingConfig',

    # Utils
    'create_sample_thesis_data',
    'create_sample_light_update_data',
    'create_sample_earnings_preview_data',
    'create_sample_financials_data',
    'create_sample_company_model_data', 
    'create_sample_company_model_template_data'
]


# Package metadata
__version__ = "1.0.0"
__author__ = "Lucas Escobar"
__description__ = "Automated research content generation for Bloomberg RMS"