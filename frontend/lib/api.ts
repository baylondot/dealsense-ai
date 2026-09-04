import type { CompanyAnalysis } from "./types";

const baseUrl = process.env.NEXT_PUBLIC_API_URL?.replace(/\/$/, "");
const forceMock = process.env.NEXT_PUBLIC_USE_MOCK === "true";
const requestTimeoutMs = 120_000;

class ApiError extends Error {
  constructor(message: string, public readonly status?: number) {
    super(message);
    this.name = "ApiError";
  }
}

function isCompanyAnalysis(value: unknown): value is CompanyAnalysis {
  if (!value || typeof value !== "object") return false;
  const analysis = value as Record<string, unknown>;
  return (
    typeof analysis.company === "string" &&
    typeof analysis.summary === "string" &&
    typeof analysis.business_model === "string" &&
    Array.isArray(analysis.products) &&
    Array.isArray(analysis.customers) &&
    Array.isArray(analysis.competitors) &&
    Array.isArray(analysis.risks) &&
    typeof analysis.swot === "object" &&
    analysis.swot !== null &&
    typeof analysis.signals === "object" &&
    analysis.signals !== null &&
    typeof analysis.acquisition_score === "number" &&
    typeof analysis.recommendation === "string"
  );
}

async function readError(response: Response): Promise<string> {
  try {
    const payload: unknown = await response.json();
    if (payload && typeof payload === "object" && "detail" in payload && typeof payload.detail === "string") {
      return payload.detail;
    }
  } catch {
    // Fall through to the status-based message.
  }
  return `Analysis request failed (${response.status})`;
}

export async function analyzeCompany(url: string, refresh = false): Promise<CompanyAnalysis> {
  if (forceMock) {
    const { mockAnalysis } = await import("./mock");
    await new Promise((resolve) => setTimeout(resolve, 850));
    return { ...mockAnalysis, company: new URL(url).hostname.replace("www.", "") || mockAnalysis.company };
  }
  if (!baseUrl) {
    throw new ApiError("Analysis is unavailable because the backend URL is not configured.");
  }

  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), requestTimeoutMs);
  try {
    const response = await fetch(`${baseUrl}/api/analyze`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url, refresh }),
      cache: "no-store",
      signal: controller.signal
    });

    if (!response.ok) {
      throw new ApiError(await readError(response), response.status);
    }

    const payload: unknown = await response.json();
    if (!isCompanyAnalysis(payload)) {
      throw new ApiError("The backend returned an unexpected analysis response.");
    }
    return payload;
  } catch (error) {
    if (error instanceof ApiError) throw error;
    if (error instanceof DOMException && error.name === "AbortError") {
      throw new ApiError("The analysis is taking too long. Please try again.");
    }
    throw new ApiError("Unable to reach the analysis backend. Check that it is running and try again.");
  } finally {
    clearTimeout(timeout);
  }
}