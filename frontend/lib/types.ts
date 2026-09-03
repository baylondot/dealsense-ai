export type SignalMap = {
  is_saas: boolean;
  is_b2b: boolean;
  is_b2c: boolean;
  recurring_revenue: boolean;
  ai_company: boolean;
  enterprise_focus: boolean;
  marketplace: boolean;
  subscription_model: boolean;
  global_presence: boolean;
  open_source: boolean;
  mobile_app: boolean;
  api_platform: boolean;
};

export type Evidence = {
  source?: string;
  quote?: string;
  confidence?: number;
};

export type Competitor = {
  name: string;
  reason?: string;
  evidence?: Evidence[];
};

export type NewsItem = {
  title: string;
  summary?: string;
  source?: string;
  url?: string;
  published_date?: string | null;
  event_type?: string;
  investment_impact?: "positive" | "negative" | "neutral" | string;
  confidence?: number;
  evidence?: Evidence[];
};

export type CompanyAnalysis = {
  company: string;
  summary: string;
  industry: string;
  business_model: string;
  products: string[];
  customers: string[];
  competitors: Competitor[];
  risks: string[];
  swot: {
    strengths: string[];
    weaknesses: string[];
    opportunities: string[];
    threats: string[];
  };
  signals: SignalMap;
  acquisition_score: number;
  recommendation: string;
  evidence?: Evidence[];
  news?: NewsItem[];
};

export type AnalyzeResponse = CompanyAnalysis;