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
from .registry import TEMPLATE_REGISTRY, get_template, list_templates

__all__ = [
    # Templates
    'ThesisTemplate',
    'LightUpdateTemplate',
    
    # Data classes
    'ThesisTemplateData',
    'LightUpdateTemplateData',
    
    # Configs
    'ThesisPublishingConfig',
    'ThesisCDEMappingConfig',
    'LightUpdatePublishingConfig',
    'LightUpdateCDEMappingConfig',
    
    # Registry
    'TEMPLATE_REGISTRY',
    'get_template', 
    'list_templates',
]