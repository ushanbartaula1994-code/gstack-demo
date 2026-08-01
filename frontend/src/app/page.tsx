import Link from "next/link";

export default function Home() {
  return (
    <div className="flex flex-col min-h-screen bg-zinc-50 dark:bg-black">
      <main className="flex-1 flex flex-col items-center justify-center p-8">
        <div className="text-center max-w-2xl">
          <h1 className="text-5xl font-bold mb-4 bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            AI Fitness Coach
          </h1>
          <p className="text-xl text-zinc-600 dark:text-zinc-400 mb-8">
            Your personalized AI-powered workout companion
          </p>
          <div className="flex gap-4 justify-center">
            <Link
              href="/onboarding"
              className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors"
            >
              Get Started
            </Link>
            <Link
              href="/about"
              className="px-6 py-3 border border-zinc-300 hover:bg-zinc-100 dark:border-zinc-600 dark:hover:bg-zinc-800 text-zinc-900 dark:text-zinc-50 rounded-lg font-medium transition-colors"
            >
              Learn More
            </Link>
          </div>
        </div>

        <div className="mt-16 text-center text-sm text-zinc-500 dark:text-zinc-400">
          <p>Built with Next.js, TypeScript, and Tailwind CSS</p>
        </div>
      </main>
    </div>
  );
}
