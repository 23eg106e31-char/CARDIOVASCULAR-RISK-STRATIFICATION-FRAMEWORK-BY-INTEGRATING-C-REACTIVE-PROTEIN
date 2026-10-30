import React,{useState} from 'react';
const FIELDS=[
['age','Age (years)','number','1'],['sex','Sex','select',[{v:0,l:'Female'},{v:1,l:'Male'}]],['bmi','BMI (kg/m²)','number','0.1'],
['systolicBp','Systolic BP (mmHg)','number','1'],['diastolicBp','Diastolic BP (mmHg)','number','1'],
['totalCholesterol','Total cholesterol (mg/dL)','number','1'],['hdlCholesterol','HDL cholesterol (mg/dL)','number','1'],
['ldlCholesterol','LDL cholesterol (mg/dL)','number','1'],['triglycerides','Triglycerides (mg/dL)','number','1'],
['fastingGlucose','Glucose (mg/dL)','number','1'],['hba1c','HbA1c (%)','number','0.1'],['crp','hs-CRP (mg/L)','number','0.1'],
['smoker','Current smoker','select',[{v:0,l:'No'},{v:1,l:'Yes'}]],['diabetes','Diabetes','select',[{v:0,l:'No'},{v:1,l:'Yes'}]]
];
const DEFAULTS={age:55,sex:1,bmi:27.5,systolicBp:130,diastolicBp:82,totalCholesterol:200,hdlCholesterol:45,ldlCholesterol:130,triglycerides:150,fastingGlucose:95,hba1c:5.6,crp:2.1,smoker:0,diabetes:0};
export default function PatientForm({onSubmit,loading}){const [v,setV]=useState(DEFAULTS);const change=(name,type)=>(e)=>setV(p=>({...p,[name]:type==='select'?Number(e.target.value):e.target.value===''?'':Number(e.target.value)}));return <form className="patient-form" onSubmit={e=>{e.preventDefault();onSubmit(v)}}><div className="form-head"><div><h2>Patient Clinical Profile</h2><p>Enter the clinical values used by the connected TabPFN cardiovascular risk model.</p></div><span className="model-chip">14 inputs</span></div><div className="form-grid">{FIELDS.map(([name,label,type,step])=><label className="form-field" key={name}><span>{label}</span>{type==='select'?<select value={v[name]} onChange={change(name,'select')}>{step.map(o=><option value={o.v} key={o.v}>{o.l}</option>)}</select>:<input type="number" step={step} value={v[name]} onChange={change(name,'number')} required/>}</label>)}</div><button className="submit-btn" disabled={loading}>{loading?<><span className="spinner"/> Scoring with TabNet…</>:'Assess cardiovascular risk'}</button></form>}
