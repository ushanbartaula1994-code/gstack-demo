/**
 * Authentication utilities for Supabase integration
 */

import { supabase, createServerClient, createClientClient } from './client';
import type { User } from '@supabase/supabase-js';

// Type for user session
export interface AuthUser {
  id: string;
  email: string | null;
  name: string | null;
  image: string | null;
}

// Type for auth state
export interface AuthState {
  user: AuthUser | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
}

// Sign up a new user with email and password
export async function signup(email: string, password: string): Promise<{ user: AuthUser | null; error: string | null }> {
  try {
    const { data, error } = await supabase.auth.signUp({
      email,
      password,
    });

    if (error) {
      return { user: null, error: error.message };
    }

    if (!data.user) {
      return { user: null, error: 'No user data returned' };
    }

    return {
      user: {
        id: data.user.id,
        email: data.user.email,
        name: data.user.user_metadata?.name || null,
        image: data.user.user_metadata?.image || null,
      },
      error: null,
    };
  } catch (err) {
    return { user: null, error: (err as Error).message };
  }
}

// Sign in with email and password
export async function signin(email: string, password: string): Promise<{ user: AuthUser | null; error: string | null }> {
  try {
    const { data, error } = await supabase.auth.signInWithPassword({
      email,
      password,
    });

    if (error) {
      return { user: null, error: error.message };
    }

    if (!data.user) {
      return { user: null, error: 'No user data returned' };
    }

    return {
      user: {
        id: data.user.id,
        email: data.user.email,
        name: data.user.user_metadata?.name || null,
        image: data.user.user_metadata?.image || null,
      },
      error: null,
    };
  } catch (err) {
    return { user: null, error: (err as Error).message };
  }
}

// Sign out the current user
export async function signout(): Promise<{ error: string | null }> {
  try {
    const { error } = await supabase.auth.signOut();
    return { error: error?.message || null };
  } catch (err) {
    return { error: (err as Error).message };
  }
}

// Get the current user from the session
export async function getCurrentUser(): Promise<AuthUser | null> {
  try {
    const { data: { user } } = await supabase.auth.getUser();

    if (!user) {
      return null;
    }

    return {
      id: user.id,
      email: user.email,
      name: user.user_metadata?.name || null,
      image: user.user_metadata?.image || null,
    };
  } catch (err) {
    console.error('Error getting current user:', err);
    return null;
  }
}

// Get the current session
export async function getSession() {
  try {
    const { data: { session } } = await supabase.auth.getSession();
    return session;
  } catch (err) {
    console.error('Error getting session:', err);
    return null;
  }
}

// Server-sided user retrieval (for Server Components)
export async function getServerUser() {
  try {
    const supabase = createServerClient();
    const { data: { user } } = await supabase.auth.getUser();

    return user;
  } catch (err) {
    console.error('Error getting server user:', err);
    return null;
  }
}

// Reset password
export async function resetPassword(email: string): Promise<{ error: string | null }> {
  try {
    const { error } = await supabase.auth.resetPasswordForEmail(email);
    return { error: error?.message || null };
  } catch (err) {
    return { error: (err as Error).message };
  }
}

// Update user profile
export async function updateProfile(name: string, image?: string): Promise<{ error: string | null }> {
  try {
    const { error } = await supabase.auth.updateUser({
      data: {
        name,
        image,
      },
    });
    return { error: error?.message || null };
  } catch (err) {
    return { error: (err as Error).message };
  }
}

// On auth state change callback type
export type AuthStateChangeCallback = (state: AuthState) => void;

// Subscribe to auth state changes (for real-time updates)
export function subscribeToAuthStateChange(callback: AuthStateChangeCallback): () => void {
  return supabase.auth.onAuthStateChange((event, session) => {
    const user = session?.user ? {
      id: session.user.id,
      email: session.user.email,
      name: session.user.user_metadata?.name || null,
      image: session.user.user_metadata?.image || null,
    } : null;

    callback({
      user,
      isAuthenticated: !!user,
      isLoading: false,
      error: null,
    });
  });
}