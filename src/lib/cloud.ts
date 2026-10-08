import {createClient} from '@supabase/supabase-js';
const env=import.meta.env;
export const supabase=env.VITE_SUPABASE_URL&&env.VITE_SUPABASE_ANON_KEY?createClient(env.VITE_SUPABASE_URL,env.VITE_SUPABASE_ANON_KEY):null;
