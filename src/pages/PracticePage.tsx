import {useMemo,useState} from 'react';
import {Exercise} from '../components/Exercise';
import {lessons} from '../content';
import {missed} from '../lib/progress';
import {useProgress} from '../lib/store';

export function PracticePage(){
 const {progress}=useProgress();const [course,setCourse]=useState('linear-algebra');const [topic,setTopic]=useState('systems');const [level,setLevel]=useState('all');const [review,setReview]=useState(false);
 const topics=lessons.filter(l=>l.courseId===course);
 const exercises=useMemo(()=>{const missedIds=new Set(missed(progress).map(e=>e.id));return lessons.filter(l=>l.id===topic).flatMap(l=>l.exercises).filter(e=>(level==='all'||String(e.difficulty)===level)&&(!review||missedIds.has(e.id)));},[topic,level,review,progress]);
 const chooseCourse=(next:string)=>{setCourse(next);setTopic(lessons.find(l=>l.courseId===next)?.id??'');};
 return <section className="page container"><span className="eyebrow orange">Practice center</span><h1>Build skill through purposeful attempts.</h1><p className="lead">Choose a topic and difficulty, or focus only on questions your latest attempt missed. Every topic contains at least ten exercises with progressive hints and a hidden solution.</p><div className="filter-bar"><label>Course<select value={course} onChange={e=>chooseCourse(e.target.value)}><option value="linear-algebra">Linear Algebra</option><option value="differential-equations">Differential Equations</option></select></label><label>Topic<select value={topic} onChange={e=>setTopic(e.target.value)}>{topics.map(l=><option key={l.id} value={l.id}>{l.section} · {l.title}</option>)}</select></label><label>Difficulty<select value={level} onChange={e=>setLevel(e.target.value)}><option value="all">All levels</option><option value="1">Beginner</option><option value="2">Intermediate</option><option value="3">Challenge</option></select></label><label className="choice"><input type="checkbox" checked={review} onChange={e=>setReview(e.target.checked)}/>Review missed only</label></div><p>{exercises.length} practice problem{exercises.length===1?'':'s'} in this selection</p><div className="practice-stack">{exercises.map(e=><Exercise key={e.id} exercise={e}/>)}{exercises.length===0&&<div className="empty"><h2>No missed problems in this selection.</h2><p>Complete more practice or turn off “Review missed only.”</p></div>}</div></section>;
}
