# MathPath content audit

Status date: October 8, 2026

MathPath publishes all 51 requested sections as original supplementary lessons: 27 Linear Algebra and 24 Differential Equations. Each has at least three worked examples and ten exercises. There are 210 examples and 567 exercises in total. Every Linear Algebra lesson also has three detailed method-guide sections, at least five examples, and at least twelve exercises. The professor's skipped chapter and section numbers are preserved.

The 43 new lesson pages include topic-specific explanations, definitions, reasoning, formulas, common mistakes, prerequisites, and original problems. The eight previously published IDs and their existing exercise content remain available. Function-space and weighted-inner-product problems extend the Inner Product Spaces lesson.

`python3 scripts/build_curriculum.py` uses SymPy assertions for 673 new examples and exercises. The records are in `docs/curriculum-verification.json`. The previously published examples and exercises retain their earlier mathematical review and regression checks. Formulas are also validated with KaTeX. See [Curriculum authoring](CURRICULUM_AUTHORING.md) for reproduction instructions.

Reading references locate related Linear Algebra and Differential Equations material by file and page. They identify readings rather than the origin of the independently authored examples and exercises. No lesson claims to transcribe or certify unreviewed handwritten work.

## Private Differential Equations source inventory

The supplied archive contains all 14 expected PDFs and 106 pages. Text extraction works, but handwritten work must be checked visually page by page. The PDFs are kept outside the repository and excluded from public deployment.

Identified material includes sections 1.1, 2.2–2.5, 4.1, 4.3–4.6, 6.1–6.2, 7.1–7.5, 8.3, 8.5–8.6, and 9.2. These topics now have dedicated original lessons with matching reading references.

### Review flag

`8.6.pdf`, page 1, prints the system as `X′ = A(t)X` while applying the eigenvector–exponential theorem in a form that requires a constant coefficient matrix `A`. This is recorded as a suspected notation error pending full mathematical review.

## Private Linear Algebra source inventory

`LINEAR PROFESSOR V.pdf` is a readable, unencrypted 90-page document supplied on October 8, 2026. Its printed text provides section boundaries, theorems, and unsolved example prompts. It is stored outside the repository. All 27 requested sections now have matching page references and original extended explanations and problems.

Coverage includes cryptograms in 2.6, ODE solution spaces and Wronskians in 4.8, integral Gram–Schmidt, and matrix-to-polynomial transformations. Corrections distinguish a basis for a three-dimensional span from a basis for R⁴ or P₅, use det(A−λI) for the characteristic polynomial, and explicitly address complex eigenvalues. Sections 1.3 and 5.5 in the PDF remain outside the requested curriculum.

## Current limitations

- Full visual verification of every handwritten solution remains separate from the independently checked MathPath problems.
- Automatic grading of general symbolic expressions is not implemented; those questions provide complete solutions and explicit self-assessment.
