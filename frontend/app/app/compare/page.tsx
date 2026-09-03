import { mockComparison } from "@/lib/mock";

export default function ComparePage() {
  return <>
    <div className="app-header"><div><div className="eyebrow">Comparison</div><h1 className="app-title">Company comparison</h1><div className="muted">Frontend workspace for the existing deterministic comparison engine.</div></div></div>
    <div className="workspace">
      <div className="analyze-form"><input placeholder="Add analyzed company URL or select existing analysis"/><button className="btn btn-primary">Add company</button></div>
      <table className="compare-table">
        <thead><tr><th>Dimension</th>{mockComparison.map(x=><th key={x.company}>{x.company}</th>)}</tr></thead>
        <tbody>
          <tr><td>Acquisition score</td>{mockComparison.map(x=><td key={x.company}><strong>{x.score}</strong></td>)}</tr>
          <tr><td>Recurring revenue</td>{mockComparison.map(x=><td key={x.company} className={x.recurring?"good":"bad"}>{x.recurring?"Yes":"No"}</td>)}</tr>
          <tr><td>B2B</td>{mockComparison.map(x=><td key={x.company} className={x.b2b?"good":"bad"}>{x.b2b?"Yes":"No"}</td>)}</tr>
          <tr><td>AI company</td>{mockComparison.map(x=><td key={x.company} className={x.ai?"good":"warn"}>{x.ai?"Yes":"No"}</td>)}</tr>
          <tr><td>Risk</td>{mockComparison.map(x=><td key={x.company}>{x.risk}</td>)}</tr>
        </tbody>
      </table>
      <div className="status">Mock data is shown until a comparison API is exposed. The existing backend comparison logic is not duplicated here.</div>
    </div>
  </>;
}