import MarketingNav from "./MarketingNav";
import Reveal from "./Reveal";

const features = [
  ["01", "Company Intelligence", "Turn a company URL into structured business, market, product and investment intelligence."],
  ["02", "Evidence Intelligence", "Trace important conclusions back to sources, quotes and confidence instead of reading an unsupported summary."],
  ["03", "News Intelligence", "Surface recent events and classify their potential investment impact with source-aware context."],
  ["04", "Company Comparison", "Compare existing company intelligence side-by-side without rebuilding the underlying research."],
  ["05", "Investment Assessment", "Bring signals, risks, SWOT and deterministic acquisition scoring into one decision surface."],
  ["06", "Reports & Memos", "Move from analysis to an investment memo or explicitly requested PDF report."],
];

export default function MarketingPage() {
  return (
    <div className="page-shell">
      <MarketingNav />

      <main>
        <section className="hero">
          <div className="container">
            <Reveal>
              <div className="eyebrow" style={{textAlign:"center"}}>AI-native due diligence</div>
              <h1>See the deal before you spend the days finding it.</h1>
              <p>
                DealSense turns company research into structured investment intelligence—
                from the first URL to evidence, risks, competitors, news and acquisition assessment.
              </p>
              <div className="hero-actions">
                <a className="btn btn-primary" href="/app/analyze">Analyze a company →</a>
                <a className="btn" href="#workflow">Explore the platform</a>
              </div>

              <div className="hero-console">
                <div className="console-top"><i className="dot"/><i className="dot"/><i className="dot"/><span style={{marginLeft:8,color:"#697384",fontSize:11}}>DealSense / analysis</span></div>
                <div className="console-body">
                  <div className="console-input">
                    <div className="console-label">Company target</div>
                    <div className="fake-input">https://company.com</div>
                    <div style={{marginTop:28,color:"#717b8b",fontSize:12}}>Research → evidence → analysis → investment view</div>
                  </div>
                  <div className="console-results">
                    <div className="console-label">Acquisition assessment</div>
                    <div className="score-ring"><span className="score-number">76</span></div>
                    <div style={{fontWeight:700}}>Attractive candidate</div>
                    <div style={{color:"#737d8d",fontSize:12,marginTop:6}}>Signals, risks and source-backed findings unified.</div>
                  </div>
                </div>
              </div>
            </Reveal>
          </div>
        </section>

        <section className="section" id="intelligence">
          <div className="container">
            <Reveal>
              <div className="section-head">
                <div className="eyebrow">01 — Intelligence</div>
                <h2>From raw company information to a decision surface.</h2>
                <p className="lead">The product is designed around the way investment professionals actually investigate a target: gather, verify, structure, compare, then decide.</p>
              </div>
            </Reveal>
            <div className="story">
              <Reveal>
                <div className="sticky">
                  <div className="product-frame">
                    <div className="product-top"><span>DealSense intelligence</span><span>Live workspace</span></div>
                    <div className="mock-grid">
                      <div className="metric"><small>Acquisition score</small><b>76</b></div>
                      <div className="metric"><small>Confidence</small><b>82%</b></div>
                      <div className="metric metric-wide"><small>Investment signals</small><div className="tags" style={{marginTop:14}}><span className="tag">SaaS</span><span className="tag">B2B</span><span className="tag">Recurring</span><span className="tag">Enterprise</span></div></div>
                      <div className="metric metric-wide"><small>Signal profile</small><div className="mini-bars">{[42,70,56,82,65,91,73].map((h,i)=><i key={i} style={{height:`${h}%`}} />)}</div></div>
                    </div>
                  </div>
                </div>
              </Reveal>
              <div className="steps">
                {[
                  ["Research", "Collect website context and external company information through the existing backend pipeline."],
                  ["Structure", "Normalize findings into typed company intelligence instead of leaving analysts with raw text."],
                  ["Verify", "Expose evidence, source information and confidence alongside important conclusions."],
                  ["Assess", "Combine risks, signals, SWOT, news and deterministic acquisition scoring."],
                  ["Compare", "Reuse existing analyses to answer which target is stronger and why."],
                ].map(([title,desc],i)=>(
                  <Reveal key={title}><div className="step"><strong>{String(i+1).padStart(2,"0")} / {title}</strong><span>{desc}</span></div></Reveal>
                ))}
              </div>
            </div>
          </div>
        </section>

        <section className="section" id="workflow">
          <div className="container">
            <Reveal>
              <div className="section-head">
                <div className="eyebrow">02 — Workflow</div>
                <h2>A research workflow that feels like software, not a spreadsheet.</h2>
                <p className="lead">Each surface has a clear job. The user should always know what was found, where it came from, and what action comes next.</p>
              </div>
            </Reveal>
            <div className="feature-grid">
              {features.map(([n,title,desc])=>(
                <Reveal key={n}><article className="feature"><div className="feature-icon">{n}</div><h3>{title}</h3><p>{desc}</p></article></Reveal>
              ))}
            </div>
          </div>
        </section>

        <section className="section" id="platform">
          <div className="container">
            <Reveal>
              <div className="section-head">
                <div className="eyebrow">03 — Platform</div>
                <h2>One system. Multiple investment workspaces.</h2>
                <p className="lead">The landing experience introduces the product; the application becomes a focused workboard for analysis, comparison, evidence, news, portfolio intelligence and reporting.</p>
              </div>
            </Reveal>
            <div className="story">
              <Reveal>
                <div className="product-frame">
                  <div className="product-top"><span>DealSense workspace</span><span>Investment intelligence</span></div>
                  <div className="steps">
                    <div className="step"><strong>Analyze</strong><span>Company intelligence, score, recommendation, risks and signals.</span></div>
                    <div className="step"><strong>Compare</strong><span>Side-by-side investment-relevant differences across existing analyses.</span></div>
                    <div className="step"><strong>Portfolio</strong><span>Aggregate company scores, risks, concentration and rankings.</span></div>
                  </div>
                </div>
              </Reveal>
              <Reveal>
                <div>
                  <div className="metric" style={{marginBottom:12}}><small>Architecture</small><b style={{fontSize:22}}>Frontend → FastAPI → Python</b><span className="muted" style={{display:"block",marginTop:8,fontSize:12}}>The frontend stays independent from backend intelligence and can use isolated mock data until each API is available.</span></div>
                  <div className="metric"><small>Design principle</small><b style={{fontSize:22}}>Evidence over decoration</b><span className="muted" style={{display:"block",marginTop:8,fontSize:12}}>Charts and motion are used to clarify investment information—not to make the interface look busy.</span></div>
                </div>
              </Reveal>
            </div>
          </div>
        </section>

        <section className="cta">
          <div className="container">
            <Reveal>
              <div className="eyebrow">DealSense AI</div>
              <h2>Move from research overload to investment clarity.</h2>
              <p>Start with a company URL. Enter the workspace when you are ready to investigate the deal.</p>
              <div className="hero-actions"><a className="btn btn-primary" href="/app/analyze">Open DealSense →</a></div>
            </Reveal>
          </div>
        </section>
      </main>

      <footer className="footer"><div className="container">DealSense AI · Investment intelligence infrastructure</div></footer>
    </div>
  );
}