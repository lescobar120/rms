# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

import pandas as pd

from .document_generation.styling import TableStyle
from .document_generation.document_styler import DocumentStyler
from .document_generation.table_builder import TableBuilder
from .document_generation import BloombergReportGenerator, TableStyle
from .document_generation.utils import convert_docx_to_pdf_silently
from .data_models import (
    CompanyInfo, InvestmentRecommendation,
    IdeaStage, BuySellRec, InvestmentThemeTagList,
    ModelHeader, CompanyModelInfo, RecommendationData,
    ValuationScenarios, TargetPriceData, FinancialMetric,
    FinancialsData, CompanyModelData,
    EarningsEstimate, EarningsScenario, HistoricalPattern
) 
from .templates.thesis_template import ThesisTemplateData
from .templates.light_update_template import LightUpdateTemplateData
from .templates.company_model_template import CompanyModelTemplateData
from .templates.earnings_preview_template import EarningsPreviewTemplateData

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
        buy_sell_rec=BuySellRec.BUY,
        idea_stage=IdeaStage.ACTIVE,
        esg_rating="Leading",
        theme=InvestmentThemeTagList.TECH_TRIFECTA,
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
        buy_sell_rec=BuySellRec.HOLD,
        idea_stage=IdeaStage.WIP,
        esg_rating="Improving",
        theme=InvestmentThemeTagList.APPLYING_AI,
        last_price=415.26,
        base_target=450.00,
        bull_target=500.00,
        bear_target=380.00
    )
    
    return LightUpdateTemplateData(
        company_info=company_info,
        recommendation=recommendation
    )


def create_sample_financials_data() -> FinancialsData:
    """Create sample financial data for testing"""
    years = ['2022', '2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030']
    
    # Generate realistic sample metrics
    financial_metrics = [
        FinancialMetric('EPS Adj', {
            '2022': 4.78, '2023': 5.24, '2024': 8.22, '2025': 10.20,
            '2026': 11.85, '2027': 13.15, '2028': 14.22, '2029': 15.38, '2030': 16.44
        }),
        FinancialMetric('Revenue', {
            '2022': 31352, '2023': 34009, '2024': 37972, '2025': 42850,
            '2026': 48327, '2027': 53891, '2028': 59441, '2029': 64923, '2030': 70284
        }),
        FinancialMetric('EBITDA', {
            '2022': 8151, '2023': 9001, '2024': 11538, '2025': 14510,
            '2026': 17298, '2027': 19802, '2028': 22109, '2029': 24187, '2030': 26102
        }),
        FinancialMetric('Free Cash Flow', {
            '2022': 6932, '2023': 7787, '2024': 10165, '2025': 12844,
            '2026': 15386, '2027': 17721, '2028': 19884, '2029': 21853, '2030': 23654
        })
    ]
    
    return FinancialsData(years=years, metrics=financial_metrics)


def create_sample_company_model_data() -> CompanyModelData:
    """Create sample company model data for testing"""
    header = ModelHeader(
        analyst_name="Lucas Escobar",
        note_type="Company Model",
        idea_stage=IdeaStage.ACTIVE
    )
    
    company_info = CompanyModelInfo(
        company_name="Salesforce Inc"
    )
    
    recommendation = RecommendationData(
        current_buy_sell_rec=BuySellRec.BUY,
        current_ow_uw_rec="OW",
        current_esg_rating="Leading",
        previous_buy_sell_rec=BuySellRec.BUY,
        previous_ow_uw_rec="OW",
        previous_esg_rating="Leading"
    )
    
    valuation_scenarios = ValuationScenarios()
    
    target_price = TargetPriceData(
        base_target_px=285.00,
        base_probability=0.65,
        base_exp_return=0.15,
        bull_target_px=350.00,
        bull_probability=0.25,
        bull_exp_return=0.35,
        bear_target_px=220.00,
        bear_probability=0.10,
        bear_exp_return=-0.10
    )
    
    financials = create_sample_financials_data()
    
    return CompanyModelData(
        header=header,
        company_info=company_info,
        recommendation=recommendation,
        valuation_scenarios=valuation_scenarios,
        target_price=target_price,
        financials=financials,
        investment_thesis="Salesforce continues to dominate the CRM market with strong recurring revenue growth and expanding platform capabilities.",
        model_assumptions="Assumes 15% annual revenue growth, improving margins through operational efficiency, and successful AI product integration driving higher ASPs."
    )



def create_sample_company_model_template_data() -> CompanyModelTemplateData:
    """Create sample data for company model template"""
    company_info = CompanyInfo(
        name="Salesforce Inc",
        country="US",
        analyst="Lucas Escobar",
        gics_sector="Information Technology",
        gics_industry_group="Software & Services",
        gics_industry="Software",
        gics_sub_industry="Application Software"
    )
    
    recommendation = InvestmentRecommendation(
        buy_sell_rec=BuySellRec.BUY,
        idea_stage=IdeaStage.ACTIVE,
        esg_rating="Leading",
        theme=InvestmentThemeTagList.APPLYING_AI,
        last_price=248.50,
        base_target=285.00,
        bull_target=350.00,
        bear_target=220.00
    )
    
    return CompanyModelTemplateData(
        company_info=company_info,
        recommendation=recommendation,
        investment_thesis="Salesforce continues to dominate the CRM market with strong recurring revenue growth and expanding platform capabilities.",
        model_assumptions="Assumes 15% annual revenue growth, improving margins through operational efficiency, and successful AI product integration driving higher ASPs.",
        financials_data = create_sample_financials_data()
    )


def create_sample_earnings_preview_data() -> EarningsPreviewTemplateData:
    """Create sample data for earnings preview template"""

    company_info = CompanyInfo(
        name="Microsoft Corporation",
        country="US",
        analyst="Lucas Escobar",
        gics_sector="Information Technology",
        gics_industry_group="Technology, Hardware, & Equipment",
        gics_industry="Software",
        gics_sub_industry="Systems Software"
    )

    recommendation = InvestmentRecommendation(
        buy_sell_rec=BuySellRec.BUY,
        idea_stage=IdeaStage.ACTIVE,
        esg_rating="Leading",
        theme=InvestmentThemeTagList.APPLYING_AI,
        last_price=420.50,
        base_target=480.00,
        bull_target=520.00,
        bear_target=390.00
    )

    # Create sample estimates
    estimates = [
        EarningsEstimate("Revenue", 64.50, 65.20),  # Analyst above consensus
        EarningsEstimate("EPS", 2.78, 2.85),        # Analyst above consensus
        EarningsEstimate("Azure Growth", 26.0, 28.0) # Analyst more optimistic
    ]

    # Create scenarios
    scenarios = [
        EarningsScenario(
            "Bull", 0.25, 66.5, 2.95,
            ["Strong Azure demand", "Office 365 price increases", "AI monetization"],
            "+8% to +12%"
        ),
        EarningsScenario(
            "Base", 0.50, 65.2, 2.85,
            ["Steady cloud growth", "In-line guidance", "Normal seasonality"],
            "+3% to +6%"
        ),
        EarningsScenario(
            "Bear", 0.25, 63.8, 2.70,
            ["Macro headwinds", "Cloud optimization", "Competition pressure"],
            "-5% to -8%"
        )
    ]

    # Historical patterns
    historical_patterns = [
        HistoricalPattern("Q1 2024", 2.1, 4.3, 3.2, 1.8),
        HistoricalPattern("Q4 2023", -0.8, 1.9, -1.4, 2.1),
        HistoricalPattern("Q3 2023", 1.5, 3.1, 4.7, 3.9),
        HistoricalPattern("Q2 2023", 0.9, 2.8, 1.2, 0.8)
    ]

    return EarningsPreviewTemplateData(
        company_info=company_info,
        recommendation=recommendation,
        earnings_date="2024-07-24",
        quarter="Q2 2024",
        estimates=estimates,
        scenarios=scenarios,
        historical_patterns=historical_patterns,
        key_metrics_to_watch=[
            "Azure revenue growth (expecting 28% vs 26% consensus)",
            "Office 365 commercial seat growth",
            "AI services revenue contribution",
            "Operating margin expansion",
            "FY25 guidance update"
        ],
        management_guidance_focus=[
            "FY25 total revenue outlook",
            "Azure growth trajectory",
            "AI revenue monetization timeline",
            "Capital expenditure plans"
        ],
        key_questions=[
            "How is Copilot adoption progressing across enterprise customers?",
            "What's the competitive impact from Google Cloud's pricing actions?",
            "How should we think about AI infrastructure capex going forward?",
            "Any updates on the Activision integration synergies?"
        ],
        risk_factors=[
            "Macro-driven cloud optimization by enterprise customers",
            "Increased competition in AI/cloud space",
            "Currency headwinds in international markets"
        ],
        catalysts=[
            "Strong Copilot adoption metrics",
            "Accelerating Azure consumption growth",
            "Better-than-expected AI monetization"
        ],
        sector_earnings_context="Tech sector showing mixed results with cloud leaders outperforming",
        competitive_context="Maintaining market share gains vs AWS, ahead of Google Cloud"
    )

