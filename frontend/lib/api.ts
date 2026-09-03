import { mockAnalysis } from "./mock";
import type { CompanyAnalysis } from "./types";

const baseUrl = process.env.NEXT_PUBLIC_API_URL?.replace(/\/$/, "");
const forceMock = process.env.NEXT_PUBLIC_USE_MOCK === "true";

export async function analyzeCompany(url: string, refresh = false): Promise<CompanyAnalysis> {
  if (!baseUrl || forceMock) {
    await new Promise((resolve) => setTimeout(resolve, 850));
    return { ...mockAnalysis, company: new URL(url).hostname.replace("www.", "") || mockAnalysis.company };
  }

  const response = await fetch(`${baseUrl}/api/analyze`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url, refresh }),
    cache: "no-store"
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || `Analysis request failed (${response.status})`);
  }

  return response.json() as Promise<CompanyAnalysis>;
}