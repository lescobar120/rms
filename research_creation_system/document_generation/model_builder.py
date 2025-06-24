from typing import List, Dict, Any, Optional, Tuple, Union
from ..data_models import InvestmentRecommendation
from .excel_document_styling import ExcelStyler


class ModelBuilder:
    """Builds Excel model components (similar to TableBuilder for Word)"""
    
    def __init__(self, styler: ExcelStyler):
        self.styler = styler
    
    def write_header_row(self, worksheet, row: int, 
                        left_label: str, left_value: str,
                        right_label: str, right_value: str) -> None:
        """Write a header row with left and right label/value pairs"""
        # Left side - merged cells
        worksheet.merge_range(f'B{row}:C{row}', left_label, self.styler.get_format('blue_header'))
        worksheet.merge_range(f'D{row}:E{row}', left_value, self.styler.get_format('light_blue_input'))
        
        # Right side - merged cells
        worksheet.merge_range(f'G{row}:H{row}', right_label, self.styler.get_format('blue_header'))
        worksheet.merge_range(f'I{row}:L{row}', right_value, self.styler.get_format('light_blue_input'))
    
    def write_title_section(self, worksheet, row: int, title: str) -> None:
        """Write the company model title"""
        worksheet.merge_range(f'B{row}:L{row+1}', title, self.styler.get_format('blue_title'))
    

    ##  Update this section
    def write_recommendation_table(self, worksheet, start_row: int, 
                                  recommendation: InvestmentRecommendation,
                                  valuation_scenarios: Dict[str, str],
                                  target_data: Dict[str, Any]) -> None:
        """Write the recommendation and valuation table"""
        
        # Main table headers
        worksheet.write(start_row-1, 1, 'Recommendation', self.styler.get_format('table_header'))
        worksheet.write(start_row-1, 2, 'Current', self.styler.get_format('table_header'))
        worksheet.write(start_row-1, 3, 'Previous', self.styler.get_format('table_header'))
        
        # Valuation table headers
        worksheet.merge_range(f'H{start_row}:I{start_row}', 'Valuation Scenarios', self.styler.get_format('table_header'))
        worksheet.write(start_row-1, 9, 'Target Px', self.styler.get_format('table_header'))
        worksheet.write(start_row-1, 10, 'Probability', self.styler.get_format('table_header'))
        worksheet.write(start_row-1, 11, 'Exp Rtn', self.styler.get_format('table_header'))
        
        # Recommendation data rows
        rec_data = [
            ('Buy/Sell/Hold Rec', recommendation.buy_sell_rec, ''),
            ('OW/UW Rec', getattr(recommendation, 'ow_uw_rec', 'OW'), ''),
            ('ESG Rating', getattr(recommendation, 'esg_rating', 'Leading'), '')
        ]
        
        # Valuation data
        val_data = [
            (valuation_scenarios.get("base", "Base Case"), target_data["base"]),
            (valuation_scenarios.get("bull", "Bull Case"), target_data["bull"]),
            (valuation_scenarios.get("bear", "Bear Case"), target_data["bear"])
        ]
        
        # Write recommendation rows and valuation rows
        for i, (label, current, previous) in enumerate(rec_data):
            row = start_row + i
            worksheet.write(row, 1, label, self.styler.get_format('table_header'))
            worksheet.write(row, 2, current, self.styler.get_format('light_blue_input'))
            worksheet.write(row, 3, previous, self.styler.get_format('light_blue_input'))
            
            # Write valuation data for corresponding rows
            if i < len(val_data):
                scenario_name, scenario_data = val_data[i]
                worksheet.merge_range(f'H{row+1}:I{row+1}', scenario_name, self.styler.get_format('table_header'))
                worksheet.write(row, 9, scenario_data["target"], self.styler.get_format('number_cell'))
                worksheet.write(row, 10, scenario_data["probability"], self.styler.get_format('percent_cell'))
                worksheet.write(row, 11, scenario_data["return"], self.styler.get_format('percent_cell'))
    

    def write_thesis_section(self, worksheet, start_row: int, thesis_text: str) -> None:
        """Write model assumptions section"""
        # Section header
        worksheet.merge_range(f'B{start_row}:L{start_row}', 'Investment Thesis', 
                            self.styler.get_format('table_header'))
        
        # Assumptions text
        worksheet.merge_range(f'B{start_row+1}:L{start_row+7}', thesis_text, 
                            self.styler.get_format('light_blue_input'))


    def write_assumptions_section(self, worksheet, start_row: int, assumptions_text: str) -> None:
        """Write model assumptions section"""
        # Section header
        worksheet.merge_range(f'B{start_row}:L{start_row}', 'Key Model Assumptions', 
                            self.styler.get_format('table_header'))
        
        # Assumptions text
        worksheet.merge_range(f'B{start_row+1}:L{start_row+7}', assumptions_text, 
                            self.styler.get_format('light_blue_input'))
        
    

    def write_financials_table(self, worksheet, start_row: int, financials_data: Dict[str, Any]) -> None:
        """Write financial model table"""
        # This is a simplified version - can be expanded based on your FinancialsData structure
        
        # Section header
        worksheet.merge_range(f'B{start_row+1}:C{start_row+1}', 'Financials & Forecasts', 
                            self.styler.get_format('table_header'))
        
        # Table headers (years)
        years = financials_data.get('years', ['2023', '2024', '2025', '2026', '2027'])
        # worksheet.write(start_row, 1, 'Metric', self.styler.get_format('table_header'))
        for i, year in enumerate(years[:9]):  # Limit to 6 years to fit
            worksheet.write(start_row, i+3, year, self.styler.get_format('table_header'))
        
        # Financial metrics rows
        metrics = financials_data.get('metrics', [])
        for row_idx, metric in enumerate(metrics[:10]):  # Limit to 10 metrics
            actual_row = start_row + 1 + row_idx

            worksheet.merge_range(f'B{actual_row+1}:C{actual_row+1}', metric.metric_name, self.styler.get_format('table_header'))
            
            for col_idx, year in enumerate(years[:9]):
                value = metric.values.get(year, '')
                cell_format = self.styler.get_format('number_cell') if isinstance(value, (int, float)) else self.styler.get_format('regular_cell')
                worksheet.write(actual_row, col_idx+3, value, cell_format)

