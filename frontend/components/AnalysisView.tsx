"use client";

import { useState } from "react";
import { analyzeCompany } from "@/lib/api";
import type { CompanyAnalysis } from "@/lib/types";

export default function AnalysisView() {
  const [url, setUrl] = useState("");
  const [result, setResult] = useState<CompanyAnalysis | null>(null);
  const [status, setStatus] = useState("");
  const [busy, setBusy] = useState(false);

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    if (!url.trim()) return;
    try {
      new URL(url);
    } catch {
      setStatus("Enter a valid company URL, for example https://company.com");
      return;
    }
    setBusy(true);
    setResult(null);
    setStatus("Running company intelligence…");
    try {
      const data = await analyzeCompany(url.trim());
      setResult(data);
      setStatus("Analysis ready.");
    } catch (error) {
      setStatus(error instanceof Error ? error.message : "Analysis failed.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <>
      <div className="app-header">
        <div><div className="eyebrow">Company intelligence</div><h1 className="app-title">Analyze a company</h1><div className="muted">Run the existing DealSense analysis through the API when available, or use isolated mock mode.</div></div>
      </div>

      <div className="workspace">
        <form className="analyze-form" onSubmit={submit}>
          <input value={url} onChange={e=>setUrl(e.target.value)} placeholder="https://company.com" aria-label="Company URL"/>
          <button className="btn btn-primary" disabled={busy}>{busy ? "Analyzing…" : "Analyze"}</button>
        </form>
        {status && <div className="status">{status}</div>}
      </div>

      {result && (
        <section className="results">
          <div className="results-hero">
            <div className="result-card">
              <div className="eyebrow">Company</div>
              <h2 style={{font:"700 31px Manrope",letterSpacing:"-.045em",margin:"8px 0"}}>{result.company}</h2>
              <p className="muted" style={{lineHeight:1.7,fontSize:13}}>{result.summary}</p>
              <div className="tags" style={{marginTop:17}}>
                <span className="tag">{result.industry}</span><span className="tag">{result.business_model}</span>
              </div>
            </div>
            <div className="result-card">
              <div className="eyebrow">Acquisition score</div>
              <div className="score-large">{result.acquisition_score}</div>
              <div className="score-meta">{result.recommendation}</div>
            </div>
          </div>

          <div className="result-grid">
            <div className="result-card"><h3>Products</h3><ul className="result-list">{result.products.map(x=><li key={x}>{x}</li>)}</ul></div>
            <div className="result-card"><h3>Customers</h3><ul className="result-list">{result.customers.map(x=><li key={x}>{x}</li>)}</ul></div>
            <div className="result-card"><h3>Investment signals</h3><div className="tags">{Object.entries(result.signals).filter(([,v])=>v).map(([k])=><span className="tag" key={k}>{k.replaceAll("_"," ")}</span>)}</div></div>
          </div>

          <div className="result-grid">
            <div className="result-card"><h3>SWOT — Strengths</h3><ul className="result-list">{result.swot.strengths.map(x=><li key={x}>{x}</li>)}</ul></div>
            <div className="result-card"><h3>SWOT — Weaknesses</h3><ul className="result-list">{result.swot.weaknesses.map(x=><li key={x}>{x}</li>)}</ul></div>
            <div className="result-card"><h3>Risks</h3><ul className="result-list">{result.risks.map(x=><li key={x}>{x}</li>)}</ul></div>
          </div>

          <div className="result-card">
            <h3>Competitors</h3>
            <div className="evidence">{result.competitors.map(c=><div className="evidence-item" key={c.name}><strong>{c.name}</strong><p>{c.reason}</p></div>)}</div>
          </div>

          <div className="result-card">
            <h3>Evidence</h3>
            <div className="evidence">{(result.evidence ?? []).map((e,i)=><div className="evidence-item" key={i}><small>{e.source ?? "Source"} · confidence {e.confidence ?? "—"}</small><p>“{e.quote ?? "No quote provided."}”</p></div>)}</div>
          </div>

          <div className="result-card">
            <h3>News Intelligence</h3>
            <div className="news-list">{(result.news ?? []).map((n,i)=><div className="news-item" key={i}><div><div className="news-date">{n.published_date ?? "Date unavailable"}</div><div className="news-source">{n.source ?? "Source unavailable"}</div></div><div><h4>{n.title}</h4><p>{n.summary}</p></div><div className={n.investment_impact==="positive"?"good":n.investment_impact==="negative"?"bad":"warn"}>{n.investment_impact ?? "unknown"}</div></div>)}</div>
          </div>
        </section>
      )}
    </>
  );
}