import {useEffect,useLayoutEffect,useState} from 'react';
import {useLocation} from 'react-router-dom';
import {ArrowUp} from 'lucide-react';

export function ScrollControls(){
 const {pathname,hash}=useLocation();
 const [visible,setVisible]=useState(false);

 useLayoutEffect(()=>{
  // New pages start at the top; native anchor links keep their destination.
  if(!hash)window.scrollTo({top:0,left:0,behavior:'instant'});
 },[pathname]);

 useEffect(()=>{
  const update=()=>setVisible(window.scrollY>500);
  update();window.addEventListener('scroll',update,{passive:true});
  return ()=>window.removeEventListener('scroll',update);
 },[]);

 const backToTop=()=>{
  document.querySelector<HTMLElement>('main')?.focus({preventScroll:true});
  const reduced=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  window.scrollTo({top:0,left:0,behavior:reduced?'instant':'smooth'});
 };

 return visible?<button type="button" className="back-to-top" aria-label="Back to top" title="Back to top" onClick={backToTop}>
  <ArrowUp size={20} aria-hidden="true"/><span>Back to top</span>
 </button>:null;
}
