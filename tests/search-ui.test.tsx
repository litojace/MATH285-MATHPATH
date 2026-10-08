import {describe,expect,it} from 'vitest';
import {fireEvent,render,screen} from '@testing-library/react';
import {MemoryRouter,useLocation} from 'react-router-dom';
import {SearchBox} from '../src/components/Search';
import {SearchPage} from '../src/pages/SearchPage';
import {searchLessons} from '../src/lib/search';

function Location(){const location=useLocation();return <output data-testid="location">{location.pathname}{location.search}</output>}
describe('desktop search UI',()=>{
 it('submits with Enter and preserves the query',()=>{render(<MemoryRouter><SearchBox/><Location/></MemoryRouter>);const input=screen.getByLabelText('Search topics, formulas, or equations');fireEvent.change(input,{target:{value:'integrating factor'}});fireEvent.submit(input.closest('form')!);expect(screen.getByTestId('location')).toHaveTextContent('/search?q=integrating%20factor');});
 it('opens a suggestion after a pointer focus change',()=>{render(<MemoryRouter><SearchBox/><Location/></MemoryRouter>);const input=screen.getByLabelText('Search topics, formulas, or equations');fireEvent.focus(input);fireEvent.change(input,{target:{value:'eigen'}});const suggestion=screen.getByRole('option',{name:/Eigenvalues and Eigenvectors/});fireEvent.mouseDown(suggestion);fireEvent.click(suggestion);expect(screen.getByTestId('location')).toHaveTextContent('/lessons/eigenvalues');});
 it('shows all matches from the first typed letter and supports keyboard selection',()=>{
  render(<MemoryRouter><SearchBox/><Location/></MemoryRouter>);
  const input=screen.getByRole('combobox');fireEvent.change(input,{target:{value:'m'}});
  const matches=searchLessons('m');expect(matches.length).toBeGreaterThan(4);
  expect(screen.getAllByRole('option')).toHaveLength(matches.length);
  expect(input).toHaveAttribute('aria-expanded','true');
  fireEvent.keyDown(input,{key:'ArrowDown'});expect(screen.getAllByRole('option')[0]).toHaveAttribute('aria-selected','true');
  fireEvent.keyDown(input,{key:'Enter'});expect(screen.getByTestId('location')).toHaveTextContent(`/lessons/${matches[0].lesson.id}`);
 });
 it('dismisses and clears suggestions without losing the input focus',()=>{
  render(<MemoryRouter><SearchBox/></MemoryRouter>);const input=screen.getByRole('combobox');
  fireEvent.focus(input);fireEvent.change(input,{target:{value:'matrix'}});fireEvent.keyDown(input,{key:'Escape'});
  expect(screen.queryByRole('listbox')).not.toBeInTheDocument();
  fireEvent.focus(input);expect(screen.getByRole('listbox')).toBeInTheDocument();
  fireEvent.click(screen.getByRole('button',{name:'Clear search input'}));expect(input).toHaveValue('');expect(input).toHaveFocus();
  expect(screen.queryByRole('listbox')).not.toBeInTheDocument();
 });
 it('filters the full search page while the user types',async()=>{render(<MemoryRouter><SearchPage/></MemoryRouter>);const input=screen.getByLabelText('Search all lesson content');fireEvent.change(input,{target:{value:'eigenvalues'}});expect(await screen.findByText(/matching lesson/)).toBeInTheDocument();expect(screen.getByRole('heading',{name:/Eigenvalues and Eigenvectors/})).toBeInTheDocument();expect(screen.queryByText('Introduction to Systems of Linear Equations')).not.toBeInTheDocument();});
});
