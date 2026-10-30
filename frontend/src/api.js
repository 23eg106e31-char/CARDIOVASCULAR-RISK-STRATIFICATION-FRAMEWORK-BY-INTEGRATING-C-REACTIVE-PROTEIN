import axios from 'axios';
const API_BASE=import.meta.env.VITE_API_BASE_URL||'/api';
export async function assessRisk(patient){const r=await axios.post(`${API_BASE}/risk/assess`,patient);return r.data;}
export async function fetchHistory(){const r=await axios.get(`${API_BASE}/risk/history`);return r.data;}
