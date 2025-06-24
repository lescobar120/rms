


# =============================================================================
# EXCEL MODEL GENERATOR
# =============================================================================

from typing import List, Dict, Any, Optional, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum
import datetime
from pathlib import Path

import xlsxwriter

from .excel_styling import ExcelStyleConfig
from .excel_document_styling import ExcelStyler
from .model_builder import ModelBuilder
from ..data_models import (
    CompanyInfo, InvestmentRecommendation, 
    ModelHeader, CompanyModelInfo,
    CompanyModelData
)


class ExcelModelGenerator:
    """Main class for generating Excel company models (similar to BloombergReportGenerator for Word)"""
    
    def __init__(self, style_config: ExcelStyleConfig = None):
        self.styler = ExcelStyler(style_config)
        self.model_builder = ModelBuilder(self.styler)
        self.workbook = None
        self.worksheet = None
    
    def create_workbook(self, output_path: str, worksheet_name: str = "Company Model") -> xlsxwriter.Workbook:
        """Create a new Excel workbook with styling"""
        self.workbook = xlsxwriter.Workbook(output_path)
        self.worksheet = self.workbook.add_worksheet(worksheet_name)
        
        # Initialize styles
        self.styler.initialize_formats(self.workbook)
        
        # Set up worksheet structure
        self._setup_worksheet()
        
        return self.workbook
    
    def _setup_worksheet(self):
        """Set up basic worksheet structure and column widths"""
        # Set column widths (Bloomberg style)
        column_widths = {
            'A': 3,   # Grey margin column
            'B': 18,  # Labels
            'C': 12,  # Values
            'D': 12,  # Values
            'E': 12,  # Values
            'F': 12,   # Spacer
            'G': 12,  # Labels
            'H': 12,  # Values
            'I': 12,  # Values
            'J': 12,  # Target Px
            'K': 12,  # Probability
            'L': 12,  # Exp Return
        }
        
        for col, width in column_widths.items():
            self.worksheet.set_column(f'{col}:{col}', width)
        
        # Set grey background for areas outside template
        self._set_grey_background()
    
    def _set_grey_background(self):
        """Set grey background for areas outside the template (B1:L41)"""
        grey_format = self.styler.get_format('grey_background')
        
        # Set grey background for row 1 (entire row)
        self.worksheet.set_row(0, None, grey_format)
        
        # Set grey background for column A (entire column)
        self.worksheet.set_column('A:A', 3, grey_format)
        
        # Set grey background for columns M onwards
        self.worksheet.set_column('M:XFD', None, grey_format)
        
        # Set grey background for rows below row 41
        for row in range(41, 1000):
            self.worksheet.set_row(row, None, grey_format)
    
    # def add_header_section(self, analyst_name: str, note_type: str = "Company Model", 
    #                       revision_date: str = None, idea_stage: str = "ACTIVE") -> None:
    #     """Add header section with analyst info"""
    #     if not revision_date:
    #         revision_date = datetime.datetime.now().strftime("%d-%b-%y")
        
    #     # Row 2: Analyst Name and Revision Date
    #     self.model_builder.write_header_row(
    #         self.worksheet, 2, 
    #         left_label="Analyst Name", left_value=analyst_name,
    #         right_label="Revision Date:", right_value=revision_date
    #     )
        
    #     # Row 3: Note Type and Idea Stage
    #     self.model_builder.write_header_row(
    #         self.worksheet, 3,
    #         left_label="Note Type:", left_value=note_type,
    #         right_label="Idea Stage (EQ EVAL):", right_value=idea_stage
    #     )

    def add_header_section(self, data: ModelHeader) -> None:
        """Add header section with analyst info"""
        
        # Row 2: Analyst Name and Revision Date
        self.model_builder.write_header_row(
            self.worksheet, 2, 
            left_label="Analyst Name", left_value=data.analyst_name,
            right_label="Revision Date:", right_value=data.revision_date
        )
        
        # Row 3: Note Type and Idea Stage
        self.model_builder.write_header_row(
            self.worksheet, 3,
            left_label="Note Type:", left_value=data.note_type,
            right_label="Idea Stage (EQ EVAL):", right_value=data.idea_stage.value
        )
    
    # def add_company_title(self, company_name: str, model_date: str = None) -> None:
    #     """Add company model title"""
    #     if not model_date:
    #         model_date = datetime.datetime.now().strftime("%m/%d/%Y")
        
    #     title = f"Company Model: {company_name} ({model_date})"
    #     self.model_builder.write_title_section(self.worksheet, 5, title)
    

    def add_company_title(self, data: CompanyModelInfo) -> None:
        """Add company model title"""
        
        title = f"Company Model: {data.company_name} ({data.model_date})"
        self.model_builder.write_title_section(self.worksheet, 5, title)


    ### Modify with CompanyModelData > Will need to update write_recommendation_table() in model_builder as well
    def add_recommendation_section(self, recommendation: InvestmentRecommendation,
                                 valuation_scenarios: Dict[str, str] = None,
                                 target_data: Dict[str, Any] = None) -> None:
        """Add recommendation and valuation table"""
        if not valuation_scenarios:
            valuation_scenarios = {
                "base": "Base Case",
                "bull": "Bull Case", 
                "bear": "Bear Case"
            }
        
        if not target_data:
            # Calculate expected returns
            base_return = (recommendation.base_target - recommendation.last_price) / recommendation.last_price
            bull_return = (getattr(recommendation, 'bull_target', recommendation.base_target * 1.2) - recommendation.last_price) / recommendation.last_price
            bear_return = (getattr(recommendation, 'bear_target', recommendation.base_target * 0.8) - recommendation.last_price) / recommendation.last_price
            
            target_data = {
                "base": {
                    "target": recommendation.base_target,
                    "probability": 0.65,
                    "return": base_return
                },
                "bull": {
                    "target": getattr(recommendation, 'bull_target', recommendation.base_target * 1.2),
                    "probability": 0.25,
                    "return": bull_return
                },
                "bear": {
                    "target": getattr(recommendation, 'bear_target', recommendation.base_target * 0.8),
                    "probability": 0.10,
                    "return": bear_return
                }
            }
        
        self.model_builder.write_recommendation_table(
            self.worksheet, 8, recommendation, valuation_scenarios, target_data
        )


    # def add_model_thesis_section(self, thesis_text: str = "", start_row: int = 13) -> None:
    #     """Add model assumptions section"""
    #     if not thesis_text:
    #         thesis_text = "Investment thesis will be detailed here."
        
    #     self.model_builder.write_thesis_section(self.worksheet, start_row, thesis_text)


    def add_model_thesis_section(self, data: CompanyModelData) -> None:
        """Add model assumptions section"""
        
        self.model_builder.write_thesis_section(self.worksheet, 13, data.investment_thesis)
    
    
    # def add_model_assumptions_section(self, assumptions_text: str = "", start_row: int = 22) -> None:
    #     """Add model assumptions section"""
    #     if not assumptions_text:
    #         assumptions_text = "Key model assumptions and methodology will be detailed here."
        
    #     self.model_builder.write_assumptions_section(self.worksheet, start_row, assumptions_text)


    def add_model_assumptions_section(self, data: CompanyModelData) -> None:
        """Add model assumptions section"""

        self.model_builder.write_assumptions_section(self.worksheet, 22, data.model_assumptions)  

    
    def add_financials_section(self, financials_data: Dict[str, Any], start_row: int = 30) -> None:
        """Add financial model section"""
        
        self.model_builder.write_financials_table(self.worksheet, start_row, financials_data)
    
    def save_workbook(self) -> None:
        """Save and close the workbook"""
        if not self.workbook:
            raise ValueError("No workbook to save")
        
        self.workbook.close()




