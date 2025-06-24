import xlsxwriter
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import datetime
from pathlib import Path
from enum import Enum

# Data structures for company model template
class IdeaStage(str, Enum):
    """Idea stage enumeration"""
    IDEA = "Idea"
    WIP = "WIP"
    PASS = "Pass"
    ACTIVE = "Active"
    EXIT = "Exit"

class BuySellRec(str, Enum):
    """Buy/Sell recommendation enumeration"""
    STRONG_BUY = "Strong Buy"
    BUY = "Buy"
    HOLD = "Hold"
    SELL = "Sell"
    STRONG_SELL = "Strong Sell"
    INACTIVE = "Inactive"

@dataclass
class ModelHeader:
    """Header information for company model"""
    analyst_name: str
    note_type: str
    revision_date: str
    idea_stage_eq_eval: IdeaStage
    
@dataclass
class CompanyModelInfo:
    """Company model title information"""
    company_name: str
    model_date: str

@dataclass
class RecommendationData:
    """Recommendation table data"""
    current_buy_sell_rec: BuySellRec
    current_ow_uw_rec: str
    current_esg_rating: str
    previous_buy_sell_rec: Optional[BuySellRec] = None
    previous_ow_uw_rec: str = ""
    previous_esg_rating: str = ""
    
@dataclass
class ValuationScenarios:
    """Valuation scenarios data"""
    base_case: str
    bull_case: str
    bear_case: str


@dataclass
class TargetPriceData:
    """Target price and probability data for all scenarios"""
    # Base Case
    base_target_px: float
    base_probability: float
    base_exp_return: float
    
    # Bull Case (optional)
    bull_target_px: Optional[float] = None
    bull_probability: Optional[float] = None
    bull_exp_return: Optional[float] = None
    
    # Bear Case (optional)
    bear_target_px: Optional[float] = None
    bear_probability: Optional[float] = None
    bear_exp_return: Optional[float] = None

    
@dataclass
class FinancialMetric:
    """Single financial metric across years"""
    metric_name: str
    values: Dict[str, Any]  # year -> value mapping
    
@dataclass
class FinancialsData:
    """Complete financials and forecast data"""
    years: List[str]  # e.g., ['2022', '2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030']
    metrics: List[FinancialMetric]

@dataclass
class CompanyModelData:
    """Complete data structure for company model"""
    header: ModelHeader
    company_info: CompanyModelInfo
    recommendation: RecommendationData
    valuation_scenarios: ValuationScenarios
    target_price: TargetPriceData
    financials: FinancialsData
    investment_thesis: str = ""
    model_assumptions: str = ""


class CompanyModelExcelGenerator:
    """Generates Excel company model files with Bloomberg-style formatting"""
    
    def __init__(self):
        self.workbook = None
        self.worksheet = None
        self.formats = {}
        
    def create_formats(self):
        """Create all the formatting styles needed"""
        # Blue header format (matching Bloomberg blue) - for labels
        self.formats['blue_header'] = self.workbook.add_format({
            'bg_color': '#4472C4',  # Bloomberg-style blue
            'font_color': 'white',
            'bold': True,
            'font_size': 11,
            'font_name': 'Calibri',
            'border': 1,
            'border_color': '#2F5597',
            'align': 'left',
            'valign': 'vcenter'
        })
        
        # Blue title format for company name
        self.formats['blue_title'] = self.workbook.add_format({
            'bg_color': '#4472C4',
            'font_color': 'white', 
            'bold': True,
            'font_size': 14,
            'font_name': 'Calibri',
            'border': 1,
            'border_color': '#2F5597',
            'align': 'left',
            'valign': 'vcenter'
        })

        # Light blue format for INPUT cells (not section headers)
        self.formats['light_blue_header'] = self.workbook.add_format({
            'bg_color': '#D9E2F3',  # Light blue
            'font_color': 'black',
            'bold': False,  # Input cells are not bold
            'font_size': 10,
            'font_name': 'Calibri',
            'border': 1,
            'border_color': '#4472C4',
            'align': 'left',
            'valign': 'top',  # Changed from 'vcenter' to 'top'
            'text_wrap': True  # Add this line for wrap text
        })
        
        # Regular cell format
        self.formats['regular_cell'] = self.workbook.add_format({
            'font_size': 10,
            'font_name': 'Calibri',
            'border': 1,
            'border_color': '#CCCCCC',
            'align': 'left',
            'valign': 'vcenter'
        })
        
        # Number cell format
        self.formats['number_cell'] = self.workbook.add_format({
            'font_size': 10,
            'font_name': 'Calibri',
            'border': 1,
            'border_color': '#CCCCCC',
            'align': 'right',
            'valign': 'vcenter',
            'num_format': '#,##0.00'
        })
        
        # Percentage format
        self.formats['percent_cell'] = self.workbook.add_format({
            'font_size': 10,
            'font_name': 'Calibri',
            'border': 1,
            'border_color': '#CCCCCC',
            'align': 'right',
            'valign': 'vcenter',
            'num_format': '0.0%'
        })
        
        # Header row for tables - left aligned
        self.formats['table_header'] = self.workbook.add_format({
            'bg_color': '#4472C4',
            'font_color': 'white',
            'bold': True,
            'font_size': 11,  # Changed from 10 to 11
            'font_name': 'Calibri',
            'border': 1,
            'border_color': '#2F5597',
            'align': 'left',  # Changed from 'center' to 'left'
            'valign': 'vcenter'
        })
        
        # Row label format
        self.formats['row_label'] = self.workbook.add_format({
            'bg_color': '#D9E2F3',
            'font_color': 'black',
            'bold': True,
            'font_size': 10,
            'font_name': 'Calibri',
            'border': 1,
            'border_color': '#4472C4',
            'align': 'left',
            'valign': 'vcenter'
        })
        
        # Grey background for outside template area - darker grey
        self.formats['grey_background'] = self.workbook.add_format({
            'bg_color': '#C0C0C0',  # Even darker grey color
            'border': 0
        })
        
        # Dark blue border format for template outline
        self.formats['template_border'] = self.workbook.add_format({
            'border': 3,  # Thick border
            'border_color': '#2F5597',  # Dark blue color
            'bg_color': 'white'  # No background color interference
        })
        
    def write_header_section(self, data: ModelHeader):
        """Write the header section with analyst info"""
        # Row 2: Analyst Name (merged) and Revision Date (merged)
        self.worksheet.merge_range('B2:C2', 'Analyst Name', self.formats['blue_header'])  # Merged B2:C2
        self.worksheet.merge_range('D2:E2', data.analyst_name, self.formats['light_blue_header'])  # Merged D2:E2
        self.worksheet.merge_range('G2:H2', 'Revision Date:', self.formats['blue_header'])  # Merged G2:H2
        self.worksheet.merge_range('I2:L2', data.revision_date, self.formats['light_blue_header'])  # Merged I2:L2
        
        # Row 3: Note Type (merged) and Idea Stage (EQ EVAL) (merged)
        self.worksheet.merge_range('B3:C3', 'Note Type:', self.formats['blue_header'])  # Merged B3:C3
        self.worksheet.merge_range('D3:E3', data.note_type, self.formats['light_blue_header'])  # Merged D3:E3
        self.worksheet.merge_range('G3:H3', 'Idea Stage (EQ EVAL):', self.formats['blue_header'])  # Merged G3:H3
        self.worksheet.merge_range('I3:L3', data.idea_stage_eq_eval, self.formats['light_blue_header'])  # Merged I3:L3
        
    def write_company_title(self, data: CompanyModelInfo):
        """Write the company model title"""
        title = f"Company Model: {data.company_name} ({data.model_date})"
        
        # Merge cells B5:L6 for the title (moved up from B6:L6)
        self.worksheet.merge_range('B5:L6', title, self.formats['blue_title'])
        
    #def write_recommendation_table(self, rec_data: RecommendationData, val_data: ValuationScenarios, target_data: TargetPriceData):
    def write_recommendation_table(self, data: CompanyModelData):
        """Write the recommendation and valuation table"""
        start_row = 7  # Row 8 in Excel (0-indexed)

        # Extract the needed data
        rec_data = data.recommendation
        val_data = data.valuation_scenarios
        target_data = data.target_price
        
        # Main table headers
        self.worksheet.write(start_row, 1, 'Recommendation', self.formats['table_header'])  # B8
        self.worksheet.write(start_row, 2, 'Current', self.formats['table_header'])  # C8
        self.worksheet.write(start_row, 3, 'Previous', self.formats['table_header'])  # D8
        
        # Valuation table headers (with merged cells for labels)
        self.worksheet.merge_range('H8:I8', 'Valuation Scenarios', self.formats['table_header'])  # H8:I8 merged and left-aligned
        self.worksheet.write(start_row, 9, 'Target Px', self.formats['table_header'])  # J8
        self.worksheet.write(start_row, 10, 'Probability', self.formats['table_header'])  # K8
        self.worksheet.write(start_row, 11, 'Exp Rtn', self.formats['table_header'])  # L8
            
        # Row data
        rows_data = [
            ('Buy/Sell Rec', rec_data.current_buy_sell_rec, rec_data.previous_buy_sell_rec, 'Base Case'),
            ('OW/UW Rec', rec_data.current_ow_uw_rec, rec_data.previous_ow_uw_rec, 'Bull Case'),
            ('ESG Rating', rec_data.current_esg_rating, rec_data.previous_esg_rating, 'Bear Case'),
        ]
        
        for i, row_data in enumerate(rows_data):
            row_num = start_row + 1 + i
            
            # Write metric name (column B)
            self.worksheet.write(row_num, 1, row_data[0], self.formats['blue_header'])
            
            # Write current value (column C) - as input cells
            if row_data[1]:  # Only if there's data
                self.worksheet.write(row_num, 2, row_data[1], self.formats['light_blue_header'])
            
            # Write previous value (column D) - as input cells
            if row_data[2]:  # Only if there's data
                self.worksheet.write(row_num, 3, row_data[2], self.formats['light_blue_header'])
            
            # Write valuation scenario (columns H:I merged) - as labels
            if row_data[3]:  # Only if there's data
                self.worksheet.merge_range(f'H{row_num+1}:I{row_num+1}', row_data[3], self.formats['blue_header'])  # H9:I9, H10:I10, H11:I11

            # Add target price data for each scenario
            if i == 0:  # Base Case row
                self.worksheet.write(row_num, 9, target_data.base_target_px, self.formats['light_blue_header'])   # J9 - Target Px
                self.worksheet.write(row_num, 10, target_data.base_probability, self.formats['light_blue_header']) # K9 - Probability  
                self.worksheet.write(row_num, 11, target_data.base_exp_return, self.formats['light_blue_header'])  # L9 - Exp Rtn
            elif i == 1:  # Bull Case row
                bull_target = target_data.bull_target_px if target_data.bull_target_px is not None else ''
                bull_prob = target_data.bull_probability if target_data.bull_probability is not None else ''
                bull_return = target_data.bull_exp_return if target_data.bull_exp_return is not None else ''
                
                self.worksheet.write(row_num, 9, bull_target, self.formats['light_blue_header'])   # J10 - Bull Target
                self.worksheet.write(row_num, 10, bull_prob, self.formats['light_blue_header'])    # K10 - Bull Probability
                self.worksheet.write(row_num, 11, bull_return, self.formats['light_blue_header'])  # L10 - Bull Exp Rtn
            elif i == 2:  # Bear Case row
                bear_target = target_data.bear_target_px if target_data.bear_target_px is not None else ''
                bear_prob = target_data.bear_probability if target_data.bear_probability is not None else ''
                bear_return = target_data.bear_exp_return if target_data.bear_exp_return is not None else ''
                
                self.worksheet.write(row_num, 9, bear_target, self.formats['light_blue_header'])   # J11 - Bear Target
                self.worksheet.write(row_num, 10, bear_prob, self.formats['light_blue_header'])    # K11 - Bear Probability
                self.worksheet.write(row_num, 11, bear_return, self.formats['light_blue_header'])  # L11 - Bear Exp Rtn

        # Add Investment Thesis header and merged cell area
        self.worksheet.merge_range('B13:L13', 'Investment Thesis', self.formats['blue_header'])  # B13
        self.worksheet.merge_range('B14:L20', data.investment_thesis, self.formats['light_blue_header'])  # B14:L20

    def write_model_assumptions_section(self, data: CompanyModelData):
        """Write the Model Assumptions section header"""
        # Model Assumptions header as merged cell
        self.worksheet.merge_range('B22:L22', 'Model Assumptions', self.formats['blue_header'])  # B22
        
        # Add merged cell area for model assumptions input (back to original rows)
        self.worksheet.merge_range('B23:L29', data.model_assumptions, self.formats['light_blue_header'])  # B23:L29
        
    def write_financials_table(self, financials: FinancialsData):
        """Write the Financials & Forecasts table"""
        start_row = 30  # Row 31 in Excel (correct position)
        
        # Section header as merged cell in columns B:C at row 31
        self.worksheet.merge_range(f'B{start_row+1}:C{start_row+1}', 'Financials & Forecasts', self.formats['blue_header'])  # B31:C31 merged
        
        # Table headers (years) - starting at column D at row 31
        for col, year in enumerate(financials.years):
            self.worksheet.write(start_row, col + 3, year, self.formats['table_header'])  # D31, E31, F31, etc.
            
        # Financial metrics rows (starting at row 32)
        for row_idx, metric in enumerate(financials.metrics):
            data_row = start_row + 1 + row_idx
            
            # Metric name merged across columns B:C at correct rows
            self.worksheet.merge_range(f'B{data_row+1}:C{data_row+1}', metric.metric_name, self.formats['blue_header'])  # B32:C32, B33:C33, etc.
            
            # Values for each year - as input cells starting at column D
            for col_idx, year in enumerate(financials.years):
                value = metric.values.get(year, '')
                if isinstance(value, (int, float)):
                    self.worksheet.write(data_row, col_idx + 3, value, self.formats['light_blue_header'])  # D32, E32, etc.
                else:
                    self.worksheet.write(data_row, col_idx + 3, value, self.formats['light_blue_header'])
                    
    def set_column_widths(self):
        """Set appropriate column widths"""
        # Set column widths to match the layout
        self.worksheet.set_column('A:A', 3)      # Column A - very narrow
        self.worksheet.set_column('B:B', 16.5)   # Row labels - slightly wider
        self.worksheet.set_column('C:L', 12)     # Data columns
        
    def add_template_border(self):
        """Add dark blue border around the template area B2:L41 - perimeter only"""
        # xlsxwriter doesn't have set_border, so let's create invisible cells with just outer borders
        # We'll write invisible content with only the outer borders
        
        # Create formats for each edge
        top_left_format = self.workbook.add_format({
            'top': 2, 'top_color': '#2F5597',
            'left': 2, 'left_color': '#2F5597',
            'font_color': 'white', 'bg_color': 'white'  # Make invisible
        })
        
        top_format = self.workbook.add_format({
            'top': 2, 'top_color': '#2F5597',
            'font_color': 'white', 'bg_color': 'white'
        })
        
        top_right_format = self.workbook.add_format({
            'top': 2, 'top_color': '#2F5597',
            'right': 2, 'right_color': '#2F5597',
            'font_color': 'white', 'bg_color': 'white'
        })
        
        left_format = self.workbook.add_format({
            'left': 2, 'left_color': '#2F5597',
            'font_color': 'white', 'bg_color': 'white'
        })
        
        right_format = self.workbook.add_format({
            'right': 2, 'right_color': '#2F5597',
            'font_color': 'white', 'bg_color': 'white'
        })
        
        bottom_left_format = self.workbook.add_format({
            'bottom': 2, 'bottom_color': '#2F5597',
            'left': 2, 'left_color': '#2F5597',
            'font_color': 'white', 'bg_color': 'white'
        })
        
        bottom_format = self.workbook.add_format({
            'bottom': 2, 'bottom_color': '#2F5597',
            'font_color': 'white', 'bg_color': 'white'
        })
        
        bottom_right_format = self.workbook.add_format({
            'bottom': 2, 'bottom_color': '#2F5597',
            'right': 2, 'right_color': '#2F5597',
            'font_color': 'white', 'bg_color': 'white'
        })
        
        # Apply borders to perimeter only (this is complex with xlsxwriter)
        # For now just skip the border for now
        # The template looks good without it, and adding perimeter-only borders
        # in xlsxwriter is quite complex and might interfere with existing formatting
        pass
        
    def set_grey_background(self):
        """Set grey background for areas outside the template (B1:L41)"""
        # Set grey background for row 1 (entire row)
        self.worksheet.set_row(0, None, self.formats['grey_background'])
        
        # Set grey background for column A (entire column)
        self.worksheet.set_column('A:A', 3, self.formats['grey_background'])
        
        # Set grey background for columns M onwards (from M1 to end)
        self.worksheet.set_column('M:XFD', None, self.formats['grey_background'])
        
        # Set grey background for rows below row 41 (row 42 onwards)
        for row in range(41, 1000):  # Set grey for rows 42-1000
            self.worksheet.set_row(row, None, self.formats['grey_background'])
        
    def generate_model(self, data: CompanyModelData, output_path: str):
        """Generate the complete company model Excel file"""
        self.workbook = xlsxwriter.Workbook(output_path)
        self.worksheet = self.workbook.add_worksheet('Company Model')
        
        # Create all formats
        self.create_formats()
        
        # Set column widths
        self.set_column_widths()
        
        # Set grey background for outside template area
        self.set_grey_background()
        
        # Note: Template border functionality removed for now due to xlsxwriter complexity
        # The template area is clearly defined by the grey background
        
        # Write all sections
        self.write_header_section(data.header)
        self.write_company_title(data.company_info)
        #self.write_recommendation_table(data.recommendation, data.valuation_scenarios, data.target_price)
        self.write_recommendation_table(data)
        # self.write_model_assumptions_section()
        self.write_model_assumptions_section(data)
        self.write_financials_table(data.financials)
        
        # Close and save
        self.workbook.close()
        print(f"Company model generated: {output_path}")


def create_sample_company_model_data() -> CompanyModelData:
    """Create sample data for testing the company model generator"""
    
    # Header information
    header = ModelHeader(
        analyst_name="Lucas Escobar",
        note_type="Company Model",
        revision_date="01-Jun-25",
        idea_stage_eq_eval=IdeaStage.ACTIVE,
    )
    
    # Company information
    company_info = CompanyModelInfo(
        company_name="Salesforce Inc",
        model_date="06/01/2025"
    )
    
    # Recommendation data
    recommendation = RecommendationData(
        current_buy_sell_rec=BuySellRec.BUY,
        current_ow_uw_rec="OW",
        current_esg_rating="Leading",
        previous_buy_sell_rec=BuySellRec.BUY,
        previous_ow_uw_rec="OW",
        previous_esg_rating="Leading"
    )

    # Valuation scenarios
    valuation_scenarios = ValuationScenarios(
        base_case="Base Case",
        bull_case="Bull Case", 
        bear_case="Bear Case"
    )
    
    # Target price data
    target_price = TargetPriceData(
        # Base Case
        base_target_px=285.00,
        base_probability=0.65,
        base_exp_return=0.15,
        
        # Bull Case (optional)
        bull_target_px=350.00,
        bull_probability=0.25,
        bull_exp_return=0.35,
        
        # Bear Case (optional)
        bear_target_px=220.00,
        bear_probability=0.10,
        bear_exp_return=-0.10
    )
    
    # Financial data
    years = ['2022', '2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030']
    
    financial_metrics = [
        FinancialMetric('EPS Adj', {
            '2022': 4.78, '2023': 5.24, '2024': 8.22, '2025': 10.20,
            '2026': 11.22, '2027': 12.34, '2028': 13.58, '2029': '', '2030': ''
        }),
        FinancialMetric('EPS GAAP', {
            '2022': 1.48, '2023': 0.21, '2024': 4.20, '2025': 6.36,
            '2026': 7.07, '2027': 7.78, '2028': 8.47, '2029': '', '2030': ''
        }),
        FinancialMetric('Sales', {
            '2022': 26490, '2023': 31352, '2024': 34857, '2025': 37985,
            '2026': 41658, '2027': 45825, '2028': 50438, '2029': '', '2030': ''
        }),
        FinancialMetric('Gross Margin', {
            '2022': '78%', '2023': '73%', '2024': '80%', '2025': '77%',
            '2026': '0.85', '2027': '0.53', '2028': '1.03', '2029': '', '2030': ''
        }),
        FinancialMetric('EBITDA', {
            '2022': 8249, '2023': 10854, '2024': 14591, '2025': 15975,
            '2026': 17572, '2027': 19329, '2028': 21262, '2029': '', '2030': ''
        }),
        FinancialMetric('EBIT', {
            '2022': 1851, '2023': 1058, '2024': 10632, '2025': 12458,
            '2026': 14107, '2027': 15122, '2028': 16634, '2029': '', '2030': ''
        }),
        FinancialMetric('Pre-Tax Profit', {
            '2022': 5235, '2023': 6698, '2024': 10571, '2025': 11080,
            '2026': 12188, '2027': 13406, '2028': 14747, '2029': '', '2030': ''
        }),
        FinancialMetric('Net Income Adj', {
            '2022': 4655, '2023': 5224, '2024': 8087, '2025': 9930,
            '2026': 10923, '2027': 12015, '2028': 13216, '2029': '', '2030': ''
        }),
        FinancialMetric('Net Income GAAP', {
            '2022': 1444, '2023': 208, '2024': 4136, '2025': 6197,
            '2026': 6816, '2027': 7498, '2028': 8248, '2029': '', '2030': ''
        })
    ]
    
    financials = FinancialsData(
        years=years,
        metrics=financial_metrics
    )

    return CompanyModelData(
        header=header,
        company_info=company_info,
        recommendation=recommendation,
        valuation_scenarios=valuation_scenarios,
        target_price=target_price,
        financials=financials,
        investment_thesis="Salesforce remains well-positioned in the CRM market with strong cloud growth prospects. The company's recurring revenue model and expanding customer base provide sustainable competitive advantages.",
        model_assumptions="Base case assumes 15% revenue growth through 2027, driven by continued cloud adoption and market share gains. Operating margin expansion to 25% by 2026 through operational leverage and cost discipline."
    )

