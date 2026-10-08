import {describe,expect,it} from 'vitest';
import katex from 'katex';
import {lessons} from '../src/content';
import {practiceAdditions} from '../src/content/practice-additions';

const exercise=(id:string)=>Object.values(practiceAdditions).flat().find(e=>e.id===id)!;
const derivative=(f:(x:number)=>number,x:number)=>(f(x+1e-5)-f(x-1e-5))/2e-5;
describe('supplementary practice mathematics',()=>{
 it('renders every formula, hint and worked step without LaTeX errors',()=>{
  for(const lesson of lessons){
   const steps=[...lesson.definitions,...lesson.formulas,...(lesson.methodGuide??[]),...lesson.examples.flatMap(e=>e.steps),...lesson.exercises.flatMap(e=>[{math:e.math},...e.hints,...e.solutionSteps])];
   for(const step of steps)if(step.math)expect(()=>katex.renderToString(step.math!,{throwOnError:true})).not.toThrow();
  }
 });
 it('satisfies the original equations for matrix-valued system answers',()=>{
  const [[x],[y]]=exercise('systems-6').answer as number[][];
  expect(2*x+3*y).toBe(1);expect(4*x-y).toBe(9);
  const [[a],[b],[c]]=exercise('systems-10').answer as number[][];
  expect([a+b+c,a-b+c,2*a+b-c]).toEqual([6,2,1]);
 });
 it('checks projection residuals are perpendicular and normalized answers have length one',()=>{
  const [[x],[y]]=exercise('projection-7').answer as number[][];
  expect(x+y).toBe(0);expect([4-x,-y]).toEqual([2,2]);
  const [[a],[b]]=exercise('projection-8').answer as number[][];
  expect(a*a+b*b).toBeCloseTo(1,12);
  const [[u],[v]]=exercise('projection-9').answer as number[][];
  expect(u+v).toBe(0);expect([3-u,1-v]).toEqual([2,2]);
 });
 it('checks first-order solutions by differential residuals and initial values',()=>{
  const families=[
   {y:(x:number)=>2*Math.exp(x*x/2),f:(x:number,y:number)=>x*y,x0:0,y0:2},
   {y:(x:number)=>1/(1+Math.exp(-x)),f:(_x:number,y:number)=>y*(1-y),x0:0,y0:.5},
   {y:(x:number)=>.75*x*x+1.25/(x*x),f:(x:number,y:number)=>3*x-2*y/x,x0:1,y0:2},
   {y:(x:number)=>x/2-.25+.25*Math.exp(-2*x),f:(x:number,y:number)=>x-2*y,x0:0,y0:0},
  ];
  for(const {y,f,x0,y0} of families){expect(y(x0)).toBeCloseTo(y0,10);for(const x of [.5,1,1.5])expect(derivative(y,x)).toBeCloseTo(f(x,y(x)),7);}
  expect(families[2].y(2)).toBe(exercise('linear-ode-7').answer);
 });
 it('independently computes Euler and Heun updates',()=>{
  let x=0,y=1;for(let i=0;i<2;i++){y+=.5*(x+y);x+=.5;}
  expect(y).toBe(exercise('euler-6').answer);
  const h=.2,prediction=1+h;
  expect(1+h*(1+prediction)/2).toBeCloseTo(exercise('euler-7').answer as number,12);
  expect((1+.1)**2).toBeLessThan(Math.exp(.2));
 });
});
