# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

import pandas as pd

from .document_generation.styling import TableStyle
from .document_generation.document_styler import DocumentStyler
from .document_generation.table_builder import TableBuilder
from .data_models import CompanyInfo, InvestmentRecommendation
from .document_generation import BloombergReportGenerator, TableStyle
from .document_generation.utils import convert_docx_to_pdf_silently
from .data_models import CompanyInfo, InvestmentRecommendation
from .templates.thesis_template import ThesisTemplateData
from .templates.light_update_template import LightUpdateTemplateData


def create_sample_thesis_data() -> ThesisTemplateData:
    """Create sample data for thesis template"""
    company_info = CompanyInfo(
        name="Apple Inc",
        country="US",
        analyst="Lucas Escobar",
        gics_sector="Information Technology",
        gics_industry_group="Technology, Hardware, & Equipment",
        gics_industry="Technology Hardware, Storage &",
        gics_sub_industry="Technology Hardware, Storage &"
    )
    
    recommendation = InvestmentRecommendation(
        buy_sell_rec="Buy",
        idea_stage="ACTIVE",
        esg_rating="Leading",
        theme="Tech Innovation",
        last_price=203.92,
        base_target=300.00,
        bull_target=355.00,
        bear_target=200.00
    )
    
    thesis_text = """Apple's near-term growth could land in the low-single digits, driven by a steady services 
business that thrives on an installed base of 2.2 billion active devices."""
    
    # Sample financial data
    financials_data = {
        "": ["Sales", "EPS Adj", "EPS GAAP", "Gross Profit", "Gross Margin", "EBITDA", "EBIT", 
             "Net Income, Adj", "Net Income, GAAP", "CAPEX", "FCF"],
        "2022 A": ["394328", "6.11", "6.11", "170782", "43.31", "130541", "119437", 
                   "99803", "99803", "-10708", "111443"],
        "2023 A": ["383285", "6.13", "6.13", "169148", "44.13", "125820", "114301", 
                   "96995", "96995", "-10595", "99584"],
        "2024 A*": ["391035", "6.75", "6.08", "180683", "46.21", "134661", "123216", 
                    "103998", "93736", "-9447", "108807"],
        "2025 E": ["94832", "7.16", "6", "---", "46.55", "0", "127791", 
                   "107406", "9843", "-11053", "104200"],
        "2026 E": ["100113", "7.64", "7", "---", "46.55", "0", "132856", 
                   "111615", "11094", "-12261", "121756"],
        "2027 E": ["453388", "8.44", "8.44", "---", "47.15", "158062", "143773", 
                   "121776", "121776", "-11400", "128150"],
        "Est Source": ["Internal (EQ)", "Consensus", "Internal (EQ)", "", "Consensus", 
                       "Internal (EQ)", "Consensus", "Consensus", "Internal (EQ)", "Consensus", "Consensus"]
    }
    financials_df = pd.DataFrame(financials_data)
    
    # Sample portfolio data
    portfolio_data = {
        "ID": ["EQUITY8_US", "EQUITY8_US_VALUE", "EQUITY8_CANADIAN", "EQUITY8_EM", 
               "EQUITY8_ESG", "EQUITY8_GLOBAL", "EQUITY8_LONG_SHORT", "EQUITY8_MID_CAP_GROWTH", "EQUITY8_SMALL_CAP_GROWTH"],
        "Port Wgt": ["5.45", "0.07", "4.06", "0", "5.15", "3.88", "4.94", "0.1", "0"],
        "Bench Wgt": ["5.21", "0", "0", "0", "5.76", "4.18", "5.45", "0", "0"],
        "Active Wgt": ["-0.24", "-0.07", "-4.06", "0", "0.61", "0.31", "0.51", "-0.1", "0"],
        "TotRtn Port": ["1.53", "1.53", "1.53", "0", "1.53", "1.53", "1.53", "1.53", "0"],
        "TotRtn Bench": ["1.53", "0", "0", "0", "1.53", "1.53", "1.53", "0", "0"],
        "TotRtn Active": ["0", "1.53", "1.53", "0", "0", "0", "0", "1.53", "0"],
        "Tot Attr": ["0", "0", "0", "0", "0", "0", "0", "0", "0"]
    }
    portfolio_df = pd.DataFrame(portfolio_data)
    
    return ThesisTemplateData(
        company_info=company_info,
        recommendation=recommendation,
        thesis_text=thesis_text,
        financials_df=financials_df,
        portfolio_df=portfolio_df
    )


def create_sample_light_update_data() -> LightUpdateTemplateData:
    """Create sample data for light update template"""
    company_info = CompanyInfo(
        name="Microsoft Corporation", 
        country="US",
        analyst="Lucas Escobar",
        gics_sector="Information Technology",
        gics_industry_group="Software & Services",
        gics_industry="Software",
        gics_sub_industry="Systems Software"
    )
    
    recommendation = InvestmentRecommendation(
        buy_sell_rec="Hold",
        idea_stage="MONITORING",
        esg_rating="Improving",
        theme="Cloud Computing",
        last_price=415.26,
        base_target=450.00,
        bull_target=500.00,
        bear_target=380.00
    )
    
    return LightUpdateTemplateData(
        company_info=company_info,
        recommendation=recommendation
    )

