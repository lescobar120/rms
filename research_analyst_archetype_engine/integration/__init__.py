"""
Integration bridges with external systems.

This module provides clean interfaces for connecting the archetype
system with existing Bloomberg RMS API functionality, template
generation systems, and other external components.

The integration layer prevents tight coupling while enabling
rich interactions between systems.
"""

try:
    from .rms_bridge import (
        RMSIntegration,
        NotePublishingBridge,
        CDEDataBridge,
        TaggingBridge
    )
    _RMS_INTEGRATION_AVAILABLE = True
except ImportError:
    _RMS_INTEGRATION_AVAILABLE = False

try:
    from .template_bridge import (
        TemplateIntegration,
        TemplateSelector,
        DataInjector,
        ContentGenerator
    )
    _TEMPLATE_INTEGRATION_AVAILABLE = True
except ImportError:
    _TEMPLATE_INTEGRATION_AVAILABLE = False

# Configuration and setup helpers
from .config import (
    IntegrationConfig,
    setup_integrations,
    validate_integration_config
)

# Base integration interfaces
from .interfaces import (
    IntegrationBridge,
    PublishingBridge,
    DataBridge
)

__all__ = [
    # Configuration
    "IntegrationConfig",
    "setup_integrations",
    "validate_integration_config",
    
    # Base interfaces
    "IntegrationBridge",
    "PublishingBridge", 
    "DataBridge",
]

# Add available integrations to exports
if _RMS_INTEGRATION_AVAILABLE:
    __all__.extend([
        "RMSIntegration",
        "NotePublishingBridge",
        "CDEDataBridge", 
        "TaggingBridge"
    ])

if _TEMPLATE_INTEGRATION_AVAILABLE:
    __all__.extend([
        "TemplateIntegration",
        "TemplateSelector",
        "DataInjector",
        "ContentGenerator"
    ])