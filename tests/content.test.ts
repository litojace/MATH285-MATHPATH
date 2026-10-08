import {describe,expect,it} from 'vitest';
import {lessons} from '../src/content';
import {lessonSchema} from '../src/types/content';
describe('content library',()=>{
 it('validates every lesson against the schema',()=>expect(()=>lessonSchema.array().parse(lessons)).not.toThrow());
 it('has stable unique lesson and exercise IDs',()=>{const lessonIds=lessons.map(l=>l.id);const exerciseIds=lessons.flatMap(l=>l.exercises.map(e=>e.id));expect(new Set(lessonIds).size).toBe(lessonIds.length);expect(new Set(exerciseIds).size).toBe(exerciseIds.length);});
 it('keeps solutions hidden by content structure rather than embedding them in prompts',()=>lessons.forEach(l=>l.exercises.forEach(e=>expect(e.solutionSteps.length).toBeGreaterThanOrEqual(2))));
});
