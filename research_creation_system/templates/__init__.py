"""
Research template implementations
"""

from .thesis_template import (
    ThesisTemplate,
    ThesisTemplateData,
    ThesisPublishingConfig,
    ThesisCDEMappingConfig
)
from .light_update_template import (
    LightUpdateTemplate,
    LightUpdateTemplateData,
    LightUpdatePublishingConfig,
    LightUpdateCDEMappingConfig  
)
from .earnings_preview_template import (
    EarningsPreviewTemplate,
    EarningsPreviewTemplateData,
    EarningsPreviewPublishingConfig,
    EarningsPreviewCDEMappingConfig
)
from .company_model_template import (
    CompanyModelTemplate,
    CompanyModelTemplateData, 
    CompanyModelPublishingConfig,
    CompanyModelCDEMappingConfig
)
from .registry import TEMPLATE_REGISTRY, get_template, list_templates

__all__ = [
    # Templates
    'ThesisTemplate',
    'LightUpdateTemplate',
    'EarningsPreviewTemplate',
    'CompanyModelTemplate',
    
    # Data classes
    'ThesisTemplateData',
    'LightUpdateTemplateData',
    'EarningsPreviewTemplateData',
    'CompanyModelTemplateData',
    
    # Configs
    'ThesisPublishingConfig',
    'ThesisCDEMappingConfig',
    'LightUpdatePublishingConfig',
    'LightUpdateCDEMappingConfig',
    'EarningsPreviewPublishingConfig',
    'EarningsPreviewCDEMappingConfig',
    'CompanyModelPublishingConfig',
    'CompanyModelCDEMappingConfig',
    
    # Registry
    'TEMPLATE_REGISTRY',
    'get_template', 
    'list_templates',
]


