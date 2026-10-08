import {useEffect,useId,useRef,useState} from 'react';
import {useNavigate,Link,useLocation} from 'react-router-dom';
import {Search as SearchIcon,ArrowUpRight,ArrowRight,X} from 'lucide-react';
import {searchLessons} from '../lib/search';
type SearchBoxProps={large?:boolean;variant?:'compact'|'page';value?:string;onQueryChange?:(query:string)=>void;onSearch?:(query:string)=>void};
export function SearchBox({large=false,variant='compact',value,onQueryChange,onSearch}:SearchBoxProps){
 const [internalQuery,setInternalQuery]=useState('');const [open,setOpen]=useState(false);const [active,setActive]=useState(-1);
 const [placement,setPlacement]=useState({above:false,height:340});
 const query=value??internalQuery;const navigate=useNavigate();const location=useLocation();const id=useId();
 const wrapper=useRef<HTMLDivElement>(null);const input=useRef<HTMLInputElement>(null);const list=useRef<HTMLDivElement>(null);
 const matches=query.trim()?searchLessons(query):[];const visible=open&&Boolean(query.trim());const page=variant==='page';
 const change=(next:string)=>{if(value===undefined)setInternalQuery(next);onQueryChange?.(next);setActive(-1);setOpen(true);};
 const close=()=>{setOpen(false);setActive(-1);};
 useEffect(()=>{close();},[location.key]);
 useEffect(()=>{const outside=(event:PointerEvent)=>{if(!wrapper.current?.contains(event.target as Node))close();};document.addEventListener('pointerdown',outside);return ()=>document.removeEventListener('pointerdown',outside);},[]);
 useEffect(()=>{
  if(!visible)return;
  const position=()=>{const rect=wrapper.current?.getBoundingClientRect();if(!rect)return;const below=window.innerHeight-rect.bottom-12;const above=below<260&&rect.top>below;setPlacement({above,height:Math.max(100,Math.min(340,(above?rect.top-12:below)-90))});};
  position();window.addEventListener('resize',position);window.addEventListener('scroll',position,true);
  return ()=>{window.removeEventListener('resize',position);window.removeEventListener('scroll',position,true);};
 },[visible]);
 useEffect(()=>{if(visible&&active>=0)list.current?.querySelector(`[data-index="${active}"]`)?.scrollIntoView?.({block:'nearest'});},[active,visible]);
 const submit=()=>{const clean=query.trim();close();if(onSearch)onSearch(clean);else navigate(clean?`/search?q=${encodeURIComponent(clean)}`:'/search');};
 return <div ref={wrapper} className={`search-wrap ${large?'large':''} ${page?'page-search-wrap':''}`} onBlur={e=>{if(e.relatedTarget&&!e.currentTarget.contains(e.relatedTarget))close();}}>
  <form className={page?'page-search':'search-box'} role="search" onSubmit={e=>{e.preventDefault();submit();}}>
   <SearchIcon size={large||page?23:18} aria-hidden="true"/>
   <label className="sr-only" htmlFor={`${id}-input`}>{page?'Search all lesson content':'Search topics, formulas, or equations'}</label>
   <input ref={input} id={`${id}-input`} role="combobox" aria-autocomplete="list" aria-haspopup="listbox" aria-expanded={visible} aria-controls={visible?`${id}-list`:undefined} aria-activedescendant={visible&&active>=0?`${id}-option-${active}`:undefined}
    value={query} onFocus={()=>setOpen(true)} onChange={e=>change(e.target.value)} onKeyDown={e=>{
     if(e.key==='Escape'){e.preventDefault();close();}
     if((e.key==='ArrowDown'||e.key==='ArrowUp')&&matches.length){e.preventDefault();setOpen(true);setActive(index=>e.key==='ArrowDown'?Math.min(index+1,matches.length-1):index<0?matches.length-1:Math.max(index-1,0));}
     if(e.key==='Enter'&&visible&&active>=0&&matches[active]){e.preventDefault();navigate(`/lessons/${matches[active].lesson.id}`);close();}
    }} placeholder={page?'Topic, formula, or equation':'Search lessons…'} autoComplete="off"/>
   {query&&<button className="search-clear" type="button" aria-label="Clear search input" onClick={()=>{change('');input.current?.focus();}}><X size={17}/></button>}
   <button className={page?'button primary':'search-submit'} aria-label="Search lessons" title="Search" type="submit">{page?'Search':<ArrowUpRight size={20}/>}</button>
  </form>
  {visible&&<div className={`suggestions ${placement.above?'above':''}`}>
   <div className="suggestions-heading"><span>Lesson suggestions</span><span role="status" aria-live="polite">{matches.length} match{matches.length===1?'':'es'}</span></div>
   <div ref={list} className="suggestions-list" style={{maxHeight:placement.height}} id={`${id}-list`} role="listbox" aria-label="Search suggestions">
    {matches.map(({lesson},index)=><Link id={`${id}-option-${index}`} data-index={index} role="option" aria-label={`${lesson.title}, ${lesson.courseId==='linear-algebra'?'Linear Algebra':'Differential Equations'}, Section ${lesson.section}`} aria-selected={active===index} tabIndex={-1} key={lesson.id} to={`/lessons/${lesson.id}`}
     className={`suggestion ${active===index?'active':''}`} onMouseDown={e=>{if(e.button===0)e.preventDefault();}} onClick={close}>
     <span className="suggestion-content"><strong><Highlight text={lesson.title} query={query}/></strong><small>{lesson.courseId==='linear-algebra'?'Linear Algebra':'Differential Equations'} <span aria-hidden="true">·</span> Section {lesson.section}</small></span><ArrowUpRight size={17} aria-hidden="true"/>
    </Link>)}
   </div>
   {matches.length===0&&<p className="suggestions-empty">No lessons match. Try another topic or a shorter search.</p>}
   <Link className="suggestions-footer" to={`/search?q=${encodeURIComponent(query.trim())}`} onClick={close}>See all results <ArrowRight size={16} aria-hidden="true"/></Link>
  </div>}
 </div>;
}
export function Highlight({text,query}:{text:string,query:string}){const token=query.trim();const index=text.toLowerCase().indexOf(token.toLowerCase());if(!token||index<0)return <>{text}</>;return <>{text.slice(0,index)}<mark>{text.slice(index,index+token.length)}</mark>{text.slice(index+token.length)}</>;}
