import {useState} from 'react';
import {Lightbulb,CheckCircle2} from 'lucide-react';
import type {Exercise as ExerciseType} from '../types/content';
import {MathBlock,Steps} from './Math';
import {checkAnswer} from '../lib/math';
import {useProgress} from '../lib/store';
export function Exercise({exercise:e}:{exercise:ExerciseType}){
 const {progress,update}=useProgress();const [input,setInput]=useState('');const [hints,setHints]=useState(0);const [open,setOpen]=useState(false);const [message,setMessage]=useState('');const [correct,setCorrect]=useState<boolean|null>(null);
 const record=(value:boolean)=>update(p=>({...p,attempts:[...p.attempts,{exerciseId:e.id,correct:value,at:new Date().toISOString(),hinted:hints>0,solutionViewed:open||p.solutions.includes(e.id)}]}));
 function submit(event:React.FormEvent){event.preventDefault();if(!input.trim()){setMessage('Enter an answer first.');setCorrect(null);return;}const result=checkAnswer(e,input);setMessage(result.message);setCorrect(result.correct);if(result.correct!==null)record(result.correct);}
 return <article className="exercise card"><div className="row spread"><span className="eyebrow orange">{['','Beginner','Intermediate','Challenge'][e.difficulty]} practice</span>{progress.attempts.some(a=>a.exerciseId===e.id&&a.correct)&&<CheckCircle2 size={18} aria-label="Previously answered correctly"/>}</div><h3>{e.prompt}</h3><MathBlock math={e.math}/>
 {e.answerType!=='self-check'?<form onSubmit={submit}><label htmlFor={e.id}>Your answer{e.answerType==='matrix'?' (commas between entries; semicolons between rows)':''}</label>{e.answerType==='multiple-choice'?<fieldset><legend className="sr-only">Choose an answer</legend>{e.choices?.map(c=><label className="choice" key={c}><input type="radio" name={e.id} value={c} checked={input===c} onChange={()=>setInput(c)}/>{c}</label>)}</fieldset>:<input id={e.id} value={input} onChange={ev=>setInput(ev.target.value)} autoComplete="off" placeholder={e.answerType==='matrix'?'2; 3':'A number or fraction'}/>}<button className="button primary" type="submit">Check answer</button></form>:<p>Explain your reasoning on paper, then use the solution to self-assess. Automatic checking is unavailable for this problem.</p>}
 {message&&<p role="status" className={correct?'feedback success':'feedback'}>{message}</p>}
 <div className="row wrap"><button className="button subtle" disabled={hints===e.hints.length} onClick={()=>{setHints(n=>n+1);update(p=>({...p,hints:{...p.hints,[e.id]:(p.hints[e.id]??0)+1}}));}}><Lightbulb size={16}/>{hints===e.hints.length?'All hints shown':`Hint ${hints+1} of ${e.hints.length}`}</button><button className="button subtle" aria-expanded={open} aria-controls={`${e.id}-solution`} onClick={()=>{setOpen(v=>!v);if(!open)update(p=>({...p,solutions:[...new Set([...p.solutions,e.id])]}));}}>{open?'Hide Step-by-Step Solution':'Show Step-by-Step Solution'}</button></div>
 {hints>0&&<div className="hint"><Steps steps={e.hints.slice(0,hints)}/></div>}{open&&<div id={`${e.id}-solution`} className="solution"><h4>Work through the solution</h4><Steps steps={e.solutionSteps}/>{e.answerType==='self-check'&&<div className="row"><button onClick={()=>{record(true);setMessage('Self-assessment recorded.');}}>My reasoning matches</button><button onClick={()=>{record(false);setMessage('Added to review.');}}>I need more practice</button></div>}</div>}
 </article>;
}
