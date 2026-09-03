const evidence = [
  ["B2B positioning", "Company website", "The interface is prepared to show the actual source-backed claim returned by the backend.", 86],
  ["Recurring model", "Company research", "Evidence records can display source, quote and confidence together.", 79],
  ["Competitive pressure", "External research", "Use this surface for the existing evidence objects rather than a second evidence format.", 73]
];

export default function EvidencePage() {
  return <>
    <div className="app-header"><div><div className="eyebrow">Evidence</div><h1 className="app-title">Evidence intelligence</h1><div className="muted">A source-first view of why the platform believes important claims.</div></div></div>
    <div className="workspace">
      <div className="evidence">{evidence.map(([claim,source,quote,confidence])=><div className="evidence-item" key={claim}><strong>{claim}</strong><div style={{marginTop:7}}><small>{source} · confidence {confidence}%</small></div><p>“{quote}”</p><a href="#" className="muted" style={{fontSize:11}}>Open source →</a></div>)}</div>
      <div className="status">These are frontend demonstration records. Live evidence should come from the existing backend Evidence Engine through a future API endpoint.</div>
    </div>
  </>;
}