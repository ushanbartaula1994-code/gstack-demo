/**
 * Constants for the AI Fitness Coach application
 */

// Application constants
export const APP_NAME = "AI Fitness Coach";
export const APP_DESCRIPTION = "Your personalized AI-powered workout companion";

// API constants
export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
export const API_TIMEOUT = 10000; // 10 seconds

// Core exercises for MVP (5 exercises with form analysis)
export const CORE_EXERCISES = [
  { id: "squat", name: "Squat", muscleGroups: ["quadriceps", "glutes", "hamstrings"] },
  { id: "push-up", name: "Push-up", muscleGroups: ["chest", "shoulders", "triceps"] },
  { id: "lunge", name: "Lunge", muscleGroups: ["quadriceps", "glutes", "hamstrings"] },
  { id: "plank", name: "Plank", muscleGroups: ["core", "shoulders", "back"] },
  { id: "glute-bridge", name: "Glute Bridge", muscleGroups: ["glutes", "hamstrings", "lower back"] },
] as const;

export type CoreExerciseId = (typeof CORE_EXERCISES)[number]["id"];

// Fitness levels
export const FITNESS_LEVELS = ["beginner", "intermediate", "advanced"] as const;
export type FitnessLevel = (typeof FITNESS_LEVELS)[number];

// Fitness goals
export const FITNESS_GOALS = [
  "strength",
  "endurance",
  "fat_loss",
  "general_fitness",
] as const;
export type FitnessGoal = (typeof FITNESS_GOALS)[number];

// Equipment options
export const EQUIPMENT_TYPES = [
  "bodyweight",
  "dumbbells",
  "resistance_bands",
  "full_gym",
] as const;
export type EquipmentType = (typeof EQUIPMENT_TYPES)[number];

// Workout durations (minutes)
export const WORKOUT_DURATIONS = [10, 15, 20, 30, 45, 60, 90] as const;

// Workout frequency (days per week)
export const WORKOUT_FREQUENCIES = [1, 2, 3, 4, 5, 6, 7] as const;

// Form analysis thresholds
export const FORM_ANALYSIS_PROFORM_ACCURACY_THRESHOLD = 80; // 80% accuracy threshold

// Subscription tiers
export const SUBSCRIPTION_TIERS = ["free", "premium"] as const;
export type SubscriptionTier = (typeof SUBSCRIPTION_TIERS)[number];

// Free tier limits
export const FREE_TIER_LIMITS = {
  WORKOUTS_PER_WEEK: 3,
  FORM_ANALYSIS: true, // Basic form analysis available
  ADVANCED_FEATURES: false,
};

// Premium tier limits
export const PREMIUM_TIER_LIMITS = {
  WORKOUTS_PER_WEEK: Infinity,
  FORM_ANALYSIS: true,
  ADVANCED_FEATURES: true,
};

// Storage keys
export const STORAGE_KEYS = {
  USER_TOKEN: "ai-fit-token",
  USER_PROFILE: "ai-fit-profile",
  ONBOARDING_COMPLETE: "ai-fit-onboarding",
  THEME: "ai-fit-theme",
};

// Navigation paths
export const PATHS = {
  HOME: "/",
  ONBOARDING: "/onboarding",
  WORKOUTS: "/workouts",
  WORKOUT: "/workouts/[id]",
  SESSION: "/sessions/[id]",
  PROGRESS: "/progress",
  SETTINGS: "/settings",
  SUBSCRIBE: "/subscribe",
};

// MediaPipe configuration
export const MEDIAPIPE_CONFIG = {
  DETECTION_CONFIDENCE: 0.5,
  TRACKING_CONFIDENCE: 0.5,
  MAX_FACES: 1,
};
