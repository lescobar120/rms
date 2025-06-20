# =============================================================================
# TEMPLATE REGISTRY
# =============================================================================

from typing import Dict, Type, List
from ..base.template_base import BaseTemplate
from .thesis_template import ThesisTemplate
from .light_update_template import LightUpdateTemplate



TEMPLATE_REGISTRY: Dict[str, Type[BaseTemplate]] = {
    "thesis": ThesisTemplate,
    "light_update": LightUpdateTemplate,
    # Future templates can be added here
}

def get_template(name: str) -> Type[BaseTemplate]:
    if name not in TEMPLATE_REGISTRY:
        raise ValueError(f"Unknown template: {name}")
    return TEMPLATE_REGISTRY[name]

def list_templates() -> List[str]:
    return list(TEMPLATE_REGISTRY.keys())