# =============================================================================
# EARNINGS PREVIEW TEMPLATE
# =============================================================================

from ..base.template_base import BaseTemplate, BasePublishingConfig, BaseCDEMappingConfig
from ..data_models import CompanyInfo, InvestmentRecommendation, EarningsEstimate, EarningsScenario, HistoricalPattern

from ..document_generation import BloombergReportGenerator, TableStyle
from ..document_generation.utils import convert_docx_to_pdf_silently

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import datetime
import pandas as pd


@dataclass
class EarningsPreviewTemplateData:
    """Data structure for earnings preview template"""
    company_info: CompanyInfo
    recommendation: InvestmentRecommendation


    # Earnings-specific data
    earnings_date: str  # "2024-07-25"
    quarter: str  # "Q2 2024"
    estimates: List[EarningsEstimate]
    scenarios: List[EarningsScenario] = field(default_factory=list)
    historical_patterns: List[HistoricalPattern] = field(default_factory=list)

    # Key focus areas
    key_metrics_to_watch: List[str] = field(default_factory=list)
    management_guidance_focus: List[str] = field(default_factory=list)
    key_questions: List[str] = field(default_factory=list)
    risk_factors: List[str] = field(default_factory=list)
    catalysts: List[str] = field(default_factory=list)

    # Market context
    sector_earnings_context: str = ""
    competitive_context: str = ""

    # Optional overrides
    analyst_name: str = ""
    note_type: str = "Earnings Preview"

    def __post_init__(self):
        """Set defaults after initialization"""
        if not self.analyst_name:
            self.analyst_name = self.company_info.analyst
    
        # Set basic defaults if lists are empty
        if not self.estimates:
            self.estimates = [
                EarningsEstimate("Revenue", 100.0, 102.0),
                EarningsEstimate("EPS", 1.50, 1.55)
            ]
    
        if not self.scenarios:
            self.scenarios = [
                EarningsScenario("Bull", 0.25, 105.0, 1.60,
                            ["Strong demand", "Margin expansion"], "+5% to +8%"),
                EarningsScenario("Base", 0.50, 102.0, 1.55,
                            ["In-line results", "Steady margins"], "+1% to +3%"),
                EarningsScenario("Bear", 0.25, 98.0, 1.45,
                            ["Weak demand", "Margin pressure"], "-3% to -8%")
            ]
   
        if not self.key_metrics_to_watch:
            self.key_metrics_to_watch = ["Revenue growth", "Margin trends", "Guidance"]


class EarningsPreviewPublishingConfig(BasePublishingConfig):
    """Publishing configuration specific to earnings preview template"""
    pass

class EarningsPreviewCDEMappingConfig(BaseCDEMappingConfig):
    """CDE mapping configuration for earnings preview template"""
    def __init__(self,
    buy_sell_field: str = "U1R2I",
    target_price_field: str = "U1R2J",
    revenue_estimate_field: str = "U1R2K",
    eps_estimate_field: str = "U1R2L",
    earnings_date_field: str = "U1R2M"):
        field_mappings = {
        "buy_sell_rec": buy_sell_field,
        "base_target": target_price_field,
        "revenue_estimate": revenue_estimate_field,
        "eps_estimate": eps_estimate_field,
        "earnings_date": earnings_date_field
        }
        super().__init__(field_mappings)

class EarningsPreviewTemplate(BaseTemplate):
    """Earnings preview template for pre-earnings analysis"""

    @property
    def template_name(self) -> str:
        return "earnings_preview"

    @property
    def output_file_types(self) -> List[str]:
        return ["docx", "pdf"]

    @property
    def required_data_fields(self) -> List[str]:
        return ["company_info", "recommendation", "earnings_date", "estimates"]

    def generate_document(self, data: EarningsPreviewTemplateData, output_filename: str) -> Dict[str, str]:
        """Generate earnings preview document (DOCX and PDF)"""
        self.validate_data(data)
    
        docx_path = f"{output_filename}.docx"
        pdf_path = f"{output_filename}.pdf"
    
        # Initialize generator
        generator = BloombergReportGenerator(self.style_config)
        generator.create_document()
    
        # Add earnings preview specific sections
        self.add_earnings_preview_sections(generator, data)
    
        # Save documents
        generator.save_document(docx_path)
        convert_docx_to_pdf_silently(docx_path, pdf_path)
    
        return {"docx": docx_path, "pdf": pdf_path}

    def add_earnings_preview_sections(self, generator: BloombergReportGenerator, data: EarningsPreviewTemplateData):
        """Add sections specific to earnings preview"""
    
        # Header with earnings date prominence
        title = f"{data.company_info.name} - {data.quarter} Earnings Preview"
        generator.add_earnings_preview_section(title, data.earnings_date)

        # Company info and recommendation (condensed)
        generator.add_company_info_section(data.company_info)
        generator.add_recommendation_section(data.recommendation)
    
        # Core earnings preview sections
        self._add_estimates_vs_consensus_section(generator, data)
        self._add_scenario_analysis_section(generator, data)
        # self._add_key_metrics_section(generator, data)
        generator.add_key_metrics_section(data.key_metrics_to_watch)

        if data.historical_patterns:
            self._add_historical_performance_section(generator, data)

        # self._add_management_focus_section(generator, data)
        # self._add_risks_and_catalysts_section(generator, data)

        # Management focus section
        generator.add_management_focus_section(
            data.management_guidance_focus,
            data.key_questions
        )

        # Risks and catalysts
        generator.add_risks_catalysts_section(data.risk_factors, data.catalysts)
    
        if data.sector_earnings_context or data.competitive_context:
            #self._add_market_context_section(generator, data)
            generator.add_market_context_section(
                data.sector_earnings_context,
                data.competitive_context
            )

    def _add_estimates_vs_consensus_section(self, generator: BloombergReportGenerator, data: EarningsPreviewTemplateData):
        """Add analyst estimates vs consensus comparison"""
        # generator.add_heading("Our Estimates vs. Consensus", level=2)
    
        # Create table data
        table_data = [["Metric", "Consensus", "Our Estimate", "Difference", "Difference %"]]
        for estimate in data.estimates:
            table_data.append([
                estimate.metric_name,
                f"{estimate.consensus_estimate:.2f}",
                f"{estimate.analyst_estimate:.2f}",
                f"{estimate.difference:+.2f}",
                f"{estimate.difference_pct:+.1f}%"
            ])
    
        generator.add_estimates_comparison_section(table_data)

    def _add_scenario_analysis_section(self, generator: BloombergReportGenerator, data: EarningsPreviewTemplateData):
        """Add scenario analysis table"""
        # generator.add_heading("Scenario Analysis", level=2)
    
        # Create scenario table
        table_data = [["Scenario", "Probability", "Revenue", "EPS", "Expected Stock Reaction"]]
        scenario_details = []
        for scenario in data.scenarios:
            table_data.append([
                scenario.scenario_name,
                f"{scenario.probability:.0%}",
                f"${scenario.revenue_estimate:.1f}B",
                f"${scenario.eps_estimate:.2f}",
                scenario.stock_reaction
            ])
    
        # generator.add_table(table_data, style=self._get_default_style())
    
        # # Add scenario assumptions
        # for scenario in data.scenarios:
        #     generator.add_paragraph(f"**{scenario.scenario_name} Case Assumptions:**")
        #     for assumption in scenario.key_assumptions:
        #         generator.add_paragraph(f"• {assumption}")
            
            # Prepare scenario details
            assumptions_text = f"**{scenario.scenario_name} Case Assumptions:** " + "; ".join(scenario.key_assumptions)
            scenario_details.append(assumptions_text)
   
        generator.add_scenario_analysis_section(table_data, scenario_details)
        

    # def _add_key_metrics_section(self, generator: BloombergReportGenerator, data: EarningsPreviewTemplateData):
    #     """Add key metrics to watch"""
    #     generator.add_heading("Key Metrics to Watch", level=2)
    
    #     for metric in data.key_metrics_to_watch:
    #         generator.add_paragraph(f"• **{metric}**")

    def _add_historical_performance_section(self, generator: BloombergReportGenerator, data: EarningsPreviewTemplateData):
        """Add historical earnings performance"""
        # generator.add_heading("Historical Earnings Performance", level=2)
    
        table_data = [["Quarter", "Revenue Surprise %", "EPS Surprise %", "1-Day Reaction", "1-Week Reaction"]]
        for pattern in data.historical_patterns:
            table_data.append([
                pattern.quarter,
                f"{pattern.revenue_surprise_pct:+.1f}%",
                f"{pattern.eps_surprise_pct:+.1f}%",
                f"{pattern.stock_reaction_1d:+.1f}%",
                f"{pattern.stock_reaction_1w:+.1f}%"
            ])

        generator.add_historical_earnings_section(table_data)
        # generator.add_table(table_data, style=self._get_default_style())

    # def _add_management_focus_section(self, generator: BloombergReportGenerator, data: EarningsPreviewTemplateData):
    #     """Add management guidance and Q&A focus"""
    #     generator.add_heading("Management Guidance & Key Questions", level=2)
    
    #     if data.management_guidance_focus:
    #         generator.add_paragraph("**Expected Guidance Updates:**")
    #         for guidance in data.management_guidance_focus:
    #             generator.add_paragraph(f"• {guidance}")
    
    #     if data.key_questions:
    #         generator.add_paragraph("**Key Questions for Management:**")
    #         for question in data.key_questions:
    #             generator.add_paragraph(f"• {question}")

    # def _add_risks_and_catalysts_section(self, generator: BloombergReportGenerator, data: EarningsPreviewTemplateData):
    #     """Add risks and catalysts"""
    #     generator.add_heading("Risks & Catalysts", level=2)
    
    #     if data.risk_factors:
    #         generator.add_paragraph("**Key Risks:**")
    #         for risk in data.risk_factors:
    #             generator.add_paragraph(f"• {risk}")
    
    #     if data.catalysts:
    #         generator.add_paragraph("**Potential Catalysts:**")
    #         for catalyst in data.catalysts:
    #             generator.add_paragraph(f"• {catalyst}")

    # def _add_market_context_section(self, generator: BloombergReportGenerator, data: EarningsPreviewTemplateData):
    #     """Add market and competitive context"""
    #     generator.add_heading("Market Context", level=2)
    
    #     if data.sector_earnings_context:
    #         generator.add_paragraph(f"**Sector Context:** {data.sector_earnings_context}")
    
    #     if data.competitive_context:
    #         generator.add_paragraph(f"**Competitive Positioning:** {data.competitive_context}")

    def get_required_tags(self, data: EarningsPreviewTemplateData, config: EarningsPreviewPublishingConfig) -> List[str]:
        """Get tag types needed for earnings preview template"""
        return ["primary_security", "author"] + [f"taglist_{i}" for i in range(len(config.taglists))]

    def prepare_cde_data(self, data: EarningsPreviewTemplateData, ticker: str,
                        config: EarningsPreviewPublishingConfig,
                        cde_config: EarningsPreviewCDEMappingConfig) -> pd.DataFrame:
        """Prepare CDE data for earnings preview template"""
        date_str = datetime.datetime.strptime(config.as_of_date, '%Y-%m-%d').strftime('%Y%m%d')
    
        cde_records = []
    
        # Basic recommendation fields
        if "buy_sell_rec" in cde_config.field_mappings:
            cde_records.append({
                'parsekey': ticker,
                'field': cde_config.field_mappings["buy_sell_rec"],
                'value': data.recommendation.buy_sell_rec,
                'date': date_str
            })
    
        if "base_target" in cde_config.field_mappings:
            cde_records.append({
                'parsekey': ticker,
                'field': cde_config.field_mappings["base_target"],
                'value': data.recommendation.base_target,
                'date': date_str
            })
    
        # Earnings-specific fields
        revenue_estimate = next((e.analyst_estimate for e in data.estimates if "Revenue" in e.metric_name), None)
        eps_estimate = next((e.analyst_estimate for e in data.estimates if "EPS" in e.metric_name), None)
    
        if revenue_estimate and "revenue_estimate" in cde_config.field_mappings:
            cde_records.append({
                'parsekey': ticker,
                'field': cde_config.field_mappings["revenue_estimate"],
                'value': revenue_estimate,
                'date': date_str
            })
    
        if eps_estimate and "eps_estimate" in cde_config.field_mappings:
            cde_records.append({
                'parsekey': ticker,
                'field': cde_config.field_mappings["eps_estimate"],
                'value': eps_estimate,
                'date': date_str
            })
    
        if "earnings_date" in cde_config.field_mappings:
            cde_records.append({
                'parsekey': ticker,
                'field': cde_config.field_mappings["earnings_date"],
                'value': data.earnings_date,
                'date': date_str
            })
    
        return pd.DataFrame(cde_records)

