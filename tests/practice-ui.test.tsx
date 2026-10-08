import {describe,expect,it,vi} from 'vitest';
import {fireEvent,render,screen,within} from '@testing-library/react';
import {MemoryRouter,Route,Routes} from 'react-router-dom';
import {ProgressProvider} from '../src/lib/store';
import {LessonPage} from '../src/pages/LessonPage';

vi.mock('../src/components/Visualization',()=>({Visualization:()=> <div data-testid="lesson-visualization"/>}));

describe('lesson practice',()=>{
 it('does not show an unrelated default vector visualization on a Laplace lesson',()=>{
  render(<MemoryRouter initialEntries={['/lessons/differential-equations-7-1']}><ProgressProvider><Routes><Route path="/lessons/:lessonId" element={<LessonPage/>}/></Routes></ProgressProvider></MemoryRouter>);
  expect(screen.getByRole('heading',{level:1,name:'Laplace Transform'})).toBeInTheDocument();
  expect(screen.queryByTestId('lesson-visualization')).not.toBeInTheDocument();
 });
 it('has no tutor mode and keeps solutions hidden until explicitly opened',()=>{
  localStorage.clear();
  render(<MemoryRouter initialEntries={['/lessons/systems']}><ProgressProvider><Routes><Route path="/lessons/:lessonId" element={<LessonPage/>}/></Routes></ProgressProvider></MemoryRouter>);
  const sections=screen.getByRole('navigation',{name:'Lesson sections'});
  expect(within(sections).getAllByRole('button')).toHaveLength(2);
  expect(screen.queryByText(/tutor mode/i)).not.toBeInTheDocument();
  fireEvent.click(within(sections).getByRole('button',{name:'Practice & solutions'}));
  const reveal=screen.getAllByRole('button',{name:'Show Step-by-Step Solution'});
  expect(reveal).toHaveLength(10);
  expect(screen.queryByText('Work through the solution')).not.toBeInTheDocument();
  const problem=screen.getByText('Solve for y by subtracting the equations.').closest('article')!;
  fireEvent.change(within(problem).getByLabelText('Your answer'),{target:{value:'99'}});
  fireEvent.click(within(problem).getByRole('button',{name:'Check answer'}));
  expect(within(problem).queryByText('Work through the solution')).not.toBeInTheDocument();
  fireEvent.click(within(problem).getByRole('button',{name:'Hint 1 of 3'}));
  expect(within(problem).getByText('The x coefficients already agree.')).toBeInTheDocument();
  expect(within(problem).queryByText('Subtract the second equation from the first.')).not.toBeInTheDocument();
  fireEvent.click(within(problem).getByRole('button',{name:'Show Step-by-Step Solution'}));
  expect(within(problem).getByText('Work through the solution')).toBeInTheDocument();
  fireEvent.change(within(problem).getByLabelText('Your answer'),{target:{value:'3'}});
  fireEvent.click(within(problem).getByRole('button',{name:'Check answer'}));
  expect(within(problem).getByRole('status')).toHaveClass('success');
 });
});
