import {createContext,useContext,useEffect,useRef,useState,type ReactNode} from 'react';
import type {User} from '@supabase/supabase-js';
import {freshProgress,loadProgress,mergeProgress,progressKey,progressSchema,type Progress} from './progress';
import {supabase} from './cloud';
type Store={progress:Progress,update:(fn:(p:Progress)=>Progress)=>void,reset:()=>Promise<void>,user:User|null,cloudStatus:string};
const Context=createContext<Store|null>(null);
export function ProgressProvider({children}:{children:ReactNode}){
 const [progress,setProgress]=useState(loadProgress);const [user,setUser]=useState<User|null>(null);const [cloudStatus,setStatus]=useState(supabase?'Cloud not signed in':'Guest mode · saved on this device');const [loaded,setLoaded]=useState(false);const progressRef=useRef(progress);progressRef.current=progress;
 const update=(fn:(p:Progress)=>Progress)=>setProgress(p=>progressSchema.parse(fn(p)));
 useEffect(()=>{try{localStorage.setItem(progressKey,JSON.stringify(progress));}catch{setStatus('Storage unavailable. Export progress before leaving.');}},[progress]);
 useEffect(()=>{
 if(!supabase)return;
 let active=true;
 const {data}=supabase.auth.onAuthStateChange((_event,session)=>{if(active){setLoaded(false);setUser(session?.user??null);}});
 supabase.auth.getSession().then(({data,error})=>{if(active){if(error)setStatus(error.message);setUser(data.session?.user??null);}});
 return ()=>{active=false;data.subscription.unsubscribe();};
 },[]);
 useEffect(()=>{
 if(!supabase||!user){setStatus(supabase?'Guest mode · cloud not signed in':'Guest mode · saved on this device');return;}
 let active=true;
 supabase.from('learning_progress').select('data').eq('user_id',user.id).maybeSingle().then(({data,error})=>{
 if(!active)return;if(error){setStatus(`Cloud unavailable: ${error.message}`);return;}
 const parsed=progressSchema.safeParse(data?.data);
 if(data&&!parsed.success){setStatus('Cloud data format needs migration; local data preserved.');return;}
 setProgress(p=>parsed.success?mergeProgress(parsed.data,p):p);setLoaded(true);setStatus('Cloud connected · guest progress merged');
 });return ()=>{active=false;};
 },[user]);
 useEffect(()=>{
 if(!supabase||!user||!loaded)return;
 const timer=window.setTimeout(()=>{supabase!.from('learning_progress').upsert({user_id:user.id,data:progress}).then(({error})=>setStatus(error?`Cloud save failed: ${error.message}`:'Cloud synced'));},700);
 return ()=>clearTimeout(timer);
 },[progress,user,loaded]);
 const reset=async()=>{const next=freshProgress();if(supabase&&user){const {error}=await supabase.from('learning_progress').upsert({user_id:user.id,data:next});if(error){setStatus(`Reset failed: ${error.message}`);return;}}setProgress(next);};
 return <Context.Provider value={{progress,update,reset,user,cloudStatus}}>{children}</Context.Provider>;
}
export function useProgress(){const c=useContext(Context);if(!c)throw Error('Progress provider missing');return c;}
