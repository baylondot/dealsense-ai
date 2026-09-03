import { mockPortfolio } from "@/lib/mock";

export default function PortfolioPage() {
  return <>
    <div className="app-header"><div><div className="eyebrow">Portfolio intelligence</div><h1 className="app-title">Portfolio</h1><div className="muted">A focused workspace for aggregate company intelligence and risk.</div></div><button className="btn btn-primary">Add company</button></div>
    <div className="workspace-grid">
      <div className="workspace-card"><div className="eyebrow">Companies</div><h3>3</h3><p>Tracked in this demonstration portfolio.</p></div>
      <div className="workspace-card"><div className="eyebrow">Average score</div><h3>77</h3><p>Derived from the portfolio mock records.</p></div>
      <div className="workspace-card"><div className="eyebrow">Risk concentration</div><h3>Medium</h3><p>Two companies currently represented as medium risk.</p></div>
    </div>
    <div className="workspace" style={{marginTop:14}}>
      <table className="compare-table"><thead><tr><th>Company</th><th>Industry</th><th>Score</th><th>Risk</th></tr></thead><tbody>{mockPortfolio.map(x=><tr key={x.company}><td>{x.company}</td><td>{x.industry}</td><td><strong>{x.score}</strong></td><td>{x.risk}</td></tr>)}</tbody></table>
      <div className="status">Mock data only. The existing backend portfolio module is lightweight/in-memory and is not yet exposed through FastAPI.</div>
    </div>
  </>;
}