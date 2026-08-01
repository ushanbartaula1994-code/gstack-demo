// Common types for the AI Fitness Coach application

// User and Authentication types
export interface User {
  id: string;
  email: string;
  name?: string;
  createdAt: string;
  updatedAt: string;
}

export interface AuthUser extends User {
  token: string;
}

// Fitness Profile types
export type FitnessLevel = "beginner" | "intermediate" | "advanced";
export type FitnessGoal = "strength" | "endurance" | "fat_loss" | "general_fitness";
export type EquipmentType = "bodyweight" | "dumbbells" | "full_gym";

export interface FitnessProfile {
  id: string;
  userId: string;
  goals: FitnessGoal[];
  equipment: EquipmentType[];
  fitnessLevel: FitnessLevel;
  availableDays: number; // Days per week
  availableTime: number; // Minutes per workout
  createdAt: string;
  updatedAt: string;
}

// Exercise types
export interface Exercise {
  id: string;
  name: string;
  description: string;
  muscleGroups: string[];
  difficulty: FitnessLevel;
  videoUrl?: string;
  createdAt: string;
}

// Workout types
export interface WorkoutExercise {
  id: string;
  exerciseId: string;
  exercise: Exercise;
  sets: number;
  reps: number;
  restTime: number; // seconds
  order: number;
}

export interface Workout {
  id: string;
  userId: string;
  title: string;
  description?: string;
  exercises: WorkoutExercise[];
  createdAt: string;
  completedAt?: string;
}

// Workout Session types
export interface FormAnalysisEvent {
  id: string;
  sessionId: string;
  exerciseId: string;
  poseData: unknown; // Will be defined based on MediaPipe output
  feedback: string;
  accuracy: number; // 0-100
  timestamp: string;
}

export interface WorkoutSession {
  id: string;
  workoutId: string;
  userId: string;
  startedAt: string;
  completedAt?: string;
  duration: number; // seconds
  calories?: number;
  formAnalysisEvents: FormAnalysisEvent[];
}

// Progress tracking types
export interface ProgressMetrics {
  id: string;
  userId: string;
  date: string;
  workoutsCompleted: number;
  totalDuration: number;
  averageFormScore?: number;
  streaks: number;
}

// API Response types
export interface ApiResponse<T> {
  data: T;
  message?: string;
  success: boolean;
}

export interface ApiError {
  message: string;
  errors?: Record<string, string[]>;
}

// Form analysis types
export interface FormFeedback {
  isCorrect: boolean;
  errors: string[];
  suggestions: string[];
  score: number; // 0-100
}

// Subscription types
export type SubscriptionTier = "free" | "premium";

export interface Subscription {
  id: string;
  userId: string;
  tier: SubscriptionTier;
  status: "active" | "canceled" | "past_due";
  currentPeriodEnd: string;
  createdAt: string;
}
