'use client';

/**
 * React Context for Supabase Authentication
 */

import React, { createContext, useContext, useEffect, useState, useCallback } from 'react';
import type { ReactNode } from 'react';
import { supabase } from './client';
import type { AuthUser, AuthState } from './auth';

// Context type
interface AuthContextType extends AuthState {
  signup: (email: string, password: string) => Promise<{ user: AuthUser | null; error: string | null }>;
  signin: (email: string, password: string) => Promise<{ user: AuthUser | null; error: string | null }>;
  signout: () => Promise<{ error: string | null }>;
  getCurrentUser: () => Promise<AuthUser | null>;
  updateProfile: (name: string, image?: string) => Promise<{ error: string | null }>;
}

// Default context value
const defaultAuthContext: AuthContextType = {
  user: null,
  isAuthenticated: false,
  isLoading: true,
  error: null,
  signup: async () => ({ user: null, error: 'Auth context not initialized' }),
  signin: async () => ({ user: null, error: 'Auth context not initialized' }),
  signout: async () => ({ error: 'Auth context not initialized' }),
  getCurrentUser: async () => null,
  updateProfile: async () => ({ error: 'Auth context not initialized' }),
};

// Create context
const AuthContext = createContext<AuthContextType>(defaultAuthContext);

// Auth provider component
interface AuthProviderProps {
  children: ReactNode;
}

export function AuthProvider({ children }: AuthProviderProps) {
  const [authState, setAuthState] = useState<AuthState>({
    user: null,
    isAuthenticated: false,
    isLoading: true,
    error: null,
  });

  // Initialize auth state on mount
  useEffect(() => {
    const initializeAuth = async () => {
      try {
        const { data: { user } } = await supabase.auth.getUser();

        if (user) {
          setAuthState({
            user: {
              id: user.id,
              email: user.email,
              name: user.user_metadata?.name || null,
              image: user.user_metadata?.image || null,
            },
            isAuthenticated: true,
            isLoading: false,
            error: null,
          });
        } else {
          setAuthState({
            user: null,
            isAuthenticated: false,
            isLoading: false,
            error: null,
          });
        }
      } catch (error) {
        setAuthState({
          user: null,
          isAuthenticated: false,
          isLoading: false,
          error: (error as Error).message,
        });
      }
    };

    initializeAuth();

    // Subscribe to auth state changes
    const { data: { subscription } } = supabase.auth.onAuthStateChange((event, session) => {
      const user = session?.user ? {
        id: session.user.id,
        email: session.user.email,
        name: session.user.user_metadata?.name || null,
        image: session.user.user_metadata?.image || null,
      } : null;

      setAuthState({
        user,
        isAuthenticated: !!user,
        isLoading: false,
        error: null,
      });
    });

    // Cleanup subscription on unmount
    return () => {
      subscription?.unsubscribe();
    };
  }, []);

  // Sign up function
  const signup = useCallback(async (email: string, password: string) => {
    try {
      setAuthState(prev => ({ ...prev, isLoading: true, error: null }));

      const { data, error } = await supabase.auth.signUp({
        email,
        password,
      });

      if (error) {
        setAuthState(prev => ({ ...prev, isLoading: false, error: error.message }));
        return { user: null, error: error.message };
      }

      if (!data.user) {
        setAuthState(prev => ({ ...prev, isLoading: false, error: 'No user data returned' }));
        return { user: null, error: 'No user data returned' };
      }

      const user: AuthUser = {
        id: data.user.id,
        email: data.user.email,
        name: data.user.user_metadata?.name || null,
        image: data.user.user_metadata?.image || null,
      };

      setAuthState({
        user,
        isAuthenticated: true,
        isLoading: false,
        error: null,
      });

      return { user, error: null };
    } catch (error) {
      const errorMessage = (error as Error).message;
      setAuthState(prev => ({ ...prev, isLoading: false, error: errorMessage }));
      return { user: null, error: errorMessage };
    }
  }, []);

  // Sign in function
  const signin = useCallback(async (email: string, password: string) => {
    try {
      setAuthState(prev => ({ ...prev, isLoading: true, error: null }));

      const { data, error } = await supabase.auth.signInWithPassword({
        email,
        password,
      });

      if (error) {
        setAuthState(prev => ({ ...prev, isLoading: false, error: error.message }));
        return { user: null, error: error.message };
      }

      if (!data.user) {
        setAuthState(prev => ({ ...prev, isLoading: false, error: 'No user data returned' }));
        return { user: null, error: 'No user data returned' };
      }

      const user: AuthUser = {
        id: data.user.id,
        email: data.user.email,
        name: data.user.user_metadata?.name || null,
        image: data.user.user_metadata?.image || null,
      };

      setAuthState({
        user,
        isAuthenticated: true,
        isLoading: false,
        error: null,
      });

      return { user, error: null };
    } catch (error) {
      const errorMessage = (error as Error).message;
      setAuthState(prev => ({ ...prev, isLoading: false, error: errorMessage }));
      return { user: null, error: errorMessage };
    }
  }, []);

  // Sign out function
  const signout = useCallback(async () => {
    try {
      setAuthState(prev => ({ ...prev, isLoading: true, error: null }));

      const { error } = await supabase.auth.signOut();

      if (error) {
        setAuthState(prev => ({ ...prev, isLoading: false, error: error.message }));
        return { error: error.message };
      }

      setAuthState({
        user: null,
        isAuthenticated: false,
        isLoading: false,
        error: null,
      });

      return { error: null };
    } catch (error) {
      const errorMessage = (error as Error).message;
      setAuthState(prev => ({ ...prev, isLoading: false, error: errorMessage }));
      return { error: errorMessage };
    }
  }, []);

  // Get current user function
  const getCurrentUser = useCallback(async () => {
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
    } catch (error) {
      console.error('Error getting current user:', error);
      return null;
    }
  }, []);

  // Update profile function
  const updateProfile = useCallback(async (name: string, image?: string) => {
    try {
      const { error } = await supabase.auth.updateUser({
        data: {
          name,
          image,
        },
      });

      if (error) {
        return { error: error.message };
      }

      // Update local state
      setAuthState(prev => ({
        ...prev,
        user: prev.user ? {
          ...prev.user,
          name,
          image: image || prev.user.image,
        } : null,
      }));

      return { error: null };
    } catch (error) {
      return { error: (error as Error).message };
    }
  }, []);

  // Context value
  const contextValue: AuthContextType = {
    ...authState,
    signup,
    signin,
    signout,
    getCurrentUser,
    updateProfile,
  };

  return (
    <AuthContext.Provider value={contextValue}>
      {children}
    </AuthContext.Provider>
  );
}

// Custom hook to use auth context
export function useAuth() {
  const context = useContext(AuthContext);

  if (context === defaultAuthContext) {
    throw new Error('useAuth must be used within an AuthProvider');
  }

  return context;
}

export { AuthContext, defaultAuthContext };

export default AuthProvider;