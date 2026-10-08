import type {Lesson} from '../types/content';
import {MathBlock} from './Math';

export function MethodGuide({guide}:{guide:Lesson['methodGuide']}){
 if(!guide?.length)return null;
 return <section className="method-guide" aria-label="Detailed method guide">
  <h3>Work through the method</h3>
  {guide.map((part,index)=><div className="method-guide-part" key={part.title}>
   <span className="method-guide-number" aria-hidden="true">{index+1}</span>
   <div><h4>{part.title}</h4><p className="lesson-prose">{part.text}</p>{part.math&&<MathBlock math={part.math}/>}</div>
  </div>)}
 </section>;
}
