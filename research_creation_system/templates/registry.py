# =============================================================================
# TEMPLATE REGISTRY
# =============================================================================

from typing import Dict, Type, List
from ..base.template_base import BaseTemplate
from .thesis_template import ThesisTemplate
from .light_update_template import LightUpdateTemplate
from .earnings_preview_template import EarningsPreviewTemplate
from .company_model_template import CompanyModelTemplate


TEMPLATE_REGISTRY: Dict[str, Type[BaseTemplate]] = {
    "thesis": ThesisTemplate,
    "light_update": LightUpdateTemplate,
    "earnings_preview": EarningsPreviewTemplate,
    "company_model": CompanyModelTemplate
    # Future templates can be added here
}

def get_template(name: str) -> Type[BaseTemplate]:
    if name not in TEMPLATE_REGISTRY:
        raise ValueError(f"Unknown template: {name}")
    return TEMPLATE_REGISTRY[name]

def list_templates() -> List[str]:
    return list(TEMPLATE_REGISTRY.keys())