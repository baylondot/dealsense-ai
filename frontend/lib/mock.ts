import type { CompanyAnalysis } from "./types";

export const mockAnalysis: CompanyAnalysis = {
  company: "Northstar Systems",
  summary: "A B2B software company providing workflow and intelligence infrastructure for mid-market operations teams.",
  industry: "B2B Software",
  business_model: "Subscription",
  products: ["Workflow platform", "Analytics", "Automation", "API"],
  customers: ["Operations teams", "Technology companies", "Mid-market enterprises"],
  competitors: [
    { name: "Competitor One", reason: "Overlaps in workflow automation and analytics.", evidence: [] },
    { name: "Competitor Two", reason: "Targets a similar B2B customer segment.", evidence: [] }
  ],
  risks: ["Competitive pressure", "Customer concentration", "Limited public financial information"],
  swot: {
    strengths: ["Recurring model", "B2B positioning", "API platform"],
    weaknesses: ["Concentrated customer base"],
    opportunities: ["Enterprise expansion", "Automation demand"],
    threats: ["Incumbent platforms", "Pricing pressure"]
  },
  signals: {
    is_saas: true,
    is_b2b: true,
    is_b2c: false,
    recurring_revenue: true,
    ai_company: true,
    enterprise_focus: true,
    marketplace: false,
    subscription_model: true,
    global_presence: true,
    open_source: false,
    mobile_app: false,
    api_platform: true,
    evidence: {}
  },
  acquisition_score: 76,
  recommendation: "Attractive candidate for deeper diligence, with particular attention to retention, customer concentration and competitive differentiation.",
  evidence: [
    { source: "Company website", quote: "Illustrative evidence shown in frontend mock mode.", confidence: 82 }
  ],
  news: [
    {
      title: "Recent strategic expansion",
      summary: "Illustrative news item used only to demonstrate the News Intelligence interface.",
      source: "Mock source",
      published_date: "2026-07-01",
      event_type: "strategic",
      investment_impact: "positive",
      confidence: 78
    }
  ]
};

export const mockComparison = [
  { company: "Northstar Systems", score: 76, recurring: true, b2b: true, ai: true, risk: "Medium" },
  { company: "Atlas Cloud", score: 71, recurring: true, b2b: true, ai: false, risk: "Medium" },
  { company: "Vector Labs", score: 83, recurring: true, b2b: true, ai: true, risk: "Low" }
];

export const mockPortfolio = [
  { company: "Northstar Systems", score: 76, industry: "B2B Software", risk: "Medium" },
  { company: "Vector Labs", score: 83, industry: "AI Software", risk: "Low" },
  { company: "Atlas Cloud", score: 71, industry: "Cloud Infrastructure", risk: "Medium" }
];