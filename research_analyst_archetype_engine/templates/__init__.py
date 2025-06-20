"""
Predefined archetype templates and configurations.

This module provides ready-to-use archetype definitions for common
analyst personality types, sector specialists, and demo scenarios.

Templates are designed to be:
- Realistic and believable
- Differentiated for compelling demos  
- Easily customizable through parameter overrides
- Based on real analyst behavior patterns
"""

from .standard_archetypes import (
    ArchetypeTemplates,
    # Individual template access
    create_oracle_archetype,
    create_follower_archetype,
    create_sprayer_archetype,
    create_specialist_archetype
)

try:
    from .sector_specialists import (
        SectorSpecialistTemplates,
        create_tech_specialist,
        create_healthcare_specialist,
        create_financial_specialist
    )
    _SECTOR_SPECIALISTS_AVAILABLE = True
except ImportError:
    # Sector specialists module is optional/future
    _SECTOR_SPECIALISTS_AVAILABLE = False

# Template registry for dynamic access
AVAILABLE_TEMPLATES = {
    "oracle": create_oracle_archetype,
    "follower": create_follower_archetype, 
    "sprayer": create_sprayer_archetype,
    "specialist": create_specialist_archetype,
}

if _SECTOR_SPECIALISTS_AVAILABLE:
    AVAILABLE_TEMPLATES.update({
        "tech_specialist": create_tech_specialist,
        "healthcare_specialist": create_healthcare_specialist,
        "financial_specialist": create_financial_specialist,
    })

def get_template_by_name(name: str):
    """Get archetype template by string name"""
    if name not in AVAILABLE_TEMPLATES:
        available = ", ".join(AVAILABLE_TEMPLATES.keys())
        raise ValueError(f"Unknown template '{name}'. Available: {available}")
    return AVAILABLE_TEMPLATES[name]()

def list_available_templates():
    """Return list of all available template names"""
    return list(AVAILABLE_TEMPLATES.keys())

__all__ = [
    "ArchetypeTemplates",
    "get_template_by_name", 
    "list_available_templates",
    "AVAILABLE_TEMPLATES",
    
    # Individual template functions
    "create_oracle_archetype",
    "create_follower_archetype",
    "create_sprayer_archetype", 
    "create_specialist_archetype",
] + (["SectorSpecialistTemplates"] if _SECTOR_SPECIALISTS_AVAILABLE else [])