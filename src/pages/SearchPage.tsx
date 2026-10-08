import {useDeferredValue,useEffect,useState} from 'react';
import {Link,useSearchParams} from 'react-router-dom';
import {ArrowRight,Search,Sparkles} from 'lucide-react';
import {searchLessons} from '../lib/search';
import {Highlight} from '../components/Search';

export function SearchPage(){
 const [params,setParams]=useSearchParams();
 const query=params.get('q')??'';
 const [value,setValue]=useState(query);
 const liveQuery=useDeferredValue(value.trim());
 const results=searchLessons(liveQuery);
 useEffect(()=>setValue(query),[query]);
 const searching=value.trim()!==liveQuery;
 return <section className="page container search-page">
  <span className="eyebrow blue">Topic discovery</span>
  <h1>Find the idea behind the problem.</h1>
  <p className="lead">Start typing and the lesson library filters instantly. Search by topic, abbreviation, formula, prerequisite, or a recognizable equation.</p>
  <form className="page-search" onSubmit={e=>{e.preventDefault();setParams(liveQuery?{q:liveQuery}:{});}}>
   <Search/><label className="sr-only" htmlFor="full-search">Search all lesson content</label>
   <input id="full-search" name="q" value={value} onChange={e=>setValue(e.target.value)} placeholder="Try ‘eigen’, ‘RREF’, or ‘dy/dx + 2y = 6’" autoComplete="off"/>
   <button className="button primary" type="submit">Search</button>
  </form>
  <div className="live-search-status" role="status" aria-live="polite">
   <span>{searching?'Updating results…':liveQuery?`${results.length} matching lesson${results.length===1?'':'s'}`:'Featured lessons — type to filter instantly'}</span>
   {liveQuery&&<button type="button" onClick={()=>{setValue('');setParams({});}}>Clear search</button>}
  </div>
  <div className="search-results">{results.map(({lesson,reason},index)=><Link to={`/lessons/${lesson.id}`} className="search-result" key={lesson.id}>
   <div className="search-result-index">{String(index+1).padStart(2,'0')}</div>
   <div><div className="row wrap"><span className="eyebrow">{lesson.courseId==='linear-algebra'?'Linear Algebra':'Differential Equations'}</span><span className="difficulty">{lesson.difficulty}</span></div><h2><Highlight text={lesson.title} query={liveQuery}/></h2><p><Highlight text={lesson.description} query={liveQuery}/></p><small>{reason}</small></div>
   <ArrowRight className="search-result-arrow"/>
  </Link>)}{liveQuery&&results.length===0&&<div className="empty"><Sparkles/><h2>No indexed lesson matches yet.</h2><p>Try a shorter topic name, a related concept, or a standard abbreviation. MathPath does not invent results for content that has not been written and checked.</p></div>}</div>
 </section>;
}
