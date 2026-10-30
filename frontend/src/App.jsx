import React,{useEffect,useState} from 'react';
import PatientForm from './components/PatientForm.jsx';
import RiskResult from './components/RiskResult.jsx';
import HistoryTable from './components/HistoryTable.jsx';
import {assessRisk,fetchHistory} from './api.js';

function HeartVisual(){
  return <div className="hero-visual" aria-hidden="true">
    <div className="pulse-line"><span></span></div>
    <div className="orbit orbit-one"></div><div className="orbit orbit-two"></div>
    <div className="heart-glow"></div>
    <div className="heart-symbol">♥</div>
    <div className="medical-orb orb-heart">♡</div>
    <div className="medical-orb orb-stetho">♧</div>
    <div className="medical-orb orb-chart">▥</div>
    <div className="medical-orb orb-drop">◉</div>
  </div>
}

export default function App(){
  const [result,setResult]=useState(null),[loading,setLoading]=useState(false),[error,setError]=useState(null),[history,setHistory]=useState([]),[page,setPage]=useState('home');
  const load=async()=>{try{setHistory(await fetchHistory())}catch(e){console.error(e)}};
  useEffect(()=>{if(page==='history')load()},[page]);
  const submit=async p=>{setLoading(true);setError(null);setResult(null);try{const data=await assessRisk(p);setResult(data);load()}catch(e){setError(e.response?.data?.message||e.response?.data?.error||e.response?.data?.detail||'Could not connect to the backend / ML service.')}finally{setLoading(false)}};
  const goRisk=()=>{setPage('risk');window.scrollTo({top:0,behavior:'smooth'})};
  return <div className="app">
    <header className="site-header">
      <button className="brand" onClick={()=>setPage('home')} aria-label="CV RiskAI home">
        <div className="brand-mark"><span>♥</span><i></i></div>
        <div><div className="brand-name">CV Risk<span>AI</span></div><div className="brand-sub">Cardiovascular Risk Assessment</div></div>
      </button>
      <nav className="main-nav">
        <button className={page==='home'?'active':''} onClick={()=>setPage('home')}>Home</button>
        <button className={page==='risk'?'active':''} onClick={goRisk}>Risk Analysis</button>
        <button className={page==='history'?'active':''} onClick={()=>setPage('history')}>History</button>
      </nav>
      <div className="portal"><span>●</span> Patient Portal</div>
    </header>

    {page==='home' && <main className="home-page">
      <section className="hero-home">
        <div className="hero-content">
          <p className="eyebrow">CARDIOVASCULAR HEALTH • AI-ASSISTED ASSESSMENT</p>
          <h1>Cardiovascular<br/><em>Risk Assessment</em></h1>
          <p className="hero-copy">A research-focused platform that combines clinical biomarkers, CRP information and a TabPFN machine-learning model to support cardiovascular risk assessment.</p>
          <button className="primary-cta" onClick={goRisk}>Start Risk Analysis <span>→</span></button>
          <div className="hero-points"><span>✓ Clinical biomarkers</span><span>✓ TabPFN model</span><span>✓ CRP analysis</span></div>
        </div>
        <HeartVisual/>
      </section>

      <section className="risk-intro">
        <div className="intro-copy">
          <p className="section-kicker">CARDIOVASCULAR RISK</p>
          <p><strong>Cardiovascular risk represents the likelihood of an individual developing a heart attack, stroke, heart failure, or other forms of vascular disease.</strong></p>
          <p>Up to 80% of all premature cardiovascular disease (CVD) events are preventable. Clinical guidelines from organizations like the American Heart Association emphasize evaluating these risks through a combination of lifestyle choices, clinical biometrics, and advanced medical calculators.</p>
        </div>
        <div className="risk-note"><div className="note-icon">♥</div><div><strong>Early risk awareness</strong><p>Understanding the factors that influence cardiovascular health can help support earlier prevention and informed clinical conversations.</p></div></div>
      </section>

      <section className="factor-section">
        <div className="factor-heading"><p className="section-kicker">RISK FACTORS</p><p>Medical professionals separate risk factors into two primary categories to determine where lifestyle interventions or medications can have the most impact.</p></div>
        <div className="factor-grid">
          <article className="factor-card modifiable"><div className="factor-card-head"><span className="factor-icon">✚</span><div><h2>Modifiable Risk Factors</h2><small>(Factors You Can Control)</small></div></div>
            <ul>
              <li><b>High Blood Pressure (Hypertension)</b><span>Puts continuous physical strain on the arteries, accelerating arterial stiffening and plaque buildup.</span></li>
              <li><b>Dyslipidemia (Abnormal Cholesterol)</b><span>High levels of LDL-C, triglycerides, and Lipoprotein(a) accumulate inside artery walls, narrowing blood vessels (atherosclerosis).</span></li>
              <li><b>Hyperglycemia &amp; Diabetes</b><span>High blood sugar progressively damages blood vessels and elevates cardiac risk, regardless of other health factors.</span></li>
              <li><b>Lifestyle Behaviors</b><span>Tobacco use (including vaping), lack of regular physical activity, chronic stress, poor sleep quality, and a diet high in processed fats and sodium.</span></li>
              <li><b>Obesity</b><span>Excess weight increases the body's baseline workload and typically worsens metabolic markers like blood pressure and insulin resistance.</span></li>
            </ul>
          </article>
          <article className="factor-card nonmodifiable"><div className="factor-card-head"><span className="factor-icon">⌁</span><div><h2>Non-Modifiable Risk Factors</h2><small>(Factors You Cannot Control)</small></div></div>
            <ul>
              <li><b>Age</b><span>Advanced age remains a profound baseline driver of declining cardiovascular health.</span></li>
              <li><b>Biological Sex</b><span>Men often experience an earlier clinical onset of CVD, while women see an accelerated rise in risk after menopause.</span></li>
              <li><b>Genetics and Family History</b><span>Inherited genetic predispositions can shift baseline vulnerability toward high cholesterol or early heart attacks.</span></li>
            </ul>
            <div className="factor-bottom">The earlier risk is identified, the more opportunity there is to focus on prevention.</div>
          </article>
        </div>
      </section>
      <section className="home-cta"><div><p className="section-kicker">READY TO ASSESS?</p><h2>Run a cardiovascular risk analysis</h2><p>Enter the available patient biomarkers and let the connected TabPFN  pipeline generate the research assessment.</p></div><button className="primary-cta" onClick={goRisk}>Open Risk Analysis <span>→</span></button></section>
    </main>}

    {page==='risk' && <main className="risk-page">
      <section className="page-title"><div><p className="section-kicker">CLINICAL ASSESSMENT</p><h1>Risk Analysis</h1><p>Enter the patient profile below. The connected TabPFN model will calculate the prediction and display CRP-based risk interpretation.</p></div><div className="model-status"><span></span> TabPFN pipeline</div></section>
      <div className="risk-layout"><PatientForm onSubmit={submit} loading={loading}/><div className="result-panel">{error&&<div className="error-box"><strong>Assessment failed</strong><span>{typeof error==='string'?error:JSON.stringify(error)}</span></div>}{loading&&<div className="loading-box"><span className="spinner"/> Running TabPnf inference and CRP stratification…</div>}{!loading&&!error&&<RiskResult result={result}/>}</div></div>
    </main>}

    {page==='history' && <main className="history-page"><section className="page-title"><div><p className="section-kicker">ASSESSMENT RECORDS</p><h1>History</h1><p>Review previously completed cardiovascular risk assessments.</p></div></section><HistoryTable history={history}/></main>}
    <footer><div className="footer-brand"><span>♥</span><b>CV RiskAI</b></div><p>For research and educational purposes only. This tool is not a substitute for professional medical advice, diagnosis or treatment.</p></footer>
  </div>
}
