import {lessons} from '../src/content';
const rows=lessons.map(l=>({course:l.courseId,section:l.section,lesson:l.title,examples:l.examples.length,exercises:l.exercises.length,sourcePages:l.sourceReferences.flatMap(r=>r.pageNumbers).join(', ')||'supplementary',verification:l.reviewStatus}));
console.table(rows);
console.log(`Totals: ${lessons.length} lessons, ${rows.reduce((n,r)=>n+r.examples,0)} worked examples, ${rows.reduce((n,r)=>n+r.exercises,0)} exercises.`);
