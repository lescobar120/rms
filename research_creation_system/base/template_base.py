# =============================================================================
# BASE TEMPLATE SYSTEM
# =============================================================================

import pandas as pd
import datetime
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

from research_generator import TableStyle, FontStyle


@dataclass
class TaglistMapping:
    """Mapping for taglist name and enum value"""
    taglist_name: str
    enum_value: str


class BasePublishingConfig:
    """Base configuration for publishing"""
    def __init__(self, 
                 community_name: str,
                 analyst_name: str,
                 taglists: List[TaglistMapping],
                 as_of_date: Optional[str] = None):
        self.community_name = community_name
        self.analyst_name = analyst_name
        self.taglists = taglists
        self.as_of_date = as_of_date or datetime.datetime.today().strftime('%Y-%m-%d')


class BaseCDEMappingConfig:
    """Base configuration for CDE field mappings"""
    def __init__(self, field_mappings: Dict[str, str]):
        self.field_mappings = field_mappings


class BaseTemplate(ABC):
    """Base class for all research templates"""
    
    def __init__(self, style_config: Optional[TableStyle] = None):
        self.style_config = style_config or self._get_default_style()
    
    @property
    @abstractmethod
    def template_name(self) -> str:
        """Template identifier"""
        pass
    
    @property
    @abstractmethod 
    def output_file_types(self) -> List[str]:
        """File types this template generates (e.g., ['docx', 'pdf'])"""
        pass
    
    @property
    @abstractmethod
    def required_data_fields(self) -> List[str]:
        """Required fields in the template data"""
        pass
    
    @abstractmethod
    def generate_document(self, data: Any, output_filename: str) -> Dict[str, str]:
        """
        Generate document(s) for this template
        Returns: Dict mapping file_type to file_path
        """
        pass
    
    @abstractmethod
    def get_required_tags(self, data: Any, config: BasePublishingConfig) -> List[Any]:
        """Get Bloomberg tags required for this template"""
        pass
    
    @abstractmethod
    def prepare_cde_data(self, data: Any, ticker: str, config: BasePublishingConfig, 
                        cde_config: BaseCDEMappingConfig) -> pd.DataFrame:
        """Prepare CDE data for this template"""
        pass
    
    def _get_default_style(self) -> TableStyle:
        """Default document styling"""
        return TableStyle(
            font=FontStyle(name='Calibri', size=10),
            alternate_shading=True,
            shade_color="F2F2F2",
            shade_header=True
        )
    
    def validate_data(self, data: Any) -> None:
        """Validate template data has required fields"""
        for field in self.required_data_fields:
            if not hasattr(data, field):
                raise ValueError(f"Template {self.template_name} requires field: {field}")
    
    def _dataframe_to_table_data(self, df: pd.DataFrame) -> List[List[str]]:
        """Convert DataFrame to table data format"""
        data = [df.columns.tolist()]
        for _, row in df.iterrows():
            data.append([str(val) for val in row.values])
        return data