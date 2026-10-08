# Implementation status

## Completed

- Responsive React, TypeScript, Vite, and Tailwind foundation with light and dark modes
- Home, course, lesson, search, practice, dashboard, formula/source library, and not-found pages
- All 51 requested sections: 27 Linear Algebra and 24 Differential Equations lessons, preserving the professor's chapter and section numbering
- 156 worked examples and 513 exercises, with at least three examples and ten exercises per lesson
- Two lesson sections: Learn and Practice & solutions; Tutor Mode and its teaching prompts/styles are removed
- Original MathPath explanations, definitions, formulas, common mistakes, prerequisite links, and course-note reading references where available
- 565 newly authored exercises/examples checked using SymPy; reproducible authoring script and mathematical check records in `scripts/build_curriculum.py` and `docs/curriculum-verification.json`
- KaTeX notation, progressive hints, hidden solutions, safe numeric/fraction/matrix checking, and self-check support
- Interactive vector, transformation, projection, slope field, growth, Euler, oscillator, and phase portrait visualizations
- Local guest progress, bookmarks, review queue, documented mastery, and optional Supabase merge/sync code; legacy stored notes remain readable to preserve saved data
- CI, Render static-site blueprint, production build, content audit, and tests

## Remaining work

- Page-by-page review of the professor's handwritten solutions; published problems are original supplements rather than transcriptions of unverified handwritten work
- Authentication UI for the optional Supabase integration
- Live Render deployment verification (the environment proxy prevents access to the public custom domain)

## Known issues

- Plotly is loaded only when a visualization mounts, but its separate production chunk is large.
- A suspected notation issue in Differential Equations `8.6.pdf` page 1 is recorded in the content audit.
- Source PDFs are private and intentionally excluded from the public application.
