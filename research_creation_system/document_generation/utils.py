import docx2pdf
import win32com.client
import os
import datetime

from .bloomberg_report_generator import BloombergReportGenerator
from .styling import FontStyle, TableStyle, BorderStyle
from ..data_models import CompanyInfo, InvestmentRecommendation

def convert_docx_to_pdf_silently(input_path: str, output_path: str):
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False   # Don't show Word UI
    word.DisplayAlerts = 0  # Disable alerts

    doc = word.Documents.Open(os.path.abspath(input_path))
    doc.SaveAs(os.path.abspath(output_path), FileFormat=17)  # 17 = PDF
    doc.Close()
    word.Quit()


def create_thesis_doc():
    """Create a sample research report"""
    
    # Create custom styling
    custom_style = TableStyle(
        font=FontStyle(name='Calibri', size=10),
        alternate_shading=True,
        shade_color="F2F2F2",
        shade_header=True  # Enable header shading
    )
    
    # Initialize generator
    generator = BloombergReportGenerator(custom_style)
    generator.create_document()
    
    # Company information
    company_info = CompanyInfo(
        name="Apple Inc",
        country="US",
        analyst="Lucas Escobar",
        gics_sector="Information Technology",
        gics_industry_group="Technology, Hardware, & Equipment",
        gics_industry="Technology Hardware, Storage &",
        gics_sub_industry="Technology Hardware, Storage &"
    )
    
    # Investment recommendation
    recommendation = InvestmentRecommendation(
        buy_sell_rec="Buy",
        idea_stage="ACTIVE",
        esg_rating="Leading",
        theme="Tech Trifecta",
        last_price=203.92,
        base_target=300.00,
        bull_target=355.00,
        bear_target=200.00
    )
    
    # Build report
    generator.add_company_header("Apple Inc")
    generator.add_company_info_section(company_info)
    generator.add_recommendation_section(recommendation)
    
    thesis_text = """Apple's near-term growth could land in the low-single digits, driven by a steady services 
business that thrives on an installed base of 2.2 billion active devices. This is even as product sales remain depressed. 
Consumer weakness in China and increased competition are hampering near-term sales."""
    
    generator.add_thesis_section("Investment Thesis:", thesis_text)
    
    # Financial data
    financials_data = [
        ["", "2022 A", "2023 A", "2024 A*", "2025 A", "2026 A", "2027 A", "Est Source"],
        ["Sales", "394328", "383285", "391035", "94832", "100113", "453388", "Internal (EQ)"],
        ["EPS Adj", "6.11", "6.13", "6.75", "7.16", "7.64", "8.44", "Consensus"],
        ["EPS GAAP", "6.11", "6.13", "6.08", "6", "7", "8.44", "Internal (EQ)"],
        ["Gross Profit", "170782", "169148", "180683", "---", "---", "---", ""],
        ["Gross Margin", "43.31", "44.13", "46.21", "46.55", "46.55", "47.15", "Consensus"],
        ["EBITDA", "130541", "125820", "134661", "0", "0", "158062", "Internal (EQ)"],
        ["EBIT", "119437", "114301", "123216", "127791", "132856", "143773", "Consensus"],
        ["Net Income, Adj", "99803", "96995", "103998", "107406", "111615", "121776", "Consensus"],
        ["Net Income, GAAP", "99803", "96995", "93736", "9843", "11094", "121776", "Internal (EQ)"],
        ["CAPEX", "-10708", "-10595", "-9447", "-11053", "-12261", "-11400", "Consensus"],
        ["FCF", "111443", "99584", "108807", "104200", "121756", "128150", "Consensus"],
    ]
    
    generator.add_financials_section("Financials & Forecasts", financials_data)
    
    portfolio_exposure_data = [
        ["ID", "Port Wgt", "Bench Wgt", "Active Wgt", "TotRtn Port", "TotRtn Bench", "TotRtn Active", "Tot Attr"],
        ["EQUITY8_US", "5.45", "5.21", "-0.24", "1.53", "1.53", "0", "0"],
        ["EQUITY8_US_VALUE", "0.07", "0", "-0.07", "1.53", "0", "1.53", "0"],
        ["EQUITY8_CANADIAN", "4.06", "0", "-4.06", "1.53", "0", "1.53", "0"],
        ["EQUITY8_EM", "0", "0", "0", "0", "0", "0", "0"],
        ["EQUITY8_ESG", "5.15", "5.76", "0.61", "1.53", "1.53", "0", "0"],
        ["EQUITY8_GLOBAL", "3.88", "4.18", "0.31", "1.53", "1.53", "0", "0"],
        ["EQUITY8_LONG_SHORT", "4.94", "5.45", "0.51", "1.53", "1.53", "0", "0"],
        ["EQUITY8_MID_CAP_GROWTH", "0.1", "0", "-0.1", "1.53", "0", "1.53", "0"],
        ["EQUITY8_SMALL_CAP_GROWTH", "0", "0", "0", "0", "0", "0", "0"]
    ]

    generator.add_portfolio_exposure_section("Portfolio Exposure", portfolio_exposure_data)

    generator.save_document("thesis_doc.docx")
    convert_docx_to_pdf_silently("thesis_doc.docx", "thesis_doc.pdf")

