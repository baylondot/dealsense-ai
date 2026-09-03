export default function MarketingNav() {
  return (
    <nav className="nav">
      <div className="container nav-inner">
        <a href="/" className="brand"><span className="brand-mark" />DealSense</a>
        <div className="nav-links">
          <a href="#intelligence">Intelligence</a>
          <a href="#workflow">Workflow</a>
          <a href="#platform">Platform</a>
        </div>
        <div className="nav-actions">
          <a className="btn" href="/app">Open workspace</a>
        </div>
      </div>
    </nav>
  );
}