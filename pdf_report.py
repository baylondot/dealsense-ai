from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable, Sequence

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import ListFlowable, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from models import CompanyAnalysis


@dataclass
class PDFReportConfig:
    """Reusable configuration for future branded or specialized report output."""

    title: str = "DealSense AI Investment Report"
    author: str = "DealSense AI"
    subject: str = "Investment Due Diligence Report"
    brand_primary: str = "#103A68"
    brand_secondary: str = "#1F4E79"
    accent: str = "#D9EAF7"
    logo_path: str | None = None
    output_dir: str | Path | None = None


class PDFReportGenerator:
    """Generate a professional investment report from a structured CompanyAnalysis object."""

    def __init__(self, config: PDFReportConfig | None = None):
        self.config = config or PDFReportConfig()
        self.styles = getSampleStyleSheet()
        self.title_style = ParagraphStyle(
            "ReportTitle",
            parent=self.styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=26,
            leading=30,
            textColor=colors.HexColor(self.config.brand_primary),
            spaceAfter=18,
        )
        self.section_style = ParagraphStyle(
            "SectionTitle",
            parent=self.styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=16,
            leading=20,
            textColor=colors.HexColor(self.config.brand_primary),
            spaceBefore=18,
            spaceAfter=8,
        )
        self.subsection_style = ParagraphStyle(
            "SubsectionTitle",
            parent=self.styles["Heading3"],
            fontName="Helvetica-Bold",
            fontSize=11,
            leading=14,
            textColor=colors.HexColor(self.config.brand_secondary),
            spaceBefore=12,
            spaceAfter=6,
        )
        self.body_style = ParagraphStyle(
            "BodyText",
            parent=self.styles["BodyText"],
            fontName="Helvetica",
            fontSize=10,
            leading=14,
            spaceAfter=8,
            textColor=colors.black,
        )
        self.muted_style = ParagraphStyle(
            "MutedText",
            parent=self.body_style,
            fontSize=9,
            textColor=colors.HexColor("#555555"),
            spaceAfter=6,
        )
        self.label_style = ParagraphStyle(
            "LabelText",
            parent=self.body_style,
            fontName="Helvetica-Bold",
            fontSize=9,
            leading=12,
            spaceAfter=4,
        )

    def generate(self, company: CompanyAnalysis, output_path: str | Path | None = None) -> str:
        resolved = self._resolve_output_path(output_path, company)
        resolved_path = Path(resolved)
        resolved_path.parent.mkdir(parents=True, exist_ok=True)

        doc = SimpleDocTemplate(
            str(resolved_path),
            pagesize=A4,
            leftMargin=0.75 * inch,
            rightMargin=0.75 * inch,
            topMargin=0.75 * inch,
            bottomMargin=0.75 * inch,
            title=self.config.title,
            author=self.config.author,
            subject=self.config.subject,
        )

        story = self._build_story(company)
        doc.build(story)
        return str(resolved_path)

    def _resolve_output_path(self, output_path: str | Path | None, company: CompanyAnalysis) -> str:
        if output_path:
            path = Path(output_path)
            if path.suffix.lower() == ".pdf":
                return str(path)
            if path.exists() and path.is_dir():
                return str(path / self._slugify(company.company or "company_report") / "report.pdf")
            return str(path / "report.pdf") if not path.suffix else str(path)

        base_dir = Path(self.config.output_dir) if self.config.output_dir else Path.cwd() / "reports"
        filename = f"{self._slugify(company.company or 'company_report')}.pdf"
        return str(base_dir / filename)

    def _build_story(self, company: CompanyAnalysis):
        story = []

        story.extend(self._cover_page(company))
        story.append(PageBreak())

        story.extend(self._section("Executive Summary", _safe_text(company.summary)))
        story.extend(self._section("Company Overview", self._company_overview(company)))
        story.extend(self._section("Business Model", _safe_text(company.business_model)))
        story.extend(self._section("Industry", _safe_text(company.industry)))
        story.extend(self._section("Products", self._render_bullets(company.products)))
        story.extend(self._section("Customers", self._render_bullets(company.customers)))
        story.extend(self._section("Investment Signals", self._render_signals(company)))
        story.extend(self._section("Competitor Analysis", self._render_competitors(company.competitors)))
        story.extend(self._section("Risk Analysis", self._render_risks(company.risks)))
        story.extend(self._section("SWOT Analysis", self._render_swot(company.swot)))
        story.extend(self._section("Evidence Summary", self._render_evidence(company.evidence)))
        story.extend(self._section("Final Recommendation", self._render_recommendation(company)))

        return story

    def _cover_page(self, company: CompanyAnalysis):
        company_name = _safe_text(company.company, "Unnamed Company")
        recommendation = _safe_text(company.recommendation, "No recommendation available.")
        generation_date = datetime.now().strftime("%B %d, %Y")

        title_block = [
            Paragraph("DealSense AI", self.muted_style),
            Spacer(1, 0.18 * inch),
            Paragraph(company_name, self.title_style),
            Spacer(1, 0.18 * inch),
            Paragraph("Investment Due Diligence Report", self.subsection_style),
        ]

        score_text = f"Acquisition Score: {int(company.acquisition_score or 0)}/100"
        summary_table = Table(
            [[score_text, recommendation]],
            colWidths=[2.5 * inch, 3.5 * inch],
            rowHeights=[0.8 * inch],
        )
        summary_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor(self.config.accent)),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor(self.config.brand_secondary)),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 12),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                    ("TOPPADDING", (0, 0), (-1, -1), 12),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
                ]
            )
        )

        return [
            Spacer(1, 0.5 * inch),
            *title_block,
            Spacer(1, 0.35 * inch),
            Paragraph(f"Recommendation: {recommendation}", self.body_style),
            Spacer(1, 0.15 * inch),
            summary_table,
            Spacer(1, 0.4 * inch),
            Paragraph(f"Generated on: {generation_date}", self.muted_style),
        ]

    def _company_overview(self, company: CompanyAnalysis) -> str:
        overview = [
            _safe_text(company.summary),
            "",
            f"Industry: {_safe_text(company.industry)}",
            f"Business Model: {_safe_text(company.business_model)}",
        ]
        return "\n".join(overview)

    def _render_bullets(self, items: Sequence[str] | None) -> list[Any]:
        cleaned = [str(item).strip() for item in (items or []) if str(item).strip()]
        if not cleaned:
            cleaned = ["Not enough information."]
        bullet_items = [Paragraph(f"• {item}", self.body_style) for item in cleaned]
        return bullet_items

    def _render_signals(self, company: CompanyAnalysis):
        signals = company.signals
        if signals is None:
            return [Paragraph("No investment signals available.", self.body_style)]

        signal_map = {
            "SaaS": getattr(signals, "is_saas", False),
            "B2B": getattr(signals, "is_b2b", False),
            "B2C": getattr(signals, "is_b2c", False),
            "Recurring Revenue": getattr(signals, "recurring_revenue", False),
            "AI Company": getattr(signals, "ai_company", False),
            "Enterprise Focus": getattr(signals, "enterprise_focus", False),
            "Marketplace": getattr(signals, "marketplace", False),
            "Subscription Model": getattr(signals, "subscription_model", False),
            "Global Presence": getattr(signals, "global_presence", False),
            "Open Source": getattr(signals, "open_source", False),
            "Mobile App": getattr(signals, "mobile_app", False),
            "API Platform": getattr(signals, "api_platform", False),
        }

        identified = [name for name, value in signal_map.items() if value]
        if not identified:
            identified = ["No positive investment signals identified in the current analysis."]

        return self._render_bullets(identified)

    def _render_competitors(self, competitors: Sequence[Any] | None):
        if not competitors:
            return [Paragraph("No competitor information available.", self.body_style)]

        entries = []
        for competitor in competitors:
            if isinstance(competitor, str):
                entries.append(Paragraph(f"• {competitor}", self.body_style))
                continue
            name = _safe_text(getattr(competitor, "name", ""), "Unnamed competitor")
            reason = _safe_text(getattr(competitor, "reason", ""), "No rationale provided.")
            evidence = self._evidence_text(getattr(competitor, "evidence", None))
            entries.append(Paragraph(name, self.subsection_style))
            entries.append(Paragraph(reason, self.body_style))
            entries.append(Paragraph(evidence, self.body_style))
            entries.append(Spacer(1, 0.08 * inch))

        return entries

    def _render_risks(self, risks: Sequence[Any] | None):
        if not risks:
            return [Paragraph("No risk information available.", self.body_style)]

        entries = []
        for risk in risks:
            if isinstance(risk, str):
                entries.append(Paragraph(f"• {risk}", self.body_style))
                continue
            title = _safe_text(getattr(risk, "title", ""), "Unnamed risk")
            description = _safe_text(getattr(risk, "description", ""), "No description provided.")
            evidence = self._evidence_text(getattr(risk, "evidence", None))
            entries.append(Paragraph(title, self.subsection_style))
            entries.append(Paragraph(description, self.body_style))
            entries.append(Paragraph(evidence, self.body_style))
            entries.append(Spacer(1, 0.08 * inch))

        return entries

    def _render_swot(self, swot: Any):
        if swot is None:
            strengths = weaknesses = opportunities = threats = []
        else:
            strengths = list(getattr(swot, "strengths", []) or [])
            weaknesses = list(getattr(swot, "weaknesses", []) or [])
            opportunities = list(getattr(swot, "opportunities", []) or [])
            threats = list(getattr(swot, "threats", []) or [])

        def cell(items: Sequence[str]) -> str:
            if not items:
                return "Not enough information."
            return "\n".join(f"• {item}" for item in items)

        data = [
            ["Strengths", "Weaknesses"],
            [cell(strengths), cell(weaknesses)],
            ["Opportunities", "Threats"],
            [cell(opportunities), cell(threats)],
        ]

        table = Table(data, colWidths=[2.8 * inch, 2.8 * inch], rowHeights=[0.25 * inch, 1.3 * inch, 0.25 * inch, 1.3 * inch])
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(self.config.accent)),
                    ("BACKGROUND", (0, 2), (-1, 2), colors.HexColor(self.config.accent)),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor(self.config.brand_secondary)),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 8),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                    ("TOPPADDING", (0, 0), (-1, -1), 8),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTNAME", (0, 2), (-1, 2), "Helvetica-Bold"),
                ]
            )
        )
        return [table]

    def _render_evidence(self, evidence_items: Sequence[Any] | None):
        if not evidence_items:
            return [Paragraph("No direct evidence available.", self.body_style)]

        entries = []
        for evidence in evidence_items:
            source = _safe_text(getattr(evidence, "source", ""), "Unknown source")
            confidence = getattr(evidence, "confidence", 0)
            quote = _safe_text(getattr(evidence, "quote", ""), "No quotation provided.")
            entries.append(Paragraph(f"Source: {source} | Confidence: {confidence}/100", self.label_style))
            entries.append(Paragraph(f'"{quote}"', self.body_style))
            entries.append(Spacer(1, 0.08 * inch))

        return entries

    def _render_recommendation(self, company: CompanyAnalysis):
        score = int(company.acquisition_score or 0)
        recommendation = _safe_text(company.recommendation, "No recommendation available.")
        summary = (
            f"Acquisition score: {score}/100. "
            f"Based on the current analysis, the investment recommendation is: {recommendation}"
        )
        return [Paragraph(summary, self.body_style)]

    def _section(self, title: str, body: str | list[Any]):
        if isinstance(body, str):
            content = [Paragraph(body, self.body_style)]
        elif isinstance(body, list):
            content = body
        else:
            content = [body]

        return [Paragraph(title, self.section_style), *content, Spacer(1, 0.12 * inch)]

    def _evidence_text(self, evidence_items: Sequence[Any] | None) -> str:
        if not evidence_items:
            return "Evidence: None provided."

        fragments = []
        for evidence in evidence_items:
            source = _safe_text(getattr(evidence, "source", ""), "Unknown source")
            confidence = getattr(evidence, "confidence", 0)
            quote = _safe_text(getattr(evidence, "quote", ""), "No quotation provided.")
            fragments.append(f"Evidence from {source} (confidence {confidence}/100): {quote}")
        return " ".join(fragments) if fragments else "Evidence: None provided."

    def _slugify(self, text: str) -> str:
        normalized = "".join(char.lower() if char.isalnum() or char in "-_ " else "-" for char in text)
        normalized = "-".join(part for part in normalized.split() if part)
        return normalized or "company-report"


def _safe_text(value: str | None, fallback: str = "Not enough information.") -> str:
    if value is None:
        return fallback
    cleaned = value.strip()
    return cleaned if cleaned else fallback


def generate_pdf_report(
    company: CompanyAnalysis,
    output_path: str | Path | None = None,
    config: PDFReportConfig | None = None,
) -> str:
    """Generate a reusable PDF report from an existing CompanyAnalysis object.

    Returns the absolute path to the created PDF so the UI or API layer can provide a download.
    """

    generator = PDFReportGenerator(config=config)
    return generator.generate(company, output_path=output_path)
