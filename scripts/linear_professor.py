"""Original explanations and problems aligned to LINEAR PROFESSOR V.pdf.

The private 90-page PDF supplies the section boundaries and method coverage.
These are newly authored supplements, not transcriptions of its exercises.
"""
import sympy as S

READINGS = {
 '1.1':(1,2),'1.2':(3,5),'2.1':(7,9),'2.2':(10,13),'2.3':(14,17),
 '2.4':(18,20),'2.6':(20,21),'3.1':(22,24),'3.2':(25,26),
 '3.3':(26,29),'3.4':(29,31),'4.1':(32,34),'4.2':(35,38),
 '4.3':(38,38),'4.4':(39,43),'4.5':(44,46),'4.6':(47,51),
 '4.7':(52,55),'4.8':(56,57),'5.1':(58,62),'5.2':(63,67),
 '5.3':(68,71),'6.1':(73,74),'6.2':(75,78),'6.3':(79,85),
 '6.4':(86,87),'7.1':(88,90),
}

# Each guide explains a decision, its mechanism, and how to check the result.
GUIDES = {
 '1.1':[
 ('Recognize what the system is asking', 'An equation imposes one condition on an entire ordered tuple. A solution must satisfy every condition at once, with the variables in the stated order. Linear means each variable appears only to the first power, with constant coefficients: products such as xy and functions such as sin(x) are excluded. A missing variable has coefficient zero. Before calculating, identify the variables, coefficients, and constant terms; do not confuse a coefficient that happens to be zero with an extra unknown.'),
 ('Why elimination preserves solutions', 'Swapping equations changes their order, not their requirements. Multiplying an equation by a nonzero scalar changes its appearance but can be undone by dividing. Replacing one equation by itself plus a multiple of another can also be undone. These reversible operations preserve exactly the same solution set. Multiplying by zero is forbidden because it can erase a condition. Write the operation next to each new system so you can explain why the transformed system is equivalent.'),
 ('Interpret the final equations', 'A contradictory equation, such as 0=5, makes the whole system inconsistent. An identity, such as 0=0, contributes no new condition. In a consistent system, a variable not determined by a leading equation becomes a parameter. State the full family of ordered tuples, not just one convenient member. With a parameter in the coefficients, separate any exceptional value before dividing by an expression involving that parameter; the exceptional case can change the number of solutions.'),
 ],
 '1.2':[
 ('Translate the system into an augmented matrix', 'Choose one variable order and keep it for every row. Enter a zero wherever a variable is absent; put the constants in the last column. The vertical bar separates coefficients from constants, but row operations act on the whole row, including the constants. A row operation is not a column operation: swapping coefficient columns changes the meaning of the variables unless you track that permutation separately.'),
 ('Build pivots in the professor’s convention', 'The notes use leading ones in row-echelon form. Some textbooks allow other nonzero pivots in REF, but we normalize them here. Find a nonzero entry in the next usable column, swap it into position if necessary, scale its row to make the pivot one, then eliminate entries below it. Continue to the right and downward, leaving zero rows at the bottom. Keep fractions exact rather than rounding; early decimals can hide an exact contradiction.'),
 ('Choose back-substitution or full reduction', 'Gaussian elimination stops at echelon form, then solves from the last nonzero row upward. Gauss–Jordan elimination also clears entries above every pivot, producing RREF. Either method must inspect the augmented column for contradictions before assigning parameters. In a consistent system, assign one parameter to each nonpivot variable and express pivot variables in terms of them. A homogeneous system always contains the zero solution; it has nonzero solutions precisely when at least one variable is free.'),
 ],
 '2.1':[
 ('Use dimensions to decide whether an operation exists', 'Addition and subtraction require matching shapes because they compare corresponding entries. For multiplication, the number of columns of the first matrix must equal the number of rows of the second. The outside dimensions give the shape of the answer. Write these sizes before doing arithmetic. Matrix equality requires both the same shape and equality of every corresponding entry; an equation between matrices therefore represents several scalar equations.'),
 ('Understand a row–column product', 'To compute entry (i,j) of AB, pair row i of A with column j of B, multiply the matching entries, and add. This sum combines all intermediate contributions from the shared index. It is not entrywise multiplication. A rectangular product can be defined in one order and undefined in the reverse order. Even when both orders exist, they may have different shapes or different entries. Calculate one complete row of the answer at a time to avoid losing positions.'),
 ('Read matrix equations and transposes', 'The jth column of A is the output A sends the jth standard basis vector to. Consequently Ax is a linear combination of A’s columns with weights taken from x. This connects multiplication directly to systems. A transpose exchanges row and column roles, so its dimensions reverse. For a product, the factor order also reverses under transposition. Check a computed matrix-vector result by writing out its row equations and substituting the proposed vector.'),
 ],
 '2.2':[
 ('Keep the valid algebra rules', 'Associativity lets you move parentheses in a defined product, while distributivity lets you expand sums without changing factor order. It does not let you rearrange factors. Identity matrices must have the appropriate sizes: the identity on the left acts on rows and the identity on the right acts on columns. When proving a rule, compare the general (i,j) entry on both sides rather than verifying only one numerical example.'),
 ('Know why cancellation can fail', 'Nonzero matrices can multiply to the zero matrix. Likewise AC=BC need not imply A=B: the matrix C may erase the directions in which A and B differ. This is why scalar cancellation cannot be imported automatically. If C is invertible, right multiplication by its inverse restores cancellation. Without an inverse, give an explicit counterexample or analyze the null directions instead of dividing by a matrix.'),
 ('Handle transpose and symmetry carefully', 'A symmetric matrix is square and equals its transpose. The transpose of AB is BᵀAᵀ because rows become columns and the intermediate indices exchange roles. Even when A and B are symmetric, their product need not be symmetric: its transpose is BA, so AB is symmetric exactly when the two factors commute. To disprove a universal rule, one counterexample is enough; to prove it, arbitrary matrices of compatible dimensions must be considered.'),
 ],
 '2.3':[
 ('An inverse undoes a transformation', 'For a square matrix A, an inverse must undo multiplication on both sides. It is not formed by taking reciprocals of individual entries. A singular matrix loses information, so two inputs can share an output and no operation can recover every original input. For a square matrix, an invertible matrix has a unique solution for every right-hand side. A determinant test is useful after Chapter 3, but row reduction already gives an inverse test here.'),
 ('Explain the augmented-matrix algorithm', 'Start with [A|I]. Every row operation is left multiplication by an elementary matrix, and it must be applied across both blocks. If the accumulated operations turn the left block into I, their product E satisfies EA=I and the right block records E. Thus that right block is A⁻¹. If the left block develops a missing pivot and cannot become I, stop: the matrix is singular. Show intermediate augmented matrices so the procedure can be reproduced.'),
 ('Use inverses in the correct order', 'In AX=b, multiply on the left by A⁻¹ to obtain X=A⁻¹b. In XA=B, multiply on the right. To undo a product AB, first undo B and then A, so its inverse is B⁻¹A⁻¹. Prove an inverse claim by multiplying it with the original matrix and obtaining I; also substitute a proposed system solution into AX=b. Computing an inverse is useful for several right-hand sides, though elimination is often quicker for a single system.'),
 ],
 '2.4':[
 ('Construct one elementary matrix per operation', 'An elementary matrix is obtained by performing exactly one allowed row operation on an identity matrix. The same operation is then performed on any compatible A by multiplying EA on the left. Right multiplication instead acts on columns and has a different interpretation. To recognize an elementary matrix, compare it with I and identify the one swap, one nonzero scaling, or one row replacement that produced it.'),
 ('Track the order of several operations', 'If E₁ is applied first and E₂ second, the final result is E₂E₁A. The newest operation appears farthest left. Record both the operation and its elementary matrix at every step. The inverse of a swap is the same swap; the inverse of scaling by c is scaling by 1/c; the inverse of adding c times another row is subtracting that multiple. These observations explain why elementary matrices preserve row equivalence.'),
 ('Recover a factorization and test special properties', 'If a sequence reduces A to I, then Eₖ⋯E₁A=I. Solve for A by reversing the order and inverting each factor. This expresses every invertible square matrix as a product of elementary matrices. Separately, the notes discuss idempotence: A²=A means applying A twice has the same effect as once. Idempotent does not mean identity or invertible. A nontrivial projection can be idempotent and singular, while a row-swap matrix generally squares to I rather than to itself.'),
 ],
 '2.6':[
 ('Turn letters into numerical blocks', 'The notes use 0 for a space and 1 through 26 for A through Z. Replace each character by its number, preserving spaces, then divide the sequence into row vectors of the chosen block length. Pad the final block with zeroes if needed and explain the padding. This is a teaching model for matrix operations, not a modern secure encryption system. Its purpose is to show how an invertible matrix can change and recover numerical information.'),
 ('Encode from the right', 'For a row message block r, the encoded block is c=rA. The order matters: A must have as many rows and columns as the block length. Compute each output entry by pairing r with the appropriate column of A. Encoded entries can exceed 26 or be negative; they are numbers to transmit, not letters to decode immediately. Using the same matrix for every block gives a consistent encoding rule.'),
 ('Decode and verify the complete message', 'Choose an invertible encoding matrix so information can be recovered. From c=rA, multiply on the right by A⁻¹ to obtain r=cA⁻¹. Keep exact fractions during inversion; valid original letter blocks should recover exact integers. Translate those integers back to characters and remove only the padding that was deliberately added. Verify a recovered block by encoding it again. A singular encoding matrix can collapse different blocks to the same output and cannot guarantee unique decoding.'),
 ],
 '3.1':[
 ('Separate a determinant from a matrix', 'A determinant is one scalar associated with a square matrix, not a new matrix. For a 2×2 matrix it is the difference of two cross-products. That shortcut does not extend to an arbitrary matrix size. Geometrically, the determinant gives signed area or volume scaling; a zero value means at least one direction has collapsed. The sign contains orientation information, while the absolute value gives the volume factor.'),
 ('Build minors and cofactors', 'The minor Mᵢⱼ is the determinant left after deleting row i and column j. The cofactor adds the alternating sign (−1)^(i+j). Draw the checkerboard sign pattern before expanding, especially when entries are already negative. A minor is itself a determinant, so a 3×3 expansion produces 2×2 calculations. Keep the deleted row and column distinct from the entry multiplying that minor.'),
 ('Choose an efficient expansion', 'Cofactor expansion works along any one row or any one column; choose one with many zeroes. Each term is the original entry times its cofactor. Do not sum expansions from multiple rows. For a triangular matrix, the determinant is the product of the diagonal entries, because all other permutation contributions vanish. Check a larger determinant using a different expansion or row operations; two methods help catch an isolated sign error.'),
 ],
 '3.2':[
 ('Attach a determinant effect to each operation', 'Swapping two rows changes the determinant’s sign. Scaling one row by c multiplies the determinant by c. Adding a multiple of one row to another leaves it unchanged. These rules also hold for columns. Write the factor or sign beside every operation; otherwise an easy triangular determinant can still produce the wrong original answer. Scaling an entire n×n matrix is n separate row scalings, not one.'),
 ('Reduce to triangular form without unnecessary fractions', 'Use row replacements to create zeroes below a diagonal entry, moving a nonzero pivot into place when needed. Unlike RREF, determinant calculation does not require normalized pivots or clearing entries above them. Fraction-free row replacements often keep the arithmetic shorter. Once the matrix is triangular, multiply its diagonal entries, then undo the recorded scaling factors and signs to recover the determinant of the original matrix.'),
 ('Use structure before doing a full elimination', 'A zero row, a zero column, or two proportional rows force a zero determinant. If one column has just one nonzero entry, cofactor expansion can reduce a 4×4 calculation to 3×3 immediately. A zero pivot alone does not prove singularity: first check whether a swap can supply a pivot. For a parameter-dependent pivot, keep its exceptional zero case separate instead of dividing through it and silently losing that case.'),
 ],
 '3.3':[
 ('Distinguish product, transpose, and sum rules', 'For same-size square matrices, det(AB)=det(A)det(B), and transposing leaves the determinant unchanged. In contrast, there is no general rule det(A+B)=det(A)+det(B). Before using an identity, check its hypotheses and the operation involved. You can compute a product determinant without computing the entire product, which is especially helpful when matrices are large but their individual determinants are known.'),
 ('Track dimension when scaling or inverting', 'Multiplying an n×n matrix by c scales all n rows, so the factor is cⁿ. Inverting requires a nonzero determinant and changes that determinant to its reciprocal. Combining these rules lets you evaluate expressions such as det(cA⁻¹Bᵀ) in stages. State the matrix size explicitly; a missing exponent is a common source of otherwise plausible answers. Never write an inverse determinant formula for a singular matrix.'),
 ('Find all singular parameter values', 'Treat the determinant as a polynomial in the parameter and solve det(A)=0. Factor the polynomial before solving; a quadratic or cubic can give several exceptional values. Those values are exactly where the square matrix ceases to be invertible. Check each proposed value by substitution into the polynomial, and establish that no other roots exist. A determinant zero classifies the matrix, but it does not by itself classify every system Ax=b; consistency also depends on b.'),
 ],
 '3.4':[
 ('Construct the adjugate in two stages', 'First calculate every cofactor, including its sign. Then transpose the whole cofactor matrix to obtain the adjugate, called the adjoint in these notes. This use of adjoint is different from the conjugate transpose terminology sometimes used in complex linear algebra. Do not skip the transpose. The identity A adj(A)=det(A)I explains why dividing the adjugate by a nonzero determinant yields the inverse.'),
 ('Use Cramer’s Rule under its hypotheses', 'For n equations in n unknowns, check that the coefficient determinant is nonzero. To compute xᵢ, replace column i of A with the entire constant vector b, leaving every other column unchanged. Divide that new determinant by det(A). Replacing a row is the wrong operation. Cramer’s Rule is useful for deriving a formula or finding one particular component; for large systems, elimination usually involves less computation.'),
 ('Do not apply the formula across a zero denominator', 'If det(A)=0, Cramer’s Rule cannot be used to conclude that the system has no solution. A singular system can instead have infinitely many solutions, or none. Return to the augmented matrix and examine its row reduction. For a computed inverse, verify the adjugate identity; for a computed solution, substitute into the original equations. These checks test the actual mathematical statement rather than just the last arithmetic line.'),
 ],
 '4.1':[
 ('Treat a vector as an ordered object', 'In Rⁿ, a vector has n real coordinates in a fixed order. Addition and scalar multiplication act coordinate by coordinate. A row display and a column display may describe the same coordinates informally, but matrix products require the correct orientation. Higher dimensions use the same arithmetic even when a picture is unavailable. Equality means every coordinate agrees, so one vector equation can be expanded into n scalar equations.'),
 ('Recognize a linear-combination question', 'To express w as a combination of v₁ through vₖ, introduce one unknown coefficient per vector, then place those vectors in the columns of a matrix. Solve Ac=w. A consistent coefficient system proves membership in the span; an inconsistent one proves nonmembership. The coefficients describe the combination, not the coordinates of the input vectors themselves. Keep the entire coefficient tuple, including any free parameters.'),
 ('Use the answer to explain the geometry', 'One nonzero vector spans a line through the origin. Two independent vectors span a plane through the origin, even inside R⁴ or R⁵. A third vector already in that plane adds no new direction. Reconstruct the target from your computed coefficients as a final check. A negative coefficient reverses a direction and a zero coefficient omits it; neither is a failure of the linear-combination idea.'),
 ],
 '4.2':[
 ('Specify both the set and the operations', 'A vector space consists of objects together with rules for adding them and multiplying them by scalars. Those objects can be tuples, polynomials, matrices, or functions. The usual real vector-space axioms apply only after the scalar field and operations have been stated. With unusual addition, even the zero vector may look unfamiliar. Do not assume that a set is a vector space merely because its elements resemble vectors.'),
 ('Prove a failure with one concrete example', 'A vector space must satisfy all ten axioms. To disprove the claim, it is enough to exhibit one failed axiom and specific allowed inputs. The integers fail closure under real scalar multiplication, because half of 1 is not an integer. Polynomials of exactly degree two fail the zero-vector requirement and can add to a lower degree. Polynomials of degree at most two include these lower-degree results and do form P₂.'),
 ('Prove a positive claim without checking only samples', 'For the usual operations on Rⁿ, matrices, and Pₙ, verify closure for arbitrary elements and explain why the algebraic laws hold coordinatewise. If operations are changed, test identities directly with arbitrary symbols before invoking familiar rules. For example, a subtraction-based second coordinate can destroy commutativity. A translated set may form a vector space with specially defined operations, but that does not make it a subspace under the usual operations.'),
 ],
 '4.3':[
 ('Use the ambient vector space to shorten the proof', 'A subspace inherits its operations from an already established vector space. It therefore inherits the associative and distributive laws; the main work is proving it contains zero and is closed under addition and scalar multiplication. Begin with arbitrary members, not numerical samples. A homogeneous linear constraint is preserved under linear combinations because applying its left-hand side to au+bv gives a times the first zero plus b times the second zero.'),
 ('Distinguish a linear constraint from a nonlinear one', 'A plane ax+by+cz=0 passes through the origin and is a subspace. Replacing zero by a nonzero constant makes an affine plane that fails the zero test. Conditions such as xy=0 can contain zero and still fail addition. Similarly, idempotent matrices satisfy A²=A, but the set of all such matrices is not closed under arbitrary scaling. Passing one test is not enough; a single counterexample to either closure condition settles a negative result.'),
 ('Parameterize and find spanning directions', 'After proving a set is a subspace, solve its defining constraints to express a general element using free parameters. Separate the coefficients of those parameters into vectors. These vectors span the set, and pivot or coordinate arguments can show they are independent. For polynomial constraints, translate values such as p(1)=0 into equations on coefficients. This links the abstract subspace test to the concrete row-reduction methods already learned.'),
 ],
 '4.4':[
 ('Solve two different matrix questions', 'For spanning, ask whether every target w can be produced by Ac=w. For independence, ask whether Ac=0 has any nonzero coefficient solution. Both use the same column matrix A, but the right-hand side changes the question. In Rⁿ, spanning requires a pivot in every row; independence requires a pivot in every column. A rectangular matrix can satisfy one condition without the other.'),
 ('Interpret a dependence relation', 'If c₁v₁+⋯+cₖvₖ=0 with at least one nonzero coefficient, solve for a vector whose coefficient is nonzero. That vector is redundant because it lies in the span of the others. A set containing the zero vector is automatically dependent. More than n vectors in Rⁿ are dependent because a coefficient matrix with n rows cannot have more than n pivots. Fewer than n vectors cannot span all of Rⁿ.'),
 ('Transfer the method to polynomials and matrices', 'Use a fixed coordinate system for the ambient space. For P₂, send a+bx+cx² to (a,b,c), including zero coefficients for absent powers. For a 2×2 matrix, use a consistent order such as (a₁₁,a₁₂,a₂₁,a₂₂). Assemble these coordinate vectors as columns and reduce. A dependence relation in coordinates is the same relation between the original objects, so translate the result back into polynomials or matrices to explain it.'),
 ],
 '4.5':[
 ('A basis must meet two requirements', 'A basis both spans the space and is independent. Spanning ensures every object can be expressed; independence ensures its coefficients are unique. Two different coefficient lists for the same vector would subtract to a nontrivial dependence relation. In an n-dimensional space, an independent set of n vectors is automatically a basis, as is a spanning set of n vectors. This shortcut requires knowing the dimension first.'),
 ('Extract a basis from a redundant list', 'Put the candidate vectors into columns and row-reduce. The pivot positions tell you which original vectors to retain. Row operations preserve relations among columns, but they change the columns themselves, so a basis for the original span uses original pivot columns. Alternatively, when a subspace is described by constraints, use free parameters to construct a basis. State the ambient space and the dimension of the resulting subspace separately.'),
 ('Count dimensions in abstract spaces', 'Pₙ has n+1 basis vectors 1,x,…,xⁿ because the constant coefficient is an independent coordinate too. Mₘₓₙ has mn independent entry positions. Symmetric n×n matrices have n(n+1)/2 independent entries, while constraints can reduce that count further. The dimension measures independent parameters, not the largest exponent or the number of displayed rows. Check a proposed basis by reconstructing an arbitrary object and showing its coefficients are uniquely determined.'),
 ],
 '4.6':[
 ('Keep the three fundamental spaces distinct', 'For an m×n matrix, the column space lies in Rᵐ, while the row space and null space lie in Rⁿ. Rank is the common dimension of row space and column space. Row reduction preserves the row space, so nonzero echelon rows supply a row-space basis. For the column space, take pivot columns of the original matrix. Reducing first and then copying reduced columns generally gives the wrong original column space.'),
 ('Build a null-space basis from free variables', 'Solve Ax=0 and assign one parameter to each free variable. Write the solution as a sum of parameter multiples of fixed vectors; those vectors form a null-space basis. Each must independently satisfy Ax=0, and their number must equal n minus rank. Rank-nullity counts input dimensions: use the number of columns, not rows. A rectangular map can have full row rank and still have a nontrivial null space.'),
 ('Connect these spaces to a nonhomogeneous system', 'Ax=b is consistent exactly when b lies in the column space, equivalently when augmenting with b does not increase rank. For a consistent system, find one particular solution xₚ and add every null-space vector. The resulting affine set xₚ+ker(A) generally is not a vector subspace unless b=0. If there are free variables, do not report the particular solution alone as the complete solution set.'),
 ],
 '4.7':[
 ('Keep a vector separate from its coordinates', 'An ordered basis labels a coordinate system. Its coordinate column tells you how much of each basis vector to combine; it is not usually the standard coordinate column of the vector. Put the basis vectors into the columns of B. Then v=B[v]ᵦ converts basis coordinates to the actual vector, while solving Bc=v finds coordinates. Order matters: swapping basis vectors swaps the corresponding coordinate entries.'),
 ('Name the direction of a transition matrix', 'To send B-coordinates to C-coordinates, the transition matrix is C⁻¹B. Its jth column is the C-coordinate column of the jth B-basis vector. You can find it by reducing [C|B] to [I|C⁻¹B]. The notes sometimes name the reverse-direction matrix P and the forward one P⁻¹; both conventions are valid. Always write an equation with the input and output basis labels before deciding which matrix to use.'),
  ('Check conversion by reconstruction', 'Given c=[v]ᵦ, compute d=P꜀←ᵦc. Since B multiplies B-coordinates and C multiplies C-coordinates, the reconstruction check is Bc=Cd. This explicit label check prevents a very common order error. The reverse transition is the inverse of the forward transition. The same method works for polynomials after replacing each basis polynomial with its coefficient vector in a fixed standard order.'),
 ],
 '4.8':[
 ('See differential-equation solutions as vectors', 'The professor’s application here is the solution space of a homogeneous linear differential equation. The vectors are functions, and addition and scalar multiplication are pointwise. A linear differential operator sends a combination af+bg to aL[f]+bL[g], so its zero-output functions form a subspace. On an interval with continuous coefficients and a nonzero leading coefficient, an order-n homogeneous equation has an n-dimensional solution space.'),
 ('Verify functions before claiming a basis', 'Differentiate each proposed function as many times as required and substitute into the equation. Satisfying the equation establishes membership, not independence. A list can contain several solutions but still fail to be a fundamental set if one is a combination of the others. To obtain the full general solution, you need n independent solutions of the order-n equation on a regular interval. State the constants and the interval under consideration.'),
 ('Use the Wronskian with the right scope', 'Construct a matrix whose columns are the functions and whose successive rows are their derivatives. A nonzero Wronskian at one point proves independence for sufficiently differentiable functions. For solutions of the same regular homogeneous linear ODE, a vanishing Wronskian implies dependence. For arbitrary smooth functions, an identically zero Wronskian alone need not prove dependence. When a direct constant-coefficient relation is visible, exhibit it; that is a stronger explanation than a determinant calculation alone.'),
 ],
 '5.1':[
 ('Calculate lengths and distances from differences', 'The dot product sums matching coordinate products. The squared length is v·v, so take the nonnegative square root to get length. Distance between u and v is the length of u−v, not the difference of their lengths. To find a unit vector in the direction of a nonzero vector, divide every coordinate by its length. The zero vector has length zero and cannot be normalized to a direction.'),
 ('Use angles and orthogonality responsibly', 'For two nonzero vectors, divide their dot product by the product of their lengths to get the cosine of the angle. A zero dot product means perpendicular vectors; a negative dot product means an obtuse angle. State whether an approximate angle is in radians or degrees. Cauchy–Schwarz guarantees the cosine ratio is between −1 and 1. With rounded arithmetic, a tiny overshoot can occur, so retain exact square roots until the final approximation.'),
 ('Explain the inequalities and equality cases', 'Cauchy–Schwarz bounds how much two vectors can align: equality occurs when they are linearly dependent, including cases involving a zero vector. The triangle inequality says that traveling directly is no longer than traveling through an intermediate point. Equality in the nonzero triangle case requires the same direction, not merely any proportionality. Pythagoras holds when the dot product is zero, as follows by expanding (u+v)·(u+v). These results work in Rⁿ just as in a plane.'),
 ],
 '5.2':[
 ('Check that the proposed pairing is an inner product', 'For real spaces, an inner product is symmetric, bilinear, and positive definite. A weighted coordinate product works when every weight is positive; a negative weight can produce a negative squared norm, while a zero weight can assign zero norm to a nonzero object. Test these possibilities explicitly. A function involving products of coordinates from just one argument may fail bilinearity even if it looks similar to a dot product.'),
 ('Follow the specified geometry', 'For polynomials, a coefficient inner product and an integral inner product are different rules and can give different angles or projections for the same two polynomials. For matrices, pair corresponding entries with the stated weights. For continuous functions on a nontrivial interval, integrate f(t)g(t); the integral of f(t)² is positive for a nonzero continuous function. Specify the interval, because changing it changes the inner product and therefore the geometry.'),
 ('Derive projection from an orthogonal error', 'To approximate v using multiples of a nonzero u, write the candidate cu and require the error v−cu to be orthogonal to u. Solving that one equation gives c=⟨v,u⟩/⟨u,u⟩. The denominator is a squared norm, not a norm. This derivation works for weighted vectors, matrices, and functions. Check your final residual using the same inner product used for the projection; a Euclidean dot-product check can be wrong in a weighted space.'),
 ],
 '5.3':[
 ('Orthogonal is different from orthonormal', 'Orthogonal vectors have zero pairings with one another. Orthonormal vectors also each have length one. A set of nonzero orthogonal vectors is independent, because pairing a dependence relation with each vector isolates its coefficient. Such a set is a basis for its span; it is a basis for the whole ambient space only when its size equals that space’s dimension. Three vectors cannot be a basis for R⁴, regardless of orthogonality.'),
 ('Subtract every previously found component', 'Set u₁=v₁. For the next vector, subtract its projection onto each earlier orthogonal uⱼ, not onto the original uncorrected vⱼ. The result is perpendicular to all earlier directions. Calculate numerators and denominators explicitly, retain fractions, and only then normalize. If a result is zero, the original list was dependent and cannot be normalized as an independent list. Keep the orthogonal stage separate from the unit-length stage.'),
 ('Extend the process to function spaces', 'Replace dot products by the specified integral inner product, leaving the Gram–Schmidt structure unchanged. Symmetry of the interval can make odd integrands integrate to zero, simplifying calculations. Starting with 1,x,x² produces a basis for P₂; starting with only x,x³,x⁵ produces a basis for their three-dimensional span, not all of P₅, whose dimension is six. Verify all pairwise inner products and check that the new vectors span the same space as the original list.'),
 ],
 '6.1':[
 ('Test the two preservation rules', 'A linear map preserves vector addition and real scalar multiplication. It therefore preserves every finite linear combination. Write the rules for arbitrary inputs, not just one numerical pair. Every matrix transformation is linear. A formula with a nonzero constant translation fails the zero test; a formula containing a square can preserve zero and still fail scalar multiplication. Thus T(0)=0 is necessary but not sufficient.'),
 ('Interpret domain and codomain', 'The domain specifies allowable inputs; the codomain specifies where outputs are declared to live. The range may be smaller than the codomain. A map from P₂ to P₁ can be differentiation because a quadratic derivative is at most linear. A map from matrices to polynomials can also be linear if each output coefficient depends linearly on the input entries. Check that the formula really produces an element of the claimed codomain.'),
 ('Recover a map from a basis', 'Once a map is known to be linear, its outputs on a basis determine every output. Express v as a basis combination, apply T to each basis vector, and use the same coefficients. This is the reason matrix columns encode a map. Differentiation, integration with a fixed lower endpoint, and evaluation at a fixed point are linear operations on suitable function spaces. Their outputs have different dimensions, so distinguish a scalar-valued evaluation from a polynomial-valued derivative.'),
 ],
 '6.2':[
 ('Solve the zero-output problem', 'The kernel consists of all domain vectors sent to zero. For a matrix map, solve Ax=0; for a polynomial map, equate output coefficients to zero. A kernel basis describes the independent ways information can be lost. A map is one-to-one precisely when this kernel contains only zero, because two equal outputs imply their input difference lies in the kernel. Remember that the kernel belongs to the domain, not the codomain.'),
 ('Describe reachable outputs', 'The range consists of all outputs the map actually produces. The images of domain basis vectors span it. Reduce their coordinate columns and retain the original pivot-image vectors as a range basis. To prove a specific output is reachable, solve for a preimage; to disprove it, identify an unsatisfied output constraint. A full row rank matrix map onto Rᵐ is onto, but a full column rank map from a smaller input space need not be onto its larger codomain.'),
 ('Apply rank-nullity with the correct dimension', 'Rank plus nullity equals the dimension of the domain. For differentiation P₂→P₁, the constants form a one-dimensional kernel and the two-dimensional range is all P₁. If the very same output formula is declared as a map P₂→P₂, its rank stays two but it is no longer onto that three-dimensional codomain. One-to-one and onto coincide for endomorphisms of equal finite dimensions, but should be tested separately in a rectangular setting.'),
 ],
 '6.3':[
 ('Build columns from basis images', 'Choose and state ordered domain and codomain bases. Apply T to each domain basis vector, express each output in the codomain basis, and place those coordinate columns side by side. The resulting matrix has one column per input basis vector and one row per output coordinate. This rule works for ordinary vectors, polynomials, and matrices. A transformation M₂ₓ₂→P₂ therefore has a 3×4 representing matrix.'),
 ('Compute an output through its coordinates', 'First find the input coordinate column in the domain basis. Multiply by the representing matrix to obtain the output coordinate column in the codomain basis. Finally reconstruct the actual output object if requested. These are three separate stages. For a polynomial operator, differentiating each basis monomial shows which coefficient moves to which row. Include zero coefficients and identify the degree bound of the codomain before assembling columns.'),
 ('Handle composition and independent basis choices', 'For S after T, the matrix product is [S][T], with the first-applied map on the right. The intermediate bases must match or a transition matrix is needed between them. If A is a standard-coordinate matrix and B,C are domain and codomain basis matrices, the nonstandard matrix is C⁻¹AB. When the domain and codomain are different spaces, this is a two-basis representation change, not necessarily a similarity transformation.'),
 ],
 '6.4':[
 ('Define P by an equation before using similarity', 'Let A represent an endomorphism in basis B. Define P to send new C-coordinates into old B-coordinates, so [v]ᵦ=P[v]꜀. Apply A in the old coordinates, then convert the result back with P⁻¹. The new matrix is therefore A꜀=P⁻¹AP. If instead you define P in the opposite direction, the displayed formula reverses accordingly. The coordinate equation, not the letter P alone, determines the correct order.'),
 ('Check that the diagram commutes', 'For any new-coordinate column c, the old-coordinate column is Pc. The old-coordinate output is APc, while the converted new-coordinate output is P A꜀c. Equality for every c means AP=P A꜀. This equation is a convenient verification that does not require interpreting the entries visually. You can also compute T of each new basis vector directly and compare its new-coordinate column with the corresponding column of A꜀.'),
 ('Understand what changes and what stays fixed', 'Similar matrices represent the same linear map in different bases of the same space. Their entries can differ, but determinant, trace, characteristic polynomial, eigenvalues, and rank agree. Equal determinant and trace alone do not prove similarity. Row equivalence is also different: row operations generally change the map rather than merely its coordinate description. Similarity requires an invertible P and the two-sided transformation P⁻¹AP.'),
 ],
 '7.1':[
 ('Derive the characteristic equation', 'An eigenvector must be nonzero and satisfy Av=λv. Rearranging gives (A−λI)v=0. A nonzero solution exists exactly when this square coefficient matrix is singular, so compute det(A−λI)=0. The determinant is the characteristic polynomial; the matrix A−λI itself is not a polynomial scalar. Subtract λ only from diagonal entries, factor the resulting polynomial, and list each root with its algebraic multiplicity.'),
 ('Solve a separate null space for each eigenvalue', 'For each root, substitute λ into A−λI and row-reduce the homogeneous system. Parameterize the null space and give a basis for the eigenspace. Every nonzero combination of its basis vectors is an eigenvector for that λ, while zero belongs to the eigenspace but is not an eigenvector. Verify every basis vector by multiplying Av and comparing with λv. A repeated root does not automatically give several independent eigenvectors.'),
 ('Separate multiplicities and real versus complex answers', 'Algebraic multiplicity counts repetitions as a root; geometric multiplicity is the eigenspace dimension. The latter can be smaller, preventing a full eigenbasis. Over the real numbers, a real matrix may have no real eigenvalues; the notes’ final 2×2 example requires distinguishing this from complex eigenvalues. Over the complex numbers, continue with conjugate roots and complex vectors. Trace and determinant give useful sum and product checks, counting all eigenvalues with multiplicity over the complex field.'),
 ],
}

GUIDE_FORMULAS = {
 '1.1':r'\mathcal S=\{x:Ax=b\}', '1.2':r'\operatorname{rank}(A)+\#\text{free variables}=n',
 '2.1':r'(AB)_{ij}=\sum_{k=1}^{n}a_{ik}b_{kj}', '2.2':r'AC=BC,\ C\text{ invertible}\ \Longrightarrow\ A=B',
 '2.3':r'[A\mid I]\longrightarrow[I\mid A^{-1}]', '2.4':r'E_k\cdots E_1A=I\ \Longrightarrow\ A=E_1^{-1}\cdots E_k^{-1}',
 '2.6':r'c=rA,\qquad r=cA^{-1}', '3.1':r'\det A=\sum_j a_{ij}(-1)^{i+j}\det A_{ij}',
 '3.2':r'\det(U)=(-1)^s\left(\prod_i c_i\right)\det(A)',
 '3.3':r'\det(cA^{-1}B^T)=c^n\frac{\det B}{\det A}', '3.4':r'x_i=\frac{\det A_i}{\det A},\quad\det A\ne0',
 '4.1':r'\begin{bmatrix}v_1&\cdots&v_k\end{bmatrix}c=w', '4.2':r'\dim P_n=n+1,\quad\dim M_{m\times n}=mn',
 '4.3':r'Au=Av=0\ \Longrightarrow\ A(\alpha u+\beta v)=0', '4.4':r'Ac=0\ \Longrightarrow\ c=0\quad\text{(independence)}',
 '4.5':r'\text{basis}=\text{spanning}+\text{independent}', '4.6':r'\{x:Ax=b\}=x_p+\ker A\quad\text{if consistent}',
 '4.7':r'C[v]_{\mathcal C}=B[v]_{\mathcal B},\quad P_{\mathcal C\leftarrow\mathcal B}=C^{-1}B',
 '4.8':r'W(f_1,\ldots,f_n)=\det\big(f_j^{(i-1)}\big)_{i,j=1}^n',
 '5.1':r'\|u+v\|^2=\|u\|^2+2u\cdot v+\|v\|^2',
 '5.2':r'\langle v-cu,u\rangle=0\ \Longrightarrow\ c=\frac{\langle v,u\rangle}{\langle u,u\rangle}',
 '5.3':r'u_k=v_k-\sum_{j<k}\frac{\langle v_k,u_j\rangle}{\langle u_j,u_j\rangle}u_j',
 '6.1':r'T\left(\sum_jc_jb_j\right)=\sum_jc_jT(b_j)', '6.2':r'\dim\ker T+\dim\operatorname{range}T=\dim V',
 '6.3':r'[T]_{\mathcal C\leftarrow\mathcal B}=C^{-1}AB', '6.4':r'AP=PA_{\mathcal C},\quad A_{\mathcal C}=P^{-1}AP',
 '7.1':r'1\le\dim\ker(A-\lambda I)\le\operatorname{mult}(\lambda)',
}

def problem(section,k,mode,P,st,latex):
 """Two distinct problem families per section, with exact symbolic checks."""
 M=S.Matrix; R=S.Rational; x=S.Symbol('x',real=True); q=S.Symbol('q',real=True)
 def checked(prompt,math,answer,steps,hints,proofs,kind='self-check',choices=None):
  return P(prompt,math,answer,steps,hints,proofs,kind,choices)
 def reduce_steps(A):
  """Show every actual row operation, checking against independently computed RREF."""
  B=A.copy(); steps=[st('Start with the matrix in the stated column order.',latex(B))]; row=0
  for col in range(B.cols):
   pivot=next((r for r in range(row,B.rows) if B[r,col]!=0),None)
   if pivot is None:continue
   if pivot!=row:
    B.row_swap(pivot,row);steps.append(st(f'Swap rows {row+1} and {pivot+1} to place a nonzero pivot.',latex(B)))
   factor=B[row,col]
   if factor!=1:
    B.row_op(row,lambda value,j:value/factor);steps.append(st(f'Divide row {row+1} by {factor}, including the augmented entries.',latex(B)))
   for r in range(B.rows):
    if r!=row and B[r,col]!=0:
     multiple=B[r,col];B.row_op(r,lambda value,j:value-multiple*B[row,j])
     steps.append(st(f'Replace row {r+1} by row {r+1} minus ({multiple}) times row {row+1}.',latex(B)))
   row+=1
   if row==B.rows:break
  assert B==A.rref()[0]
  return steps,B
 def dotsteps(A,B):
  steps=[st('Check the inner dimensions and the output shape.',rf'({A.rows}\times{A.cols})({B.rows}\times{B.cols})\longrightarrow {A.rows}\times{B.cols}')]
  for i in range(A.rows):
   calculations=[r'+'.join(rf'({latex(A[i,j])})({latex(B[j,c])})' for j in range(A.cols)) for c in range(B.cols)]
   steps.append(st(f'Compute row {i+1} by pairing this row with each column.',r'\begin{bmatrix}'+r'&'.join(calculations)+r'\end{bmatrix}'))
  steps.append(st('Simplify each entry without changing its position.',latex(A*B)))
  return steps
 if section=='1.1':
  if mode==0:
   sol=M([k-1/(q-2),1/(q-2)]);A=M([[1,1],[2,q]]);rhs=M([k,2*k+1])
   return checked('Classify the system for every real q, and give its solution when one exists.',rf'x+y={k},\quad 2x+qy={2*k+1}',None,
    [st('Eliminate x by subtracting twice the first equation from the second.',r'(q-2)y=1'),st('Separate q=2 before dividing: it would require 0=1, so there is no solution.'),st('For q≠2 the equation fixes y uniquely.',r'y=\frac1{q-2}'),st(f'Substitute y into x+y={k}.',rf'x={k}-\frac1{{q-2}}'),st('Check both equations by multiplying the coefficient matrix by the solution.',rf'{latex(A)}{latex(sol)}={latex(rhs)}'),st('There is no infinite-solution case because the exceptional row is contradictory.')],
    ['Subtract twice the first equation.','Which value of q would make the new coefficient zero?','Treat that value separately, then solve for the other values.'],[(A*sol,rhs),(S.det(A),q-2)])
  u,v=S.symbols('u v',real=True);sol=M([k-u-v,u,v]);A=M([[1,1,1],[2,2,2]])
  return checked('Write the full solution set and explain how many independent parameters it needs.',rf'x+y+z={k},\quad 2x+2y+2z={2*k}',None,
   [st('Subtract twice the first equation from the second.',r'0=0'),st('The second equation is redundant; three variables are constrained by just one independent equation.'),st('Choose y=u and z=v freely.',r'u,v\in\mathbb R'),st('Solve the remaining equation for x.',rf'x={k}-u-v'),st('Write the complete vector family.',rf'\begin{{bmatrix}}x\\y\\z\end{{bmatrix}}={latex(sol)}'),st('Substitution works for every u and v, so the family is complete.',rf'A{latex(sol)}={latex(M([k,2*k]))}')],
   ['Compare the two equations.','Count variables and independent equations.','Assign separate parameters to y and z.'],[(A*sol,M([k,2*k])),(S.Integer(A.rank()),S.Integer(1))])
 if section=='1.2':
  A=M([[1,2,0,-1],[2,4,1,1],[3,6,1,0]]);rhs=M([k,3*k+1,4*k+1]) if mode==0 else S.zeros(3,1)
  steps,red=reduce_steps(A.row_join(rhs));u,v=S.symbols('u v',real=True)
  sol=M([rhs[0]-2*u+v,u,rhs[1]-2*rhs[0]-3*v,v])
  steps.extend([st('Pivot columns are 1 and 3; columns 2 and 4 are free. Set x₂=u and x₄=v.'),st('Solve the two nonzero rows for the pivot variables.',latex(sol)),st('The zero row is an identity, so it imposes no additional restriction.'),st('Verify the entire two-parameter family in the original system.',rf'A{latex(sol)}={latex(rhs)}')])
  return checked('Reduce the augmented matrix and give every solution.' if mode==0 else 'Find a two-vector basis for the homogeneous solution space.',rf'A={latex(A)},\quad b={latex(rhs)},\quad Ax=b',None,steps,
   ['Keep the constants as the last column.','Only columns 1 and 3 contain coefficient pivots.','Choose two independent free parameters and separate their vector coefficients.'],[(A*sol,rhs),(A*M([-2,1,0,0]),S.zeros(3,1)),(A*M([1,0,-3,1]),S.zeros(3,1)),(red,A.row_join(rhs).rref()[0])]) if mode==0 else checked('Find a basis for the homogeneous solution space, not just one solution.',rf'A={latex(A)},\quad Ax=0',None,
   steps+[st('Separate the two parameters into basis vectors.',rf'x=u{latex(M([-2,1,0,0]))}+v{latex(M([1,0,-3,1]))}'),st('Their second and fourth coordinates prove independence; each is annihilated by A.')],
   ['Reduce [A|0].','There are two free variables.','Read one basis vector from each parameter.'],[(A*sol,rhs),(A*M([-2,1,0,0]),S.zeros(3,1)),(A*M([1,0,-3,1]),S.zeros(3,1)),(S.Integer(M.hstack(M([-2,1,0,0]),M([1,0,-3,1])).rank()),S.Integer(2))])
 if section=='2.1':
  A=M([[1,k],[0,2],[-1,1]]);B=M([[2,0,1],[1,-1,k]])
  result=A*B if mode==0 else (A*B).T
  steps=dotsteps(A,B)
  if mode:steps.extend([st('Transpose the 3×3 result by exchanging rows and columns.',latex(result)),st('Check the reverse-order transpose identity independently.',rf'B^TA^T={latex(B.T*A.T)}')])
  else:steps.append(st('The reverse product BA exists but has shape 2×2, so it cannot equal this 3×3 result.',latex(B*A)))
  return checked('Compute AB and explain why BA is a different-size result.' if mode==0 else 'Compute (AB)ᵀ and verify it using BᵀAᵀ.',rf'A={latex(A)},\quad B={latex(B)}',result,steps,
   ['Check both products’ dimensions.','Use row-column products, including the zero entries.','For a transpose, exchange indices and reverse factor order.'],[(result,A*B if mode==0 else B.T*A.T)],'matrix')
 if section=='2.2':
  if mode==0:
   A=M([[k,1],[0,2]]);B=M([[k,4],[0,-3]]);C=M([[1,0],[0,0]])
   return checked('Explain why AC=BC does not permit cancellation of C in this example.',rf'A={latex(A)},\ B={latex(B)},\ C={latex(C)}',None,
    [*dotsteps(A,C),st('Compute BC separately.',latex(B*C)),st('The products agree, but A and B differ in their second columns.'),st('C keeps the first column and erases the second, so the differing information is lost.'),st('C is singular, so multiplying by an inverse is impossible.',r'\det C=0')],
    ['Calculate AC and BC.','Which columns does multiplication by C retain?','Identify why no inverse can restore the erased information.'],[(A*C,B*C),(C.det(),S.Integer(0)),(A[0,1]-B[0,1],S.Integer(-3))])
  A=M([[1,k],[k,0]]);B=M([[2,0],[0,1]])
  return checked('Both matrices are symmetric. Determine whether their product is symmetric and justify your answer.',rf'A={latex(A)},\quad B={latex(B)}',None,
   [st('Check the given symmetry.',rf'A^T=A,\quad B^T=B'),*dotsteps(A,B),st('Transpose AB and compare the two off-diagonal entries.',latex((A*B).T)),st(f'The off-diagonal entries {k} and {2*k} differ, so AB is not symmetric.'),st('The general condition is commutation.',r'(AB)^T=BA,\quad AB\text{ symmetric}\iff AB=BA')],
   ['Compute both off-diagonal entries of AB.','Use (AB)ᵀ=BᵀAᵀ.','Symmetric factors alone do not imply a symmetric product.'],[(A.T,A),(B.T,B),((A*B).T,B*A),((A*B)[0,1]-(A*B)[1,0],-S.Integer(k))])
 if section=='2.3':
  A=M([[1,2,k],[0,1,3],[1,1,k+1]])
  steps,red=reduce_steps(A.row_join(S.eye(3)));inv=A.inv()
  steps.extend([st('The left block is I, so read the right block as A⁻¹.',latex(inv)),st('Check both orders of multiplication.',r'AA^{-1}=A^{-1}A=I_3')])
  if mode==0:return checked('Find this 3×3 inverse using augmented row reduction.',rf'A={latex(A)}',inv,steps,
   ['Augment A with I₃.','Apply each operation to all six columns.','Read the inverse only after the left block becomes I₃.'],[(A*inv,S.eye(3)),(inv*A,S.eye(3)),(red,S.eye(3).row_join(inv))],'matrix')
  target=M([k,-1,2]);rhs=A*target
  steps.extend([st('Now multiply the right-hand side on the left by the inverse.',rf'x=A^{{-1}}b={latex(inv)}{latex(rhs)}={latex(target)}'),st('Check the three original row equations.',rf'A{latex(target)}={latex(rhs)}')])
  return checked('Use Gauss–Jordan inversion to solve Ax=b. Enter the solution column.',rf'A={latex(A)},\quad b={latex(rhs)}',target,steps,
   ['First compute the inverse with [A|I].','The solution is A⁻¹b, not bA⁻¹.','Verify by substituting into all three equations.'],[(A*inv,S.eye(3)),(inv*rhs,target),(A*target,rhs)],'matrix')
 if section=='2.4':
  if mode==0:
   A=M([[1,k,0],[0,1,1],[1,0,1]]);E1=M([[0,1,0],[1,0,0],[0,0,1]]);E2=M([[1,0,0],[0,1,0],[2,0,1]])
   return checked('Swap rows 1 and 2, then add twice the new row 1 to row 3. Give the resulting matrix and show the elementary factors.',rf'A={latex(A)}',E2*E1*A,
    [st('Apply the first operation to I₃ to construct E₁.',latex(E1)),st('The first intermediate matrix is E₁A.',latex(E1*A)),st('Apply the second operation to I₃ to construct E₂.',latex(E2)),st('The second operation acts on the already swapped matrix.',rf'B=E_2E_1A={latex(E2*E1*A)}'),st('The order of factors matches the order of action from right to left.')],
    ['Construct each elementary matrix from I₃.','The second operation uses the new row 1.','Put the first operation nearest A.'],[(E2*E1*A,E2*(E1*A)),(E1*E1,S.eye(3)),(E2.inv()*E2,S.eye(3))],'matrix')
  A=M([[1,k,0],[0,1,0],[0,0,1]]);E=M([[1,-k,0],[0,1,0],[0,0,1]])
  return checked('Factor A into elementary matrices, then decide whether A is idempotent.',rf'A={latex(A)}',None,
   [st(f'A is itself elementary: add {k} times row 2 to row 1 of I₃.'),st('The reverse operation reduces A to I₃.',rf'E={latex(E)},\quad EA=I_3'),st('Invert that reduction to recover the factorization.',r'A=E^{-1}'),st('Compute the square explicitly.',latex(A*A)),st(f'Its (1,2) entry is {2*k} instead of {k}, so A is not idempotent.')],
   ['An elementary matrix uses exactly one row operation.','Undo row addition by changing its sign.','Idempotence means A²=A, not A²=I.'],[(E*A,S.eye(3)),(E.inv(),A),((A*A)[0,1],S.Integer(2*k)),((A*A-A)[0,1],S.Integer(k))])
 if section=='2.6':
  A=M([[1,2,k],[0,1,3],[1,1,k+1]]);row=M([[13,1,16]]) if mode==0 else M([[25,5,19]]);coded=row*A
  if mode==0:
   return checked('Encode the block MAP using A=1,…,Z=26 and row-vector multiplication.',rf'A={latex(A)}',coded,
    [st('Convert the letters to numbers in the same order.',r'M=13,\quad A=1,\quad P=16,\quad r=[13\ \ 1\ \ 16]'),st('Right-multiply the row block by the encoding matrix.',rf'c=rA={latex(row)}{latex(A)}'),st('Compute the first coded entry.',r'13(1)+1(0)+16(1)=29'),st('Compute the second coded entry.',r'13(2)+1(1)+16(1)=43'),st('Compute the third coded entry.',rf'13({k})+1(3)+16({k+1})={29*k+19}'),st('The encoded row contains transmitted numbers, not new letter codes.',latex(coded)),st('Check by right-multiplying with A⁻¹.',rf'A^{{-1}}={latex(A.inv())},\quad cA^{{-1}}={latex(row)}')],
    ['Convert M,A,P to 13,1,16.','The row block multiplies the matrix on the right.','Pair the message row with each column of A.'],[(coded*A.inv(),row)],'matrix')
  return checked('Decode this numerical row block into letters. Show the inverse and verify by re-encoding.',rf'A={latex(A)},\quad c={latex(coded)}',None,
   [st('The determinant is nonzero, so decoding is unique.',rf'\det A={latex(A.det())}'),*reduce_steps(A.row_join(S.eye(3)))[0],st('Read the right block as the inverse.',latex(A.inv())),st('Multiply the coded row on the right by that inverse.',rf'r=cA^{{-1}}={latex(row)}'),st('Translate the recovered integers.',r'25=Y,\quad5=E,\quad19=S\quad\Longrightarrow\quad\text{YES}'),st('Re-encode to verify the transmitted block.',rf'{latex(row)}A={latex(coded)}')],
    ['Use r=cA⁻¹ for a row block.','Reduce [A|I₃] to compute the inverse.','Translate integers only after recovering the uncoded block.'],[(coded*A.inv(),row),(row*A,coded),(A.det(),S.Integer(4))])
 if section=='3.1':
  A=M([[k,0,2],[1,3,0],[0,-1,4]]) if mode==0 else M([[k,0,0,1],[0,2,1,0],[0,0,3,0],[0,0,0,-1]])
  if mode==0:
   minor1=A.minor_submatrix(0,0);minor3=A.minor_submatrix(0,2)
   steps=[st('Expand along row 1, where the middle entry is zero. Its signs are +, −, +.'),st('Compute the first minor.',rf'M_{{11}}=\det{latex(minor1)}={latex(minor1.det())}'),st('Compute the third minor.',rf'M_{{13}}=\det{latex(minor3)}={latex(minor3.det())}'),st('Apply the entry and cofactor signs.',rf'\det A={k}({minor1.det()})+2({minor3.det()})={latex(A.det())}'),st('Check by expanding down column 3.',rf'2C_{{13}}+4C_{{33}}={latex(A.det())}')]
  else:steps=[st('All entries below the diagonal are zero, so A is upper triangular.'),st('Multiply all four diagonal entries.',rf'\det A=({k})(2)(3)(-1)={latex(A.det())}'),st('The off-diagonal entries do not change a triangular determinant.'),st('Check by expanding column 1: its only nonzero entry multiplies a 3×3 triangular minor.',rf'\det A={k}\det{latex(A.minor_submatrix(0,0))}={latex(A.det())}'),st('A nonzero product shows the matrix is invertible.')]
  return checked('Evaluate the determinant using cofactor expansion.' if mode==0 else 'Evaluate this 4×4 determinant using its triangular structure.',rf'A={latex(A)}',A.det(),steps,
   ['Look for zero entries before choosing a method.','For cofactors, use the checkerboard signs.','For a triangular matrix, use every diagonal entry.'],[(A.det(),k*minor1.det()+2*minor3.det() if mode==0 else -S.Integer(6*k))],'numeric')
 if section=='3.2':
  U=M([[2,1,k],[0,3,2],[0,0,-1]]);swap=M([[0,1,0],[1,0,0],[0,0,1]]);scale=S.diag(2,1,1);replace=M([[1,0,0],[0,1,0],[k,0,1]])
  A=(replace*scale*swap).inv()*U
  if mode==0:
   return checked('A is transformed into U by a row swap, scaling the new first row by 2, then adding k times row 1 to row 3. Find det(A).',rf'k={k},\quad U={latex(U)}',A.det(),
    [st('The swap multiplies the determinant by −1.'),st('Scaling one row by 2 multiplies it by 2.'),st('Row replacement does not change it, so the overall factor is −2.',r'\det U=-2\det A'),st('Multiply the triangular diagonal.',r'\det U=2(3)(-1)=-6'),st('Undo the recorded factor.',r'\det A=\frac{-6}{-2}=3')],
    ['Record the determinant effect of each operation.','The last row replacement has factor 1.','The triangular determinant is the modified determinant, not the original one.'],[(U.det(),-2*A.det()),(A.det(),S.Integer(3))],'numeric')
  A=M([[k,1,0,2],[0,2,1,0],[1,0,3,0],[2,1,1,0]]);minor=A.minor_submatrix(0,3)
  return checked('Find this 4×4 determinant by a sparse-column expansion followed by a 3×3 calculation.',rf'A={latex(A)}',A.det(),
   [st('Column 4 has one nonzero entry, in row 1. Its cofactor sign is negative.'),st('Delete row 1 and column 4.',latex(minor)),st('Evaluate the remaining 3×3 determinant.',rf'\det M=0-2(1-6)+1(1-0)={latex(minor.det())}'),st('Restore the original entry and sign.',rf'\det A=-2({latex(minor.det())})={latex(A.det())}'),st('The answer is independent of k because its entry is outside the surviving minor.')],
    ['Expand along the last column.','The (1,4) sign is −.','Multiply the minor determinant by −2.'],[(A.det(),-2*minor.det()),(minor.det(),S.Integer(11))],'numeric')
 if section=='3.3':
  if mode==0:
   A=M([[1,q,2],[-2,0,-q],[3,1,2*k]]);det=S.factor(A.det());roots=S.solve(det,q)
   return checked('Find every real q for which A is singular.',rf'A={latex(A)}',None,
    [st('Singularity is equivalent to det(A)=0.'),st('Expand along row 1; keep q symbolic.',rf'\det A={latex(S.expand(det))}'),st('Factor or use the quadratic formula.',rf'{latex(det)}=0'),st('List both roots.',rf'q\in\left\{{{", ".join(latex(r) for r in roots)}\right\}}'),st('The polynomial has degree two and these are its two distinct real roots, so there are no other singular values.')],
    ['Compute the determinant before solving for q.','Do not divide by q and risk removing q=0 without checking.','Solve the full quadratic and substitute both roots.'],[(det.subs(q,r),S.Integer(0)) for r in roots]+[(S.expand(det),S.expand(S.prod(q-r for r in roots)*S.Poly(det,q).LC()))])
  A=S.diag(1,2,3);B=M([[k,1,0],[0,2,1],[0,0,-2]]);result=(2*A.inv()*B.T).det()
  return checked('Evaluate det(2A⁻¹Bᵀ) using determinant identities, without forming the product.',rf'A={latex(A)},\quad B={latex(B)}',result,
   [st('Both matrices are 3×3, so scaling the entire product by 2 contributes 2³.'),st('The inverse contributes a reciprocal; the transpose leaves a determinant unchanged.',r'\det(2A^{-1}B^T)=2^3\frac{\det B}{\det A}'),st('Use the triangular diagonal products.',rf'\det A=6,\quad\det B={-4*k}'),st('Substitute and simplify.',rf'8\frac{{{-4*k}}}{{6}}={latex(result)}'),st('A has nonzero determinant, which justifies the inverse.')],
    ['Use the exponent 3 for the scalar factor.','Replace det(A⁻¹) by 1/det(A).','Use det(Bᵀ)=det(B).'],[(result,8*B.det()/A.det())],'numeric')
 if section=='3.4':
  A=M([[1,2,k],[0,1,3],[1,1,k+1]])
  if mode==0:
   cof=A.cofactor_matrix();adj=cof.T;inv=A.inv()
   return checked('Find A⁻¹ using all cofactors and the adjugate.',rf'A={latex(A)}',inv,
    [st('Compute the determinant before dividing.',rf'\det A={latex(A.det())}'),st('For example, delete row 1 and column 2 and apply its negative cofactor sign.',rf'C_{{12}}=-\det{latex(A.minor_submatrix(0,1))}={latex(cof[0,1])}'),st('Compute every signed cofactor.',latex(cof)),st('Transpose the cofactor matrix to obtain the adjugate.',latex(adj)),st('Divide the adjugate by the determinant.',latex(inv)),st('Check the adjugate identity.',rf'A\operatorname{{adj}}(A)={latex(A.det()*S.eye(3))}')],
    ['Use signs (−1)^(i+j) for the minors.','Transpose the entire cofactor matrix.','Verify A adj(A)=det(A)I before accepting the inverse.'],[(A*adj,A.det()*S.eye(3)),(adj/A.det(),inv),(A*inv,S.eye(3))],'matrix')
  sol=M([k,1,-1]);rhs=A*sol;dets=[];steps=[st('Check the determinant and Cramer’s Rule hypothesis.',rf'\det A={latex(A.det())}\ne0')]
  for i in range(3):
   Ai=A.copy();Ai[:,i]=rhs;dets.append(Ai.det());steps.append(st(f'Replace column {i+1}, keeping the other columns fixed.',rf'A_{{{i+1}}}={latex(Ai)},\quad\det A_{{{i+1}}}={latex(Ai.det())}'))
  steps.extend([st('Divide each replacement determinant by det(A).',latex(sol)),st('Substitute into the original system.',rf'A{latex(sol)}={latex(rhs)}')])
  return checked('Solve the 3×3 system using Cramer’s Rule. Enter its solution column.',rf'A={latex(A)},\quad Ax={latex(rhs)}',sol,steps,
   ['Check det(A)≠0.','Replace a column, not a row.','Use the same original determinant in each denominator.'],[(M(dets)/A.det(),sol),(A*sol,rhs)],'matrix')
 if section=='4.1':
  u=M([1,0,1,2]);v=M([0,1,-1,1]);w=M([1,1,0,-1]);A=M.hstack(u,v,w);coords=M([k,-1,2]);target=A*coords
  if mode==0:
   steps,red=reduce_steps(A.row_join(target));steps.extend([st('Each column belongs to one proposed spanning vector. Read the three coefficients.',latex(coords)),st('Reconstruct the four-coordinate target from these coefficients.',rf'{k}u-v+2w={latex(target)}')])
   return checked('Express b as a combination of u,v,w in R⁴. Enter the three coefficients as a column.',rf'u={latex(u)},\quad v={latex(v)},\quad w={latex(w)},\quad b={latex(target)}',coords,steps,
    ['There are three coefficient unknowns but four coordinate equations.','Put u,v,w into columns of a 4×3 matrix.','Check all four target coordinates after solving.'],[(A*coords,target),(S.Integer(A.rank()),S.Integer(3))],'matrix')
  outsider=target+M([1,0,0,0]);normal=A.T.nullspace()[0];normal=normal/normal[0]
  return checked('Decide whether b belongs to span{u,v,w}, and justify using all four coordinates.',rf'u={latex(u)},\ v={latex(v)},\ w={latex(w)},\ b={latex(outsider)}',None,
   [st('Form the coefficient matrix with u,v,w as columns.',latex(A)),st('A normal direction to this three-dimensional span is annihilated by Aᵀ.',rf'n={latex(normal)},\quad n^TA=0'),st('Every linear combination of u,v,w must therefore satisfy nᵀb=0.'),st('The proposed target fails that constraint.',rf'n^Tb={latex((normal.T*outsider)[0])}\ne0'),st('No coefficient tuple can reproduce all four coordinates, so b is outside the span.')],
    ['A three-vector span in R⁴ need not fill R⁴.','Find a constraint satisfied by each spanning vector.','Test the target against that same constraint.'],[(A.T*normal,S.zeros(3,1)),((normal.T*outsider)[0],S.Integer(1)),(S.Integer(A.rank()),S.Integer(3))])
 if section=='4.2':
  if mode==0:
   p=x*x+k*x;negative=-p
   return checked('Is the set of polynomials of exactly degree two a real vector space under the usual operations? Contrast it with P₂.',rf'p(x)={latex(p)},\quad -p(x)={latex(negative)}',None,
    [st('Both displayed polynomials have a nonzero quadratic coefficient, so both have exactly degree two.'),st('Add them.',r'p+(-p)=0'),st('The zero polynomial is not of exactly degree two, so addition is not closed.'),st('Scalar multiplication by zero fails too, because 0p=0 must belong to any vector space.'),st('P₂ instead allows degree at most two and includes zero. Coefficientwise addition and scaling stay inside it.'),st('Its standard basis has three independent directions.',r'\mathcal B=(1,x,x^2),\quad\dim P_2=3')],
    ['Check the zero-vector requirement.','Add a polynomial to its negative.','Distinguish exactly degree two from degree at most two.'],[(p+negative,S.Integer(0)),(S.Integer(S.Poly(p,x).degree()),S.Integer(2)),(S.Integer(S.Poly(negative,x).degree()),S.Integer(2))])
  u=M([k,1]);v=M([1,2]);op=lambda a,b:M([a[0]+b[0],a[1]-b[1]])
  return checked('With u⊕v=(u₁+v₁,u₂−v₂) and ordinary scalar multiplication, is R² a vector space?',rf'u={latex(u)},\quad v={latex(v)}',None,
   [st('Test commutativity using allowed inputs.'),st('Apply the proposed addition in the first order.',rf'u\oplus v={latex(op(u,v))}'),st('Reverse the inputs.',rf'v\oplus u={latex(op(v,u))}'),st('The second coordinates differ, so commutativity fails.'),st('A single failed vector-space axiom disproves the claim; there is no need to test all remaining axioms.')],
   ['The set alone does not determine vector-space structure.','Use the supplied addition, not ordinary vector addition.','Compare u⊕v with v⊕u.'],[((op(u,v)-op(v,u))[1],S.Integer(-2))])
 if section=='4.3':
  if mode==0:
   a,b,c=S.symbols('a b c',real=True);p=a+b*x+c*x*x;basis=[x-k,x*x-k*k]
   return checked(f'Prove W={{p∈P₂:p({k})=0}} is a subspace and find a basis.',rf'W=\{{a+bx+cx^2:a+{k}b+{k*k}c=0\}}',None,
    [st('The zero polynomial satisfies the defining constraint.'),st(f'Evaluation is linear, so a combination of two polynomials vanishing at {k} still vanishes there.',rf'(\alpha p+\beta q)({k})=\alpha p({k})+\beta q({k})=0'),st('Solve the coefficient constraint for a.',rf'a=-{k}b-{k*k}c'),st('Separate the two free coefficients.',rf'p(x)=b(x-{k})+c(x^2-{k*k})'),st('These two polynomials are independent: the x² coefficient forces c=0, and the x coefficient then forces b=0.'),st(f'A basis is (x−{k},x²−{k*k}), and W has dimension two.')],
    [f'Translate p({k})=0 into a coefficient equation.','Use b and c as free parameters.','Check closure and independence, not just spanning.'],[(p.subs(a,-k*b-k*k*c),b*basis[0]+c*basis[1]),(basis[0].subs(x,k),S.Integer(0)),(basis[1].subs(x,k),S.Integer(0)),(S.Integer(M([[-k,-k*k],[1,0],[0,1]]).rank()),S.Integer(2))])
  A=M([[1,k],[0,0]])
  return checked('Does the set of all idempotent 2×2 matrices form a subspace? Give a closure counterexample.',rf'A={latex(A)},\quad W=\{{B:B^2=B\}}',None,
   [st('A belongs to W because A²=A.',latex(A*A)),st('A subspace must contain every real multiple of A.'),st('Consider 2A and calculate its square.',rf'2A={latex(2*A)},\quad(2A)^2={latex(4*A)}'),st('These two matrices differ because A is nonzero.'),st('Thus 2A is not idempotent, and W fails scalar closure even though it contains the zero matrix.')],
    ['Check whether A²=A.','A subspace must be closed under multiplication by 2.','Compare (2A)² with 2A.'],[(A*A,A),((2*A)*(2*A),4*A),((4*A-2*A)[0,0],S.Integer(2))])
 if section=='4.4':
  if mode==0:
   polys=[1+x,k+x*x,1+x+k+x*x];A=M([[1,k,k+1],[1,0,1],[0,1,1]]);relation=M([1,1,-1])
   return checked('Test these polynomials for independence and find a nontrivial dependence relation.',rf'p_1={latex(polys[0])},\ p_2={latex(polys[1])},\ p_3={latex(polys[2])}',None,
    [st('Use coefficient order (constant,x,x²). Missing powers have zero coefficients.',latex(A)),st('The third coordinate column equals the sum of the first two.'),st('Translate the column relation back to the actual polynomials.',r'p_1+p_2-p_3=0'),st('The coefficient tuple (1,1,−1) is nonzero, proving dependence.'),st('The first two are independent because their x and x² coefficients isolate their respective weights.'),st('Their span has dimension two, so these three polynomials do not span all of P₂.')],
    ['Represent each polynomial by all three coefficients.','Compare the third polynomial with the first two.','A dependence relation needs a nonzero coefficient tuple.'],[(A*relation,S.zeros(3,1)),(S.expand(polys[0]+polys[1]-polys[2]),S.Integer(0)),(S.Integer(A.rank()),S.Integer(2))])
  v1=M([1,0,k]);v2=M([0,1,1]);v3=v1+v2;A=M.hstack(v1,v2,v3);target=M([1,1,k+2]);normal=M([-k,-1,1])
  return checked('Determine whether S spans R³ and whether it is independent. Then test whether b is in its span.',rf'S=\{{{latex(v1)},{latex(v2)},{latex(v3)}\}},\quad b={latex(target)}',None,
   [st('The third vector equals the sum of the first two, so S is dependent.'),st('The first two vectors are independent from their first two coordinates.'),st('Their span is therefore a plane, not all of R³.'),st(f'Every spanning vector satisfies {k}z₁+z₂−z₃=0.',rf'n={latex(normal)},\quad n^TA=0'),st('The proposed target fails that constraint.',rf'n^Tb={latex((normal.T*target)[0])}'),st('It is outside the span even though its first two coordinates look compatible.')],
    ['Inspect whether one vector is redundant.','Count independent directions.','Check the third coordinate as well as the first two.'],[(v1+v2,v3),(A.T*normal,S.zeros(3,1)),((normal.T*target)[0],S.Integer(1)),(S.Integer(A.rank()),S.Integer(2))])
 if section=='4.5':
  if mode==0:
   a,b=S.symbols('a b',real=True);target=M([[a,b],[b,-k*a]]);B1=M([[1,0],[0,-k]]);B2=M([[0,1],[1,0]])
   return checked('Find a basis and dimension for the symmetric 2×2 matrices satisfying the stated diagonal constraint.',rf'W=\{{A:A^T=A,\ {k}a_{{11}}+a_{{22}}=0\}}',None,
    [st(f'A symmetric matrix has equal off-diagonal entries. The constraint forces the second diagonal entry to be −{k} times the first.',latex(target)),st('Separate the two freely chosen parameters.',rf'A=a{latex(B1)}+b{latex(B2)}'),st('Both proposed basis matrices satisfy symmetry and the diagonal constraint.'),st('A zero combination forces a=0 from entry (1,1) and b=0 from entry (1,2).'),st('Thus the two matrices span W and are independent, making a basis of dimension two.')],
    ['Write the most general matrix satisfying both conditions.','Identify its free entry parameters.','Use one basis matrix per independent parameter.'],[(a*B1+b*B2,target),(B1.T,B1),(B2.T,B2),(k*B1[0,0]+B1[1,1],S.Integer(0)),(k*B2[0,0]+B2[1,1],S.Integer(0)),(S.Integer(M([[1,0],[0,1],[0,1],[-k,0]]).rank()),S.Integer(2))])
  A=M([[1,0,1,k],[0,1,1,k],[1,1,2,2*k]]);steps,red=reduce_steps(A)
  steps.extend([st('The pivot columns are 1 and 2. Retain those columns from the original matrix.',latex(A[:,:2])),st('The other columns are combinations of them.',rf'v_3=v_1+v_2,\quad v_4={k}(v_1+v_2)'),st('The two retained columns are independent, so this span has dimension two.')])
  return checked('Extract a basis for the span of the four displayed columns.',rf'A={latex(A)}',None,steps,
    ['Reduce the columns to locate pivot positions.','Use original columns at those positions.','Express the nonpivot columns in terms of the retained ones.'],[(A[:,2],A[:,0]+A[:,1]),(A[:,3],k*(A[:,0]+A[:,1])),(S.Integer(A[:,:2].rank()),S.Integer(2))])
 if section=='4.6':
  A=M([[1,2,0,k],[0,0,1,1],[2,4,1,2*k+1]]);N=M.hstack(M([-2,1,0,0]),M([-k,0,-1,1]));steps,red=reduce_steps(A)
  if mode==0:
   steps.extend([st('Two nonzero RREF rows form a row-space basis.',latex(red[:2,:])),st('Columns 1 and 3 are pivots, so the column-space basis uses those original columns.',latex(M.hstack(A[:,0],A[:,2]))),st('The free variables x₂=s and x₄=t produce this null-space basis.',latex(N)),st('Check both null vectors and the dimension formula.',r'AN=0,\quad\operatorname{rank}A=2,\quad\operatorname{nullity}A=4-2=2')])
   return checked('Find bases for the row, column, and null spaces and state rank and nullity.',rf'A={latex(A)}',None,steps,
    ['Row and null vectors have four coordinates; column vectors have three.','Use original columns but reduced rows.','Two free variables should yield two null vectors.'],[(A*N,S.zeros(3,2)),(S.Integer(A.rank()),S.Integer(2)),(S.Integer(N.rank()),S.Integer(2)),(S.Integer(M.hstack(A[:,0],A[:,2]).rank()),S.Integer(2))])
  particular=M([k,0,1,0]);rhs=A*particular;u,v=S.symbols('s t',real=True);family=particular+N*M([u,v]);bad=rhs+M([0,0,1])
  return checked('Describe all solutions for b, then explain why replacing b by c makes the system inconsistent.',rf'A={latex(A)},\quad b={latex(rhs)},\quad c={latex(bad)}',None,
   [st('The third coefficient row is twice the first plus the second. Consistency requires b₃=2b₁+b₂.'),st('The displayed b satisfies that constraint and admits this particular solution.',latex(particular)),st('Add the null-space family to get every solution.',latex(family)),st('The two parameters account for all free variables because rank(A)=2 and there are four inputs.'),st('The new c violates the required right-hand-side relation by 1.',r'c_3-2c_1-c_2=1'),st('Its augmented matrix has a contradiction, so no solution exists.')],
    ['Compare row 3 with rows 1 and 2.','Find one solution, then add the null space.','Test the same row relation on each right-hand side.'],[(A*family,rhs),(bad[2]-2*bad[0]-bad[1],S.Integer(1)),(S.Integer(A.row_join(bad).rank()),S.Integer(3)),(S.Integer(A.rank()),S.Integer(2))])
 if section=='4.7':
  B=M([[1,1,0],[0,1,1],[0,0,1]]);C=M([[1,0,1],[0,1,0],[0,0,1]]);coords=M([k,-1,2]);Pcb=C.inv()*B;new=Pcb*coords
  if mode==0:
   steps,red=reduce_steps(C.row_join(B));steps.extend([st('The right block is the transition from B-coordinates to C-coordinates.',latex(Pcb)),st('Apply it to the input coordinate column.',rf'[v]_{{\mathcal C}}={latex(Pcb)}{latex(coords)}={latex(new)}'),st('Reconstruct using each basis to confirm the same actual vector.',rf'B[v]_{{\mathcal B}}=C[v]_{{\mathcal C}}={latex(B*coords)}')])
   return checked('Find the transition matrix from B to C using row reduction, then convert the given coordinates. Enter the converted column.',rf'B={latex(B)},\ C={latex(C)},\ [v]_{{\mathcal B}}={latex(coords)}',new,steps,
    ['Reduce [C|B], with the destination basis on the left.','The right block becomes C⁻¹B.','Check reconstruction in both bases.'],[(C*Pcb,B),(C*new,B*coords),(red,S.eye(3).row_join(Pcb))],'matrix')
  # The same coordinate matrices represent ordered polynomial bases in P₂.
  return checked('Convert a polynomial from basis (1,1+x,x+x²) to (1,x,1+x²). Show both coordinate systems.',rf'[p]_{{\mathcal B}}={latex(coords)}',None,
   [st('Represent each basis polynomial by its coefficients in (1,x,x²).',rf'B={latex(B)},\quad C={latex(C)}'),st('Build the actual polynomial’s standard coefficient column.',rf'[p]_{{\rm std}}=B[p]_{{\mathcal B}}={latex(B*coords)}'),st('Read the standard polynomial.',latex((B*coords)[0]+(B*coords)[1]*x+(B*coords)[2]*x*x)),st('Solve C[p]꜀=[p]std.',rf'[p]_{{\mathcal C}}=C^{{-1}}B[p]_{{\mathcal B}}={latex(new)}'),st('Recombine the C-basis polynomials with these new weights.',latex(new[0]+new[1]*x+new[2]*(1+x*x))),st('The reconstructed polynomial matches, so only its description changed.')],
    ['Include constant, linear, and quadratic coefficients.','Put basis-polynomial coefficients in columns.','Use C⁻¹B to convert from B to C.'],[(C*new,B*coords),(new[0]+new[1]*x+new[2]*(1+x*x),(B*coords)[0]+(B*coords)[1]*x+(B*coords)[2]*x*x)])
 if section=='4.8':
  if mode==0:
   f=S.exp(k*x)*S.cos(x);g=S.exp(k*x)*S.sin(x);L=lambda h:S.diff(h,x,2)-2*k*S.diff(h,x)+(k*k+1)*h;W=S.simplify(f*S.diff(g,x)-g*S.diff(f,x))
   return checked('Verify both functions solve the ODE, prove independence, and state the general solution.',rf"y''-{2*k}y'+{k*k+1}y=0,\quad f={latex(f)},\quad g={latex(g)}",None,
    [st('Differentiate each function twice, retaining both exponential and trigonometric terms.',rf"f'={latex(S.diff(f,x))},\quad g'={latex(S.diff(g,x))}"),st('Substitute into the differential operator; both residuals simplify to zero.',r'L[f]=L[g]=0'),st('Compute the two-function Wronskian.',rf"W=fg'-gf'={latex(W)}"),st('This positive exponential never vanishes, so the two solutions are independent.'),st('The second-order equation has continuous coefficients and leading coefficient 1 on R, so two independent solutions form a fundamental set.'),st('Write every solution with two independent constants.',rf'y=C_1{latex(f)}+C_2{latex(g)}')],
    ['Use the product rule in every derivative.','Membership in the solution space is not yet independence.','A nonzero Wronskian completes the basis argument.'],[(S.simplify(L(f)),S.Integer(0)),(S.simplify(L(g)),S.Integer(0)),(W,S.exp(2*k*x))])
  f=S.Integer(1);g=S.cos(k*x);h=2+3*g;L=lambda v:S.diff(v,x,3)+k*k*S.diff(v,x);W=S.wronskian([f,g,h],x)
  return checked('Three functions solve this third-order ODE. Do they form a fundamental set? Give the missing type of solution.',rf"k={k},\quad y'''+{k*k}y'=0,\quad f=1,\quad g={latex(g)},\quad h={latex(h)}",None,
   [st('Check each function by differentiating three times.',r'L[f]=L[g]=L[h]=0'),st('Exhibit the constant-coefficient dependence relation.',r'h-2f-3g=0'),st('Consequently their Wronskian is zero and they do not form a three-dimensional basis.',r'W(f,g,h)=0'),st('A sine solution supplies the missing independent direction.',rf'j(x)={latex(S.sin(k*x))}'),st('For the list (1,cos(kx),sin(kx)), the Wronskian is k³, which is nonzero for the stated positive k.',rf'W(1,\cos({k}x),\sin({k}x))={k**3}'),st('The general solution therefore uses a constant, a cosine, and a sine.',rf'y=C_1+C_2\cos({k}x)+C_3\sin({k}x)')],
    ['Look for a direct relation among f,g,h.','Three listed solutions can still be dependent.','Differentiate sin(kx) and check both membership and independence.'],[(S.simplify(L(v)),S.Integer(0)) for v in [f,g,h,S.sin(k*x)]]+[(h-2*f-3*g,S.Integer(0)),(S.simplify(W),S.Integer(0)),(S.simplify(S.wronskian([f,g,S.sin(k*x)],x)),S.Integer(k**3))])
 if section=='5.1':
  if mode==0:
   u=M([k,1,-1,2]);v=M([1,-k,2,0]);product=u.dot(v);normu=S.sqrt(u.dot(u));normv=S.sqrt(v.dot(v));dist=S.sqrt((u-v).dot(u-v));ratio=S.simplify(product/(normu*normv))
   return checked('For these R⁴ vectors, find their dot product, norms, distance, and exact cosine of the angle.',rf'u={latex(u)},\quad v={latex(v)}',None,
    [st('Multiply matching entries and sum.',rf'u\cdot v=({k})(1)+(1)({-k})+(-1)(2)+(2)(0)={product}'),st('Compute each squared length before taking its square root.',rf'\|u\|={latex(normu)},\quad\|v\|={latex(normv)}'),st('Subtract vectors before computing distance.',rf'u-v={latex(u-v)},\quad d(u,v)={latex(dist)}'),st('The exact cosine is the dot product divided by the product of norms.',rf'\cos\theta={latex(ratio)}'),st('It is negative, so the angle is obtuse. Both norms are nonzero, making the formula valid.'),st('Cauchy–Schwarz bounds the squared dot product by the product of squared lengths.',rf'{product**2}\le {u.dot(u)*v.dot(v)}')],
    ['Use all four coordinates.','Distance is the norm of u−v.','Keep the square roots exact in the angle formula.'],[(product,S.Integer(-2)),(dist**2,(u-v).dot(u-v)),(ratio**2,product**2/(u.dot(u)*v.dot(v)))])
  u=M([k,2,-1]);v=-2*u
  return checked('Show that Cauchy–Schwarz is an equality here but the triangle inequality is strict. Explain the geometric difference.',rf'u={latex(u)},\quad v={latex(v)}',None,
   [st('The vectors are nonzero and point in opposite directions because v=−2u.'),st('Compute their dot product and norm product.',rf'|u\cdot v|=2\|u\|^2={2*u.dot(u)},\quad\|u\|\|v\|={2*u.dot(u)}'),st('Cauchy–Schwarz equality therefore holds.'),st('Their sum is −u, so its norm is only ‖u‖.',rf'\|u+v\|={latex(S.sqrt(u.dot(u)))}'),st('The sum of their separate lengths is three times as large.',rf'\|u\|+\|v\|={latex(3*S.sqrt(u.dot(u)))}'),st('Triangle equality requires compatible same-direction travel, while Cauchy–Schwarz allows opposite-direction proportionality.')],
    ['Notice v is a negative multiple of u.','Absolute value removes the sign in Cauchy–Schwarz.','Compare the length of u+v with the two separate lengths.'],[(u.dot(v),-2*u.dot(u)),((u+v).dot(u+v),u.dot(u)),(v.dot(v),4*u.dot(u))])
 if section=='5.2':
  if mode==0:
   A=M([[1,k],[0,-1]]);B=M([[2,1],[1,1]]);ip=lambda U,V:2*U[0,0]*V[0,0]+U[0,1]*V[0,1]+U[1,0]*V[1,0]+2*U[1,1]*V[1,1];coef=S.cancel(ip(A,B)/ip(B,B));proj=coef*B;res=A-proj
   return checked('Use the weighted matrix inner product to project A onto B. Give the projection matrix.',rf'A={latex(A)},\ B={latex(B)},\quad\langle U,V\rangle=2u_{{11}}v_{{11}}+u_{{12}}v_{{12}}+u_{{21}}v_{{21}}+2u_{{22}}v_{{22}}',proj,
    [st('Pair corresponding entries using the specified weights.',rf'\langle A,B\rangle=2(1)(2)+({k})(1)+0(1)+2(-1)(1)={ip(A,B)}'),st('Compute the squared norm of the projection direction.',rf'\langle B,B\rangle={ip(B,B)}'),st('Divide the pairing by that squared norm.',rf'c={latex(coef)}'),st('Multiply every entry of B by c.',latex(proj)),st('Compute the residual.',latex(res)),st('Verify orthogonality with this weighted inner product.',r'\langle A-cB,B\rangle=0')],
    ['The weights on the two diagonal entries are 2.','The denominator is ⟨B,B⟩.','Use the weighted pairing again for the error check.'],[(ip(res,B),S.Integer(0)),(ip(B,B),S.Integer(12)),(ip(A,B),S.Integer(k+2))],'matrix')
  f=x*x+k;g=S.Integer(1);ip=lambda u,v:S.integrate(u*v,(x,-1,1));coef=ip(f,g)/ip(g,g);res=f-coef
  return checked('Find the best constant approximation to f under the integral inner product on [−1,1], and its squared error norm.',rf'f(x)={latex(f)},\quad\langle f,g\rangle=\int_{{-1}}^1 f(x)g(x)\,dx',None,
   [st('Every constant is a multiple of g(x)=1, so project onto this direction.'),st('Compute the numerator by integrating the function.',rf'\langle f,1\rangle={latex(ip(f,g))}'),st('Compute the denominator, the interval length.',r'\langle1,1\rangle=2'),st('Divide to obtain the best constant.',rf'c={latex(coef)}'),st('Subtract to find the error function and check its orthogonality.',rf'r(x)={latex(res)},\quad\int_{{-1}}^1r(x)\,dx=0'),st('Integrate the square of the error, not its absolute value.',rf'\|r\|^2=\int_{{-1}}^1r(x)^2\,dx={latex(ip(res,res))}'),st('Any other constant adds a nonzero orthogonal constant component and therefore increases squared error.')],
    ['A constant approximation lies in span{1}.','Compute both integrals for the projection coefficient.','Subtract the approximation before squaring the error.'],[(ip(res,g),S.Integer(0)),(coef,S.Integer(k)+R(1,3)),(ip(res,res),R(8,45))])
 if section=='5.3':
  if mode==0:
   vectors=[M([1,0,1,0]),M([1,1,1,1]),M([0,k,1,1])];ip=lambda a,b:a.dot(b)
  else:vectors=[S.Integer(1),x,x*x+k*x];ip=lambda a,b:S.integrate(a*b,(x,-1,1))
  orth=[];steps=[]
  for i,v in enumerate(vectors):
   steps.append(st(f'Start orthogonal direction {i+1} from the original input.',latex(v)));u=v
   for j,previous in enumerate(orth):
    coef=S.simplify(ip(v,previous)/ip(previous,previous));u=u-coef*previous
    steps.append(st(f'Subtract its component along the already orthogonal direction {j+1}.',rf'\frac{{\langle v_{{{i+1}}},u_{{{j+1}}}\rangle}}{{\langle u_{{{j+1}}},u_{{{j+1}}}\rangle}}={latex(coef)}'))
   u=S.simplify(u);orth.append(u);steps.append(st(f'The resulting perpendicular direction is u{i+1}.',latex(u)))
  normalized=[S.simplify(v/S.sqrt(ip(v,v))) for v in orth]
  steps.extend([st('Normalize only after the orthogonal stage.',rf'\left({", ".join(latex(v) for v in normalized)}\right)'),st('Check every distinct pair has inner product zero and every normalized vector has squared norm one.'),st('These three vectors form a basis for the original span.' if mode==0 else 'The three resulting polynomials form an orthonormal basis for P₂, whose dimension is three.')])
  proofs=[(ip(orth[i],orth[j]),S.Integer(0)) for i in range(3) for j in range(i)]+[(ip(v,v),S.Integer(1)) for v in normalized]
  if mode==0:proofs.append((S.Integer(M.hstack(*vectors).rank()),S.Integer(3)))
  else:proofs.append((S.Integer(M([[S.expand(v).coeff(x,j) for v in vectors] for j in range(3)]).rank()),S.Integer(3)))
  return checked('Apply Gram–Schmidt to obtain an orthonormal basis for this three-dimensional subspace of R⁴.' if mode==0 else 'Apply Gram–Schmidt to the ordered polynomials using the integral inner product on [−1,1].',rf'(v_1,v_2,v_3)=\left({", ".join(latex(v) for v in vectors)}\right)',None,steps,
   ['Use projections onto already corrected orthogonal vectors.','For the third vector, subtract two components.','Check all pairwise inner products before and after normalization.'],proofs)
 if section=='6.1':
  if mode==0:
   a,b,c,alpha,beta=S.symbols('a b c alpha beta',real=True);p=a+b*x+c*x*x;T=lambda f:S.diff(f,x)+k*f.subs(x,0);g=1+x
   return checked('Prove T:P₂→P₁ is linear and determine its action on an arbitrary polynomial.',rf"T(p)=p'+{k}p(0)",None,
    [st('Differentiate an arbitrary input polynomial and evaluate it at zero.',rf"p={latex(p)},\quad p'={latex(S.diff(p,x))},\quad p(0)=a"),st('Combine the two outputs.',rf'T(p)={latex(T(p))}'),st('The result has degree at most one, so it lies in the stated codomain P₁.'),st('Differentiation and evaluation both preserve linear combinations.',rf'T(\alpha p+\beta q)=\alpha T(p)+\beta T(q)'),st('Check the three basis images.',rf'T(1)={k},\quad T(x)=1,\quad T(x^2)=2x'),st('These images determine the output of every polynomial in P₂.')],
    ['Evaluation at zero produces a scalar, interpreted here as a constant polynomial.','Test an arbitrary linear combination.','Check that the result stays in P₁.'],[(T(alpha*p+beta*g),alpha*T(p)+beta*T(g)),(T(p),k*a+b+2*c*x),(T(x*x),2*x)])
  u=M([1,0]);T=lambda v:M([v[0]**2,k*v[1]])
  return checked('T sends zero to zero. Does that prove it is linear? Decide using a specific scalar test.',rf'T(x,y)=(x^2,{k}y)',None,
   [st('Indeed T(0,0)=(0,0), so the necessary zero test passes.'),st('Choose u=(1,0) and scalar 2.',rf'T(u)={latex(T(u))}'),st('Compute T(2u) using the actual formula.',latex(T(2*u))),st('Compute 2T(u) separately.',latex(2*T(u))),st('The first coordinates are 4 and 2, so scalar multiplication is not preserved.'),st('Therefore T is nonlinear even though it preserves zero.')],
    ['The zero test is necessary but not sufficient.','Use a nonzero first coordinate.','Compare T(2u) with 2T(u).'],[(T(S.zeros(2,1)),S.zeros(2,1)),((T(2*u)-2*T(u))[0],S.Integer(2))])
 if section=='6.2':
  if mode==0:
   a,b,c=S.symbols('a b c',real=True);A=M([[0,1,0],[0,0,2]]);null=M([1,0,0]);preimage=k*x+x*x
   return checked(f'For differentiation T:P₂→P₁, find bases for the kernel and range, test one-to-one and onto, and find a preimage of {k}+2x.',rf"T(p)=p',\quad q(x)={k}+2x",None,
    [st('For p=a+bx+cx², the output is b+2cx. It is zero exactly when b=c=0.'),st('The kernel consists of all constants.',r'\ker T=\operatorname{span}\{1\},\quad\operatorname{nullity}T=1'),st('Every linear polynomial d+ex is the derivative of dx+(e/2)x² plus a constant.'),st('Thus the range is all of P₁, with basis (1,x) and rank two.'),st('Nonzero constants map to zero, so T is not one-to-one; it is onto P₁.'),st('For this target, one preimage and all its alternatives are explicit.',rf'p(x)={latex(preimage)}+C'),st('Check dimensions using the domain P₂.',r'1+2=3=\dim P_2')],
    ['Differentiate arbitrary coefficients.','Zero output leaves the constant coefficient free.','Onto concerns the declared codomain P₁.'],[(A*null,S.zeros(2,1)),(S.Integer(A.rank()),S.Integer(2)),(S.diff(preimage,x),k+2*x)])
  A=M([[1,0,k],[0,1,1]]);target=M([k,2]);kernel=M([-k,-1,1]);particular=M([k,2,0]);t=S.Symbol('t',real=True)
  return checked('For T:R³→R², find the kernel, range, and every preimage of b. Decide one-to-one and onto.',rf'T(v)=Av,\quad A={latex(A)},\quad b={latex(target)}',None,
   [st('Set the output coordinates to zero.',rf'x+{k}z=0,\quad y+z=0'),st('Choose z=t and solve for x,y.',rf'\ker T=\operatorname{{span}}\left\{{{latex(kernel)}\right\}}'),st('The first two image columns are the standard basis of R², so the range is all of R².'),st('The kernel has dimension one and range dimension two; their sum is the domain dimension three.'),st('Find a convenient preimage by setting z=0.',latex(particular)),st('Add the full kernel to describe every preimage.',latex(particular+t*kernel)),st('The map is onto, but not one-to-one because its kernel is nontrivial.')],
    ['Solve Av=0 for the kernel.','The output space has dimension two.','A particular preimage plus the kernel gives all preimages.'],[(A*kernel,S.zeros(2,1)),(A*(particular+t*kernel),target),(S.Integer(A.rank()),S.Integer(2))])
 if section=='6.3':
  if mode==0:
   A=M([[1,-k,0,0],[0,0,-1,2],[0,1,1,0]]);input=M([k,1,2,-1]);output=A*input
   return checked('Find the representing matrix for T:M₂ₓ₂→P₂ in the standard entry and monomial bases, then compute T of the given matrix.',rf'T\!\left(\begin{{bmatrix}}a&b\\c&d\end{{bmatrix}}\right)=(a-{k}b)+(2d-c)x+(b+c)x^2,\quad V={latex(M([[k,1],[2,-1]]))}',None,
    [st('Order the input basis as E₁₁,E₁₂,E₂₁,E₂₂ and the output basis as 1,x,x².'),st('Evaluate T on E₁₁ and E₁₂.',rf'T(E_{{11}})=1,\quad T(E_{{12}})=-{k}+x^2'),st('Evaluate T on E₂₁ and E₂₂.',r'T(E_{21})=-x+x^2,\quad T(E_{22})=2x'),st('Place their coefficient columns into a 3×4 matrix.',latex(A)),st('Convert the input matrix to a four-entry coordinate column.',latex(input)),st('Multiply to get the output coefficient column.',latex(output)),st('Reconstruct the polynomial.',latex(output[0]+output[1]*x+output[2]*x*x))],
    ['One column corresponds to each input basis matrix.','Keep the input entry order consistent.','The answer matrix must have three rows and four columns.'],[(A*input,output),(output,M([0,-4,3]))])
  basis=[S.Integer(1),x,x*x,x**3];T=lambda p:2*p+k*S.diff(p,x)-S.diff(p,x,2);images=[S.expand(T(v)) for v in basis];A=M([[p.coeff(x,i) for p in images] for i in range(4)]);input=M([1,-1,k,2]);p=sum(input[i]*basis[i] for i in range(4));output=A*input
  return checked('Build the standard matrix of this polynomial differential operator, then apply it to p.',rf"T(p)=2p+{k}p'-p'',\quad p={latex(p)}",None,
   [st('Use the ordered monomial basis (1,x,x²,x³).'),*[st(f'Apply the operator to basis monomial {i+1}.',rf'T({latex(v)})={latex(images[i])}') for i,v in enumerate(basis)],st('Collect each image’s coefficients as a column.',latex(A)),st('Multiply by the input coefficient vector.',rf'[T(p)]={latex(A)}{latex(input)}={latex(output)}'),st('Reconstruct and independently differentiate the original polynomial to verify.',latex(T(p)))],
    ['Differentiate each monomial once and twice.','Missing powers produce zero entries.','Check the matrix output against direct differentiation.'],[(sum(output[i]*basis[i] for i in range(4)),T(p)),(A.det(),S.Integer(16))])
 if section=='6.4':
  A=M([[k,1],[0,k+1]]);Pmat=M([[1,1],[1,2]]);new=Pmat.inv()*A*Pmat
  if mode==0:
   return checked('Find the matrix in the new basis C=((1,1),(1,2)) and verify its similarity to A.',rf'A={latex(A)},\quad P={latex(Pmat)}',new,
    [st('P sends C-coordinates to standard coordinates because its columns are the C-basis vectors.'),st('Invert the basis matrix.',latex(Pmat.inv())),st('Apply A after converting the input coordinates.',rf'AP={latex(A*Pmat)}'),st('Convert the output back to C-coordinates.',rf'A_{{\mathcal C}}=P^{{-1}}AP={latex(new)}'),st('Check the commuting relation.',rf'AP=PA_{{\mathcal C}}={latex(A*Pmat)}'),st('Trace and determinant remain the same.',rf'\operatorname{{tr}}A_{{\mathcal C}}={S.trace(A)},\quad\det A_{{\mathcal C}}={A.det()}')],
    ['Name the direction of P.','Apply the conversion, transformation, and reverse conversion in that order.','Check AP=P A꜀.'],[(A*Pmat,Pmat*new),(S.trace(A),S.trace(new)),(A.det(),new.det())],'matrix')
  target=M([1,-k]);old=Pmat*target;newout=new*target
  return checked('Given new-basis input coordinates, compute the output coordinates using both paths and explain why they agree.',rf'A={latex(A)},\quad P={latex(Pmat)},\quad[v]_{{\mathcal C}}={latex(target)}',newout,
   [st('Convert the input to the old coordinates.',rf'[v]_{{\rm old}}=P[v]_{{\mathcal C}}={latex(old)}'),st('Apply the old transformation matrix.',rf'[T(v)]_{{\rm old}}=A[v]_{{\rm old}}={latex(A*old)}'),st('Convert that output back.',rf'[T(v)]_{{\mathcal C}}=P^{{-1}}A[v]_{{\rm old}}={latex(newout)}'),st('Alternatively, compute the new transformation matrix.',rf'A_{{\mathcal C}}=P^{{-1}}AP={latex(new)}'),st('Its direct action on new coordinates gives the identical output.',rf'A_{{\mathcal C}}[v]_{{\mathcal C}}={latex(newout)}'),st('This verifies the coordinate changes describe one transformation.')],
    ['The coordinate column belongs to the new basis.','Convert with P before applying A.','Use P⁻¹ to convert the output back.'],[(Pmat.inv()*A*old,newout),(Pmat*newout,A*old)],'matrix')
 if section=='7.1':
  lam=S.Symbol('lambda')
  if mode==0:
   A=M([[k,1,0],[0,k,0],[0,0,k+1]]);e1=M([1,0,0]);e3=M([0,0,1]);char=S.factor((A-lam*S.eye(3)).det())
   return checked('Find all eigenvalues and eigenspace bases, and compare algebraic and geometric multiplicities.',rf'k={k},\quad A={latex(A)}',None,
    [st('Use the triangular diagonal to calculate the characteristic polynomial.',rf'\det(A-\lambda I)={latex(char)}'),st('The repeated eigenvalue k has algebraic multiplicity two; k+1 has multiplicity one.',rf'\lambda_1={k},\quad\lambda_2={k+1}'),st('For λ=k, solve the homogeneous system.',rf'A-{k}I={latex(A-k*S.eye(3))}'),st('It requires the second and third coordinates to vanish, leaving only the first free.',rf'E_{{{k}}}=\operatorname{{span}}\left\{{{latex(e1)}\right\}}'),st('For λ=k+1, the first two coordinates vanish.',rf'E_{{{k+1}}}=\operatorname{{span}}\left\{{{latex(e3)}\right\}}'),st('Check both vectors by direct multiplication.',rf'Ae_1={k}e_1,\quad Ae_3={k+1}e_3'),st('The repeated root has geometric multiplicity one. Only two independent eigenvectors exist, so this 3×3 matrix cannot have an eigenbasis.')],
    ['Repeated roots do not guarantee multiple independent eigenvectors.','Solve a separate null-space equation for each eigenvalue.','Compare each null-space dimension with its root multiplicity.'],[(A*e1,k*e1),(A*e3,(k+1)*e3),(S.Integer(len((A-k*S.eye(3)).nullspace())),S.Integer(1)),(S.Integer(len((A-(k+1)*S.eye(3)).nullspace())),S.Integer(1)),(char,(k-lam)**2*(k+1-lam))])
  A=M([[0,-k],[k,0]]);val=S.I*k;v=M([1,-S.I]);char=(A-lam*S.eye(2)).det()
  return checked('Find eigenvalues over R and over C, and give a complex eigenvector for each complex root.',rf'k={k},\quad A={latex(A)}',None,
   [st('Subtract λ from both diagonal entries.',rf'A-\lambda I={latex(A-lam*S.eye(2))}'),st('Compute the characteristic equation.',rf'\lambda^2+{k*k}=0'),st('Since k is positive, the sum is positive for every real λ. There are no real eigenvalues or real eigenvectors.'),st('Over C, the roots are conjugate imaginary numbers.',rf'\lambda=\pm {k}i'),st('For λ=ki, solve the first row equation and choose a nonzero first coordinate.',rf'v_+={latex(v)}'),st('Conjugation gives the other eigenvector.',rf'v_-={latex(S.conjugate(v))}'),st('Check each eigenpair directly.',rf'Av_+={k}iv_+,\quad Av_-=-{k}iv_-')],
    ['A real matrix can lack real eigenvalues.','Solve λ²=−k² over the requested field.','Verify complex vectors with the same Av=λv equation.'],[(char,lam*lam+k*k),(A*v,val*v),(A*S.conjugate(v),-val*S.conjugate(v))])
 raise ValueError(section)


def expand_linear(lessons,audit,P,st,latex):
 for lesson in lessons:
  if lesson['courseId']!='linear-algebra':continue
  section=lesson['section'];first,last=READINGS[section]
  lesson['sourceReferences']=[{'fileName':'LINEAR PROFESSOR V.pdf','section':section,'pageNumbers':list(range(first,last+1))}]
  lesson['methodGuide']=[{'title':title,'text':text,**({'math':GUIDE_FORMULAS[section]} if i==1 else {})} for i,(title,text) in enumerate(GUIDES[section])]
  lesson['estimatedMinutes']+=20
  lesson['keywords']+= [title for title,_ in GUIDES[section]]
  if section=='2.6':
   lesson['bigIdea']='An invertible matrix can encode a numerical message and then recover it exactly. The professor’s application uses 0 for a blank and 1 through 26 for A through Z. Group the numbers into row blocks of a fixed length, then multiply each block on the right by the encoding matrix.\nDecoding applies the inverse on the right to undo that operation. The order follows the row-vector convention: c=rA means r=cA⁻¹. Encoded numbers need not remain between 0 and 26. This model teaches reversibility and multiplication order; it is not a modern secure encryption method. Other matrix models, such as resource totals and production balances, are included as additional applications.'
   lesson['reasoning']='Multiplying by an invertible matrix is reversible. The identity AA⁻¹=I proves that encoding followed by decoding returns the original row block: (rA)A⁻¹=r. A singular matrix loses some input information and cannot guarantee recovery of every message.'
   lesson['formulas'].insert(0,st('Row-block encoding and decoding.',r'c=rA,\quad r=cA^{-1},\quad\det A\ne0'))
   lesson['keywords']+=['cryptogram','encoding','decoding','message','row block']
   lesson['definitions'] += [st('Cryptogram: a message represented using a chosen encoding rule.'),st('Uncoded row block: a fixed-length row of numerical character codes before matrix multiplication.'),st('Encoding matrix: an invertible square matrix that sends each row block r to rA.'),st('Decoding: right multiplication of a coded row by the inverse encoding matrix to recover its original entries.')]
   lesson['mistakes']+=['Decoding a row block by multiplying the inverse on the left','Turning encoded numbers into letters before decoding','Forgetting to preserve spaces and track padding']
  if section=='4.8':
   lesson['bigIdea']='Here the professor connects vector spaces to homogeneous differential equations. The vectors are functions: adding solutions and multiplying them by constants produces more solutions because the differential operator is linear.\nA regular order-n homogeneous linear equation has an n-dimensional solution space. Finding n functions that solve it is not enough; those functions must also be independent. Verify every function by differentiation and substitution, then use a direct dependence test or a Wronskian to decide whether the list is a basis. Additional coordinate models illustrate the same vector-space ideas with polynomials and matrices.'
   lesson['reasoning']='The zero-output functions of a linear differential operator form its kernel, hence a vector space. Independent solutions provide coordinates for every solution on a regular interval. A Wronskian measures independence through the functions and their derivatives, while an explicit constant relation proves when a proposed list is redundant.'
   lesson['formulas'].insert(0,st('A fundamental solution set gives the general homogeneous solution.',r'y=\sum_{j=1}^{n}C_jy_j,\quad W(y_1,\ldots,y_n)\ne0'))
   lesson['keywords']+=['Wronskian','homogeneous differential equation','solution space','fundamental solution set']
   lesson['definitions'] += [st('Linear differential operator: a rule made from a linear combination of a function and its derivatives, with coefficient functions independent of the input function.'),st('Homogeneous solution space: the functions y satisfying L[y]=0 on a specified interval.'),st('Fundamental solution set: n independent solutions of a regular order-n homogeneous linear ODE; they form a basis for its solution space.'),st('Wronskian: the determinant whose columns are the proposed functions and whose rows contain successive derivatives, used to test independence under the stated hypotheses.',GUIDE_FORMULAS['4.8'])]
   lesson['mistakes']+=['Checking that functions solve the ODE but never checking independence','Using the converse Wronskian test for arbitrary smooth functions','Calling a dependent list a fundamental solution set']
  lesson['summary']=lesson['description']+' '+lesson['reasoning']
  for mode in range(2):
   example=problem(section,mode+2,mode,P,st,latex)
   eid=f'{lesson["id"]}-professor-aligned-example-{mode+1}'
   audit.append({'id':eid,'assertions':example.pop('_proofs')})
   lesson['examples'].append({'title':example['prompt'],'difficulty':mode+2,'steps':[st(example['prompt'],example['math']),*example['solutionSteps']]})
   exercise=problem(section,mode+4,mode,P,st,latex)
   eid=f'{lesson["id"]}-extended-{mode+1}'
   audit.append({'id':eid,'assertions':exercise.pop('_proofs')})
   lesson['exercises'].append({'id':eid,'lessonId':lesson['id'],'difficulty':mode+2,**exercise})
