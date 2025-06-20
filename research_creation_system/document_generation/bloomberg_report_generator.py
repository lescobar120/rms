from typing import List, Dict, Any, Optional, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum
import datetime
from pathlib import Path

from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_ROW_HEIGHT_RULE
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.table import Table, _Cell
from docx.text.paragraph import Paragraph

from .styling import TableStyle
from .document_styler import DocumentStyler
from .table_builder import TableBuilder
from ..data_models import CompanyInfo, InvestmentRecommendation



class BloombergReportGenerator:
    """Main class for generating Bloomberg RMS NOTEs"""
    
    def __init__(self, style_config: TableStyle = None):
        self.styler = DocumentStyler(style_config)
        self.table_builder = TableBuilder(self.styler)
        self.doc = None
    
    def create_document(self, margins: float = 0.5) -> Document:
        """Create a new document with custom margins"""
        self.doc = Document()
        
        # Set margins
        section = self.doc.sections[0]
        section.top_margin = Inches(margins)
        section.bottom_margin = Inches(margins)
        section.left_margin = Inches(margins)
        section.right_margin = Inches(margins)

        # Add a header
        header = section.header
        header_para = header.paragraphs[0] if header.paragraphs else header.add_paragraph()
        run = header_para.add_run("Bloomberg")
        run.font.name = 'Calibri (Headings)'  # Use a clean, modern font
        run.font.size = Pt(24)
        run.bold = True
        # Align to the right
        header_para.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        
        return self.doc
    
    def add_company_header(self, company_name: str) -> None:
        """Add company header to document"""
        if not self.doc:
            raise ValueError("Document not created. Call create_document() first.")
        
        self.doc.add_heading(f"{company_name}:", level=1)
    
    # def add_company_info_section(self, company_info: CompanyInfo) -> Table:
    #     """Add company information section"""
    #     self.doc.add_heading("Company Information", level=2)
        
    #     data = [
    #         (f"Company Name", company_info.name),
    #         (f"Country of Domicile", company_info.country),
    #         (f"Analyst", company_info.analyst),
    #         (f"Update", company_info.update_date),
    #         (f"GICS Sector", company_info.gics_sector),
    #         (f"GICS Group", company_info.gics_industry_group),
    #         (f"Industry", company_info.gics_industry),
    #         (f"Sub Industry", company_info.gics_sub_industry)
    #     ]
        
    #     # Split into two columns
    #     _split_idx = int(round(len(data)/2,1))
    #     paired_data = [(data[i], data[i+_split_idx]) for i in range(_split_idx)]
    #     formatted_data = []
    #     for left, right in paired_data:
    #         formatted_data.append((f"{left[0]}: {left[1]}", f"{right[0]}: {right[1]}"))
        
    #     return self.table_builder.build_key_value_table(self.doc, formatted_data)
    
    def add_company_info_section(self, company_info: CompanyInfo) -> Table:
        """Add company information section"""
        self.doc.add_heading("Company Information", level=2)
        
        # Create structured data as tuples of (key, value) pairs
        data = [
            ("Company Name", company_info.name),
            ("Country of Domicile", company_info.country),
            ("Analyst", company_info.analyst),
            ("Update", company_info.update_date),
            ("GICS Sector", company_info.gics_sector),
            ("GICS Group", company_info.gics_industry_group),
            ("Industry", company_info.gics_industry),
            ("Sub Industry", company_info.gics_sub_industry)
        ]
        
        # Split into two columns of (key, value) pairs
        split_idx = int(round(len(data)/2, 1))
        paired_data = []
        
        for i in range(split_idx):
            left_pair = data[i]  # (key, value)
            right_pair = data[i + split_idx] if i + split_idx < len(data) else ("", "")
            paired_data.append((left_pair, right_pair))
        
        return self.table_builder.build_key_value_table(self.doc, paired_data)
    
    # def add_recommendation_section(self, recommendation: InvestmentRecommendation) -> Table:
    #     """Add investment recommendation section"""
    #     self.doc.add_heading("Internal Recommendation", level=2)
        
    #     data = [
    #         (f"Buy/Sell Rec: {recommendation.buy_sell_rec}", 
    #          f"Last Price: {recommendation.last_price}"),
    #         (f"Idea Stage: {recommendation.idea_stage}", 
    #          f"Base Target Price: {recommendation.base_target}"),
    #         (f"ESG Rating: {recommendation.esg_rating}", 
    #          f"Bull Target Price: {recommendation.bull_target}"),
    #         (f"Investment Theme: {recommendation.theme}", 
    #          f"Bear Target Price: {recommendation.bear_target}")
    #     ]
        
    #     return self.table_builder.build_key_value_table(self.doc, data)

    def add_recommendation_section(self, recommendation: InvestmentRecommendation) -> Table:
        """Add investment recommendation section"""
        self.doc.add_heading("Internal Recommendation", level=2)
        
        # Create structured data as tuples of (key, value) pairs
        data = [
            ("Buy/Sell Rec", recommendation.buy_sell_rec),
            ("Last Price", str(recommendation.last_price)),
            ("Idea Stage", recommendation.idea_stage), 
            ("Base Target Price", str(recommendation.base_target)),
            ("ESG Rating", recommendation.esg_rating),
            ("Bull Target Price", str(recommendation.bull_target)),
            ("Investment Theme", recommendation.theme),
            ("Bear Target Price", str(recommendation.bear_target))
        ]
        
        # Split into two columns of (key, value) pairs
        split_idx = int(round(len(data)/2, 1))
        paired_data = []
        
        for i in range(split_idx):
            left_pair = data[i]  # (key, value)
            right_pair = data[i + split_idx] if i + split_idx < len(data) else ("", "")
            paired_data.append((left_pair, right_pair))
        
        # Use the new mixed format method
        return self.table_builder.build_key_value_table(self.doc, paired_data)
    
    def add_thesis_section(self, thesis_title: str, thesis_text: str) -> Table:
        """Add investment thesis section"""
        self.doc.add_paragraph("")  # Add spacing
        
        data = [thesis_title, thesis_text]
        return self.table_builder.build_single_column_table(self.doc, data)
    
    def add_financials_section(self, title: str, financial_data: List[List[str]]) -> Table:
        """Add financials section"""
        self.doc.add_heading(title, level=2)
        return self.table_builder.build_data_table(self.doc, financial_data, has_header=True)
    
    def add_portfolio_exposure_section(self, title: str, exposure_data: List[List[str]]) -> Table:
        """Add financials section"""
        self.doc.add_heading(title, level=2)
        return self.table_builder.build_data_table(self.doc, exposure_data, has_header=True)
    
    def save_document(self, filename: str) -> None:
        """Save the document"""
        if not self.doc:
            raise ValueError("No document to save")
        
        self.doc.save(filename)




