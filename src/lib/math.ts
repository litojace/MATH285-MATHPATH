import type {Exercise} from '../types/content';
export function parseNumber(input:string):number|null {
 const text=input.trim();
 if (!/^[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?(?:\s*\/\s*[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?)?$/.test(text)) return null;
 const parts=text.split('/').map(Number);
 const value=parts.length===2?parts[0]/parts[1]:parts[0];
 return Number.isFinite(value)?value:null;
}
export function near(a:number,b:number){return Math.abs(a-b)<=1e-8*Math.max(1,Math.abs(b));}
export function checkAnswer(e:Exercise,input:string):{correct:boolean|null,message:string}{
 if(e.answerType==='self-check')return {correct:null,message:'Compare your reasoning with the solution, then record your self-assessment.'};
 if(e.answerType==='multiple-choice')return {correct:input===e.answer,message:input===e.answer?'Correct. You found the right idea.':'Try again. Use a hint to check the underlying idea.'};
 if(e.answerType==='numeric'){
 const n=parseNumber(input); if(n===null)return {correct:null,message:'Enter a finite number or a fraction such as 3/4.'};
 const correct=near(n,e.answer as number);return {correct,message:correct?'Correct. Your calculation checks out.':'Not yet. Check the signs and each operation; a hint can help.'};
 }
 const rows=input.trim().split(';').map(row=>row.trim().split(/[\s,]+/).map(parseNumber));
 const target=e.answer as number[][];
 if(rows.length!==target.length||rows.some((r,i)=>r.length!==target[i].length||r.some(x=>x===null)))return {correct:null,message:`Enter ${target.length} rows with ${target[0].length} entries each. Separate entries with commas and rows with semicolons.`};
 const correct=rows.every((r,i)=>r.every((x,j)=>near(x!,target[i][j])));return {correct,message:correct?'Correct. Every entry matches.':'Not yet. Compare corresponding entries and check the row operations.'};
}
export const dot=(a:number[],b:number[])=>a.reduce((total,x,i)=>total+x*b[i],0);
export const transform=(a:number[][],v:number[])=>a.map(row=>dot(row,v));
export function projection(v:number[],u:number[]){const denominator=dot(u,u);return denominator===0?null:u.map(x=>x*dot(v,u)/denominator);}
export function euler(k:number,y0:number,h:number,count:number){const points=[{x:0,y:y0}];for(let i=0;i<count;i++)points.push({x:(i+1)*h,y:points[i].y+h*k*points[i].y});return points;}
