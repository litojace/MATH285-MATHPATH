import {exerciseIndex,lessons} from '../content';
import {z} from 'zod';
const attempt=z.object({exerciseId:z.string(),correct:z.boolean(),at:z.string(),hinted:z.boolean(),solutionViewed:z.boolean()});
export const progressSchema=z.object({version:z.literal(1),completed:z.array(z.string()),bookmarks:z.array(z.string()),recent:z.array(z.string()),attempts:z.array(attempt),hints:z.record(z.number().int().nonnegative()),solutions:z.array(z.string()),notes:z.record(z.string())});
export type Progress=z.infer<typeof progressSchema>;
export const freshProgress=():Progress=>({version:1,completed:[],bookmarks:[],recent:[],attempts:[],hints:{},solutions:[],notes:{}});
export const progressKey='mathpath.progress.v1';
export function loadProgress():Progress{try{return progressSchema.parse(JSON.parse(localStorage.getItem(progressKey)??'null'));}catch{return freshProgress();}}
export function mastery(p:Progress,lessonId:string){
 const exercises=lessons.find(l=>l.id===lessonId)?.exercises??[];
 const total=exercises.reduce((a,e)=>a+e.difficulty,0);
 const earned=exercises.reduce((a,e)=>{const attempts=p.attempts.filter(x=>x.exerciseId===e.id);const latest=attempts.at(-1);return a+(latest?.correct?e.difficulty*(latest.hinted||latest.solutionViewed?0.5:1):0);},0);
 return total?Math.round(100*earned/total):0;
}
export function accuracy(p:Progress){return p.attempts.length?Math.round(100*p.attempts.filter(x=>x.correct).length/p.attempts.length):null;}
export function missed(p:Progress){const latest=new Map(p.attempts.map(a=>[a.exerciseId,a]));return [...latest.values()].filter(a=>!a.correct).map(a=>exerciseIndex[a.exerciseId]).filter(Boolean);}
export function mergeProgress(a:Progress,b:Progress):Progress{
 const unique=(x:string[],y:string[])=>[...new Set([...x,...y])];
 const attempts=[...new Map([...a.attempts,...b.attempts].map(x=>[`${x.exerciseId}:${x.at}:${x.correct}`,x])).values()].sort((x,y)=>x.at.localeCompare(y.at));
 return {version:1,completed:unique(a.completed,b.completed),bookmarks:unique(a.bookmarks,b.bookmarks),recent:unique(b.recent,a.recent).slice(-8),attempts,hints:Object.fromEntries(unique(Object.keys(a.hints),Object.keys(b.hints)).map(id=>[id,Math.max(a.hints[id]??0,b.hints[id]??0)])),solutions:unique(a.solutions,b.solutions),notes:{...a.notes,...b.notes}};
}
