"""
Document generation components for Bloomberg research reports
"""

# Import main classes that other modules will commonly use
from .bloomberg_report_generator import BloombergReportGenerator
from .styling import TableStyle, FontStyle, BorderStyle, AlignmentType
from .document_styler import DocumentStyler
from .table_builder import TableBuilder
from .utils import convert_docx_to_pdf_silently

# Define what gets imported with "from document_generation import *"
__all__ = [
    # Main generator
    'BloombergReportGenerator',
    
    # Styling
    'TableStyle',
    'FontStyle', 
    'BorderStyle',
    'AlignmentType',
    
    # Component classes
    'DocumentStyler',
    'TableBuilder',
    
    # Utilities
    'convert_docx_to_pdf_silently',
]