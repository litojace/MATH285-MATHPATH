import {useEffect,useRef,useState} from 'react';
import type {Data,Layout} from 'plotly.js';
import {dot,euler,projection,transform} from '../lib/math';
const labels:Record<string,string>={vectors:'Vector addition & scaling',transform:'Matrix transformations',projection:'Orthogonal projection',slope:'Slope field & initial-value curve',growth:'Growth, decay & logistic models',euler:'Euler approximation',oscillator:'Oscillation & phase portrait'};
export function Visualization({initial='vectors'}:{initial?:string}){
 const [mode,setMode]=useState(initial);const [a,setA]=useState(1);const [b,setB]=useState(2);const [k,setK]=useState(1);const [h,setH]=useState(0.1);const [preset,setPreset]=useState('shear');const [logistic,setLogistic]=useState(false);const [error,setError]=useState('');const target=useRef<HTMLDivElement>(null);
 useEffect(()=>{
 let disposed=false;let cleanup:(()=>void)|undefined;
 import('plotly.js-dist-min').then(({default:Plotly})=>{
 if(disposed||!target.current)return;
 const node=target.current;let data:Data[]=[];let equal=true;let xlabel='Horizontal component';let ylabel='Vertical component';
 const line=(name:string,x:number[],y:number[],color:string):Data=>({name,x,y,type:'scatter',mode:'lines+markers',line:{color,width:3},marker:{size:6}});
 const vector=(name:string,v:number[],color:string)=>line(name,[0,v[0]],[0,v[1]],color);
 if(['vectors','transform','projection'].includes(mode)){
 const v=[a,b];data.push(vector('Input v',v,'#2563eb'));
 if(mode==='vectors'){data.push(vector('w = (2, −1)',[2,-1],'#0d9488'),vector('kv + w',[k*a+2,k*b-1],'#7c3aed'));}
 if(mode==='projection'){const u=[1,1],p=projection(v,u)!;data.push(line('Projection line',[-5,5],[-5,5],'#94a3b8'),vector('Projection',p,'#0d9488'),line('Perpendicular residual',[p[0],a],[p[1],b],'#7c3aed'));}
 if(mode==='transform'){
 const matrices:Record<string,number[][]>={shear:[[1,k],[0,1]],scale:[[k,0],[0,1]],reflection:[[1,0],[0,-1]],rotation:[[Math.cos(k),-Math.sin(k)],[Math.sin(k),Math.cos(k)]],eigen:[[2,1],[0,3]]};const A=matrices[preset];data.push(vector('Transformed Av',transform(A,v),'#0d9488'));
 for(let i=-4;i<=4;i++){const p=transform(A,[i,-4]),q=transform(A,[i,4]),r=transform(A,[-4,i]),s=transform(A,[4,i]);data.push({x:[p[0],q[0],null,r[0],s[0]],y:[p[1],q[1],null,r[1],s[1]],type:'scatter',mode:'lines',line:{color:'rgba(13,148,136,0.25)',width:1},showlegend:false,hoverinfo:'skip'});}
 }
 }else{
 equal=false;xlabel='x (time)';ylabel='y (solution)';const xs=Array.from({length:121},(_,i)=>i*0.025);
 if(mode==='growth'){data.push(line(logistic?'Logistic · carrying capacity 5':'Exact exponential',xs,xs.map(x=>logistic?5/(1+(5/Math.max(.1,a)-1)*Math.exp(-k*x)):a*Math.exp(k*x)),'#0d9488'));}
 if(mode==='slope'){
 for(let x=0;x<=3;x+=.3)for(let y=-1;y<=5;y+=.5){const slope=6-2*y,len=.07/Math.sqrt(1+slope*slope);data.push({x:[x-len,x+len],y:[y-slope*len,y+slope*len],type:'scatter',mode:'lines',line:{color:'#94a3b8',width:1},showlegend:false,hoverinfo:'skip'});}
 data.push(line('Exact: 3 + (y₀ − 3)e⁻²ˣ',xs,xs.map(x=>3+(a-3)*Math.exp(-2*x)),'#2563eb'));
 }
 if(mode==='euler'){const points=euler(k,a,h,Math.floor(3/h));data.push(line('Euler estimate',points.map(p=>p.x),points.map(p=>p.y),'#7c3aed'),{...line('Exact exponential',xs,xs.map(x=>a*Math.exp(k*x)),'#0d9488'),mode:'lines'});}
 if(mode==='oscillator'){const freq=Math.max(.25,Math.abs(k));const time=Array.from({length:241},(_,i)=>i*.025);if(preset==='phase'){xlabel='Position y';ylabel='Velocity y′';equal=true;data.push({...line('Phase curve',time.map(x=>a*Math.cos(freq*x)),time.map(x=>-a*freq*Math.sin(freq*x)),'#7c3aed'),mode:'lines'});}else data.push({...line('Position y = a cos(ωx)',time,time.map(x=>a*Math.cos(freq*x)),'#2563eb'),mode:'lines'});}
 }
 const dark=document.documentElement.dataset.theme==='dark';const layout:Partial<Layout>={autosize:true,height:360,margin:{l:50,r:20,t:15,b:55},paper_bgcolor:'transparent',plot_bgcolor:'transparent',font:{color:dark?'#e2e8f0':'#334155',family:'system-ui'},xaxis:{title:{text:xlabel},zerolinecolor:'#64748b',gridcolor:dark?'#334155':'#e2e8f0'},yaxis:{title:{text:ylabel},zerolinecolor:'#64748b',gridcolor:dark?'#334155':'#e2e8f0',...(equal?{scaleanchor:'x',scaleratio:1}:{})},legend:{orientation:'h',y:-.25},showlegend:true};
 Plotly.react(node,data,layout,{responsive:true,displayModeBar:false}).catch(()=>setError('The visualization could not render. The lesson formulas remain available.'));
 const observer=new ResizeObserver(()=>{Plotly.Plots.resize(node);});observer.observe(node);cleanup=()=>{observer.disconnect();Plotly.purge(node);};
 }).catch(()=>setError('Could not load the visualization. Please reload to try again.'));
 return ()=>{disposed=true;cleanup?.();};
 },[mode,a,b,k,h,preset,logistic]);
 const range=(label:string,value:number,set:(n:number)=>void,min:number,max:number,step=.25)=><label className="slider">{label}<strong>{value}</strong><input type="range" min={min} max={max} step={step} value={value} onChange={e=>set(Number(e.target.value))}/></label>;
 return <section className="card visualization"><div className="row spread"><div><span className="eyebrow teal">Explore the idea</span><h3>Change a value. Notice what happens.</h3></div></div><label>Visualization<select value={mode} onChange={e=>{setMode(e.target.value);setPreset('shear');}}>{Object.entries(labels).map(([id,label])=><option key={id} value={id}>{label}</option>)}</select></label><div className="controls">{range(['vectors','transform','projection'].includes(mode)?'v horizontal':'Initial value / amplitude',a,setA,mode==='growth'?.25:-4,4)}{['vectors','transform','projection'].includes(mode)&&range('v vertical',b,setB,-4,4)}{['vectors','transform','growth','euler','oscillator'].includes(mode)&&range('Scale / rate / angle (radians)',k,setK,-2,2)}{mode==='euler'&&range('Step size h',h,setH,.05,.5,.05)}{mode==='transform'&&<label>Transformation<select value={preset} onChange={e=>setPreset(e.target.value)}><option value="shear">Shear: (x + ky, y)</option><option value="scale">Scale: (kx, y)</option><option value="rotation">Rotate by k radians</option><option value="reflection">Reflect across horizontal axis</option><option value="eigen">Eigenvector exploration: [2 1; 0 3]</option></select></label>}{mode==='growth'&&<label className="choice"><input type="checkbox" checked={logistic} onChange={e=>setLogistic(e.target.checked)}/>Logistic growth (capacity 5)</label>}{mode==='oscillator'&&<label>View<select value={preset} onChange={e=>setPreset(e.target.value)}><option value="shear">Position over time</option><option value="phase">Phase portrait</option></select></label>}</div><div ref={target} role="img" aria-label={labels[mode]+'; the numeric description below provides a text alternative.'}/>{error&&<p role="alert">{error}</p>}<p className="muted">{mode==='vectors'?`v = (${a}, ${b}), kv + w = (${k*a+2}, ${k*b-1}). With w = (2, −1), independence is tested by determinant ${-a-2*b}; zero means the vectors span at most a line.`:mode==='projection'?`Projection onto (1,1) is (${dot([a,b],[1,1])/2}, ${dot([a,b],[1,1])/2}); the residual dot (1,1) is zero.`:mode==='transform'?'The faint grid shows how the same matrix moves the entire plane. For the eigenvector matrix, directions (1,0) and (1,1) keep their lines.':mode==='slope'?`The curve starts at y(0) = ${a} and approaches the equilibrium 3. Each segment has slope 6 − 2y.`:mode==='euler'?`Exact model y = ${a}e^(${k}x); Euler multiplier is ${Number((1+h*k).toFixed(3))}. Euler is an approximation; compare it with the exact curve.`:mode==='oscillator'?`Position y = ${a} cos(${Math.max(.25,Math.abs(k))}x); velocity is its derivative. The model is undamped.`:logistic?`Logistic model y′ = ${k} y(1 − y/5); initial value ${a}; carrying capacity 5.`:`Exponential model y′ = ${k}y; initial value ${a}. Negative rates produce decay.`}</p></section>;
}
