export default function ReportsPage() {
  return <>
    <div className="app-header"><div><div className="eyebrow">Reports</div><h1 className="app-title">Reports & PDF</h1><div className="muted">Explicit report actions—analysis never generates a PDF automatically.</div></div></div>
    <div className="workspace-grid">
      <div className="workspace-card"><div className="eyebrow">Latest report</div><h3>Not generated</h3><p>Connect this action to the existing PDF generation endpoint when it is exposed through FastAPI.</p><button className="btn" style={{marginTop:15}}>Generate report</button></div>
      <div className="workspace-card"><div className="eyebrow">Memo source</div><h3>Investment Memo</h3><p>The existing report generator returns the investment memo text. This UI is ready to display it.</p></div>
      <div className="workspace-card"><div className="eyebrow">Safety</div><h3>Explicit only</h3><p>No automatic files are created from the Analyze action.</p></div>
    </div>
  </>;
}