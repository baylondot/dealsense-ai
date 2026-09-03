import { mockAnalysis } from "@/lib/mock";

export default function NewsPage() {
  return <>
    <div className="app-header"><div><div className="eyebrow">News Intelligence</div><h1 className="app-title">Recent events, investment context</h1><div className="muted">Structured news with source, event type, impact and confidence.</div></div></div>
    <div className="workspace">
      <div className="news-list">{mockAnalysis.news?.map((n,i)=><div className="news-item" key={i}><div><div className="news-date">{n.published_date}</div><div className="news-source">{n.source}</div></div><div><h4>{n.title}</h4><p>{n.summary}</p></div><div className={n.investment_impact==="positive"?"good":n.investment_impact==="negative"?"bad":"warn"}>{n.investment_impact}</div></div>)}</div>
      <div className="status">Mock record for interface development. The existing News Intelligence backend is the source of truth for live data.</div>
    </div>
  </>;
}