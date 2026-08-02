/**
 * Type definitions for Supabase integration
 */

import type { User as SupabaseUser } from '@supabase/supabase-js';

// Database types
export interface Database {
  public: {
    Tables: {
      users: {
        Row: {
          id: string;
          email: string;
          hashed_password: string | null;
          is_active: boolean;
          is_admin: boolean;
          created_at: string | null;
          updated_at: string | null;
        };
        Insert: {
          id: string;
          email: string;
          hashed_password?: string | null;
          is_active?: boolean;
          is_admin?: boolean;
          created_at?: string | null;
          updated_at?: string | null;
        };
        Update: {
          id?: string;
          email?: string;
          hashed_password?: string | null;
          is_active?: boolean;
          is_admin?: boolean;
          created_at?: string | null;
          updated_at?: string | null;
        };
      };
      user_profiles: {
        Row: {
          id: string;
          user_id: string;
          name: string | null;
          age: number | null;
          height_cm: number | null;
          weight_kg: number | null;
          gender: string | null;
          fitness_level: 'beginner' | 'intermediate' | 'advanced';
          goals: 'strength' | 'endurance' | 'fat_loss' | 'general_fitness' | null;
          equipment: 'bodyweight' | 'dumbbells' | 'resistance_bands' | 'full_gym';
          available_days: number;
          available_time: number;
          receive_notifications: boolean;
          theme_preference: string;
          created_at: string;
          updated_at: string;
        };
        Insert: {
          id: string;
          user_id: string;
          name?: string | null;
          age?: number | null;
          height_cm?: number | null;
          weight_kg?: number | null;
          gender?: string | null;
          fitness_level?: 'beginner' | 'intermediate' | 'advanced';
          goals?: 'strength' | 'endurance' | 'fat_loss' | 'general_fitness' | null;
          equipment?: 'bodyweight' | 'dumbbells' | 'resistance_bands' | 'full_gym';
          available_days?: number;
          available_time?: number;
          receive_notifications?: boolean;
          theme_preference?: string;
          created_at?: string;
          updated_at?: string;
        };
        Update: {
          id?: string;
          user_id?: string;
          name?: string | null;
          age?: number | null;
          height_cm?: number | null;
          weight_kg?: number | null;
          gender?: string | null;
          fitness_level?: 'beginner' | 'intermediate' | 'advanced';
          goals?: 'strength' | 'endurance' | 'fat_loss' | 'general_fitness' | null;
          equipment?: 'bodyweight' | 'dumbbells' | 'resistance_bands' | 'full_gym';
          available_days?: number;
          available_time?: number;
          receive_notifications?: boolean;
          theme_preference?: string;
          created_at?: string;
          updated_at?: string;
        };
      };
      exercises: {
        Row: {
          id: string;
          name: string;
          description: string | null;
          muscle_groups: 'chest' | 'back' | 'shoulders' | 'biceps' | 'triceps' | 'core' | 'glutes' | 'quadriceps' | 'hamstrings' | 'calves' | 'full_body' | null;
          secondary_muscles: string | null;
          difficulty: 'beginner' | 'intermediate' | 'advanced';
          video_url: string | null;
          image_url: string | null;
          is_core_exercise: boolean;
          form_analysis_available: boolean;
          equipment_required: string;
          category: string;
          created_at: string;
          updated_at: string;
        };
      };
      workouts: {
        Row: {
          id: string;
          user_id: string;
          title: string;
          description: string | null;
          workout_type: string | null;
          total_duration: number | null;
          estimated_calories: number | null;
          is_completed: boolean;
          completed_at: string | null;
          rating: number | null;
          created_at: string;
          updated_at: string;
        };
      };
    };
    Views: {
      [_ in never]: never;
    };
    Functions: {
      [_ in never]: never;
    };
    Enums: {
      fitnesslevel: 'beginner' | 'intermediate' | 'advanced';
      fitnessgoal: 'strength' | 'endurance' | 'fat_loss' | 'general_fitness';
      equipmenttype: 'bodyweight' | 'dumbbells' | 'resistance_bands' | 'full_gym';
      difficultylevel: 'beginner' | 'intermediate' | 'advanced';
      musclegroup: 'chest' | 'back' | 'shoulders' | 'biceps' | 'triceps' | 'core' | 'glutes' | 'quadriceps' | 'hamstrings' | 'calves' | 'full_body';
    };
    CompositeTypes: {
      [_ in never]: never;
    };
  };
}

// User profile type for the application
export interface UserProfile {
  id: string;
  user_id: string;
  name: string | null;
  age: number | null;
  height_cm: number | null;
  weight_kg: number | null;
  gender: string | null;
  fitness_level: 'beginner' | 'intermediate' | 'advanced';
  goals: 'strength' | 'endurance' | 'fat_loss' | 'general_fitness' | null;
  equipment: 'bodyweight' | 'dumbbells' | 'resistance_bands' | 'full_gym';
  available_days: number;
  available_time: number;
  receive_notifications: boolean;
  theme_preference: string;
  created_at: string;
  updated_at: string;
}

// Exercise type
export interface Exercise {
  id: string;
  name: string;
  description: string | null;
  muscle_groups: 'chest' | 'back' | 'shoulders' | 'biceps' | 'triceps' | 'core' | 'glutes' | 'quadriceps' | 'hamstrings' | 'calves' | 'full_body' | null;
  secondary_muscles: string | null;
  difficulty: 'beginner' | 'intermediate' | 'advanced';
  video_url: string | null;
  image_url: string | null;
  is_core_exercise: boolean;
  form_analysis_available: boolean;
  equipment_required: string;
  category: string;
}

// Workout type
export interface Workout {
  id: string;
  user_id: string;
  title: string;
  description: string | null;
  workout_type: string | null;
  total_duration: number | null;
  estimated_calories: number | null;
  is_completed: boolean;
  completed_at: string | null;
  rating: number | null;
  created_at: string;
  updated_at: string;
}

// Type for Supabase authentication user
export interface AuthUser {
  id: string;
  email: string | null;
  name: string | null;
  image: string | null;
}

// Type for Supabase session
export interface AuthSession {
  access_token: string;
  refresh_token: string | null;
  user: AuthUser;
  expires_at: number;
  token_type: string;
}