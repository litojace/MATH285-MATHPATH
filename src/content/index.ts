import {lessonSchema} from '../types/content';
import {expandedLessons} from './expanded';
export const lessons=lessonSchema.array().parse(expandedLessons);
export const courses=[{id:'linear-algebra',title:'Linear Algebra',subtitle:'Understand space, structure, and transformations.',color:'blue',icon:'↗'},{id:'differential-equations',title:'Differential Equations',subtitle:'Discover the mathematics of change.',color:'teal',icon:'∿'}];
export const exerciseIndex=Object.fromEntries(lessons.flatMap(l=>l.exercises.map(e=>[e.id,e])));
