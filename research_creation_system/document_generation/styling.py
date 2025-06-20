from dataclasses import dataclass, field
from enum import Enum
from docx.enum.text import WD_ALIGN_PARAGRAPH



class AlignmentType(Enum):
    """Text alignment options"""
    LEFT = WD_ALIGN_PARAGRAPH.LEFT
    CENTER = WD_ALIGN_PARAGRAPH.CENTER
    RIGHT = WD_ALIGN_PARAGRAPH.RIGHT
    

@dataclass
class FontStyle:
    """Font styling configuration"""
    name: str = 'Calibri'
    size: int = 10
    bold: bool = False
    italic: bool = False

@dataclass
class BorderStyle:
    """Border styling configuration"""
    size: str = "8"
    style: str = "single"
    color: str = "C0C0C0"

@dataclass
class TableStyle:
    """Table styling configuration"""
    font: FontStyle = field(default_factory=FontStyle)
    border: BorderStyle = field(default_factory=BorderStyle)
    alternate_shading: bool = True
    shade_color: str = "F2F2F2"
    row_height: float = 0.2
    bold_header: bool = False
    shade_header: bool = False

