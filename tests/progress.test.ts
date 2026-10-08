import {describe,expect,it} from 'vitest';
import {freshProgress,mastery,mergeProgress} from '../src/lib/progress';
import {lessons} from '../src/content';
describe('progress',()=>{
 it('does not award mastery for opening a lesson',()=>expect(mastery(freshProgress(),'systems')).toBe(0));
 it('weights correct practice and discounts assisted work',()=>{const p=freshProgress();const lesson=lessons.find(l=>l.id==='systems')!;p.attempts=[{exerciseId:lesson.exercises[0].id,correct:true,at:'2026-01-01',hinted:false,solutionViewed:false},{exerciseId:lesson.exercises[1].id,correct:true,at:'2026-01-02',hinted:true,solutionViewed:false}];expect(mastery(p,lesson.id)).toBe(10);});
 it('merges guest progress without losing cloud completion',()=>{const a=freshProgress(),b=freshProgress();a.completed=['systems'];b.completed=['vectors'];expect(mergeProgress(a,b).completed).toEqual(['systems','vectors']);});
});
