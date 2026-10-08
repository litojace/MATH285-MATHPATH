import {ArrowRight,BookOpen} from 'lucide-react';
import {Link} from 'react-router-dom';
import type {Lesson} from '../types/content';

export function Prerequisites({lessons}:{lessons:Lesson[]}){
 if(!lessons.length)return null;
 return <section className="prerequisite-box" aria-label="Recommended prerequisites">
  <div className="prerequisite-heading"><span className="prerequisite-icon"><BookOpen size={19} aria-hidden="true"/></span><div><h3>Recommended prerequisites</h3><p>Review these foundations before you begin.</p></div></div>
  <div className="prerequisite-grid">{lessons.map(lesson=><Link className="prerequisite-link" key={lesson.id} to={`/lessons/${lesson.id}`}>
   <span className="prerequisite-section">{lesson.section}</span><span className="prerequisite-content"><small>{lesson.courseId==='linear-algebra'?'Linear Algebra':'Differential Equations'}</small><strong>{lesson.title}</strong></span><ArrowRight size={18} aria-hidden="true"/>
  </Link>)}</div>
 </section>;
}
