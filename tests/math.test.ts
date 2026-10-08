import {describe,expect,it} from 'vitest';
import {checkAnswer,euler,projection,transform} from '../src/lib/math';
import {lessons} from '../src/content';
describe('mathematical helpers',()=>{
 it('computes a matrix transformation',()=>expect(transform([[2,1],[0,3]],[1,1])).toEqual([3,3]));
 it('projects and leaves an orthogonal residual',()=>{const p=projection([3,1],[1,1])!;expect(p).toEqual([2,2]);expect((3-p[0])+(1-p[1])).toBeCloseTo(0);});
 it('performs Euler updates using the new point',()=>expect(euler(1,2,.5,2).map(p=>p.y)).toEqual([2,3,4.5]));
 it('accepts equivalent fractions safely',()=>{const exercise=lessons.find(l=>l.id==='systems')!.exercises[0];expect(checkAnswer({...exercise,answer:1.5},'3/2').correct).toBe(true);expect(checkAnswer({...exercise,answer:1.5},'alert(1)').correct).toBeNull();});
});
