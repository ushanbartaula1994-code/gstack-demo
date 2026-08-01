# AI Fitness Coach - Frontend

AI-powered fitness coach web application built with Next.js, TypeScript, and React.

## Prerequisites

- Node.js 18+ 
- npm 9+
- Git

## Getting Started

```bash
# Install dependencies
npm install

# Run the development server
npm run dev

# Open [http://localhost:3000](http://localhost:3000) in your browser
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint
- `npm run lint:fix` - Fix ESLint issues
- `npm run format` - Format code with Prettier
- `npm run format:check` - Check code formatting
- `npm run type-check` - TypeScript type checking

## Project Structure

```
frontend/
├── src/
│   ├── app/           # Next.js App Router pages
│   ├── components/    # Reusable React components
│   ├── lib/           # Utility functions, hooks, constants
│   ├── styles/        # Global styles, CSS modules
│   └── types/         # TypeScript type definitions
├── public/            # Static assets
├── .eslint.config.mjs # ESLint configuration
├── .prettierrc        # Prettier configuration
├── next.config.ts     # Next.js configuration
├── tailwind.config.ts # Tailwind CSS configuration
├── tsconfig.json      # TypeScript configuration
└── package.json
```

## Technology Stack

- **Framework:** Next.js 16 (App Router)
- **Language:** TypeScript
- **Styling:** Tailwind CSS v4
- **Linting:** ESLint with Next.js config
- **Formatting:** Prettier with Tailwind plugin

## Environment Variables

Create a `.env.local` file in the project root:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Dependencies

- [Next.js](https://nextjs.org/)
- [React](https://react.dev/)
- [TypeScript](https://www.typescriptlang.org/)
- [Tailwind CSS](https://tailwindcss.com/)
- [ESLint](https://eslint.org/)
- [Prettier](https://prettier.io/)

## Folder Conventions

- **components/** - Reusable UI components
- **lib/** - Helper functions, custom hooks, API clients
  - Example: `lib/api.ts`, `lib/hooks.ts`, `lib/utils.ts`
- **styles/** - Additional styles beyond Tailwind
  - Example: `styles/globals.css` (already exists)
- **types/** - TypeScript interfaces and types
  - Example: `types/index.ts`, `types/api.ts`

## Coding Standards

This project follows:
- TypeScript best practices
- React best practices
- ESLint rules defined in `.eslint.config.mjs`
- Prettier formatting rules defined in `.prettierrc`

## License

Private - All rights reserved.
