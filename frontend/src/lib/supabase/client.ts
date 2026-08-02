/**
 * Supabase client configuration for AI Fitness Coach
 */

import { createClient } from '@supabase/supabase-js';

// Supabase URL and public key from environment variables
const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL || '';
const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || '';

// Create Supabase client
const supabase = createClient(supabaseUrl, supabaseKey);

// Server-side Supabase client (for Server Components)
export const createServerClient = () => {
  const cookieStore = require('next/headers').cookies();
  return createClient(supabaseUrl, supabaseKey, {
    cookies: {
      getAll: () => cookieStore.getAll(),
      setAll: (cookies: any) => {
        cookies.forEach((cookie: any) => {
          if (cookie.value) {
            cookieStore.set(cookie.name, cookie.value, {
              path: '/',
              maxAge: cookie.maxAge,
              sameSite: cookie.sameSite,
              secure: cookie.secure,
            });
          } else {
            cookieStore.delete(cookie.name);
          }
        });
      },
    },
  });
};

// Client-side Supabase client (for Client Components)
export const createClientClient = () => {
  return createClient(supabaseUrl, supabaseKey);
};

export { supabase };
export default supabase;