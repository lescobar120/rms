"""
Document generation components for Bloomberg research reports
"""

# Import main classes that other modules will commonly use

# Word document generation
from .bloomberg_report_generator import BloombergReportGenerator
from .styling import TableStyle, FontStyle, BorderStyle, AlignmentType
from .document_styler import DocumentStyler
from .table_builder import TableBuilder
from .text_formatter import TextFormatter

# Excel model generation
from .excel_model_generator import ExcelModelGenerator
from .excel_styling import ExcelStyleConfig
from .excel_document_styling import ExcelStyler
from .model_builder import ModelBuilder

# Utilities
from .utils import convert_docx_to_pdf_silently

# Define what gets imported with "from document_generation import *"
__all__ = [
    # Word document generation
    'BloombergReportGenerator',
    'TableStyle',
    'FontStyle', 
    'BorderStyle',
    'AlignmentType',
    'DocumentStyler',
    'TableBuilder',
    'TextFormatter',
    
    # Excel model generation
    'ExcelModelGenerator',
    'ExcelStyleConfig',
    'ExcelStyler',
    'ModelBuilder',
    
    # Utilities
    'convert_docx_to_pdf_silently',
]