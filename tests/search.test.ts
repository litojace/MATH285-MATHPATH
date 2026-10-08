import {describe,expect,it} from 'vitest';
import {searchLessons} from '../src/lib/search';
describe('lesson search',()=>{
 it('expands common abbreviations',()=>expect(searchLessons('RREF')[0].lesson.id).toBe('systems'));
 it('recognizes a first-order linear equation topic',()=>expect(searchLessons('dy/dx + 2y = 6')[0].lesson.id).toBe('linear-ode'));
 it('finds misspellings within one edit',()=>expect(searchLessons('eignvalues')[0].lesson.id).toBe('eigenvalues'));
 it('does not invent unsupported results',()=>expect(searchLessons('topological manifold').length).toBe(0));
});
