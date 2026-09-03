import Link from "next/link";

const nav = [
  ["/app/analyze", "Analyze"],
  ["/app/compare", "Compare"],
  ["/app/evidence", "Evidence"],
  ["/app/news", "News Intelligence"],
  ["/app/portfolio", "Portfolio"],
  ["/app/reports", "Reports"],
  ["/app/memo", "Investment Memo"]
];

export default function AppShell({ children }: { children: React.ReactNode }) {
  return (
    <div className="app-shell">
      <div className="app-layout">
        <aside className="sidebar">
          <div className="sidebar-brand"><Link href="/" className="brand"><span className="brand-mark"/>DealSense</Link></div>
          <nav className="side-nav">
            {nav.map(([href,label]) => <Link key={href} href={href}>{label}</Link>)}
          </nav>
          <div style={{position:"absolute",bottom:25,left:24,right:24,color:"#596273",fontSize:11}}>
            Frontend model · API-ready
          </div>
        </aside>
        <main className="app-main">{children}</main>
      </div>
    </div>
  );
}