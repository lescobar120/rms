from dataclasses import dataclass

@dataclass
class ExcelStyleConfig:
    """Configuration for Excel styling (similar to TableStyle for Word)"""
    font_name: str = 'Calibri'
    font_size: int = 10
    header_font_size: int = 11
    title_font_size: int = 14
    bloomberg_blue: str = '#4472C4'
    light_blue: str = '#D9E2F3'
    border_color: str = '#2F5597'
    grey_background: str = '#C0C0C0'