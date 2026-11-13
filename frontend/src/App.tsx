import { useState } from 'react'
import { Activity, BookOpen, BrainCircuit, ChevronRight, FileSearch, FlaskConical, ShieldCheck } from 'lucide-react'

const stages = ['Research planning', 'Literature discovery', 'Evidence extraction', 'Comparative analysis', 'Critical review', 'Synthesis & reporting']

export default function App() {
  const [question, setQuestion] = useState('How does reflux ratio affect energy consumption and separation efficiency in distillation columns?')
  const [domain, setDomain] = useState('engineering')
  const [status, setStatus] = useState('Ready to start an investigation')
  const [plan, setPlan] = useState<string[]>([])
  const [busy, setBusy] = useState(false)

  async function startResearch() {
    setBusy(true); setStatus('Creating research plan…'); setPlan([])
    try {
      const response = await fetch('/api/v1/research/runs', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question, domain, project_id: 'local-demo', memory_scope: 'project', autonomy: 'hybrid' }),
      })
      if (!response.ok) throw new Error(`API returned ${response.status}`)
      const data = await response.json()
      setPlan(data.research_plan)
      setStatus(`${data.status.replaceAll('_', ' ')} · ${data.notice}`)
    } catch (error) { setStatus(error instanceof Error ? error.message : 'Unable to reach the API') }
    finally { setBusy(false) }
  }

  return <main className="shell">
    <aside className="sidebar">
      <div className="brand"><div className="brand-mark"><BrainCircuit size={22}/></div><div><strong>RIP</strong><small>Research Intelligence</small></div></div>
      <div className="nav-label">WORKSPACE</div>
      <div className="nav-item active"><Activity size={17}/> Research studio</div>
      <div className="nav-item"><BookOpen size={17}/> Knowledge library</div>
      <div className="nav-item"><FileSearch size={17}/> Evidence explorer</div>
      <div className="sidebar-bottom"><ShieldCheck size={16}/><span>Human-supervised research</span></div>
    </aside>
    <section className="content">
      <header><div><div className="eyebrow">RESEARCH WORKSPACE / NEW INVESTIGATION</div><h1>What are we investigating?</h1><p>Define the question. The research engine will help plan the investigation.</p></div><span className="mode-pill">HYBRID MODE</span></header>
      <section className="composer card">
        <label htmlFor="question">Research question</label>
        <textarea id="question" value={question} onChange={e => setQuestion(e.target.value)} rows={4}/>
        <div className="composer-footer"><div><label htmlFor="domain">Research domain</label><select id="domain" value={domain} onChange={e => setDomain(e.target.value)}><option value="general">General</option><option value="medical">Medical & biomedical</option><option value="engineering">Engineering</option><option value="science">Science</option><option value="ai">AI & technology</option><option value="business">Business & economics</option></select></div><button onClick={startResearch} disabled={busy || question.trim().length < 12}>{busy ? 'Planning…' : 'Create research plan'} <ChevronRight size={17}/></button></div>
      </section>
      <div className="section-heading"><div><div className="eyebrow">CONTROLLED WORKFLOW</div><h2>Research lifecycle</h2></div><span className="muted">Human approval at key stages</span></div>
      <section className="stage-grid">{stages.map((stage, i) => <div className="stage card" key={stage}><span className="stage-number">0{i + 1}</span><strong>{stage}</strong><span className="stage-state">{i === 0 ? 'Ready' : 'Pending'}</span></div>)}</section>
      <section className="result card"><div className="result-title"><FlaskConical size={18}/><strong>Investigation activity</strong></div><p>{status}</p>{plan.length > 0 && <ol>{plan.map(item => <li key={item}>{item}</li>)}</ol>}<div className="notice">Prototype status: literature search, evidence extraction and report generation are not connected yet. This workspace will not invent sources or findings.</div></section>
      <footer>Research Intelligence Platform <span>·</span> MVP foundation <span>·</span> v0.1.0</footer>
    </section>
  </main>
}
