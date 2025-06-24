import xlsxwriter
from .excel_styling import ExcelStyleConfig


class ExcelStyler:
    """Handles Excel formatting (similar to DocumentStyler for Word)"""
    
    def __init__(self, style_config: ExcelStyleConfig = None):
        self.config = style_config or ExcelStyleConfig()
        self.formats = {}
    
    def initialize_formats(self, workbook: xlsxwriter.Workbook) -> None:
        """Initialize all Excel formats"""
        
        # Blue header format (for labels)
        self.formats['blue_header'] = workbook.add_format({
            'bg_color': self.config.bloomberg_blue,
            'font_color': 'white',
            'bold': True,
            'font_size': self.config.header_font_size,
            'font_name': self.config.font_name,
            'border': 1,
            'border_color': self.config.border_color,
            'align': 'left',
            'valign': 'vcenter'
        })
        
        # Blue title format for company name
        self.formats['blue_title'] = workbook.add_format({
            'bg_color': self.config.bloomberg_blue,
            'font_color': 'white',
            'bold': True,
            'font_size': self.config.title_font_size,
            'font_name': self.config.font_name,
            'border': 1,
            'border_color': self.config.border_color,
            'align': 'left',
            'valign': 'vcenter'
        })
        
        # Light blue format for input cells
        self.formats['light_blue_input'] = workbook.add_format({
            'bg_color': self.config.light_blue,
            'font_color': 'black',
            'bold': False,
            'font_size': self.config.font_size,
            'font_name': self.config.font_name,
            'border': 1,
            'border_color': self.config.bloomberg_blue,
            'align': 'left',
            'valign': 'top',
            'text_wrap': True
        })
        
        # Regular cell format
        self.formats['regular_cell'] = workbook.add_format({
            'bg_color': self.config.light_blue,
            'font_color': 'black',
            'bold': False,
            'font_size': self.config.font_size,
            'font_name': self.config.font_name,
            'border': 1,
            'border_color': self.config.bloomberg_blue,
            'align': 'left',
            'valign': 'vcenter'
        })
        
        # Number cell format
        self.formats['number_cell'] = workbook.add_format({
            'bg_color': self.config.light_blue,
            'font_color': 'black',
            'bold': False,
            'font_size': self.config.font_size,
            'font_name': self.config.font_name,
            'border': 1,
            'border_color': self.config.bloomberg_blue,
            'align': 'right',
            'valign': 'vcenter',
            'num_format': '#,##0.00'
        })
        
        # Percentage format
        self.formats['percent_cell'] = workbook.add_format({
            'bg_color': self.config.light_blue,
            'font_color': 'black',
            'bold': False,
            'font_size': self.config.font_size,
            'font_name': self.config.font_name,
            'border': 1,
            'border_color': self.config.bloomberg_blue,
            'align': 'right',
            'valign': 'vcenter',
            'num_format': '0.0%'
        })
        
        # Table header format
        self.formats['table_header'] = workbook.add_format({
            'bg_color': self.config.bloomberg_blue,
            'font_color': 'white',
            'bold': True,
            'font_size': self.config.header_font_size,
            'font_name': self.config.font_name,
            'border': 1,
            'border_color': self.config.border_color,
            'align': 'left',
            'valign': 'vcenter'
        })
        
        # Row label format
        self.formats['row_label'] = workbook.add_format({
            'bg_color': self.config.light_blue,
            'font_color': 'black',
            'bold': True,
            'font_size': self.config.font_size,
            'font_name': self.config.font_name,
            'border': 1,
            'border_color': self.config.bloomberg_blue,
            'align': 'left',
            'valign': 'vcenter'
        })
        
        # Grey background for outside template area
        self.formats['grey_background'] = workbook.add_format({
            'bg_color': self.config.grey_background,
            'border': 0
        })
    
        # # Dark blue border format for template outline
        # self.formats['template_border'] = workbook.add_format({
        #     'border': 3,  # Thick border
        #     'border_color': '#2F5597',  # Dark blue color
        #     'bg_color': 'white'  # No background color interference
        # })


    def get_format(self, format_name: str):# -> xlsxwriter.Format:
        """Get a specific format"""
        return self.formats.get(format_name)
