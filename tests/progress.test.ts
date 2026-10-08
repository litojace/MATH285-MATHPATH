import {describe,expect,it} from 'vitest';
import {freshProgress,mastery,mergeProgress} from '../src/lib/progress';
describe('progress',()=>{
 it('does not award mastery for opening a lesson',()=>expect(mastery(freshProgress(),'systems')).toBe(0));
 it('weights correct practice and discounts assisted work',()=>{const p=freshProgress();p.attempts=[{exerciseId:'systems-1',correct:true,at:'2026-01-01',hinted:false,solutionViewed:false},{exerciseId:'systems-2',correct:true,at:'2026-01-02',hinted:true,solutionViewed:false}];expect(mastery(p,'systems')).toBe(33);});
 it('merges guest progress without losing cloud completion',()=>{const a=freshProgress(),b=freshProgress();a.completed=['systems'];b.completed=['vectors'];expect(mergeProgress(a,b).completed).toEqual(['systems','vectors']);});
});
