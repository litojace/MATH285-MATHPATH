# Implementation status

## Completed

- Responsive React, TypeScript, Vite, and Tailwind foundation with light and dark modes
- Home, course, lesson, search, practice, dashboard, formula/source library, and not-found pages
- Eight schema-validated lessons with 24 worked examples and 80 exercises spanning beginner, intermediate, and challenge levels
- Two lesson sections: Learn and Practice & solutions; Tutor Mode and its teaching prompts/styles are removed
- 56 additional original MathPath exercises with progressive hints and complete hidden worked solutions; these are supplementary practice, not reproduced professor examples
- KaTeX notation, progressive hints, hidden solutions, safe numeric/fraction/matrix checking, and self-check support
- Interactive vector, transformation, projection, slope field, growth, Euler, oscillator, and phase portrait visualizations
- Local guest progress, bookmarks, review queue, documented mastery, and optional Supabase merge/sync code; legacy stored notes remain readable to preserve saved data
- CI, Render static-site blueprint, production build, content audit, and tests

## Pending curriculum

- The 51-section curriculum in `src/content/curriculum.ts` is an authoring plan. It is not published lesson content; section coverage and provisional source references still need review. The application currently contains eight substantive lessons, not 51 completed lessons.
- Remaining source-derived Differential Equations lessons and page-by-page handwritten solution verification
- Broader independently developed Linear Algebra curriculum
- Authentication UI for the optional Supabase integration
- Full browser end-to-end suite and deployment verification

## Known issues

- Plotly is loaded only when a visualization mounts, but its separate production chunk is large.
- A suspected notation issue in Differential Equations `8.6.pdf` page 1 is recorded in the content audit.
- Source PDFs are private and intentionally excluded from the public application.
