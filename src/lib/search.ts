import {lessons} from '../content';
const synonyms:Record<string,string>={ode:'differential equation',rref:'row reduction',ivp:'initial value problem',gaussian:'row reduction',eigen:'eigenvalues',orthogonal:'projection',transformation:'transformations'};
const normalize=(s:string)=>s.toLowerCase().normalize('NFKD').replace(/[\u0300-\u036f]/g,'').replace(/[^a-z0-9′/]+/g,' ').trim();
const containsWord=(text:string,token:string)=>text.split(' ').some(word=>word===token||word.startsWith(token));
function distance(a:string,b:string){const d=Array.from({length:a.length+1},(_,i)=>[i,...Array(b.length).fill(0)]);for(let j=0;j<=b.length;j++)d[0][j]=j;for(let i=1;i<=a.length;i++)for(let j=1;j<=b.length;j++)d[i][j]=Math.min(d[i-1][j]+1,d[i][j-1]+1,d[i-1][j-1]+Number(a[i-1]!==b[j-1]));return d[a.length][b.length];}
export function searchLessons(query:string){
 const q=normalize(query);if(!q)return lessons.map(lesson=>({lesson,score:1,reason:'Explore the library'}));
 const equation=/(dy\s*\/\s*dx|y['′])\s*[+-]\s*\d*\s*y\s*=/.test(query.toLowerCase());
 const tokens=q.split(' ').filter(Boolean).flatMap(t=>[t,...(synonyms[t]?.split(' ')??[])]);
 return lessons.map(lesson=>{
 const title=normalize(lesson.title);const related=lesson.prerequisites.map(id=>lessons.find(l=>l.id===id)?.title??'').join(' ');
 const corpus=normalize([lesson.title,lesson.description,lesson.section,...lesson.keywords,...lesson.mistakes,related,...lesson.definitions.map(s=>s.text),...lesson.formulas.map(s=>s.text)].join(' '));
 let score=corpus.includes(q)?8:0;for(const token of tokens){if(containsWord(title,token))score+=5;else if(containsWord(corpus,token))score+=2;else if(token.length>=4&&corpus.split(' ').some(w=>distance(token,w)<=1))score+=1;}
 if(equation&&lesson.id==='linear-ode')score+=30;
 return {lesson,score,reason:equation&&lesson.id==='linear-ode'?'Equation pattern: first-order linear (topic recommendation only)': 'Matches lesson text, keywords, or prerequisites'};
 }).filter(r=>r.score>0).sort((a,b)=>b.score-a.score);
}
