# My Next.js Application

A modern Next.js 15 application built with best practices, featuring a monorepo structure, TypeScript, Tailwind CSS, and scalable architecture.

## 🚀 Features

- **Next.js 15** - Latest version with App Router
- **TypeScript** - Full type safety with strict mode
- **Tailwind CSS** - Utility-first CSS framework with design system
- **Monorepo Structure** - Scalable workspace configuration with Turbo
- **Feature-based Architecture** - Self-contained feature modules
- **Component Library** - Reusable UI components with variants
- **Form Validation** - Zod schemas for type-safe forms
- **Modern Tooling** - ESLint, PostCSS, proper build configuration

## 📁 Project Structure

```
my-nextjs-/
├── apps/
│   └── web/                 # Main Next.js application
│       ├── src/
│       │   ├── app/         # App Router pages and layouts
│       │   ├── components/  # Reusable UI components
│       │   ├── features/    # Feature-based modules
│       │   ├── hooks/       # Custom React hooks
│       │   ├── lib/         # Utility functions and configurations
│       │   ├── providers/   # React context providers
│       │   ├── styles/      # Global styles and Tailwind config
│       │   ├── types/       # TypeScript type definitions
│       │   └── test/        # Testing utilities and mocks
│       └── public/          # Static assets
├── packages/                # Shared packages (future use)
├── package.json            # Root workspace configuration
├── turbo.json              # Turbo build system configuration
├── pnpm-workspace.yaml     # PNPM workspace configuration
└── README.md               # Project documentation
```

## 🛠️ Tech Stack

- **Framework**: Next.js 15
- **Language**: TypeScript 5
- **Styling**: Tailwind CSS 3
- **Package Manager**: PNPM
- **Build System**: Turbo
- **Linting**: ESLint
- **Form Validation**: Zod
- **Icons**: Lucide React
- **Utilities**: clsx, tailwind-merge

## 🚀 Getting Started

### Prerequisites

- Node.js 18+ 
- PNPM 8+

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd my-nextjs-
```

2. Install dependencies:
```bash
pnpm install
```

3. Start the development server:
```bash
pnpm dev
```

4. Open [http://localhost:3000](http://localhost:3000) in your browser.

## 📝 Available Scripts

- `pnpm dev` - Start development server
- `pnpm build` - Build for production
- `pnpm start` - Start production server
- `pnpm lint` - Run ESLint
- `pnpm install:all` - Install all workspace dependencies

## 🏗️ Architecture

### Route Groups
- `(app)` - Protected application routes
- `(auth)` - Authentication pages
- `(marketing)` - Public marketing pages

### Feature Modules
Each feature is self-contained with:
- `components/` - Feature-specific components
- `server/` - Server-side logic and API routes
- `schema.ts` - Zod validation schemas

### Component Library
Reusable UI components with:
- Consistent design system
- TypeScript interfaces
- Variant support
- Accessibility features

## 🎨 Design System

The application uses a comprehensive design system built with Tailwind CSS:

- **Colors**: CSS custom properties for theming
- **Typography**: Consistent font scales
- **Spacing**: Standardized spacing system
- **Components**: Reusable UI components with variants

## 🔧 Configuration

### TypeScript
- Strict mode enabled
- Path mapping for clean imports
- Next.js specific configurations

### ESLint
- Next.js recommended rules
- TypeScript support
- Import sorting

### Tailwind CSS
- Custom color palette
- Component variants
- Dark mode support
- Responsive design utilities

## 🧪 Testing

The project includes testing infrastructure:
- Unit test setup
- E2E test configuration
- Mock handlers for API testing

## 📦 Deployment

The application is configured for deployment on:
- Vercel (recommended)
- Netlify
- Any Node.js hosting platform

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the documentation
- Review the code examples

---

Built with ❤️ using Next.js 15 and modern web technologies.
