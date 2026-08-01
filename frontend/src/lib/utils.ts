/**
 * Utility functions for the AI Fitness Coach application
 */

/**
 * Format a date to a readable string
 */
export function formatDate(date: string | Date): string {
  return new Date(date).toLocaleDateString("en-US", {
    year: "numeric",
    month: "long",
    day: "numeric",
  });
}

/**
 * Format time duration in seconds to mm:ss
 */
export function formatDuration(seconds: number): string {
  const mins = Math.floor(seconds / 60);
  const secs = seconds % 60;
  return `${mins}:${secs.toString().padStart(2, "0")}`;
}

/**
 * Capitalize the first letter of a string
 */
export function capitalize(str: string): string {
  return str.charAt(0).toUpperCase() + str.slice(1);
}

/**
 * Generate a random ID
 */
export function generateId(): string {
  return Math.random().toString(36).substring(2) + Date.now().toString(36);
}

/**
 * Debounce a function
 */
export function debounce<T extends (...args: Parameters<T>) => ReturnType<T>>(
  func: T,
  wait: number
): (...args: Parameters<T>) => void {
  let timeoutId: ReturnType<typeof setTimeout> | null = null;

  return (...args: Parameters<T>) => {
    if (timeoutId) {
      clearTimeout(timeoutId);
    }
    timeoutId = setTimeout(() => {
      func(...args);
    }, wait);
  };
}

/**
 * Format a number as a percentage
 */
export function formatPercentage(value: number, decimals = 0): string {
  return `${(value * 100).toFixed(decimals)}%`;
}

/**
 * Calculate calories burned based on workout duration and intensity
 * Simple estimation for MVP
 */
export function estimateCalories(
  durationMinutes: number,
  intensity: "low" | "medium" | "high" = "medium"
): number {
  const multipliers: Record<"low" | "medium" | "high", number> = {
    low: 3,
    medium: 5,
    high: 7,
  };
  return Math.round(durationMinutes * multipliers[intensity]);
}

/**
 * Get difficulty level color for UI
 */
export function getDifficultyColor(
  difficulty: "beginner" | "intermediate" | "advanced"
): string {
  const colors: Record<"beginner" | "intermediate" | "advanced", string> = {
    beginner: "text-green-600 bg-green-100 dark:bg-green-900/30",
    intermediate: "text-yellow-600 bg-yellow-100 dark:bg-yellow-900/30",
    advanced: "text-red-600 bg-red-100 dark:bg-red-900/30",
  };
  return colors[difficulty];
}

/**
 * Format workout time display
 */
export function formatWorkoutTime(minutes: number): string {
  if (minutes < 60) {
    return `${minutes} min`;
  }
  const hours = Math.floor(minutes / 60);
  const mins = minutes % 60;
  return mins > 0 ? `${hours}h ${mins}m` : `${hours}h`;
}
