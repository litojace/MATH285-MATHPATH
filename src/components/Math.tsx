import katex from 'katex';
import {useLayoutEffect,useMemo,useRef,useState} from 'react';
import type {Step} from '../types/content';
import {expandWideMath,verticalMath,type MathExpansion} from '../lib/math-layout';

function MathLine({math,depth=0}:{math:string;depth?:number}){
 const ref=useRef<HTMLDivElement>(null);const [expansion,setExpansion]=useState<MathExpansion|null>(null);
 const rendered=useMemo(()=>katex.renderToString(math,{throwOnError:false,trust:false,strict:'error',displayMode:true,output:'htmlAndMathml'}),[math]);
 useLayoutEffect(()=>{
  if(expansion||depth>8)return;
  let active=true;
  const measure=()=>{const el=ref.current;if(active&&el&&el.clientWidth&&el.scrollWidth>el.clientWidth+1)setExpansion(expandWideMath(math,depth+1));};
  measure();
  // KaTeX font loading can change ink width without resizing its wrapper.
  void document.fonts?.ready.then(measure);
  document.fonts?.addEventListener('loadingdone',measure);
  const observer=typeof ResizeObserver!=='undefined'?new ResizeObserver(measure):null;
  if(ref.current)observer?.observe(ref.current);
  return ()=>{active=false;observer?.disconnect();document.fonts?.removeEventListener('loadingdone',measure);};
 },[math,expansion,depth]);
 return <div ref={ref} className="math-line">{expansion?<>
  {expansion.lines.map((line,i)=><MathLine key={`${i}-${line}`} math={line} depth={depth+1}/>)}
  {expansion.definitions?.map(definition=><div className="math-definition" key={definition.label}><p>{definition.label}</p>{definition.lines.map((line,i)=><MathLine key={`${i}-${line}`} math={line} depth={depth+1}/>)}</div>)}
 </>:<div className="math-render" data-math={math} dangerouslySetInnerHTML={{__html:rendered}}/>}</div>;
}
export function MathBlock({math}:{math:string}){return <div className="math-block">{verticalMath(math).map((line,i)=><MathLine key={`${i}-${line}`} math={line}/>)}</div>;}
export function Steps({steps}:{steps:Step[]}){return <ol className="steps">{steps.map((s,i)=><li key={i}><div className="step-number">{i+1}</div><div><p>{s.text}</p>{s.math&&<MathBlock math={s.math}/>}</div></li>)}</ol>;}
