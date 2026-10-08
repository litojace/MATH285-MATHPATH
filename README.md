# MathPath

MathPath is a responsive learning platform for Linear Algebra and Differential Equations. It teaches from intuition to notation, provides progressive hints and hidden step-by-step solutions, and records guest progress locally.

## Development

Requires Node.js 22 or newer.

```bash
npm ci
npm run dev
```

Open the local URL shown by Vite. Run `npm test`, `npm run check:content`, and `npm run build` before publishing.

## Content

Lessons are structured and validated at startup with Zod. Current content is independently written supplementary material; the precise status is recorded in [docs/CONTENT_AUDIT.md](docs/CONTENT_AUDIT.md). The mastery model is documented in [docs/MASTERY.md](docs/MASTERY.md).

Original instructor PDFs are private source material and are excluded from Git. Do not add them to `public/course-notes` or publish them without the owner's explicit redistribution permission.

## Optional Supabase sync

Guest mode needs no configuration. To enable authenticated sync, create the table and policies in [docs/SUPABASE.sql](docs/SUPABASE.sql), then provide `VITE_SUPABASE_URL` and `VITE_SUPABASE_ANON_KEY`. Never expose a service-role key to the browser.

## Render deployment

The included `render.yaml` defines a Vite static site with an SPA rewrite. The build command is `npm ci && npm run build`, and the publish directory is `dist`.

No license has been selected; the repository owner should choose one before public release.
