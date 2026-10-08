import {useEffect, useState} from 'react';
import {NavLink, Route, Routes} from 'react-router-dom';
import {ArrowUpRight, BookOpen, ChartNoAxesColumnIncreasing, FlaskConical, Home, Instagram, Library, Menu, Moon, Search, Sun, X} from 'lucide-react';
import {SearchBox} from './components/Search';
import {HomePage} from './pages/HomePage';
import {CoursePage, CoursesPage} from './pages/CoursePage';
import {LessonPage} from './pages/LessonPage';
import {SearchPage} from './pages/SearchPage';
import {DashboardPage} from './pages/DashboardPage';
import {PracticePage} from './pages/PracticePage';
import {LibraryPage} from './pages/LibraryPage';
import {NotFoundPage} from './pages/NotFoundPage';

const links=[['/','Home',Home],['/courses','Courses',BookOpen],['/practice','Practice',FlaskConical],['/library','Library',Library],['/dashboard','Progress',ChartNoAxesColumnIncreasing]] as const;

export function App(){
  const [open,setOpen]=useState(false);
  const [dark,setDark]=useState(()=>localStorage.getItem('mathpath.theme')==='dark'||(!localStorage.getItem('mathpath.theme')&&matchMedia('(prefers-color-scheme: dark)').matches));
  useEffect(()=>{document.documentElement.dataset.theme=dark?'dark':'light';localStorage.setItem('mathpath.theme',dark?'dark':'light');},[dark]);
  return <div className="app-shell">
    <header className="site-header"><div className="nav-inner"><NavLink className="brand" to="/" onClick={()=>setOpen(false)} aria-label="MathPath home"><span className="brand-mark">M</span><span>Math<span>Path</span></span></NavLink>
      <nav className={open?'main-nav open':'main-nav'} aria-label="Main navigation">{links.map(([to,label,Icon])=><NavLink key={to} to={to} end={to==='/'} onClick={()=>setOpen(false)}><Icon size={17}/>{label}</NavLink>)}</nav>
      <div className="header-actions"><div className="desktop-search"><SearchBox/></div><NavLink className="icon-button mobile-search" aria-label="Search" to="/search"><Search size={19}/></NavLink><button className="icon-button" onClick={()=>setDark(v=>!v)} aria-label={`Switch to ${dark?'light':'dark'} mode`}>{dark?<Sun size={19}/>:<Moon size={19}/>}</button><button className="icon-button menu-button" onClick={()=>setOpen(v=>!v)} aria-expanded={open} aria-label="Toggle navigation">{open?<X/>:<Menu/>}</button></div>
    </div></header>
    <main><Routes><Route path="/" element={<HomePage/>}/><Route path="/courses" element={<CoursesPage/>}/><Route path="/courses/:courseId" element={<CoursePage/>}/><Route path="/lessons/:lessonId" element={<LessonPage/>}/><Route path="/search" element={<SearchPage/>}/><Route path="/practice" element={<PracticePage/>}/><Route path="/dashboard" element={<DashboardPage/>}/><Route path="/library" element={<LibraryPage/>}/><Route path="*" element={<NotFoundPage/>}/></Routes></main>
    <footer><div><NavLink className="brand" to="/"><span className="brand-mark">M</span>MathPath</NavLink><p>Clear steps. Honest progress. Mathematics that makes sense.</p></div><div><strong>Built for learning</strong><p>Guest progress stays on this device. No account required.</p></div><div className="footer-credit"><div className="creator-credit"><span className="creator-monogram" aria-hidden="true">J</span><div><span className="creator-label">Created by</span><strong className="creator-name">Jacen<span aria-hidden="true">.</span></strong></div></div><a className="creator-social" href="https://www.instagram.com/litojace/" target="_blank" rel="noopener noreferrer" aria-label="Jacen on Instagram, @litojace (opens in a new tab)"><Instagram size={21} aria-hidden="true"/><span className="creator-social-copy"><small>Connect on Instagram</small><strong>@litojace</strong></span><ArrowUpRight size={17} aria-hidden="true"/></a></div></footer>
  </div>;
}
