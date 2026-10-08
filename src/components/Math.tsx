import katex from 'katex';
import {useMemo} from 'react';
import type {Step} from '../types/content';
export function MathBlock({math}:{math:string}){const rendered=useMemo(()=>katex.renderToString(math,{throwOnError:false,trust:false,strict:'error',displayMode:true,output:'htmlAndMathml'}),[math]);return <div className="math-block" dangerouslySetInnerHTML={{__html:rendered}}/>;}
export function Steps({steps}:{steps:Step[]}){return <ol className="steps">{steps.map((s,i)=><li key={i}><div className="step-number">{i+1}</div><div><p>{s.text}</p>{s.math&&<MathBlock math={s.math}/>}</div></li>)}</ol>;}
