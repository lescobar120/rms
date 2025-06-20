# DocumentStyler class - handles styling operations
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_ROW_HEIGHT_RULE
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.table import Table, _Cell
from docx.text.paragraph import Paragraph
from .styling import TableStyle, AlignmentType, FontStyle



class DocumentStyler:
    """Handles all document styling operations"""
    
    def __init__(self, style_config: TableStyle = None):
        self.style_config = style_config or TableStyle()
    
    def set_cell_borders(self, cell: _Cell) -> None:
        """Apply borders to a table cell"""
        border_style = {
            "sz": self.style_config.border.size,
            "val": self.style_config.border.style,
            "color": self.style_config.border.color
        }
        
        tc = cell._tc
        tcPr = tc.get_or_add_tcPr()
        
        # Remove existing borders
        for border_tag in tcPr.findall(qn('w:tcBorders')):
            tcPr.remove(border_tag)
        
        # Add new borders
        tcBorders = OxmlElement('w:tcBorders')
        for edge in ("start", "top", "end", "bottom"):
            element = OxmlElement(f"w:{edge}")
            for key, val in border_style.items():
                element.set(qn(f"w:{key}"), val)
            tcBorders.append(element)
        tcPr.append(tcBorders)
    
    def set_cell_shading(self, cell: _Cell, fill_color: str) -> None:
        """Apply shading to a table cell"""
        tc = cell._tc
        tcPr = tc.get_or_add_tcPr()
        shd = OxmlElement('w:shd')
        shd.set(qn('w:val'), 'clear')
        shd.set(qn('w:color'), 'auto')
        shd.set(qn('w:fill'), fill_color)
        tcPr.append(shd)
    
    def style_cell_text(self, cell: _Cell, text: str, 
                       alignment: AlignmentType = AlignmentType.LEFT,
                       font_override: FontStyle = None) -> None:
        """Apply text styling to a cell"""
        font_style = font_override or self.style_config.font
        
        p = cell.paragraphs[0]
        p.alignment = alignment.value
        
        # Clear existing runs
        p.clear()
        
        run = p.add_run(text)
        run.font.name = font_style.name
        run.font.size = Pt(font_style.size)
        run.bold = font_style.bold
        run.italic = font_style.italic

    def style_table(self, table: Table, table_type: str = "default") -> None:
        """Apply comprehensive styling to a table"""
        for row_idx, row in enumerate(table.rows):
            # Set row height (except for content rows in thesis tables)
            if table_type == "thesis" and row_idx == 1:  # Content row in thesis table
                # Don't set fixed height for thesis content - let it expand
                pass
            else:
                row.height = Inches(self.style_config.row_height)
                row.height_rule = WD_ROW_HEIGHT_RULE.EXACTLY
            
            # Determine shading based on table type and row
            should_shade = False
            
            if table_type == "key_value":
                # For key-value tables, shade every other row starting with first
                should_shade = (self.style_config.alternate_shading and row_idx % 2 == 0)
            elif table_type == "thesis":
                # For thesis tables, shade the header row
                should_shade = (row_idx == 0 and self.style_config.shade_header)
            elif table_type == "data":
                # For data tables, shade alternate rows but not header
                should_shade = (self.style_config.alternate_shading and 
                              row_idx % 2 == 0 and row_idx > 0)
            
            for cell in row.cells:
                self.set_cell_borders(cell)
                if should_shade:
                    self.set_cell_shading(cell, self.style_config.shade_color)
