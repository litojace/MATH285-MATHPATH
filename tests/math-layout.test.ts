import {describe,expect,it} from 'vitest';
import katex from 'katex';
import {verticalMath,expandWideMath} from '../src/lib/math-layout';
import {lessons} from '../src/content';

describe('vertical mathematics',()=>{
 it('separates given equations and intermediate equalities',()=>{
  expect(verticalMath(String.raw`x=2+3=5,\quad y=4`)).toEqual(['x','=2+3','=5','y','=4']);
 });
 it('preserves fractions, integrals, nested matrices, and tuple delimiters',()=>{
  const math=String.raw`(u,v)=\left(\left[\begin{matrix}1\\2\end{matrix}\right],\left[\begin{matrix}3\\4\end{matrix}\right]\right)`;
  const output=verticalMath(math);expect(output.join('')).toContain('gathered');
  for(const line of output)expect(()=>katex.renderToString(line,{throwOnError:true})).not.toThrow();
  expect(verticalMath(String.raw`\int_0^1x\,dx=\frac{1+2}{3}`)).toEqual([String.raw`\int_0^1x\,dx`,String.raw`=\frac{1+2}{3}`]);
 });
 it('preserves every entry and the augmented divider of a wide matrix',()=>{
  const result=expandWideMath(String.raw`\left[\begin{array}{cc|c}1&2&3\\4&5&6\end{array}\right]`)!;
  expect(result.definitions![0].lines).toEqual(['(M_{1})_{1,1}=1','(M_{1})_{1,2}=2','(M_{1})_{1,3}=3','(M_{1})_{2,1}=4','(M_{1})_{2,2}=5','(M_{1})_{2,3}=6']);
  expect(result.definitions![0].label).toContain('divider follows column 2');
 });
 it('renders all published math after vertical reflow and optional expansion',()=>{
  for(const lesson of lessons){
   const steps=[...lesson.definitions,...lesson.formulas,...(lesson.methodGuide??[]),...lesson.examples.flatMap(e=>[...e.steps,...(e.finalAnswer?[e.finalAnswer]:[])]),...lesson.exercises.flatMap(e=>[{math:e.math},...e.hints,...e.solutionSteps])];
   for(const step of steps)if(step.math)for(const line of verticalMath(step.math)){
    expect(()=>katex.renderToString(line,{throwOnError:true}),line).not.toThrow();
    const expanded=expandWideMath(line);
    if(expanded)for(const part of [...expanded.lines,...(expanded.definitions??[]).flatMap(d=>d.lines)])expect(()=>katex.renderToString(part,{throwOnError:true}),part).not.toThrow();
   }
  }
 },20000);
});
