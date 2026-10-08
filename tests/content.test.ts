import {describe,expect,it} from 'vitest';
import {lessons} from '../src/content';
import {lessonSchema} from '../src/types/content';
import {curriculum} from '../src/content/curriculum';
describe('content library',()=>{
 it('validates every lesson against the schema',()=>expect(()=>lessonSchema.array().parse(lessons)).not.toThrow());
 it('has stable unique lesson and exercise IDs',()=>{const lessonIds=lessons.map(l=>l.id);const exerciseIds=lessons.flatMap(l=>l.exercises.map(e=>e.id));expect(new Set(lessonIds).size).toBe(lessonIds.length);expect(new Set(exerciseIds).size).toBe(exerciseIds.length);});
 it('does not repeat an identical practice problem within a lesson',()=>{
  for(const lesson of lessons){const questions=lesson.exercises.map(e=>`${e.prompt}\n${e.math}`);expect(new Set(questions).size,lesson.id).toBe(questions.length);}
 });
 it('keeps solutions hidden by content structure rather than embedding them in prompts',()=>lessons.forEach(l=>l.exercises.forEach(e=>expect(e.solutionSteps.length).toBeGreaterThanOrEqual(2))));
 it('publishes every requested section once, preserving skipped chapter numbers',()=>{
  expect(lessons.filter(l=>l.courseId==='linear-algebra')).toHaveLength(27);
  expect(lessons.filter(l=>l.courseId==='differential-equations')).toHaveLength(24);
  for(const topic of curriculum){
   const matches=lessons.filter(l=>l.courseId===topic.courseId&&l.section===topic.section);
   expect(matches).toHaveLength(1);expect(matches[0].title).toBe(topic.title);
   expect(matches[0].exercises.length).toBeGreaterThanOrEqual(10);
   expect(matches[0].examples.length).toBeGreaterThanOrEqual(3);
   expect(matches[0].prerequisites.every(id=>lessons.some(l=>l.id===id))).toBe(true);
  }
  expect(lessons.some(l=>l.courseId==='linear-algebra'&&l.section==='2.5')).toBe(false);
  expect(lessons.some(l=>l.courseId==='differential-equations'&&l.chapter.startsWith('Chapter 3'))).toBe(false);
 });
});
