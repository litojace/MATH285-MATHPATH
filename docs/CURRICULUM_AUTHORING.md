# Curriculum authoring and validation

`src/content/curriculum.ts` records the user's 51 requested sections. The app
loads the complete generated lessons from `src/content/course-lessons.json`.
The eight previously published lesson IDs and all their exercise IDs are kept
so links, bookmarks, and saved attempts remain valid.

The explanations and exercises are original MathPath supplements. Differential
Equations PDF references identify related readings in the privately supplied
notes; they do not attribute our problems to the professor or certify every
handwritten solution. Linear Algebra now uses the readable 90-page
`LINEAR PROFESSOR V.pdf` to align methods and provide PDF page references.
The source PDFs remain private.

The authoring script contains definitions for every listed curriculum term,
topic-specific explanations and reasoning, and parameterized problem families.
Different families teach different operations or cases; coefficient variants
provide additional practice. Three worked examples use separate parameters
from the ten practice problems. Existing practice IDs retain their content.
Inner Product Spaces includes three additional examples and exercises about
weighted inner products and function-space projection.

To regenerate, install Python 3 and SymPy, then run from the repository root:

```sh
python3 scripts/build_curriculum.py
npm test
npm run build
npm run check:content
```

The full browser suite runs against a production build:

```sh
npx playwright install chromium
npm run test:e2e
```

When using an existing system Chromium, set
`PLAYWRIGHT_CHROMIUM_EXECUTABLE` to its executable path instead of installing
the Playwright browser. The suite checks all 51 pages at phone and desktop widths.

Generation stops on a failed symbolic assertion. Checks include substitution
into systems, inverse products, projection orthogonality, ODE residuals and
initial/boundary values, and forward Laplace transforms of inverse results.
The 673 newly authored problems' assertion records are saved in
`docs/curriculum-verification.json`. Tests check section coverage, numbering,
IDs, prerequisite resolution, all rendered LaTeX, and practice interactions.

Numeric, fractional, matrix, and choice questions have automatic checking.
General symbolic expressions use explicit self-assessment after revealing the
worked solution; the app does not pretend to automatically grade algebraically
equivalent formulas. Students can record whether their reasoning matches.

`scripts/linear_professor.py` supplies three detailed method-guide sections and
two additional example/practice families for each of the 27 Linear Algebra
lessons. It covers the professor's cryptograms, ODE solution spaces and
Wronskians, polynomial and matrix vector spaces, weighted and integral inner
products, and polynomial transformations. Each new problem instance uses exact
SymPy checks before it can be published. Its row-reduction helper records every
actual operation and independently compares the result with SymPy RREF.

PDF page numbers count from the first PDF page. Overlapping references reflect
sections that share a page. The PDF also includes sections 1.3 and 5.5, but the
owner's requested 27-section numbering is preserved. Three vectors are described
as a basis for their span, rather than for R⁴ or P₅. The characteristic polynomial
is the determinant of A−λI, and real and complex eigenvalue questions are
distinguished explicitly.
