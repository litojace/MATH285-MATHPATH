"""Author original course content; SymPy checks every newly authored problem.

Run from the repository root with Python 3 + SymPy installed. Generated JSON is
checked in; the deployed application does not require Python or SymPy.
"""
import json
import subprocess
from pathlib import Path
import sympy as S
from linear_professor import expand_linear
from solution_details import enrich_examples
from differential_details import expand_problem
from legacy_example_details import expand_starters

x, y, t, z, s, a, b, c = S.symbols('x y t z s a b c', real=True)
n = S.symbols('n', integer=True, nonnegative=True)
C1, C2 = S.symbols('C_1 C_2', real=True)
R = S.Rational
M = S.Matrix
audit = []

def export(module, name):
    code = f"import {{{name}}} from './{module}';process.stdout.write(JSON.stringify({name}))"
    return json.loads(subprocess.check_output(['./node_modules/.bin/tsx', '-e', code], text=True))

topics = export('src/content/curriculum.ts', 'curriculum')
legacy = {v['id']: v for v in export('src/content/expanded.ts', 'expandedLessons')}
old_ids = {'linear-algebra-1-2': 'systems', 'linear-algebra-4-4': 'vectors',
           'linear-algebra-5-2': 'projection', 'linear-algebra-7-1': 'eigenvalues',
           'differential-equations-2-2': 'separable', 'differential-equations-2-5': 'linear-ode',
           'differential-equations-4-3': 'second-order', 'differential-equations-9-2': 'euler'}

def latex(value):
    return value if isinstance(value, str) else S.latex(value)

def st(text, value=None):
    return {'text': text, **({'math': latex(value)} if value is not None else {})}

def P(prompt, math, answer, steps, hints, proofs, kind='numeric', choices=None):
    assert len(steps) >= 2 and len(hints) == 3 and proofs
    checked = []
    for lhs, rhs in proofs:
        difference = S.simplify(lhs-rhs)
        valid = difference == S.zeros(*difference.shape) if isinstance(difference, S.MatrixBase) else difference == 0
        assert valid, (prompt, lhs, rhs, difference)
        checked.append({'left': str(lhs), 'right': str(rhs)})
    if kind == 'self-check': answer = None
    elif isinstance(answer, S.MatrixBase): answer = [[float(v) for v in row] for row in answer.tolist()]
    elif kind == 'numeric': answer = float(answer)
    return {'prompt': prompt, 'math': latex(math), 'answerType': kind,
            **({'answer': answer} if answer is not None else {}),
            **({'choices': choices} if choices else {}),
            'hints': [st(h) for h in hints], 'solutionSteps': steps,
            'verificationStatus': 'verified', '_proofs': checked}

def la_problem(section, k, mode):
    if section == '1.1':
        if mode == 0:
            u, v = k, k+1
            return P('Solve the system. Enter x and y as a column matrix.',rf'x+y={u+v},\quad x-y={u-v}',M([u,v]),
                [st('Add the equations to eliminate y.',rf'2x={2*u}\Rightarrow x={u}'),st('Substitute x into the first equation.',rf'y={u+v}-{u}={v}'),st('Check both original equations.',rf'{u}+{v}={u+v},\quad {u}-{v}={u-v}')],
                ['Add equations whose y coefficients are opposite.','Divide the resulting equation by 2.','Use either original equation to recover y.'],[(u+v,2*k+1),(u-v,-1)],'matrix')
        consistent = mode == 1
        rhs = 2*k if consistent else 2*k+1
        return P('Classify the number of solutions.',rf'x+y={k},\quad 2x+2y={rhs}', 'Infinitely many' if consistent else 'None',
            [st('Subtract twice the first equation from the second.',rf'0={rhs-2*k}'),st('A zero identity imposes no new restriction; a false identity rules out all solutions.'),st('Write the solution set.' if consistent else 'State why no pair can satisfy both equations.',rf'(x,y)=({k}-t,t),\ t\in\mathbb R' if consistent else r'0\ne1')],
            ['Compare the second equation with twice the first.','Subtract to see whether the constants agree.','Distinguish a redundant equation from a contradiction.'],[(rhs-2*k,0 if consistent else 1)],'multiple-choice',['One','Infinitely many','None'])
    if section == '2.1':
        A=M([[k,1],[2,k+1]]);B=M([[1,2],[0,k]])
        result=[A+B,A*B,(A*B).T][mode]
        title=['Find A+B.','Find AB in the stated order.','Find the transpose of AB.'][mode]
        steps=[st('Check dimensions: both matrices are 2×2.'),st('For the product, use every row-column pairing.' if mode else 'Add entries in matching positions.',rf'AB=\begin{{bmatrix}}{k}(1)+1(0)&{k}(2)+1({k})\\2(1)+({k+1})(0)&2(2)+({k+1})({k})\end{{bmatrix}}' if mode else A+B),st('Simplify the product, then transpose it.' if mode==2 else 'Simplify the entries.',result),st('For a transpose, move (i,j) to (j,i).' if mode==2 else 'Check the top-left entry.',rf'{k}+1={k+1}' if mode==0 else rf'{k}(1)+1(0)={k}')]
        return P(title,rf'A={latex(A)},\quad B={latex(B)}',result,steps,
            ['Check that the requested operation is defined.','Track row and column positions carefully.','Compute one entry at a time; multiplication is not entrywise.'],[(result,[A+B,A*B,B.T*A.T][mode])],'matrix')
    if section == '2.2':
        A=M([[1,k],[0,1]]);B=M([[1,0],[k,1]])
        if mode==0:
            return P('Find AB−BA. This measures the failure of commutativity.',rf'A={latex(A)},\ B={latex(B)}',A*B-B*A,
                [st('Compute AB by row-column multiplication.',A*B),st('Compute BA separately.',B*A),st('Subtract corresponding entries.',A*B-B*A)],
                ['Calculate both orders instead of assuming they agree.','The top-left and bottom-right entries change.','Subtract BA from AB entry by entry.'],[(A*B-B*A,M([[k*k,0],[0,-k*k]]))],'matrix')
        if mode==1:
            return P('Find A(B+I) using distributivity.',rf'A={latex(A)},\ B={latex(B)}',A*(B+S.eye(2)),
                [st('Split the product.',r'A(B+I)=AB+AI=AB+A'),st('Compute AB.',A*B),st('Add A.',A*B+A)],
                ['Distribute from the left without reversing order.','Multiplication by I leaves A unchanged.','Add the two resulting matrices.'],[(A*(B+S.eye(2)),A*B+A)],'matrix')
        return P('Can two nonzero matrices have zero product?',rf'A={latex(M([[k,0],[0,0]]))},\ B={latex(M([[0,0],[0,k]]))}','Yes',
            [st('Neither matrix is zero because k is positive.'),st('Multiply each row by each column.',S.zeros(2)),st('This disproves the scalar-style rule AB=0 ⇒ A=0 or B=0.')],
            ['Inspect which rows and columns contain the nonzero entries.','Compute all four row-column products.','One counterexample disproves a universal claim.'],[(M([[k,0],[0,0]])*M([[0,0],[0,k]]),S.zeros(2))],'multiple-choice',['Yes','No'])
    if section == '2.3':
        A=M([[1,k],[0,1]]) if mode==0 else M([[k,1],[1,0]])
        inv=A.inv()
        if mode<2:
            inverse_steps = [st('Compute the determinant and check it is nonzero.',A.det()),st('Swap diagonal entries, negate off-diagonal entries, then divide by the determinant.',inv),st('Verify the product is the identity.',A*inv)]
            if mode == 0:
                inverse_steps = [st('Augment A with the identity.',rf'\left[\begin{{array}}{{cc|cc}}1&{k}&1&0\\0&1&0&1\end{{array}}\right]'),st('Clear the entry above the second pivot.',rf'R_1\leftarrow R_1-{k}R_2'),st('The left block is now I; read the right block as the inverse.',inv),st('Multiply by A to verify.',A*inv)]
            return P('Find the inverse. Enter a 2×2 matrix.',rf'A={latex(A)}',inv,
                inverse_steps,
                ['An inverse requires a nonzero determinant.','For 2×2 matrices use the adjugate formula.','Multiply A by your candidate to confirm every entry.'],[(A*inv,S.eye(2)),(inv*A,S.eye(2))],'matrix')
        target=M([k,k+1]);rhs=A*target
        return P('Solve AX=b using the inverse. Enter X as a column matrix.',rf'A={latex(A)},\quad b={latex(rhs)}',target,
            [st('The determinant is −1, so the inverse exists.'),st('Multiply both sides on the left by the inverse.',rf'X=A^{{-1}}b={latex(inv)}{latex(rhs)}'),st('Perform the product.',target),st('Substitute into the original equation.',A*target)],
            ['Left-multiply AX=b by A⁻¹.','Keep the order A⁻¹b.','Check your result using AX, not just the inverse formula.'],[(A*target,rhs)],'matrix')
    if section == '2.4':
        E=[M([[0,1],[1,0]]),M([[k+1,0],[0,1]]),M([[1,0],[k,1]])][mode]
        op=['Swap rows 1 and 2.','Multiply row 1 by the stated nonzero factor.',f'Add {k} times row 1 to row 2.'][mode]
        A=M([[1,2],[3,4]])
        return P('Construct the elementary matrix E for this operation.',rf'\text{{{op}}}\quad c={k+1}',E,
            [st('Start from the 2×2 identity.',S.eye(2)),st('Apply the requested row operation to I, not to A.',E),st('Check its action on a sample matrix.',rf'EA={latex(E*A)}'),st('Its inverse undoes the row operation.',E.inv())],
            ['An elementary matrix is a row operation applied to I.','Preserve the untouched row of I.','Left multiplication applies this operation to any compatible matrix.'],[(E.inv()*E,S.eye(2)),(E*A,[M([[3,4],[1,2]]),M([[k+1,2*(k+1)],[3,4]]),M([[1,2],[k+3,2*k+4]])][mode])],'matrix')
    if section == '2.6':
        if mode==0:
            A=M([[2,3],[1,4]]);q=M([k,k+1]);answer=A*q
            return P('Find the output vector: total cost and total labor.',rf'A={latex(A)},\ q={latex(q)},\quad \text{{output}}=Aq',answer,
                [st('Columns represent products; rows represent cost and labor.'),st('Take each resource row dotted with the quantity vector.',rf'\text{{cost}}=2({k})+3({k+1}),\quad\text{{labor}}={k}+4({k+1})'),st('Report both outputs with their appropriate units.',answer)],
                ['A quantity vector has one entry per product.','Each output totals one resource across products.','Multiply A by q in that order.'],[(answer,M([5*k+3,5*k+4]))],'matrix')
        if mode==1:
            transition=M([[R(3,4),R(1,4)],[R(1,4),R(3,4)]]);v=M([4*k,0]);out=transition*v
            return P('Compute the next population distribution.',rf'p_{{next}}=Pp,\quad P={latex(transition)},\quad p={latex(v)}',out,
                [st('Each column gives the destinations of one source population.'),st('Multiply the transition matrix by the current distribution.',out),st('Check that total population is conserved.',rf'{3*k}+{k}={4*k}')],
                ['Use column-vector conventions.','Each column of P sums to one.','Check the sum of the resulting entries.'],[(out,M([3*k,k])),(sum(out),sum(v))],'matrix')
        A=M([[1,R(-1,4)],[R(-1,4),1]]);out=M([4*k,4*k]);d=A*out
        return P('Solve the two-sector production model (I−C)q=d.',rf'I-C={latex(A)},\quad d={latex(d)}',out,
            [st('Total production must cover internal consumption plus external demand.',r'q=Cq+d\Rightarrow(I-C)q=d'),st('The determinant 15/16 is nonzero.',A.inv()),st('Multiply the inverse by demand.',out),st('Verify the net available production.',A*out)],
            ['Move internal consumption to the left.','Invert I−C, rather than C.','Substitute the output into (I−C)q=d.'],[(A*out,d)],'matrix')
    if section == '3.1':
        A=[M([[k,2],[1,3]]),M([[1,2,0],[0,k,1],[2,0,3]]),M([[k,1,0],[0,2,1],[0,0,3]])][mode]
        value=A.det()
        if mode==0: steps=[st('Use ad−bc.',rf'\det A=({k})(3)-(2)(1)'),st('Simplify.',value)]
        elif mode==1: steps=[st('Expand along row 1 with signs +,−,+.',rf'\det A=1({3*k})-2(-2)+0'),st('Simplify.',value),st('The cofactor sign belongs to its position, not to the entry itself.')]
        else: steps=[st('The matrix is triangular, so multiply its diagonal entries.',rf'\det A=({k})(2)(3)'),st('Simplify.',value)]
        return P('Calculate the determinant.',A,value,steps,
            ['Choose a 2×2 rule or a convenient cofactor expansion.','Include alternating cofactor signs.','For a triangular matrix, only the diagonal product is needed.'],[(value,[3*k-2,3*k+4,6*k][mode])])
    if section == '3.2':
        A=M([[1,k,0],[2,2*k+1,1],[0,0,3]])
        U=M([[1,k,0],[0,1,1],[0,0,3]])
        value=[3,-3,3*(k+1)][mode]
        label=['after row replacement R₂←R₂−2R₁','after additionally swapping rows 1 and 2',f'after additionally scaling row 3 by {k+1}'][mode]
        return P(f'Find the determinant {label}.',rf'A={latex(A)}',value,
            [st('Row replacement leaves the determinant unchanged.',U),st('Multiply the diagonal of the triangular matrix.',r'\det U=1\cdot1\cdot3=3'),st(['No extra determinant factor is needed.','One row swap changes the sign.','Scaling one row scales the determinant once.'][mode],rf'\det={value}')],
            ['First reduce with a determinant-preserving row replacement.','Keep a record of swaps and row scalings.','Do not confuse row replacement with row scaling.'],[(A.det(),3),([3,-A.det(),(k+1)*A.det()][mode],value)])
    if section == '3.3':
        detA=k+1; detB=-2;value=[detA*detB,R(1,detA),4*detA][mode]
        math=[rf'\det A={detA},\quad\det B=-2;\quad\text{{find }}\det(AB)',rf'\det A={detA};\quad\text{{find }}\det(A^{{-1}})',rf'A\in\mathbb R^{{2\times2}},\quad\det A={detA};\quad\text{{find }}\det(2A)'][mode]
        return P('Use determinant identities to calculate the requested value.',math,value,
            [st(['Determinants multiply even when matrices do not commute.','A nonzero determinant makes the inverse available.','Scaling a 2×2 matrix scales two rows.'][mode]),st([r'\det(AB)=\det A\det B',r'\det(A^{-1})=1/\det A',r'\det(cA)=c^2\det A'][mode]),st('Substitute the given determinant.',value)],
            ['Choose the identity for this operation.','For cA include one factor c for every row.','For an inverse take the reciprocal, not the negative.'],[([detA*detB,R(1,detA),2**2*detA][mode],value)])
    if section == '3.4':
        A=M([[2,1],[1,1]]);v=M([k,k+1]);rhs=A*v
        if mode==0:
            Ai=A.copy();Ai[:,0]=rhs
            return P('Use Cramer’s Rule to find x.',rf'2x+y={rhs[0]},\quad x+y={rhs[1]}',k,
                [st('Find the denominator determinant.',rf'\det A=2(1)-1(1)=1'),st('Replace the x-column by the constants.',Ai),st('Divide determinants.',rf'x=\frac{{{Ai.det()}}}{{1}}={k}'),st('Verify using y.',rf'y={k+1}')],
                ['Only replace the column belonging to x.','Keep the other coefficient column unchanged.','Cramer’s Rule requires det A≠0.'],[(Ai.det()/A.det(),k),(A*v,rhs)])
        if mode==1:
            A=M([[k+1,1],[1,1]])
            adj=A.adjugate()
            return P('Find the adjugate of A.',A,adj,
                [st('Compute the cofactor matrix.',A.cofactor_matrix()),st('Transpose the cofactor matrix.',adj),st('Check the defining identity.',rf'A\operatorname{{adj}}(A)={latex(A*adj)}')],
                ['Compute signed minors.','Transpose the cofactor matrix.','For 2×2 matrices swap diagonal entries and negate off-diagonal entries.'],[(A*adj,A.det()*S.eye(2))],'matrix')
        B=M([[1,k],[2,2*k]])
        return P('Is this coefficient matrix invertible?',B,'No',
            [st('Compute the determinant.',rf'1({2*k})-{k}(2)=0'),st('A zero determinant means the columns are dependent.'),st('The second column is k times the first; the inverse does not exist.')],
            ['Calculate ad−bc.','Look for a proportional row or column.','Invertibility is equivalent to a nonzero determinant.'],[(B.det(),0)],'multiple-choice',['Yes','No'])
    if section == '4.1':
        u=M([k,1,-1]);v=M([1,k,2]);result=[u+v,2*u-v,u.dot(v)][mode]
        return P(['Add u and v.','Find the linear combination 2u−v.','Find the dot product u·v.'][mode],rf'u={latex(u)},\quad v={latex(v)}',result,
            [st('Align components in the same coordinate positions.'),st(['Add each matching pair.','Scale every component of u before subtracting v.','Multiply matching coordinates and sum.'][mode],rf'\text{{result}}={latex(result)}'),st('The result is a vector for the first two operations and a scalar for a dot product.')],
            ['Use all three coordinates.','A minus sign applies to every component of the subtracted vector.','Check whether the requested answer is a vector or a scalar.'],[(result,[M([k+1,k+1,1]),M([2*k-1,2-k,-4]),2*k-2][mode])],'numeric' if mode==2 else 'matrix')
    if section == '4.2':
        if mode==0:
            poly=k*x*x+2*x-3
            return P('Find the additive inverse of p in P₂. Compare your polynomial.',rf'p(x)={latex(poly)}',None,
                [st('An additive inverse must sum with p to the zero polynomial.'),st('Negate every coefficient.',-poly),st('Verify all coefficients cancel.',S.expand(poly-poly))],
                ['The zero vector in P₂ is the zero polynomial.','Negate all coefficients, including the constant.','Add your candidate to the original polynomial.'],[(poly+(-poly),0)],'self-check')
        if mode==1:
            degree=k+1
            return P(f'Do polynomials of degree exactly {degree} form a real vector space?',rf'\{{p:\deg p={degree}\}}','No',
                [st('Take a polynomial of the requested degree.',x**degree),st('Its additive inverse has the same degree.',-x**degree),st('Their sum is the zero polynomial, which is excluded.',S.Integer(0)),st('Therefore addition is not closed; zero is also missing.')],
                ['A vector space must contain its zero vector.','Add p and −p.','Distinguish degree at most n from degree exactly n.'],[(x**degree-x**degree,0)],'multiple-choice',['Yes','No'])
        A=M([[k,1],[0,-k]]);inv=-A
        return P('Find the additive inverse of A in the space of 2×2 matrices.',A,inv,
            [st('The matrix zero vector has zero in all four positions.',S.zeros(2)),st('Negate every entry.',inv),st('Check A+(−A).',A+inv)],
            ['This asks for an additive inverse, not a multiplicative inverse.','Negate each entry.','Check that addition produces the zero matrix.'],[(A+inv,S.zeros(2))],'matrix')
    if section == '4.3':
        if mode==0:
            return P('Is W a subspace of R³?',rf'W=\{{(x,y,z):x+{k}y-z=0\}}','Yes',
                [st('Zero satisfies the homogeneous constraint.'),st('Let u and v satisfy it; expand the constraint on au+bv.',rf'(au_1+bv_1)+{k}(au_2+bv_2)-(au_3+bv_3)=a(0)+b(0)=0'),st('Zero and closure under arbitrary linear combinations prove the subspace test.')],
                ['Check zero first.','The right side is zero, so the constraint is homogeneous.','Apply the defining equation to a general linear combination.'],[(S.expand(a*(x+k*y-z)+b*(x+k*y-z)),(a+b)*(x+k*y-z))],'multiple-choice',['Yes','No'])
        if mode==1:
            return P('Is W a subspace of R²?',rf'W=\{{(x,y):x+y={k}\}}','No',
                [st('Substitute the zero vector.',rf'0+0=0\ne{k}'),st('A subspace must contain zero.'),st('The nonzero right side shifts a line away from the origin.')],
                ['The zero-vector test can disprove the claim immediately.','Substitute (0,0).','A translated line need not be a subspace.'],[(S.Integer(k)-0,k)],'multiple-choice',['Yes','No'])
        degree=k+1
        return P(f'Find the dimension of the subspace of P{degree} satisfying p(0)=0.',rf'W=\{{p\in P_{{{degree}}}:p(0)=0\}}',degree,
            [st('Write a general polynomial.',rf'p(x)=c_0+c_1x+\cdots+c_{{{degree}}}x^{{{degree}}}'),st('At zero only the constant survives, so c₀=0.'),st('The remaining monomials span W and are independent.',rf'\mathcal B=(x,x^2,\ldots,x^{{{degree}}}),\quad\dim W={degree}')],
            ['Write a general polynomial with three coefficients.','The condition removes one coefficient.','Count independent remaining monomials.'],[(S.diff(b*x+c*x*x,x).subs(x,0),b),(S.diff(b*x+c*x*x,x,2),2*c)])
    if section == '4.5':
        if mode==0:
            B=M([[1,1],[0,1]]);v=M([2*k,k]);coords=M([k,k])
            return P('Find [v]B for the ordered basis B=(b₁,b₂).',rf'b_1={latex(B[:,0])},\ b_2={latex(B[:,1])},\ v={latex(v)}',coords,
                [st('Set v=c₁b₁+c₂b₂.',rf'c_1+c_2={2*k},\quad c_2={k}'),st('Solve for the ordered coefficients.',coords),st('Reconstruct v to check.',B*coords)],
                ['Coordinates are coefficients, not necessarily the original entries.','Place basis vectors in columns in the stated order.','Solve Bc=v.'],[(B*coords,v)],'matrix')
        if mode==1:
            degree=k+2
            return P(f'Find dim P{degree}.',rf'P_{{{degree}}}=\{{p:\deg p\le {degree}\}}',degree+1,
                [st('Use the spanning monomials.',rf'1,x,x^2,\ldots,x^{{{degree}}}'),st('If their combination is zero, every polynomial coefficient must be zero.'),st(f'There are {degree+1} independent monomials, including the constant.')],
                ['Include the constant polynomial.','Count coefficients from degree zero through degree n.','A basis must be independent as well as spanning.'],[(len([x**j for j in range(degree+1)]),degree+1)])
        B=M([[1,0,1],[0,1,k],[0,0,0]])
        return P('How many columns belong to a basis of the column space?',B,2,
            [st('The first two columns are independent.'),st('The third is their linear combination.',rf'c_3=c_1+{k}c_2'),st('Keep original columns 1 and 2; they form a two-element basis.')],
            ['Identify independent columns.','Try expressing column 3 using columns 1 and 2.','A basis removes redundant vectors without changing the span.'],[(B[:,2],B[:,0]+k*B[:,1]),(B.rank(),2)])
    if section == '4.6':
        A=M([[1,0,k],[0,1,1],[0,0,0]])
        if mode==0:
            return P('Find the nullity of A.',A,1,
                [st('There are two pivots, so rank A=2.'),st('There are three variable columns.',r'\operatorname{nullity}A=3-2=1'),st('Solve Ax=0 to display the remaining direction.',rf'\ker A=\operatorname{{span}}\{{(-{k},-1,1)\}}')],
                ['Count variable columns, not rows alone.','Apply rank plus nullity equals number of columns.','Each nonpivot column contributes a free variable.'],[(A*M([-k,-1,1]),S.zeros(3,1)),(len(A.nullspace()),1)])
        if mode==1:
            rhs=M([k,1,1])
            return P('Is Ax=b consistent?',rf'A={latex(A)},\quad b={latex(rhs)}','No',
                [st('Inspect the last equation: the last row of A is zero.',r'0=1'),st('The augmented column adds a pivot.',rf'\operatorname{{rank}}A=2,\quad\operatorname{{rank}}[A|b]=3'),st('Unequal ranks prove inconsistency.')],
                ['Look for a zero coefficient row with a nonzero constant.','Consistency requires equal coefficient and augmented ranks.','Do not treat the augmented pivot as a variable pivot.'],[(A.rank(),2),(A.row_join(rhs).rank(),3)],'multiple-choice',['Yes','No'])
        return P('Find the rank and nullity as a column vector (rank; nullity).',A,M([2,1]),
            [st('The first two rows are independent; the last is zero.',r'\operatorname{rank}A=2'),st('Subtract rank from the number of columns.',r'\operatorname{nullity}A=3-2=1'),st('Column space is the xy-plane; null space is a line, both inside R³.')],
            ['Count pivot rows for rank.','The dimension of the domain is three.','Rank-nullity describes domain dimensions, not codomain dimensions.'],[(A.rank(),2),(len(A.nullspace()),1)],'matrix')
    if section == '4.7':
        B=M([[1,k],[0,1]]);D=M([[1,0],[1,1]]);v=M([k+1,1])
        result=[B.inv()*v,D.inv()*B,D.inv()*B*M([1,k])][mode]
        math=[rf'B={latex(B)},\ v={latex(v)};\ \text{{find }}[v]_B',rf'B={latex(B)},\ C={latex(D)};\ \text{{find }}P_{{C\leftarrow B}}',rf'B={latex(B)},\ C={latex(D)},\ [v]_B={latex(M([1,k]))};\ \text{{find }}[v]_C'][mode]
        return P('Convert the stated coordinates. Basis matrices have basis vectors as columns.',math,result,
            [st('Recover the standard vector before changing coordinates.',r'v=B[v]_B'),st('Express that same vector using C.',r'[v]_C=C^{-1}B[v]_B' if mode else r'[v]_B=B^{-1}v'),st('Perform the matrix operations in order.',result),st('The represented vector stays the same even though its coordinates change.')],
            ['Identify source and destination bases.','Use destination inverse times source.','Reconstruct the standard vector to confirm the direction of the conversion.'],[([B*result,D*result,D*result][mode],[v,B,B*M([1,k])][mode])],'matrix')
    if section == '4.8':
        if mode==0:
            poly=k+(k+1)*x+2*x*x
            return P('Find the coefficient vector of p in the ordered basis (1,x,x²).',poly,M([k,k+1,2]),
                [st('Match the constant, linear, and quadratic terms in that order.'),st('Record the coefficient of each basis polynomial.',M([k,k+1,2])),st('Reconstruct p from the coordinates.',poly)],
                ['Follow the stated basis order.','The constant coefficient belongs in the first entry.','Do not substitute a value of x: this is a polynomial vector.'],[(k+(k+1)*x+2*x*x,poly)],'matrix')
        if mode==1:
            size=k+1;dimension=size*(size+1)//2
            return P(f'Find the dimension of symmetric {size}×{size} real matrices.',rf'W=\{{A\in\mathbb R^{{{size}\times{size}}}:A^T=A\}}',dimension,
                [st('Symmetry fixes each entry below the diagonal from its partner above.'),st('Count the independent diagonal and above-diagonal entries.',rf'{size}+\frac{{{size}({size}-1)}}2={dimension}'),st('A basis has one matrix per diagonal position and one symmetric pair per above-diagonal position.')],
                ['Impose Aᵀ=A before counting entries.','Do not count equal off-diagonal partners twice.','Choose entries on or above the diagonal freely.'],[(sum(size-j for j in range(size)),dimension)])
        poly=k*(1+x)+(k+1)*(x+x*x)
        return P('Find coordinates of p in the ordered basis (1+x, x+x²) of its span.',poly,M([k,k+1]),
            [st('Write p=α(1+x)+β(x+x²).'),st('Compare the constant and quadratic coefficients.',rf'\alpha={k},\quad\beta={k+1}'),st('The linear coefficient must also agree.',rf'\alpha+\beta={2*k+1}'),st('This consistency check confirms the vector lies in the stated span.')],
            ['Match constant and quadratic coefficients first.','Check the middle coefficient instead of ignoring it.','Coordinates describe the chosen subspace, not all of P₂.'],[(S.expand(poly),k+(2*k+1)*x+(k+1)*x*x)],'matrix')
    if section == '5.1':
        u=M([3*k,4*k]);v=M([4*k,-3*k]);val=[5*k,0,R(3,5)][mode]
        math=[rf'u={latex(u)};\ \text{{find }}\|u\|',rf'u={latex(u)},\ v={latex(v)};\ \text{{find }}u\cdot v',rf'p=(1,0),\ q=({3*k},{4*k});\ \text{{find }}\cos\theta'][mode]
        return P('Calculate the requested geometric quantity.',math,val,
            [st(['Square components and add.','Multiply matching components and add.','Find the dot product and both lengths.'][mode], [rf'{3*k}^2+{4*k}^2={25*k*k}',rf'({3*k})({4*k})+({4*k})(-{3*k})=0',rf'p\cdot q={3*k},\quad\|p\|=1,\quad\|q\|={5*k}'][mode]),st('Use the norm, dot product, or angle formula.',val),st(['Take the positive square root for a length.','Zero dot product means these nonzero vectors are perpendicular.','The angle is arccos(3/5), approximately 53.13 degrees.'][mode])],
            ['Choose the formula that matches the requested quantity.','Keep signs when multiplying coordinates.','For an angle divide the dot product by both positive lengths.'],[([S.sqrt(u.dot(u)),u.dot(v),R(3*k,5*k)][mode],val)])
    if section == '5.3':
        if mode==0:
            u=M([1,0]);v=M([k,1]);out=v-(v.dot(u)/u.dot(u))*u
            return P('Find the second orthogonal vector u₂ before normalization.',rf'v_1={latex(u)},\quad v_2={latex(v)}',out,
                [st('Set u₁=v₁ and compute the projection coefficient.',rf'\frac{{v_2\cdot u_1}}{{u_1\cdot u_1}}={k}'),st('Subtract the projection.',out),st('Check that the new vector is perpendicular to u₁.',out.dot(u))],
                ['Use the unnormalized first vector consistently.','Subtract the projection onto that vector.','Only normalize if the question requests a unit vector.'],[(out.dot(u),0),(out,M([0,1]))],'matrix')
        if mode==1:
            out=M([R(3,5),R(4,5)])
            return P('Normalize the orthogonal vector u₁.',M([3*k,4*k]),out,
                [st('Compute its length.',5*k),st('Divide every component by that length.',out),st('Check the resulting norm is one.',out.dot(out))],
                ['Use the positive length.','Normalize by the same scalar in every component.','A normalized vector should have squared length 1.'],[(out.dot(out),1)],'matrix')
        u=M([1,1,0]);v=M([k,k,1]);out=M([0,0,1])
        return P('Find u₂ in the Gram–Schmidt process.',rf'v_1={latex(u)},\quad v_2={latex(v)}',out,
            [st('Set u₁=v₁. Compute the coefficient.',rf'\frac{{v_2\cdot u_1}}{{u_1\cdot u_1}}=\frac{{{2*k}}}{{2}}={k}'),st('Remove the component in the first direction.',rf'u_2=v_2-{k}u_1={latex(out)}'),st('The third direction is perpendicular to u₁ and already unit length.')],
            ['Compute both dot products in R³.','Remove the entire projected vector.','Check orthogonality and nonzero length.'],[(v-k*u,out),(u.dot(out),0)],'matrix')
    if section == '5.2':
        if mode==0:
            value=2*k*k+3*(2*k)**2
            return P('Find the squared norm in this weighted inner product.',rf'\langle u,v\rangle=2u_1v_1+3u_2v_2,\quad w=({k},{2*k})',value,
                [st('The squared norm is the inner product of w with itself.',r'\|w\|^2=\langle w,w\rangle'),st('Include the positive coordinate weights.',rf'2({k})^2+3({2*k})^2={value}'),st('Positive weights make this form positive definite, so it is an inner product.')],
                ['Use the specified inner product instead of the ordinary dot product.','Insert w into both argument positions.','The question asks for squared norm, so do not take a square root.'],[(2*k*k+3*4*k*k,value)])
        if mode==1:
            f=k*t
            value=S.integrate(f,(t,0,1))
            return P('Find the inner product of f and g in this function space.',rf'\langle f,g\rangle=\int_0^1 f(t)g(t)dt,\quad f(t)={k}t,\quad g(t)=1',value,
                [st('Multiply the two functions.',f),st('Integrate their product on the prescribed interval.',rf'\int_0^1{k}t\,dt=\left[\frac{{{k}t^2}}2\right]_0^1'),st('Evaluate the endpoints.',value)],
                ['A function inner product returns a scalar.','Use the interval in the definition.','Integrate the product, rather than multiplying two separate integrals.'],[(S.integrate(f,(t,0,1)),R(k,2))])
        f=k*t;coef=R(k,2)
        return P('Project the function f onto the span of the constant function 1.',rf'\langle f,g\rangle=\int_0^1 f(t)g(t)dt,\quad f(t)={k}t',None,
            [st('Compute the numerator and denominator.',rf'\langle f,1\rangle={latex(coef)},\quad\langle1,1\rangle=1'),st('The projected function is a constant.',rf'p(t)={latex(coef)}'),st('The residual has zero inner product with 1.',rf'\int_0^1({k}t-{latex(coef)})dt=0'),st('This constant is the best approximation to f in the inner-product norm.')],
            ['Projection works in function spaces as well as Rⁿ.','Divide the two inner products.','Check orthogonality of the residual by integrating it against 1.'],[(S.integrate(f-coef,(t,0,1)),0)],'self-check')
    if section == '6.1':
        if mode==0:
            return P('Find T(v).',rf'T(x,y)=(x+{k}y,2y),\quad v=(1,2)',M([1+2*k,4]),
                [st('Substitute the two coordinates into the rule.',rf'T(1,2)=(1+{k}(2),2(2))'),st('Simplify the two outputs.',M([1+2*k,4])),st('This rule is linear because it is multiplication by a fixed matrix.',M([[1,k],[0,2]]))],
                ['Distinguish the input pair from the output pair.','Evaluate each output component.','A fixed matrix defines a linear transformation.'],[(M([[1,k],[0,2]])*M([1,2]),M([1+2*k,4]))],'matrix')
        if mode==1:
            return P('Is T linear?',rf'T(x,y)=(x+{k},y)','No',
                [st('Every linear transformation sends zero to zero.'),st('Evaluate this rule at zero.',M([k,0])),st('The nonzero constant translation violates linearity.')],
                ['Try the zero test before a lengthy calculation.','Do not confuse a straight-line graph with a linear map.','A nonzero constant offset cannot appear in a linear transformation.'],[(M([0+k,0]),M([k,0]))],'multiple-choice',['Yes','No'])
        return P(f'Is T linear from P{k+1} to P{k}?',r'T(p)=p\prime','Yes',
            [st('For example, differentiate a quadratic.',r'T(a+bx+cx^2)=b+2cx'),st('Differentiation preserves sums and scalar multiples.',r'T(\alpha p+\beta q)=\alpha T(p)+\beta T(q)'),st('Differentiation lowers a nonconstant polynomial degree by one, so every output lies in the stated codomain.')],
            ['Use differentiation rules for sums.','Use the constant-multiple derivative rule.','Check that the output lies in P₁.'],[(S.diff(a*(x*x+k*x)+b*(x+1),x),a*S.diff(x*x+k*x,x)+b*S.diff(x+1,x))],'multiple-choice',['Yes','No'])
    if section == '6.2':
        A=M([[1,k,0],[0,0,1]])
        if mode==0:
            out=M([-k,1,0])
            return P('Find a kernel basis vector with second component 1.',A,out,
                [st('Set Av=0.',rf'x+{k}y=0,\quad z=0'),st('Choose the free variable y=1.',out),st('Every kernel vector is a scalar multiple of this one.',rf'\ker T=\operatorname{{span}}\{{{latex(out)}\}}')],
                ['The kernel consists of inputs, so use three components.','Solve the homogeneous system.','Choose a convenient value of the free variable.'],[(A*out,S.zeros(2,1))],'matrix')
        if mode==1:
            return P('Is T:R³→R² onto?',rf'T(v)=Av,\quad A={latex(A)}','Yes',
                [st('Columns 1 and 3 are the standard basis of R².'),st('For any (a,b), choose the input (a,0,b).',rf'T(a,0,b)=(a,b)'),st('Every codomain vector is reached; rank T=2.')],
                ['Onto compares the range with the codomain.','Look for independent columns spanning R².','Construct an input for an arbitrary desired output.'],[(A*M([a,0,b]),M([a,b]))],'multiple-choice',['Yes','No'])
        return P('Is this T one-to-one?',rf'T(v)=Av,\quad A={latex(A)}','No',
            [st('Find a nonzero input sent to zero.',M([-k,1,0])),st('Multiply to verify.',A*M([-k,1,0])),st('A nontrivial kernel means distinct inputs can share an output.')],
            ['One-to-one is equivalent to a zero kernel.','There are more input coordinates than independent output equations.','Exhibit a nonzero vector mapped to zero.'],[(A*M([-k,1,0]),S.zeros(2,1))],'multiple-choice',['Yes','No'])
    if section == '6.3':
        A=M([[1,k],[0,2]]);B=M([[0,-1],[1,0]])
        result=[A,B*A,A*M([k,1])][mode]
        math=[rf'T(e_1)={latex(A[:,0])},\quad T(e_2)={latex(A[:,1])};\ \text{{find }}[T]',rf'[T]={latex(A)},\quad[S]={latex(B)};\ \text{{find }}[S\circ T]',rf'T(x,y)=(x+{k}y,2y);\quad\text{{find }}T({k},1)'][mode]
        return P('Find the requested matrix or output.',math,result,
            [st(['Put the image of e₁ in column 1 and the image of e₂ in column 2.','The map T acts first, so its matrix is on the right.','Use the standard matrix of T.'][mode]),st(['Assemble the columns.','Multiply [S][T] in that order.','Multiply the matrix by the input column.'][mode],result),st('Check by applying the rule to the standard basis or the specified input.')],
            ['Images of basis vectors are columns.','Composition reads right to left in a matrix product.','Check dimensions before multiplication.'],[(result,[M([[1,k],[0,2]]),M([[0,-2],[1,k]]),M([2*k,2])][mode])],'matrix')
    if section == '6.4':
        A=M([[1,0],[0,2]]);B=M([[1,k],[0,1]]);similar=B.inv()*A*B
        if mode==0:
            return P('Find the matrix of the same transformation in basis B.',rf'A={latex(A)},\quad P={latex(B)}',similar,
                [st('P maps B-coordinates to standard coordinates.',r'[T]_B=P^{-1}AP'),st('Compute AP.',A*B),st('Left-multiply by P⁻¹.',similar),st('Check AP=P[T]B.',A*B)],
                ['Use P⁻¹AP, not PAP⁻¹.','The rightmost P converts input coordinates first.','The leftmost inverse converts the output back.'],[(A*B,B*similar)],'matrix')
        if mode==1:
            return P('Find the determinant of the similar matrix P⁻¹AP.',rf'A={latex(A)},\quad P={latex(B)}',2,
                [st('Use the product rule for determinants.',r'\det(P^{-1}AP)=\det(P)^{-1}\det(A)\det(P)'),st('Cancel the inverse determinant factors.',r'\det(P^{-1}AP)=\det A=2'),st('Similarity preserves determinant and characteristic polynomial.')],
                ['The change-of-basis matrix must be invertible.','Use the reciprocal determinant for P⁻¹.','Similar matrices share the same determinant.'],[(similar.det(),A.det())])
        return P('Find the trace of P⁻¹AP.',rf'A={latex(A)},\quad P={latex(B)}',3,
            [st('Compute the similar matrix if needed.',similar),st('Add its diagonal entries.',r'\operatorname{tr}(P^{-1}AP)=1+2=3'),st('Trace is another similarity invariant.')],
            ['Trace means the sum of diagonal entries.','Changing basis does not change trace.','Off-diagonal entries do not contribute.'],[(S.trace(similar),S.trace(A))])
    raise ValueError(('Unhandled Linear Algebra section', section))

def L(f):
    return S.laplace_transform(f, t, s, noconds=True)

def de_problem(section, k, mode):
    return expand_problem(_de_problem(section,k,mode),section,k,mode,st)

def _de_problem(section, k, mode):
    if section == '1.1':
        if mode==0:
            order=k
            return P('State the order of this ODE.',rf'y^{{({order})}}+xy=0',order,
                [st('Find the highest derivative of the dependent variable.'),st(f'The derivative y^({order}) has order {order}.'),st('Coefficients and powers of x do not affect the order.')],
                ['Order refers to derivatives, not powers.','Inspect every derivative appearing in the equation.','The highest derivative determines the order.'],[(S.Integer(order),k)])
        if mode==1:
            return P('Is this differential equation linear in y?',rf'y\prime+y^2={k}x','No',
                [st('A linear equation allows y and its derivatives only to the first power.'),st('The term y² is a nonlinear power of the dependent variable.'),st('A coefficient depending on x would be allowed, but a coefficient depending on y is not.')],
                ['Distinguish powers of x from powers of y.','Look for products or nonlinear functions of the dependent variable.','A first-order equation can still be nonlinear.'],[(S.Poly(y*y,y).degree(),2)],'multiple-choice',['Yes','No'])
        f=k*S.exp(2*x)
        return P('Does the proposed function solve the initial-value problem?',rf'y\prime=2y,\quad y(0)={k},\quad y={latex(f)}','Yes',
            [st('Differentiate the candidate.',S.diff(f,x)),st('Substitute into the equation.',rf'y\prime-2y={latex(S.simplify(S.diff(f,x)-2*f))}'),st('Check the initial value separately.',rf'y(0)={k}')],
            ['Verify the equation by differentiation.','A proposed solution must satisfy the equation for every point in its interval.','Then check the initial condition.'],[(S.diff(f,x),2*f),(f.subs(x,0),k)],'multiple-choice',['Yes','No'])
    if section == '2.3':
        if mode==0:
            f=x*x+k*x*y+y*y
            return P('Find the degree of homogeneity of f.',f,2,
                [st('Replace both inputs by λ times the original inputs.',rf'f(\lambda x,\lambda y)=\lambda^2({latex(f)})'),st('The common factor is λ², so the degree is 2.'),st('Every monomial has total degree 2.')],
                ['Scale x and y together.','Count total degree of each monomial.','A common scaling exponent determines the degree.'],[(f.subs({x:a*x,y:a*y},simultaneous=True),a*a*f)])
        if mode==1:
            f=x*(k+S.log(x))
            return P('Solve on x>0 with the stated initial value. Compare your function.',rf'y\prime=\frac yx+1,\quad y(1)={k}',None,
                [st('Set y=vx and apply the product rule.',r'y\prime=v+xv\prime'),st('Substitution cancels v.',r'xv\prime=1\Rightarrow v=\ln x+C'),st('Recover y and apply the initial value.',rf'y=x(\ln x+{k})'),st('Differentiate and check y′=y/x+1.')],
                ['The right side depends on y/x.','The derivative of vx is v+xv′.','Separate the equation for v, then substitute back.'],[(S.diff(f,x),f/x+1),(f.subs(x,1),k)],'self-check')
        f=(x*x+k)/(2*x)
        return P('Solve the homogeneous equation on x>0. Compare the solution.',rf'y\prime=1-\frac yx,\quad y(1)=\frac{{{k+1}}}2',None,
            [st('Set y=vx.',r'v+xv\prime=1-v'),st('Separate for v.',r'\frac{dv}{1-2v}=\frac{dx}{x}'),st('Integration gives 1−2v=C/x²; equivalently y=x/2+C₁/x.'),st('Use the initial value to find C₁.',rf'y=\frac x2+\frac{{{k}}}{{2x}}'),st('The equilibrium v=1/2 is included when C₁=0; it was temporarily excluded by division.')],
            ['Write y′=v+xv′.','Move both v terms to the same side.','Check for constant-v solutions before dividing by 1−2v.'],[(S.diff(f,x),1-f/x),(f.subs(x,1),R(k+1,2))],'self-check')
    if section == '2.4':
        F=[x*x+k*x*y+y*y,x*y+k*x*x,x*x*y+y*y+k*x][mode]
        mx,ny=S.diff(F,x),S.diff(F,y)
        return P('Solve the exact equation implicitly. Compare your potential function.',rf'({latex(mx)})\,dx+({latex(ny)})\,dy=0',None,
            [st('Check mixed partial derivatives.',rf'M_y={latex(S.diff(mx,y))},\quad N_x={latex(S.diff(ny,x))}'),st('Integrate M with respect to x, treating y as constant.',rf'F={latex(S.integrate(mx,x))}+g(y)'),st('Differentiate this expression with respect to y and match N.',rf'g\prime(y)={latex(ny-S.diff(S.integrate(mx,x),y))}'),st('Integrate g′ and combine; the level curve is the solution.',rf'{latex(F)}=C'),st('Verify Fₓ=M and Fᵧ=N.')],
            ['Exactness compares Mᵧ with Nₓ.','The constant of x-integration can be a function of y.','Recover g(y) by matching the other partial derivative.'],[(S.diff(mx,y),S.diff(ny,x)),(S.diff(F,x),mx),(S.diff(F,y),ny)],'self-check')
    if section == '4.1':
        if mode==0:
            return P('Is the equation homogeneous?',rf'y\prime\prime+{k}y\prime+y=0','Yes',
                [st('Write the equation as L[y]=g(x).'),st('The forcing on the right is zero.',r'g(x)=0'),st('All terms involve y or its derivatives linearly, so this is a homogeneous linear equation.')],
                ['Homogeneous here means zero forcing.','Do not confuse this with a first-order function homogeneous in x,y.','Classify linearity and forcing separately.'],[(S.Integer(0),0)],'multiple-choice',['Yes','No'])
        if mode==1:
            return P('How many independent solutions form a fundamental set for this equation?',rf'y^{{(3)}}+{k}y\prime+y=0',3,
                [st('The leading coefficient is 1 and all coefficients are continuous.'),st('The equation is third order.'),st('The homogeneous solution space has dimension 3 on any interval, so a fundamental set has three independent solutions.')],
                ['Read the order.','Confirm the leading coefficient is nonzero.','The dimension theorem applies to homogeneous linear equations.'],[(S.Integer(3),3)])
        yc=C1*S.exp(x)+C2*S.exp(-x);yp=-k*x
        return P('Write the general solution, given the complementary family and a particular solution.',rf'y\prime\prime-y={k}x,\quad y_c={latex(yc)},\quad y_p={latex(yp)}',None,
            [st('The complementary family solves the zero-forcing equation.',yc),st('The particular function solves the forced equation.',rf'y_p\prime\prime-y_p={k}x'),st('Add the two pieces.',yc+yp),st('Arbitrary constants occur only in the complementary family.')],
            ['Use y=yc+yp.','A particular solution has no arbitrary constants.','Verify each piece against its corresponding right side.'],[(S.diff(yc,x,2)-yc,0),(S.diff(yp,x,2)-yp,k*x)],'self-check')
    if section == '4.1.1':
        if mode==0:
            f=k+(k+1)*x
            return P('Solve the initial-value problem. Compare your function.',rf'y\prime\prime=0,\quad y(0)={k},\quad y\prime(0)={k+1}',None,
                [st('Integrate twice.',r'y=C_1x+C_2'),st('The position condition fixes C₂ and the derivative condition fixes C₁.',rf'C_2={k},\quad C_1={k+1}'),st('State the selected straight line.',f),st('Check both conditions and y″=0.')],
                ['A second-order equation needs two conditions for an IVP.','Differentiate the general family before applying y′(0).','Use the same initial point for both conditions.'],[(S.diff(f,x,2),0),(f.subs(x,0),k),(S.diff(f,x).subs(x,0),k+1)],'self-check')
        if mode==1:
            f=k+2*x
            return P('Solve the boundary-value problem. Compare your function.',rf'y\prime\prime=0,\quad y(0)={k},\quad y(2)={k+4}',None,
                [st('The general family is y=C₁x+C₂.'),st('Use the first endpoint.',rf'C_2={k}'),st('Use the second endpoint.',rf'2C_1+{k}={k+4}\Rightarrow C_1=2'),st('The resulting solution is unique for these two endpoint conditions.',f)],
                ['Boundary conditions are specified at different points.','Use each endpoint in the same general family.','Do not replace y(2) by a derivative condition.'],[(S.diff(f,x,2),0),(f.subs(x,0),k),(f.subs(x,2),k+4)],'self-check')
        return P('How many solutions satisfy this boundary-value problem?',rf'y\prime\prime+{k*k}y=0,\quad y(0)=0,\quad y(\pi/{k})=0','Infinitely many',
            [st('Write the general family.',rf'y=C_1\cos({k}x)+C_2\sin({k}x)'),st('The first condition gives C₁=0.'),st('At x=π/k, sin(kx)=sin π=0, so the second condition places no restriction on C₂.'),st(f'Every y=C₂sin({k}x) satisfies both endpoints.')],
            ['Solve the equation before imposing conditions.','Check whether the second condition gives new information.','Boundary-value problems do not inherit automatic IVP uniqueness.'],[(S.sin(k*x).subs(x,S.pi/k),0),(S.diff(S.sin(k*x),x,2)+k*k*S.sin(k*x),0)],'multiple-choice',['One','Infinitely many','None'])
    if section == '4.1.2':
        f,g=[(S.exp(x),S.exp((k+1)*x)),(x,k*x),(S.cos(k*x),S.sin(k*x))][mode]
        wr=S.simplify(f*S.diff(g,x)-g*S.diff(f,x))
        if mode==1:
            return P('Are the two functions linearly independent?',rf'f={latex(f)},\quad g={latex(g)}','No',
                [st('The second function is a constant multiple of the first.',rf'g={k}f'),st('Write a nontrivial zero combination.',rf'{k}f-g=0'),st('This direct relation proves dependence on any interval.')],
                ['Try finding a constant multiple first.','A nontrivial relation has coefficients not all zero.','A relation must hold throughout the interval.'],[(k*f-g,0)],'multiple-choice',['Yes','No'])
        return P('Find the Wronskian at x=0.',rf'f={latex(f)},\quad g={latex(g)}',wr.subs(x,0),
            [st('Differentiate both functions.',rf'f\prime={latex(S.diff(f,x))},\quad g\prime={latex(S.diff(g,x))}'),st('Compute the determinant fg′−gf′.',wr),st('Evaluate at zero.',wr.subs(x,0)),st('A nonzero Wronskian at one point proves linear independence.')],
            ['Use functions in row 1 and derivatives in row 2.','Keep the determinant order fg′−gf′.','Evaluate after simplifying the expression.'],[(wr,f*S.diff(g,x)-g*S.diff(f,x)),(wr.subs(x,0),k)])
    if section == '4.1.3':
        if mode==0:
            f=k*S.exp(x)+(k+1)*S.exp(-x)
            return P('Verify the proposed linear combination solves the homogeneous equation.',rf'y\prime\prime-y=0,\quad y={latex(f)}','Yes',
                [st('Differentiate twice.',S.diff(f,x,2)),st('Subtract the original function.',S.simplify(S.diff(f,x,2)-f)),st('Each basis solution is annihilated by L, so every constant combination is too.')],
                ['Use the linearity of the differential operator.','Coefficients in a linear combination are constants.','Substitute into the full equation.'],[(S.diff(f,x,2)-f,0)],'multiple-choice',['Yes','No'])
        if mode==1:
            f=C1*S.cos(x)+C2*S.sin(x)+k
            return P('Give the general solution using a complementary and particular solution.',rf'y\prime\prime+y={k}',None,
                [st('The homogeneous roots are ±i.',r'y_c=C_1\cos x+C_2\sin x'),st('Try a constant particular solution.',rf'y_p={k}'),st('Add the pieces.',f),st('The forcing is reproduced because the constant has zero second derivative.')],
                ['Separate zero-forcing solutions from one particular solution.','A constant forcing suggests a constant trial.','Include two independent homogeneous terms.'],[(S.diff(f,x,2)+f,k)],'self-check')
        f=k*x*S.exp(x)
        return P('Find one particular solution. Compare your expression.',rf'y\prime-y={k}e^x',None,
            [st('The homogeneous solution contains eˣ, so a pure eˣ trial would vanish.'),st('Try yₚ=Axeˣ and differentiate.',r'y_p\prime=Ae^x+Axe^x'),st('Substitute and match the forcing.',rf'Ae^x={k}e^x\Rightarrow A={k}'),st('State one particular solution.',f)],
            ['A trial matching a homogeneous solution must be adjusted.','Multiply the trial by x.','Use the product rule when differentiating.'],[(S.diff(f,x)-f,k*S.exp(x))],'self-check')
    if section == '4.4':
        if mode==0:
            yp=R(k,3)*S.exp(2*x);force=k*S.exp(2*x)
            return P('Find one particular solution of the nonhomogeneous equation.',rf'y\prime\prime-y={latex(force)}',None,
                [st('The forcing suggests yₚ=Ae²ˣ. The homogeneous roots ±1 do not conflict.'),st('Substitute the trial.',r'4Ae^{2x}-Ae^{2x}=3Ae^{2x}'),st('Match the coefficient.',rf'A={latex(R(k,3))}'),st('State and verify the particular solution.',yp)],
                ['Choose the exponential in the forcing.','Check for resonance before using the trial.','Substitution determines the unknown coefficient.'],[(S.diff(yp,x,2)-yp,force)],'self-check')
        if mode==1:
            yp=k*x*x-2*k;force=k*x*x
            return P('Find one polynomial particular solution.',rf'y\prime\prime+y={latex(force)}',None,
                [st('Use the full quadratic trial.',r'y_p=Ax^2+Bx+C'),st('Substitute and collect powers.',r'y_p\prime\prime+y_p=Ax^2+Bx+(C+2A)'),st('Match quadratic, linear, and constant terms.',rf'A={k},\quad B=0,\quad C=-{2*k}'),st('State the particular function.',yp)],
                ['Include lower powers in a polynomial trial.','Match every coefficient, including absent terms with coefficient zero.','The second derivative contributes to the constant term.'],[(S.diff(yp,x,2)+yp,force)],'self-check')
        yp=R(k,2)*x*S.sin(x)
        return P('Find a resonant particular solution.',rf'y\prime\prime+y={k}\cos x',None,
            [st('cos x already solves the homogeneous equation, so include a factor x.'),st('Use yₚ=Ax sin x and differentiate twice.',r'y_p\prime\prime=2A\cos x-Ax\sin x'),st('Substitution cancels the x sin x terms.',rf'2A={k}\Rightarrow A={latex(R(k,2))}'),st('State the particular solution.',yp)],
            ['Check whether the forcing frequency is a homogeneous frequency.','Multiply the trigonometric trial by x for simple resonance.','Differentiate the product, not just the sine factor.'],[(S.diff(yp,x,2)+yp,k*S.cos(x))],'self-check')
    if section == '4.5':
        if mode==0:
            f=x**3+k*x;out=S.diff(f,x,2)-S.diff(f,x)
            return P('Apply the operator D²−D. Compare your polynomial.',rf'f(x)={latex(f)},\quad D=\frac{{d}}{{dx}}',None,
                [st('D² means two successive derivatives.',S.diff(f,x,2)),st('D means one derivative.',S.diff(f,x)),st('Subtract the first derivative from the second.',S.expand(out))],
                ['D²f is f″, not (f′)².','Differentiate the entire function.','Apply the operator subtraction after computing derivatives.'],[(out,6*x-3*x*x-k)],'self-check')
        if mode==1:
            r=k+2;val=r*r-3*r+2
            return P('Find the scalar multiplying eʳˣ after applying L(D).',rf'L(D)=D^2-3D+2,\quad r={r},\quad L(D)e^{{{r}x}}=?\ e^{{{r}x}}',val,
                [st('Each differentiation of eʳˣ multiplies it by r.'),st('Evaluate the operator polynomial at r.',rf'L({r})={r}^2-3({r})+2'),st('Simplify the scalar.',val)],
                ['Exponentials are eigenfunctions of constant-coefficient operators.','Replace D by r in the operator polynomial.','Keep the exponential factor outside the scalar calculation.'],[(S.diff(S.exp(r*x),x,2)-3*S.diff(S.exp(r*x),x)+2*S.exp(r*x),val*S.exp(r*x))])
        return P('Factor the operator and give its homogeneous solution family.',rf'(D^2-{2*k+1}D+{k*(k+1)})y=0',None,
            [st('Factor the polynomial.',rf'D^2-{2*k+1}D+{k*(k+1)}=(D-{k})(D-{k+1})'),st('Associate each distinct factor with an exponential solution.',rf'y_1=e^{{{k}x}},\quad y_2=e^{{{k+1}x}}'),st('Take the constant linear combination.',rf'y=C_1e^{{{k}x}}+C_2e^{{{k+1}x}}')],
            ['Factor the operator polynomial as an ordinary polynomial.','Each simple real root supplies an exponential.','Use one constant for each independent solution.'],[(S.expand((z-k)*(z-k-1)),z*z-(2*k+1)*z+k*(k+1))],'self-check')
    if section == '4.6':
        if mode==0:
            degree=k;f=x**degree
            return P('Find the smallest order of a pure derivative annihilator for this polynomial.',f,degree+1,
                [st(f'The polynomial has degree {degree}.'),st('Differentiating that many times gives a nonzero constant.',S.diff(f,x,degree)),st('One more derivative gives zero.',S.diff(f,x,degree+1)),st(f'The minimal pure derivative annihilator is D^{degree+1}.')],
                ['Each derivative reduces polynomial degree by one.','A constant needs one more derivative to vanish.','Count the final derivative that produces zero.'],[(S.diff(f,x,degree+1),0),(S.diff(f,x,degree),S.factorial(degree))])
        if mode==1:
            f=S.exp(k*x)
            return P('Find a in the annihilator D−a for the forcing.',f,k,
                [st('Differentiate the exponential.',S.diff(f,x)),st('Subtract a times the original.',rf'(D-a)e^{{{k}x}}=({k}-a)e^{{{k}x}}'),st('Set the scalar to zero.',rf'a={k}')],
                ['Apply D−a to the function.','The derivative of eᵏˣ is k times itself.','Choose a to cancel that multiplier.'],[(S.diff(f,x)-k*f,0)])
        yp=R(k,2)*x*S.exp(x)
        return P('Use an annihilator to find a particular solution.',rf'(D^2-1)y={k}e^x',None,
            [st('The forcing is annihilated by D−1.'),st('Apply it to the entire equation.',r'(D-1)^2(D+1)y=0'),st('The new independent trial beyond the original family is xeˣ.',r'y_p=Axe^x'),st('Substitute into the original equation, not just the annihilated one.',rf'2Ae^x={k}e^x\Rightarrow A={latex(R(k,2))}'),st('State the resulting particular solution.',yp)],
            ['Choose an operator that kills the forcing.','Combine repeated factors to find the resonant trial.','Recover coefficients from the original nonhomogeneous equation.'],[(S.diff(yp,x,2)-yp,k*S.exp(x))],'self-check')
    if section == '6.1':
        if mode==0:
            m=k+2;f=C1*x+C2*x**m
            return P('Solve the Cauchy–Euler equation on x>0.',rf'x^2y\prime\prime-{m}xy\prime+{m}y=0',None,
                [st('Use y=xʳ; all terms share the factor xʳ.',rf'r(r-1)-{m}r+{m}=0'),st('Factor the auxiliary polynomial.',rf'(r-1)(r-{m})=0'),st('Use the two distinct power functions.',f),st('Direct differentiation verifies both powers.')],
                ['Use powers xʳ rather than exponentials eʳˣ.','The second derivative contributes r(r−1).','Work on an interval excluding x=0.'],[(S.simplify(x*x*S.diff(f,x,2)-m*x*S.diff(f,x)+m*f),0)],'self-check')
        if mode==1:
            f=x**k*(C1+C2*S.log(x))
            return P('Solve the repeated-root Cauchy–Euler equation on x>0.',rf'x^2y\prime\prime+({1-2*k})xy\prime+{k*k}y=0',None,
                [st('Form the auxiliary equation.',rf'r(r-1)+({1-2*k})r+{k*k}=(r-{k})^2'),st('A repeated root requires an additional logarithmic solution.',rf'y_1=x^{{{k}}},\quad y_2=x^{{{k}}}\ln x'),st('Combine the independent solutions.',f)],
                ['Collect r² and r terms carefully.','Repeated Cauchy–Euler roots use ln x rather than a factor x.','Keep the interval x>0 when using ln x.'],[(S.simplify(x*x*S.diff(f,x,2)+(1-2*k)*x*S.diff(f,x)+k*k*f),0)],'self-check')
        f=C1*S.cos(k*S.log(x))+C2*S.sin(k*S.log(x))
        return P('Solve the complex-root Cauchy–Euler equation on x>0.',rf'x^2y\prime\prime+xy\prime+{k*k}y=0',None,
            [st('Use y=xʳ to obtain r²+k²=0.',rf'r=\pm {k}i'),st('Complex powers oscillate in ln x, not in x.'),st('Write a real solution family.',f),st('Differentiate with the chain rule to check the original equation.')],
            ['The auxiliary roots are imaginary.','Use cosine and sine of k ln x.','The derivative of ln x supplies 1/x.'],[(S.simplify(x*x*S.diff(f,x,2)+x*S.diff(f,x)+k*k*f),0)],'self-check')
    if section == '6.2':
        if mode==0:
            vals=M([1,k,R(k*k,2),R(k**3,6)])
            return P('Find the first four Maclaurin coefficients c₀,c₁,c₂,c₃. Enter a column vector.',rf'e^{{{k}x}}=\sum_{{n=0}}^\infty c_nx^n',vals,
                [st('Use the exponential series.',rf'e^{{{k}x}}=\sum_{{n=0}}^\infty\frac{{{k}^n}}{{n!}}x^n'),st('Evaluate kⁿ/n! for n=0,1,2,3.',vals),st('These are coefficients, not derivative values: divide by n!.')],
                ['Start with n=0.','Use the factorial in the denominator.','Check coefficients using f⁽ⁿ⁾(0)/n!.'],[(M([S.diff(S.exp(k*x),x,j).subs(x,0)/S.factorial(j) for j in range(4)]),vals)],'matrix')
        if mode==1:
            return P('Find the radius of convergence.',rf'\sum_{{n=0}}^\infty ({k}x)^n',R(1,k),
                [st('This is a geometric series with ratio kx.'),st('Convergence requires |kx|<1.',rf'|x|<\frac1{{{k}}}'),st('Thus R=1/k. At either endpoint the terms do not tend to zero, so neither endpoint belongs.')],
                ['Identify the ratio of successive terms.','Require the absolute ratio to be less than one.','Check endpoints separately from the radius.'],[(S.Integer(k)*R(1,k),1)])
        f=S.exp(k*x)
        return P('Find the power-series solution of this initial-value problem.',rf'y\prime={k}y,\quad y(0)=1',None,
            [st('Assume y=Σcₙxⁿ and differentiate termwise.'),st('Shift the derivative index to compare equal powers.',rf'(n+1)c_{{n+1}}={k}c_n'),st('Start with c₀=1 and iterate.',rf'c_n=\frac{{{k}^n}}{{n!}}'),st('Recognize the convergent exponential series.',rf'y=\sum_{{n=0}}^\infty\frac{{{k}^n x^n}}{{n!}}=e^{{{k}x}}')],
            ['Express both sides using the same power of x.','The initial value specifies c₀.','Solve the recurrence before recognizing a familiar function.'],[(S.diff(f,x),k*f),(f.subs(x,0),1)],'self-check')
    if section == '7.1':
        f=[S.exp(-k*t),t**(k%3+1),S.sin(k*t)][mode]
        F=[1/(s+k),S.factorial(k%3+1)/s**(k%3+2),k/(s*s+k*k)][mode]
        return P('Find the Laplace transform. Compare your expression in s.',rf'f(t)={latex(f)}',None,
            [st('Match the function to a basic transform or integrate the definition.',r'F(s)=\int_0^\infty e^{-st}f(t)\,dt'),st(['Combine exponential exponents and integrate the decaying exponential.','Repeated integration by parts gives n!/sⁿ⁺¹.','Integrating the sine with an exponential gives the frequency over s²+frequency².'][mode]),st('Write the transform with its convergence condition.',rf'F(s)={latex(F)},\quad '+(rf's>-{k}' if mode==0 else 's>0'))],
            ['Distinguish the time variable t from the transform variable s.','Use the table entry for this function.','Include the parameter or factorial in the numerator.'],[(L(f),F)],'self-check')
    if section == '7.2':
        if mode==3:
            F=1/(s+k)**2;f=t*S.exp(-k*t)
            return P('Invert the repeated linear factor.',F,None,
                [st('Recognize the unshifted pair.',r'\mathcal L\{t\}=1/s^2'),st('Replace s with s+k, which multiplies the time function by e⁻ᵏᵗ.',f),st('Check by transforming the result.',F)],
                ['A squared linear denominator corresponds to a time factor t.','Use the exponential shift theorem.','Do not split a repeated factor into two identical simple fractions.'],[(L(f),F)],'self-check')
        F=[1/(s+k),k/(s*s+k*k),1/((s+k)*(s+k+1))][mode]
        f=[S.exp(-k*t),S.sin(k*t),S.exp(-k*t)-S.exp(-(k+1)*t)][mode]
        steps=[st('Identify a table entry.' if mode<2 else 'Decompose into partial fractions.',F if mode<2 else rf'\frac1{{(s+{k})(s+{k+1})}}=\frac1{{s+{k}}}-\frac1{{s+{k+1}}}'),st('Apply the inverse transform term by term.',f),st('Take its Laplace transform to verify the original expression.',F)]
        return P('Find the inverse Laplace transform. Compare your time-domain function.',F,None,steps,
            ['Match the denominator to a basic transform.','Use partial fractions when factors are distinct.','Check signs and numerator factors against the table.'],[(L(f),F)],'self-check')
    if section == '7.3':
        if mode==3:
            F=S.exp(-k*s)*(1/s**2+k/s)
            return P('Transform a step multiplied by an unshifted ramp.',rf'f(t)=u(t-{k})t',None,
                [st('Rewrite t in elapsed-time form.',rf't=(t-{k})+{k}'),st('The delayed function is g(t−k), with g(τ)=τ+k.',rf'G(s)=1/s^2+{k}/s'),st('Apply the delay theorem to the entire expression.',F),st('For t<k the step makes the function zero; after k it reproduces the original ramp.')],
                ['The delay theorem requires an argument t−k.','Rewrite the unshifted ramp as (t−k)+k.','Transform g before multiplying by the delay factor.'],[(S.exp(-k*s)*L(t+k),F)],'self-check')
        if mode==0:
            f=S.exp(-k*t)*S.cos(2*t);F=(s+k)/((s+k)**2+4)
            return P('Transform the exponentially shifted function.',f,None,
                [st('Start with the cosine transform.',r'\mathcal L\{\cos2t\}=s/(s^2+4)'),st('Multiplication by e⁻ᵏᵗ replaces s by s+k.'),st('Shift every occurrence of s.',F),st('The convergence half-plane is s>−k.')],
                ['Use the first translation theorem.','A negative exponent shifts s toward s+k.','Replace s in both numerator and denominator.'],[(L(f),F)],'self-check')
        if mode==1:
            F=S.exp(-k*s)/(s*s+1)
            return P('Find the transform of the delayed sine.',rf'f(t)=u(t-{k})\sin(t-{k})',None,
                [st('The entire sine uses the elapsed time t−k.'),st('Transform the unshifted sine.',r'F_0(s)=1/(s^2+1)'),st('Apply the second translation theorem.',F),st(f'The function is zero before t={k}.')],
                ['Check that the argument is t−k.','Transform the unshifted function first.','Multiply by e⁻ᵏˢ for the delay.'],[(S.exp(-k*s)*L(S.sin(t)),F)],'self-check')
        base=1/(s+k);F=1/(s+k)**2;f=t*S.exp(-k*t)
        return P('Use differentiation of a transform to find L{t e⁻ᵏᵗ}.',f,None,
            [st('Start from the exponential transform.',base),st('Multiplication by t corresponds to minus the s-derivative.',r'\mathcal L\{tf(t)\}=-F\prime(s)'),st('Differentiate and negate.',F)],
            ['Use a transform derivative, not a time derivative.','Keep the minus sign.','Differentiate the full rational expression.'],[(-S.diff(base,s),F),(L(f),F)],'self-check')
    if section == '7.4':
        if mode==3:
            f=(1-S.exp(-k*t))/k;F=1/(s*(s+k))
            return P('Compute the convolution of 1 and e⁻ᵏᵗ.',rf'(f*g)(t)=\int_0^t1\cdot e^{{-{k}(t-\tau)}}d\tau',None,
                [st('Factor out the part independent of τ.',rf'e^{{-{k}t}}\int_0^t e^{{{k}\tau}}d\tau'),st('Integrate and evaluate the two endpoints.',rf'e^{{-{k}t}}\frac{{e^{{{k}t}}-1}}{{{k}}}'),st('Simplify the time-domain result.',f),st('The transform is the product of the two transforms.',F)],
                ['Use g(t−τ), not g(τ), in the convolution definition.','Treat t as fixed during integration over τ.','Check the answer by multiplying Laplace transforms.'],[(L(f),F),(S.integrate(S.exp(-k*(t-z)),(z,0,t)),f)],'self-check')
        if mode==0:
            f=k*S.exp(-t);F=L(f);out=s*F-k
            return P('Find L{f′} using the initial value.',rf'f(t)={latex(f)},\quad f(0)={k}',None,
                [st('Find the transform of f.',F),st('Use the derivative identity including the initial term.',rf'\mathcal L\{{f\prime\}}=sF(s)-{k}'),st('Simplify.',S.simplify(out)),st('Check by differentiating f directly.')],
                ['The initial value enters as a subtraction.','A time derivative and an s-derivative have different transform rules.','Simplify the resulting rational expression.'],[(L(S.diff(f,t)),out)],'self-check')
        if mode==1:
            F=1/(s*(s+k));f=(1-S.exp(-k*t))/k
            return P('Find the transform of the accumulated integral.',rf'g(t)=\int_0^t e^{{-{k}\tau}}\,d\tau',None,
                [st('Transform the integrand.',1/(s+k)),st('An integral from zero divides the transform by s.',F),st('Check by integrating explicitly.',f),st('Transform that result to confirm.',F)],
                ['Use the integral-from-zero transform rule.','Divide by s, rather than multiplying by s.','The lower limit controls the integration constant.'],[(L(f),F)],'self-check')
        F=(1-S.exp(-k*s))/(s*(1-S.exp(-2*k*s)))
        return P('Transform a periodic square pulse of period 2k.',rf'f(t)=1\ (0\le t<{k}),\quad f(t)=0\ ({k}\le t<{2*k}),\quad f(t+{2*k})=f(t)',None,
            [st('Use the periodic-function formula.',rf'F(s)=\frac{{\int_0^{{{2*k}}}e^{{-st}}f(t)dt}}{{1-e^{{-{2*k}s}}}}'),st('Only the first half of the period contributes.',rf'\int_0^{{{k}}}e^{{-st}}dt=\frac{{1-e^{{-{k}s}}}}{{s}}'),st('Divide by the geometric repetition factor.',F),st('The integral definition converges for s>0.')],
            ['Integrate over one complete period only.','The zero part contributes nothing.','Account for repeated periods with 1−e⁻ᵀˢ.'],[(S.simplify(F),1/(s*(1+S.exp(-k*s))))],'self-check')
    if section == '7.5':
        if mode==0:
            f=k*S.exp(-2*t);F=k/(s+2)
            return P('Solve this IVP using Laplace transforms.',rf'y\prime+2y=0,\quad y(0)={k}',None,
                [st('Transform the derivative with its initial term.',rf'sY-{k}+2Y=0'),st('Solve the algebraic equation for Y.',F),st('Apply the inverse transform.',f),st('Verify the differential equation and initial value.')],
                ['Keep y(0) in the derivative transform.','Collect all Y terms before dividing.','Recognize the shifted exponential inverse.'],[(S.diff(f,t)+2*f,0),(f.subs(t,0),k),(L(f),F)],'self-check')
        if mode==1:
            f=k*S.sin(t);F=k/(s*s+1)
            return P('Solve the second-order IVP using Laplace transforms.',rf'y\prime\prime+y=0,\quad y(0)=0,\quad y\prime(0)={k}',None,
                [st('Transform the second derivative including both initial values.',rf's^2Y-{k}+Y=0'),st('Isolate the transform.',F),st('Recognize the sine transform.',f),st('Differentiate to verify both initial conditions.')],
                ['L{y″}=s²Y−sy(0)−y′(0).','Use both initial values.','Do not confuse 1/(s²+1) with the cosine transform.'],[(S.diff(f,t,2)+f,0),(f.subs(t,0),0),(S.diff(f,t).subs(t,0),k),(L(f),F)],'self-check')
        F=S.exp(-k*s)/(s*(s+1));f=1-S.exp(-t)
        return P('Solve the delayed-forcing IVP; give the piecewise solution.',rf'y\prime+y=u(t-{k}),\quad y(0)=0',None,
            [st('Transform the step forcing and derivative.',rf'(s+1)Y=e^{{-{k}s}}/s'),st('Solve for Y.',F),st('Invert the unshifted factor.',r'\mathcal L^{-1}\{1/[s(s+1)]\}=1-e^{-t}'),st('Delay the entire response.',rf'y(t)=\begin{{cases}}0,&t<{k}\\1-e^{{-(t-{k})}},&t\ge{k}\end{{cases}}'),st('The response is continuous at activation; its derivative changes with the forcing.')],
            ['Transform the forcing as e⁻ᵏˢ/s.','Solve for Y before applying the delay rule.','Replace t by t−k throughout the delayed response.'],[(L(f),1/(s*(s+1))),(S.diff(f,t)+f,1),(f.subs(t,0),0)],'self-check')
    if section == '8.3':
        if mode==0:
            return P('Rewrite the second-order ODE as a first-order system.',rf'y\prime\prime+{k}y\prime+2y=0',None,
                [st('Introduce position and velocity.',r'x_1=y,\quad x_2=y\prime'),st('Differentiate the definitions.',r'x_1\prime=x_2'),st('Use the original equation for the velocity derivative.',rf'x_2\prime=-2x_1-{k}x_2'),st('Two first-order equations carry the same information as one second-order equation.')],
                ['Use one state for each derivative below the highest order.','The highest derivative comes from the original equation.','Keep the signs after isolating y″.'],[(S.expand(-2*x-k*y),-2*x-k*y)],'self-check')
        if mode==1:
            A=M([[1,k],[-1,2]]);out=A*M([1,2])
            return P('Compute the derivative vector at the specified state.',rf'x\prime=x+{k}y,\quad y\prime=-x+2y,\quad (x,y)=(1,2)',out,
                [st('Evaluate each rate at the same state.',rf'x\prime=1+{k}(2),\quad y\prime=-1+2(2)'),st('Simplify and collect the rates as a vector.',out),st('The vector describes the direction of motion, not the next state itself.')],
                ['Both rates depend on the current state.','Do not replace a state variable by its derivative.','Report one rate per dependent variable.'],[(out,M([1+2*k,3]))],'matrix')
        f=S.exp(t);g=(k-1)*S.exp(-t)+S.exp(t)
        return P('Solve the triangular coupled IVP.',rf'x\prime=x,\quad y\prime=2x-y,\quad x(0)=1,\quad y(0)={k}',None,
            [st('Solve the independent first equation.',r'x=e^t'),st('Insert x into the second equation.',r'y\prime+y=2e^t'),st('Use integrating factor eᵗ.',r'(e^ty)\prime=2e^{2t}'),st('Integrate and apply y(0).',rf'y=e^t+({k-1})e^{{-t}}'),st('Substitute both functions into both equations.')],
            ['Solve the equation that does not depend on the other variable first.','Use its solution as forcing in the second equation.','Apply both initial conditions independently.'],[(S.diff(f,t),f),(S.diff(g,t),2*f-g),(g.subs(t,0),k)],'self-check')
    if section == '8.5':
        A=M([[1,k],[-2,3]]);v=M([k,1]);out=A*v
        if mode==0:
            return P('Find the coefficient matrix for the system in the order X=(x,y)ᵀ.',rf'x\prime=x+{k}y,\quad y\prime=-2x+3y',A,
                [st('Read coefficients from the x′ equation for row 1.',rf'(1,{k})'),st('Read coefficients from the y′ equation for row 2.',r'(-2,3)'),st('Assemble X′=AX.',A)],
                ['Rows correspond to equations.','Columns correspond to state variables in the stated order.','Keep the minus sign on the x coefficient in the second equation.'],[(A*M([x,y]),M([x+k*y,-2*x+3*y]))],'matrix')
        if mode==1:
            return P('Find X′ at the given state.',rf'X\prime=AX,\quad A={latex(A)},\quad X={latex(v)}',out,
                [st('Use one row-column product for each rate.'),st('Calculate both entries.',out),st('The coefficient matrix acts on the state, not on the time variable.')],
                ['Multiply A by the column state.','Preserve the order of the state variables.','Evaluate both coupled derivatives at the same state.'],[(out,M([2*k,-2*k+3]))],'matrix')
        F=M([S.sin(t),k*t])
        return P('Identify the forcing vector F(t) in X′=AX+F(t).',rf'x\prime=x+{k}y+\sin t,\quad y\prime=-2x+3y+{k}t',F,
            [st('Terms involving x or y belong to AX.'),st('Terms depending only on t belong to the forcing vector.',F),st('This makes the system nonhomogeneous; no forcing term is a matrix coefficient.')],
            ['Separate state-dependent terms from time-only terms.','Keep forcing entries in equation order.','The zero-forcing test determines homogeneity.'],[(A*M([x,y])+F,M([x+k*y+S.sin(t),-2*x+3*y+k*t]))],'self-check')
    if section == '8.6':
        if mode==0:
            A=M([[1,0],[0,-k]]);f=M([C1*S.exp(t),C2*S.exp(-k*t)])
            return P('Solve the diagonal homogeneous system.',rf'X\prime={latex(A)}X',None,
                [st('The eigenvalues are the diagonal entries 1 and −k.'),st('Use their standard-basis eigenvectors.',r'v_1=(1,0)^T,\quad v_2=(0,1)^T'),st('Combine exponential eigenvector solutions.',f),st('Differentiate the vector and check X′=AX.')],
                ['Each eigenvector gives a constant direction.','Its eigenvalue controls the exponential rate.','Include one constant for each independent solution.'],[(f.diff(t),A*f)],'self-check')
        if mode==1:
            A=M([[1,k],[0,1]]);f=M([S.exp(t)*(C1+k*C2*t),C2*S.exp(t)])
            return P('Solve the repeated-eigenvalue system.',rf'X\prime={latex(A)}X',None,
                [st('The eigenvalue 1 is repeated, but the eigenspace is only one-dimensional.'),st('Solve y′=y first.',r'y=C_2e^t'),st('The first equation is x′−x=kC₂eᵗ, requiring a resonant factor t.',rf'x=e^t(C_1+{k}C_2t)'),st('Combine the two components and verify.',f)],
                ['A repeated eigenvalue does not guarantee two eigenvectors.','Use the triangular equation for the second component.','The forced first component needs a t eᵗ term.'],[(f.diff(t),A*f)],'self-check')
        A=M([[0,-k],[k,0]]);f=M([C1*S.cos(k*t)-C2*S.sin(k*t),C1*S.sin(k*t)+C2*S.cos(k*t)])
        return P('Give a real solution family for the rotational system.',rf'X\prime={latex(A)}X',None,
            [st('The characteristic equation is λ²+k²=0.',rf'\lambda=\pm{k}i'),st('Use real cosine and sine combinations.',f),st('Differentiate both components to check x′=−ky and y′=kx.'),st('The squared length stays constant: the motion is rotation.')],
            ['Complex eigenvalues occur in conjugate pairs.','Build real solutions from their real and imaginary parts.','Check signs by differentiating the two components.'],[(f.diff(t),A*f),(S.simplify(f.dot(f)),C1*C1+C2*C2)],'self-check')
    raise ValueError(('Unhandled Differential Equations section',section))

# Definitions apply to real vector spaces unless a lesson explicitly says otherwise.
# Several synonymous labels share a definition; no undefined term gets a fallback.
glossary = {}
definition_groups = '''
linear equation::An equation in which each unknown appears only to the first power and is not multiplied by another unknown. Coefficients and the constant are fixed numbers.
system of equations::A collection of equations that must hold simultaneously for the same values of all unknowns.
consistent system::A system with at least one solution; it may have exactly one or infinitely many.
inconsistent system::A system with no solution because its equations impose contradictory requirements.
equivalent system::A system with exactly the same solution set as the original, even if its equations look different.
solution set::The complete collection of inputs satisfying every equation, often expressed using free parameters.
elementary equation operation;elementary row operation;row operation::Swapping equations, multiplying an equation by a nonzero scalar, or adding a multiple of one equation to another; each is reversible.
augmented matrix::The coefficient matrix together with an extra column of right-hand-side constants. The extra column is not another variable.
row-echelon form::A matrix whose nonzero rows lie above zero rows, with each successive leading nonzero entry to the right of the one above and zeros below each leading entry.
reduced row-echelon form::Row-echelon form with leading entries equal to 1 and each leading 1 the only nonzero entry in its column.
pivot::A leading nonzero position in echelon form. Pivot columns identify dependent variables in a system and independent original columns for a column-space basis.
free variable::An unknown whose coefficient column has no pivot; it can be assigned a parameter when the system is consistent.
back-substitution::Solving an echelon system from its last nonzero equation upward, inserting already determined variables into earlier equations.
matrix dimension::The number of rows followed by the number of columns, written m×n. Order matters.
matrix entry::The number at one row-column position; aᵢⱼ is the entry in row i and column j.
addition;vector addition::Combining equal-size matrices or vectors by adding corresponding entries.
subtraction::Subtracting corresponding entries, or adding the additive inverse of the second object.
scalar multiplication::Multiplying every entry of a vector or matrix by the same scalar.
matrix multiplication::For A of size m×n and B of size n×p, AB has size m×p; entry (i,j) is row i of A dotted with column j of B.
transpose::The matrix Aᵀ obtained by exchanging rows and columns: its (j,i) entry is aᵢⱼ.
associative property::Compatible products can be regrouped: (AB)C=A(BC). This does not allow reversing their order.
distributive property::A(B+C)=AB+AC and (A+B)C=AC+BC when all terms have compatible dimensions.
identity matrix::A square matrix with diagonal entries 1 and all other entries 0; multiplying by a compatible identity leaves a matrix unchanged.
zero matrix::A matrix in which every entry is zero; its dimensions still matter.
noncommutative multiplication::The fact that AB generally differs from BA; sometimes only one of the two products is defined.
inverse matrix;invertible matrix;nonsingular matrix::For a square A, its inverse A⁻¹ satisfies AA⁻¹=A⁻¹A=I. A having such an inverse is called invertible or nonsingular.
invertibility::The property of a square matrix having a two-sided inverse; equivalently its determinant is nonzero and its columns are independent.
singular matrix;zero determinant;singularity test::A square matrix is singular when it has no inverse, equivalently det A=0. A zero determinant tests singularity but alone does not decide consistency for a nonzero right side.
Gauss–Jordan inversion::Reducing [A|I] by row operations; if the left block becomes I, the right block is A⁻¹.
elementary matrix::The identity matrix after exactly one elementary row operation. Left multiplication by it performs that row operation.
product of elementary matrices::A sequence of row operations written as a matrix product, with the rightmost factor acting first.
matrix equation;coefficient matrix::In AX=b, A holds coefficients, X holds unknowns, and b holds prescribed outputs. A coefficient matrix excludes any appended constant column.
matrix model;application of matrix algebra::A representation of quantities, interactions, or transformations using matrices; rows, columns, units, and multiplication order must be specified.
determinant::A scalar assigned to a square matrix; geometrically it measures signed volume scaling and detects invertibility.
minor::The determinant of the smaller square matrix left after deleting one specified row and column.
cofactor::The signed minor Cᵢⱼ=(−1)ⁱ⁺ʲMᵢⱼ; its sign depends on its position.
cofactor expansion::Computing a determinant by summing entries of any one row or column times their corresponding cofactors.
row swap::Exchanging two rows; it changes the determinant's sign.
row scaling::Multiplying one row by a nonzero factor; it multiplies the determinant by that factor.
row replacement::Adding a multiple of one row to another row; it leaves the determinant unchanged.
triangular matrix::A square matrix with zeros all below or all above the diagonal; its determinant is the product of diagonal entries.
determinant identity::A rule such as det(Aᵀ)=det A or det(AB)=det A det B, valid for compatible square matrices.
product rule::For determinants, det(AB)=det A det B. For differentiable functions, (uv)′=u′v+uv′. The surrounding lesson determines which rule is meant.
Cramer’s Rule::For an invertible coefficient matrix A, unknown xᵢ equals det Aᵢ / det A, where column i of Aᵢ is replaced by the right-hand-side vector.
adjugate;determinant-based inverse::The adjugate is the transpose of the cofactor matrix. When det A≠0, A⁻¹=adj(A)/det A.
vector;component::A vector in Rⁿ is an ordered list of n numbers; each position is one component or coordinate. In abstract spaces, vectors can instead be polynomials, matrices, or functions.
linear combination::A sum of vectors or functions multiplied by scalar coefficients. In an independence test for functions, these coefficients must be constants.
vector space axiom::A rule governing addition and scalar multiplication, including closure, associativity, distributivity, additive identity/inverses, and multiplication by 1.
zero vector::The additive identity of a vector space. It may be a zero column, zero matrix, zero polynomial, or identically zero function.
additive inverse::The vector −v satisfying v+(−v)=0; this differs from a multiplicative matrix inverse.
abstract vector space::A set with defined addition and scalar multiplication satisfying the vector-space axioms, even when its elements are not numerical columns.
subspace test;closure::A subset of an existing vector space is a subspace if it contains zero and every linear combination of two of its elements stays inside it. Staying inside after an operation is called closure.
polynomial subspace;matrix subspace::A collection of polynomials or matrices closed under linear combinations and containing its appropriate zero object.
span::All finite linear combinations of a collection of vectors; it is the set of outputs those vectors can generate.
linear dependence::Existence of a constant linear combination equaling zero with coefficients not all zero; at least one supplied vector or function is redundant.
linear independence::The property that the only constant linear combination equaling zero has every coefficient zero.
basis;basis selection::An independent spanning list for a vector space. To select a basis from matrix columns, retain the original columns corresponding to pivot columns.
dimension::The number of vectors in any basis of a finite-dimensional space; all bases of the same space have the same size.
standard basis::In Rⁿ, the ordered vectors e₁,…,eₙ with one entry 1 and the others 0. In Pₙ, a standard basis is 1,x,…,xⁿ.
coordinate;coordinate vector::The scalar coefficients of a vector relative to a specified ordered basis, arranged as a column.
ordered basis::A basis with a specified sequence; exchanging basis vectors exchanges the positions of the associated coordinates.
row space::The span of a matrix's rows, considered as vectors in Rⁿ for an m×n matrix.
column space::The span of a matrix's columns, a subspace of Rᵐ for an m×n matrix.
null space;kernel::The input vectors mapped to zero: for a matrix A, the solutions of Av=0.
rank::The dimension of the column space (equivalently row space), equal to the number of pivots.
nullity::The dimension of the kernel or null space, equal to the number of free variables.
rank–nullity theorem::For a linear map from a finite-dimensional domain V, rank plus nullity equals dim V; for an m×n matrix the sum is n.
transition matrix;change of basis::A conversion between coordinate systems. If B and C have basis vectors as columns, P(C←B)=C⁻¹B converts B-coordinates into C-coordinates.
basis application;dimension application;vector representation;coordinate model::Using basis coefficients to encode objects such as polynomials, signals, or matrices. Dimension counts independent information rather than the number of written entries.
dot product::For real vectors, u·v is the sum of products of corresponding components; it returns a scalar.
norm::The nonnegative length of a vector: √(u·u) for the usual dot product, or √⟨u,u⟩ for a general inner product.
distance::The norm of the difference between two points or vectors, measured in the same space.
angle::For nonzero real vectors, the angle θ in [0,π] determined by cos θ=(u·v)/(‖u‖‖v‖).
orthogonality;orthogonal vector::Two vectors are orthogonal when their inner product is zero. For the usual dot product, this means perpendicular directions.
Cauchy–Schwarz inequality::The bound |⟨u,v⟩|≤‖u‖‖v‖, which guarantees the angle formula stays between −1 and 1.
inner product::A real-valued function ⟨u,v⟩ that is linear in either argument, symmetric, and positive definite; it extends the dot product to other spaces.
orthogonal projection::The component of v along a nonzero u: (⟨v,u⟩/⟨u,u⟩)u. The remaining vector is orthogonal to u.
orthogonal set::A collection whose distinct vectors have zero inner product; an orthogonal set of nonzero vectors is independent.
orthonormal basis::A basis whose vectors are pairwise orthogonal and each have norm 1.
Gram–Schmidt process::Sequentially subtracting projections onto earlier orthogonal directions, then normalizing, to produce an orthonormal basis with the same span.
normalization::Dividing a nonzero vector by its norm to give a unit vector; it is undefined for the zero vector.
linear transformation;linearity test::A map preserving sums and scalar multiples: T(au+bv)=aT(u)+bT(v). Both properties, with correct domain and codomain, are needed.
domain::The vector space of allowable inputs of a transformation or the interval of inputs of a function.
codomain::The declared output space of a transformation; the actual range may be a smaller subset.
matrix transformation;standard matrix::A map T(v)=Av for a fixed A. Its standard matrix has the vectors T(eⱼ) as columns.
range::All output vectors actually attained by a transformation, equivalently the column space of its representing matrix.
one-to-one transformation::A map with no two distinct inputs sharing an output; for a linear map this is equivalent to kernel {0}.
onto transformation::A map whose range equals its entire declared codomain.
matrix representation::The matrix of a linear map relative to specified input/output bases, with column j equal to the output coordinates of the jth input basis vector.
composition of transformations::Applying one map and then another. For S after T, the representing product is [S][T].
similar matrix;similarity transformation::Square matrices A and B representing the same linear map in different bases satisfy B=P⁻¹AP for an invertible P.
eigenvalue;eigenvector::An eigenvector is a nonzero vector v satisfying Av=λv; the scalar λ is its eigenvalue. λ may be zero, but v may not.
characteristic equation::For a matrix, det(A−λI)=0 determines eigenvalues. For a constant-coefficient ODE, the characteristic equation comes from replacing differentiation by a scalar r.
eigenspace::The entire kernel of A−λI, including zero; its nonzero elements are the eigenvectors for λ.
algebraic multiplicity::The number of times an eigenvalue occurs as a root of the characteristic polynomial.
geometric multiplicity::The dimension of an eigenspace; it is at least one and no greater than the algebraic multiplicity for that eigenvalue.
ordinary differential equation::An equation involving derivatives of an unknown function of one independent variable.
partial differential equation::An equation involving partial derivatives of an unknown function of multiple independent variables.
order::The highest derivative order appearing in a differential equation, unrelated to powers of the dependent variable.
linearity;higher-order linear equation::An equation is linear in its dependent variable when it and its derivatives appear to the first power, are not multiplied together, and have coefficients depending only on the independent variable.
nonlinear equation::An equation violating linearity, for example by containing y², yy′, or sin y. A nonlinear equation can still be solvable by other methods.
general solution::A family containing the arbitrary constants needed to describe all solutions on a specified interval; singular solutions may need separate attention.
particular solution::One selected solution with no free constants. In a nonhomogeneous linear equation, yₚ denotes one solution reproducing the forcing, not necessarily one satisfying chosen initial values.
separation of variables;separation after substitution::Rearranging a first-order equation so an expression in the dependent variable times its differential equals an expression in the independent variable times its differential.
integration::Recovering a family of antiderivatives; indefinite integration introduces an arbitrary constant.
integration constant::A constant introduced by antiderivatives, determined by initial/boundary data when possible.
initial condition;initial-value problem::A prescribed function value or derivative at one initial point. An IVP combines a differential equation with enough such conditions.
homogeneous function;degree of homogeneity::A function with f(λx,λy)=λⁿf(x,y) is homogeneous of degree n. A first-order equation y′=F(y/x) uses degree-zero homogeneity, distinct from zero-forcing linear homogeneity.
substitution y=vx::Introducing v=y/x so that y=vx and y′=v+xv′; this converts suitable homogeneous first-order equations to separable equations.
exactness test::For M dx+N dy=0 with continuously differentiable coefficients on a suitable region, compare Mᵧ and Nₓ; equality on a rectangle guarantees a potential F.
partial derivative::Differentiation with respect to one variable while keeping the other variables fixed.
potential function::A function F(x,y) whose partial derivatives give M and N in an exact equation; solution curves satisfy F(x,y)=C.
implicit solution::A relation F(x,y)=C describing solutions without isolating y; locally it defines y(x) where Fᵧ≠0.
standard linear form::The first-order form y′+P(x)y=Q(x), with derivative coefficient 1.
integrating factor::A nonzero function μ=e^(∫P dx) making μy′+μPy=(μy)′ for a first-order linear equation.
homogeneous equation::In higher-order linear theory, an equation L[y]=0 with zero forcing; its solutions form a vector space.
nonhomogeneous equation::A linear equation L[y]=g with a forcing function g that is not identically zero; its solution set is an affine translate of the homogeneous solution space.
solution space::For a homogeneous linear equation with regular coefficients, the vector space formed by its solution functions on an interval.
boundary condition::A condition at an endpoint, with boundary-value problems typically specifying conditions at different points.
existence;uniqueness::Existence means at least one solution satisfies the data; uniqueness means exactly one. Linear IVPs have both on intervals where normalized coefficients and forcing are continuous.
Wronskian::The determinant formed from functions and their successive derivatives. A nonzero value at one point proves independence; zero everywhere alone is inconclusive for arbitrary functions.
fundamental solution set::A linearly independent collection of n solutions of a regular homogeneous nth-order linear ODE, spanning its solution space.
superposition principle;superposition::Linearity permits constant combinations of homogeneous solutions; for different forcing terms, the sum of particular solutions reproduces the summed forcing.
complementary solution::The general solution y꜀ of the associated homogeneous equation; the forced general solution is y꜀+yₚ.
characteristic root;distinct real root;distinct root::A root of the characteristic polynomial; a simple real root r gives eʳˣ for constant-coefficient ODEs, or xʳ for Cauchy–Euler equations.
repeated root::A root occurring more than once; multiplicity m requires m independent solution forms, such as eʳˣ,xeʳˣ,…,xᵐ⁻¹eʳˣ.
complex conjugate root;complex root::Nonreal roots of a real-coefficient polynomial occur in conjugate pairs α±iβ; constant-coefficient real solutions use eᵅˣcos βx and eᵅˣsin βx.
trial function::An expression with unknown coefficients chosen to match the forcing type, then substituted into the original equation.
resonance::Overlap between a proposed particular trial and the complementary solution; multiply the entire trial by enough powers of x to remove the overlap.
differential operator;operator notation::D denotes differentiation. A polynomial L(D) represents a fixed linear combination of derivatives, such as D²−3D+2.
operator polynomial;factorization::A polynomial in D that can be factored algebraically when coefficients are constant; variable coefficients require caution because multiplication and differentiation may not commute.
annihilator::A differential operator that sends a specified forcing function to zero, such as D−a for eᵃˣ or Dⁿ⁺¹ for a degree-n polynomial.
operator product::Composition of differential operators; for constant-coefficient polynomials in D, these commute and combine like ordinary polynomials.
Cauchy–Euler equation::An equation whose jth derivative is multiplied by a coefficient proportional to xʲ, so a power trial reduces it to an algebraic equation.
trial solution y=x^m;auxiliary equation::Substituting y=xᵐ into a Cauchy–Euler equation yields a polynomial in m, called the auxiliary equation.
power series::An infinite expansion Σcₙ(x−a)ⁿ about a center a, where each cₙ is a coefficient.
convergence::A series converges at an input if its partial sums approach a finite limit.
radius of convergence::The distance R from the center inside which a power series converges absolutely. Endpoints at distance R need separate tests.
term-by-term differentiation::Differentiating each term of a power series within its open interval of convergence; the radius stays the same but endpoint behavior can change.
power-series solution::A solution represented by a convergent series whose coefficients satisfy recurrences obtained from substituting into an ODE.
Laplace transform definition;improper integral::The integral F(s)=∫₀^∞e⁻ˢᵗf(t)dt, defined as a limit at infinity where it converges; it maps time functions to functions of s.
basic transform;transform table::Standard Laplace pairs such as 1↔1/s, eᵃᵗ↔1/(s−a), and sin bt↔b/(s²+b²), together with their convergence conditions.
inverse Laplace transform;inverse transform::Recovering a time-domain function f(t) from a known transform F(s), usually by matching tables and simplifying algebra.
algebraic manipulation::Rewriting a transform without changing its value, for example factoring denominators or completing the square to match a table entry.
partial fraction::Decomposing a proper rational function into simpler fractions with denominators corresponding to the original factors; repeated factors require all lower powers.
first shifting theorem;exponential shift::Multiplication by eᵃᵗ in time replaces s by s−a in the transform: L{eᵃᵗf(t)}=F(s−a).
second shifting theorem::A delayed function u(t−a)f(t−a) has transform e⁻ᵃˢF(s) for a≥0; both the step and the function's argument must be shifted.
unit step function::u(t−a) is zero before t=a and one after; its value at the single transition point does not affect the Laplace transform.
derivative of transform::Differentiation with respect to s corresponds to multiplication by −t: L{tf(t)}=−F′(s), with higher powers producing higher derivatives.
transform of derivative::Time derivatives transform to powers of s times F minus initial-value terms: L{f′}=sF−f(0).
transform of integral::An accumulated integral ∫₀ᵗf(τ)dτ transforms to F(s)/s where the transforms exist.
convolution::The integral (f*g)(t)=∫₀ᵗf(τ)g(t−τ)dτ; its Laplace transform is the product F(s)G(s).
periodic function::A function with f(t+T)=f(t) for a positive period T; its transform uses one-period integration divided by 1−e⁻ᵀˢ.
transform-domain equation::The algebraic equation for Y(s) obtained by transforming an ODE, including all initial-value terms.
piecewise forcing function::A time-dependent input specified by different formulas on different intervals, often written with unit step functions.
coupled differential equation;first-order system::Several equations giving first derivatives of multiple dependent variables; one component's rate may depend on other components.
solution vector;vector-valued function::A column of functions, one for each state variable, whose derivative is taken componentwise.
matrix notation;matrix system::The form X′=A(t)X+F(t), with coefficient rows matching equations and columns matching the declared state order.
real eigenvalue::A real λ supplying a real exponential mode eˡᵗv for a constant-coefficient homogeneous matrix system.
complex eigenvalue::A nonreal eigenvalue α+iβ, paired with its conjugate for real matrices, giving real oscillatory modes scaled by eᵅᵗ.
repeated eigenvalue::An eigenvalue with algebraic multiplicity greater than one; missing eigenvectors require generalized eigenvectors and polynomial factors in time.
Euler’s method;slope approximation;iterative calculation::A numerical recurrence yₙ₊₁=yₙ+h f(xₙ,yₙ), following the slope at the current approximate point to estimate the next one.
step size::The increment h between successive independent-variable grid points; smaller steps usually improve accuracy but require more calculations.
numerical error::The difference between an approximation and the exact solution; truncation, accumulated errors, rounding, and stability all matter.
'''
for line in definition_groups.strip().splitlines():
    names, definition = line.split('::',1)
    for name in names.split(';'): glossary[name] = definition

notes = {}
def teach(key, explanation, reasoning, mistakes):
    notes[key] = (explanation, reasoning, mistakes.split('|'))

teach('L1.1',
 'Think of an equation as a requirement, and a solution as an input that meets it. A system asks the same input to meet every requirement at once. For two variables, each nontrivial linear equation describes a line: crossing lines give one solution, coinciding lines infinitely many, and parallel distinct lines none.\nDo not decide the outcome from the number of equations alone. Simplify the equations together. A statement such as 0=1 proves inconsistency; 0=0 only says one equation repeats information. If a variable can be freely chosen after all restrictions are applied, describe the whole family using a parameter rather than guessing one pair.',
 'Reversible equation operations preserve the solution set because any input satisfying the original equations also satisfies their combinations, and the inverse operations recover the original requirements. Verification means substituting the same proposed values into every original equation.',
 'Checking only one equation|Calling a redundant equation a contradiction|Assuming two equations always give one solution')
teach('L1.2',
 'An augmented matrix records coefficients and constants while suppressing repeated variable names. Each column must keep the same variable order. Gaussian elimination builds a staircase of pivots and clears entries below them; back-substitution then solves from the bottom upward. Gauss–Jordan elimination also clears above each pivot and scales it to 1.\nAlways inspect the augmented column before reading answers. A zero coefficient row with a nonzero constant makes the system inconsistent. Otherwise, assign a parameter to every nonpivot variable column. Pivot variables depend on those parameters; an augmented-column pivot is not a new unknown.',
 'Each row operation is an invertible operation on equations. Echelon form reveals which restrictions are independent; RREF isolates each pivot variable so that its dependence on free variables is visible.',
 'Changing coefficients without changing the augmented constant|Dividing a row by zero|Counting an augmented-column pivot as a variable pivot')
teach('L2.1',
 'A matrix is a rectangular arrangement with a stated row count and column count. Addition, subtraction, and scalar multiplication act on corresponding entries. Multiplication is different: the columns of the first matrix must match the rows of the second, and each output entry is a row-column dot product.\nFor AB, entry (i,j) combines all ways input j can contribute to output i through the intermediate coordinates. This explains both the summation rule and the dimension rule. A transpose exchanges the roles of rows and columns; it does not negate entries. Write dimensions before calculating to catch undefined operations early.',
 'Matrix multiplication is defined to represent composition of linear maps. Applying B first creates intermediate coordinates; applying A combines them into final outputs. Summing those intermediate contributions gives the row-column formula.',
 'Multiplying matrices entry by entry|Reversing row and column counts|Adding matrices with different dimensions')
teach('L2.2',
 'Matrix algebra shares many familiar rules with scalar algebra, but multiplication order carries information. You may regroup a compatible triple product and distribute over sums. You may not freely exchange two factors. A product AB can be defined even when BA is not, and when both exist they can differ.\nThe identity is sized to the operation: an m×n matrix satisfies IₘA=A and AIₙ=A. Nonzero matrices can multiply to zero, so scalar cancellation arguments may fail. To cancel A from AX=AY, first know that A is invertible and multiply both equations on the same side by its inverse.',
 'Associativity and distributivity follow from expanding the finite sums defining entries. Noncommutativity reflects that doing one transformation before another can change the outcome. Inverses provide justified cancellation when ordinary scalar intuition cannot.',
 'Replacing AB by BA|Cancelling a singular matrix|Assuming AB=0 forces one factor to be zero')
teach('L2.3',
 'An inverse undoes a transformation for every possible input, not just one vector. Only square matrices can have a two-sided inverse. For a 2×2 matrix, compute ad−bc first: if it is zero, stop; if it is nonzero, the adjugate formula gives the inverse.\nFor larger matrices, augment A with I and apply Gauss–Jordan operations to both blocks. If the left block becomes I, the right block is the inverse. If a pivot is missing, A is singular. To solve AX=b with an invertible A, left-multiply by A⁻¹. Always verify a proposed inverse by checking a product equals I.',
 'The elementary matrices for row reduction form a matrix E with EA=I. When A is square and full rank, E must be A⁻¹. Thus the operations used on the identity block explicitly record the transformation that undoes A.',
 'Using the inverse formula when determinant is zero|Multiplying b by the inverse on the wrong side|Confusing additive inverse −A with multiplicative inverse A⁻¹')
teach('L2.4',
 'Every elementary row operation can be packaged as a matrix. Begin with an identity matrix and perform exactly the operation you want; the result is E. Left-multiplying a compatible A by E performs that row operation on A. Right multiplication instead acts on columns.\nA row swap undoes itself. A nonzero row scaling is undone by reciprocal scaling. Adding c times one row to another is undone by adding −c times that row. A sequence E₁, then E₂, gives E₂E₁A: the rightmost matrix acts first. These matrices explain why row operations preserve rank and invertibility.',
 'The rows of EA are the linear combinations of A’s rows specified by E. Since E comes from the identity, all unchanged rows select the original row, while the modified row applies exactly the intended combination.',
 'Applying the operation to A instead of I when constructing E|Using right multiplication for row operations|Writing successive operations in the wrong product order')
teach('L2.6',
 'A matrix model begins with meaning, not multiplication. Decide what each column quantity represents and what each output row measures. In a resource model, a row-column product totals one resource across products. In a population transition model, a column lists destinations from one source when column vectors are used.\nFor a production model q=Cq+d, total output q must supply both internal use Cq and external demand d. Rearranging gives (I−C)q=d. Solving the equation is only part of the task: inspect units, conservation rules, and whether the resulting values are physically possible. A mathematically invertible model can still use unrealistic assumptions.',
 'Linearity means each unit contributes a fixed amount, independent of other units. Summing those contributions creates a matrix product. Inverting the correct net-production matrix accounts for the feedback of internal consumption.',
 'Ignoring units or row labels|Inverting C instead of I−C|Using a transition matrix with the wrong vector convention')
teach('L3.1',
 'A determinant is a single number associated with a square matrix. In two dimensions it is ad−bc; geometrically it is signed area scaling. Negative signs indicate orientation reversal, and zero means some independent direction has collapsed.\nFor a larger square matrix, expand along any one row or column. Each term uses an entry, the determinant left after deleting its row and column, and the checkerboard cofactor sign. Choose a row or column with many zeros to reduce work. A determinant is not another matrix and is not defined for a nonsquare coefficient array.',
 'Cofactor expansion separates the determinant into contributions from one row while preserving signed volume scaling. Different expansion choices give the same scalar; using the signs correctly ensures cancellation when directions are dependent.',
 'Using the 2×2 rule on larger matrices|Dropping cofactor signs|Computing a determinant for a nonsquare matrix')
teach('L3.2',
 'Row operations make a determinant easier to compute, but each kind has a different effect. Swapping two rows reverses the sign. Multiplying one row by c multiplies the determinant by c. Adding a multiple of another row leaves the determinant unchanged.\nReduce toward triangular form and keep an operation ledger. The triangular determinant is the diagonal product; then correct for any recorded swaps or scalings to recover the original determinant. If you only use row replacements, no correction factor is needed. A zero row or two dependent rows give determinant zero.',
 'The determinant is alternating and linear in each individual row. Alternation explains the swap sign; row-linearity explains scaling; adding another row contributes a determinant with repeated rows, which is zero, explaining replacement invariance.',
 'Treating all row operations as determinant-preserving|Forgetting to undo a row-scaling factor|Adding diagonal entries instead of multiplying them')
teach('L3.3',
 'Determinant identities let you reason without expanding every matrix. A product has determinant equal to the product of determinants, transpose leaves the determinant unchanged, and an inverse has the reciprocal determinant. Each statement assumes suitable square matrices.\nScaling an n×n matrix by c scales n rows, so det(cA)=cⁿdet A. This differs from scaling one row. A matrix is invertible exactly when its determinant is nonzero. Do not extend multiplicative rules to addition: det(A+B) generally does not equal det A+det B.',
 'Volume scaling factors multiply under composition, which explains det(AB). The identity matrix has determinant 1, so applying the product rule to AA⁻¹=I forces the inverse determinant to be a reciprocal.',
 'Writing det(A+B)=det A+det B|Using c rather than cⁿ for det(cA)|Taking a reciprocal when the original determinant is zero')
teach('L3.4',
 'Cramer’s Rule isolates one unknown using determinants. Start with a square coefficient matrix A whose determinant is nonzero. To find xᵢ, replace only column i by the constants, then divide the new determinant by det A. The other coefficient columns stay in their original order.\nThe adjugate is the transpose of the entire cofactor matrix. The identity A adj(A)=(det A)I gives another inverse formula. These methods are useful for small systems and symbolic reasoning; row reduction is often more efficient for larger problems. If det A=0, neither formula permits division and consistency requires a separate check.',
 'Replacing one column by AX expresses that column as a combination of original columns. All determinant terms with repeated columns vanish, leaving only xᵢdet A. This explains the ratio instead of treating it as a memorized trick.',
 'Replacing a row in Cramer’s Rule|Forgetting the transpose in the adjugate|Concluding a singular system always has no solution')
teach('L4.1',
 'A vector in Rⁿ is an ordered list. Order and dimension are part of its identity: (1,2) differs from (2,1), and a two-component vector cannot be added to a three-component vector. Addition combines matching coordinates; scalar multiplication changes every coordinate by the same factor.\nA linear combination is built by scaling several vectors and adding them. In higher dimensions the arithmetic remains componentwise even when you cannot draw a picture. Keep track of whether an operation produces a vector or a scalar: vector addition produces another vector, while a dot product produces one number.',
 'Coordinatewise operations inherit the algebraic rules of real numbers. A linear combination describes a sequence of independent contributions in a common coordinate system, which makes the same formulas useful in geometry and data models.',
 'Mixing dimensions|Applying a scalar to only one component|Confusing a vector with its dot product')
teach('L4.2',
 'The word vector can mean more than an arrow or column of numbers. Polynomials, matrices, and functions can be vectors when their addition and scalar multiplication satisfy the same axioms. First identify the set and its operations; then check closure, identities, inverses, and the remaining algebraic rules.\nFor P₂, polynomials have degree at most two. Their sum and scalar multiples stay in P₂, and the zero polynomial is the zero vector. Polynomials of degree exactly two fail: a polynomial plus its negative produces the excluded zero polynomial. Similar reasoning applies to matrix and function spaces.',
 'The axioms specify precisely which familiar algebraic manipulations remain valid in a new setting. Once an abstract space satisfies them, linear combinations, independence, and bases can be studied without depending on a physical picture.',
 'Assuming every set of functions is a vector space|Confusing degree exactly n with degree at most n|Using a numerical zero instead of the zero object for that space')
teach('L4.3',
 'A subspace is a smaller vector space sitting inside one already known. Because the surrounding space supplies most axioms, use the short test: zero must belong, and every combination au+bv of two allowed elements must remain allowed. The scalars a and b are arbitrary real numbers.\nHomogeneous linear constraints usually define subspaces: a constraint L(v)=0 remains true for sums and scalar multiples. A nonzero right side often shifts the set away from zero and immediately fails the test. For polynomials or matrices, write a general allowed object and see what restrictions remain on its coefficients or entries.',
 'Closure under arbitrary linear combinations gives both addition and scalar multiplication closure. Inherited operations then provide the other axioms. A single counterexample can disprove a subspace claim, while a proof must cover arbitrary allowed elements.',
 'Checking only a few sample vectors|Forgetting the zero test|Assuming a line or plane away from the origin is a subspace')
teach('L4.4',
 'Span asks what you can make; independence asks whether any supplied direction is redundant. To test whether b belongs to a span, put the supplied vectors in columns and solve Ac=b. The coefficients c describe how to build b. If that system is inconsistent, b lies outside the span.\nFor independence solve Ac=0. Only the zero coefficient vector means independence; a nonzero solution displays a dependence relation. Having more vectors than the dimension guarantees dependence, but the reverse is not automatic. A collection can be independent without spanning the whole surrounding space.',
 'Matrix multiplication Ac is exactly the linear combination of A’s columns with coefficients c. This turns both spanning and independence questions into systems already understood through row reduction.',
 'Confusing spanning with independence|Using a relation that works at only one coordinate|Assuming a small collection automatically spans the entire space')
teach('L4.5',
 'A basis is a list that does both jobs: it spans the space and has no redundancy. Its coordinates are unique because two different coefficient lists would subtract to a nontrivial zero combination. Dimension counts basis vectors, not entries in an arbitrary description.\nTo select a column-space basis, reduce the matrix to locate pivot columns, then return to those columns of the original matrix. For Pₙ include the constant polynomial: the standard basis has n+1 elements. To compute coordinates in a nonstandard ordered basis, solve the basis-column system rather than copying the vector’s standard entries.',
 'Spanning guarantees every vector has coordinates; independence guarantees they are unique. The invariance of basis size makes dimension a property of the space, even though many different bases can describe it.',
 'Checking only independence or only spanning|Selecting reduced columns for the original column space|Forgetting the constant polynomial in Pₙ')
teach('L4.6',
 'Four spaces organize the information in a matrix: row space, column space, null space, and the corresponding space for the transpose. For an m×n A, rows and null-space inputs lie in Rⁿ, while columns and outputs lie in Rᵐ. Row and column spaces have the same dimension, called rank.\nCount pivots for rank and nonpivot variable columns for nullity. Rank plus nullity equals n, the domain dimension. A system Ax=b is consistent exactly when b lies in the column space, equivalently when A and [A|b] have equal rank. A consistent system is unique exactly when nullity is zero.',
 'Each pivot variable is determined by restrictions, while each free variable contributes an independent homogeneous direction. This partitions the n input degrees of freedom into rank and nullity. Nonhomogeneous solution sets are one particular solution plus the null space.',
 'Using the number of rows in rank-nullity|Confusing the ambient spaces of rows and columns|Ignoring an extra pivot in the augmented column')
teach('L4.7',
 'A vector is not the same thing as its coordinate list. The basis specifies how to turn coordinates into the actual vector. If B contains basis vectors as columns, then v=B[v]B. To express the same vector in basis C, solve C[v]C=v, giving [v]C=C⁻¹B[v]B.\nThe transition matrix therefore names a direction: destination basis on the left of the arrow, source on the right. Apply the source basis first to recover standard coordinates, then the destination inverse. Changing coordinates changes the description, not the vector itself. Reconstructing v in both bases is the best sign and order check.',
 'The formula follows by equating two descriptions of the same vector: B[v]B=C[v]C. Invertibility of basis matrices guarantees that the conversion is unique and reversible.',
 'Using B⁻¹C for a B-to-C conversion|Treating basis vectors as rows|Changing basis order without changing coordinate order')
teach('L4.8',
 'Vector spaces provide a way to encode objects with a small set of independent coefficients. A polynomial is recorded by its basis coefficients; a symmetric matrix needs fewer independent values than its total number of entries. The basis is the decoding rule for that information.\nWhen a model uses a nonstandard basis, compare coefficients or entries to find coordinates and then reconstruct the object to check. A constraint may reduce the dimension without reducing the number of written entries. A proposed basis must describe the intended subspace, not necessarily the entire surrounding polynomial or matrix space.',
 'The map from basis coefficients to objects is linear and one-to-one. Constraints remove independent degrees of freedom, so counting free coefficients after applying the constraints yields the dimension of the model space.',
 'Counting equal constrained entries twice|Using coordinates without naming a basis|Assuming a basis of a subspace spans the whole ambient space')
teach('L5.1',
 'The dot product connects coordinate arithmetic to geometry. Squaring length gives u·u. Distance is the length of a difference, not a difference of lengths. For nonzero vectors, divide their dot product by both lengths to get the cosine of the angle. Zero dot product means perpendicularity.\nKeep norms and squared norms distinct. Cauchy–Schwarz guarantees the angle formula has an allowable cosine. Parallel nonzero vectors give equality in that inequality; the sign of the dot product distinguishes same and opposite directions. The zero vector is orthogonal to every vector, but an angle involving it is undefined.',
 'The dot product is bilinear and positive definite, so it yields a nonnegative squared length. Expanding a squared difference gives the cosine rule, which explains the angle formula and the relation between inner product and distance.',
 'Taking a square root when asked for squared length|Computing an angle with a zero vector|Using ‖u‖−‖v‖ as the distance between vectors')
teach('L5.2',
 'An inner product extends the dot product to spaces where ordinary coordinate geometry is not built in. For real spaces it must be symmetric, linear, and positive definite. Weighted dot products can work when all weights are positive; function spaces can use integrals of products over an interval.\nProjection onto a nonzero u has the form cu. Choose c so the leftover v−cu is perpendicular to u, giving c=⟨v,u⟩/⟨u,u⟩. This denominator is essential unless u is already unit length. The residual measures the part that cannot be explained by the chosen direction and gives the shortest distance to its span.',
 'Orthogonality of the residual gives 0=⟨v−cu,u⟩=⟨v,u⟩−c⟨u,u⟩. Solving for c derives the projection formula. Positive definiteness ensures the denominator is nonzero for nonzero u and supports the nearest-point interpretation.',
 'Omitting the denominator for a nonunit vector|Projecting onto zero|Assuming any symmetric formula is positive definite')
teach('L5.3',
 'Gram–Schmidt separates the independent directions in a list without changing what the list spans. Keep the first vector, then remove from each later vector every component along the earlier orthogonal vectors. These subtractions create orthogonality; dividing each nonzero result by its length creates unit vectors.\nDo not mix normalized and unnormalized formulas. When projecting onto an unnormalized u, divide by ⟨u,u⟩. If the process produces zero, the supplied list was dependent at that step, so zero cannot be normalized. Check all pairwise inner products and lengths before calling the output orthonormal.',
 'Subtracting a combination of earlier directions preserves the span while making the new residual orthogonal to them. Induction applies this reasoning to each vector. Independence guarantees each residual is nonzero, allowing normalization.',
 'Removing only the last earlier projection|Normalizing a zero residual|Treating an orthogonal set as automatically unit length')
teach('L6.1',
 'A linear transformation preserves linear combinations. It must send a sum to the sum of images and a scalar multiple to the same scalar multiple of the image. A fixed matrix always defines such a map. Differentiation and evaluation can also be linear maps on appropriate function spaces.\nThe zero test is a quick way to disprove linearity: every linear map sends zero to zero. Passing that test alone does not prove linearity; a quadratic map can pass it and fail scaling. Always specify the domain and codomain and verify the rule actually lands in the declared codomain.',
 'Preserving arbitrary two-term combinations implies both additivity and homogeneity. Conversely, those two properties imply preservation of any finite combination, which makes the action on a basis enough to determine the entire map.',
 'Calling any straight-line-looking rule linear despite a constant offset|Using only the zero test as a proof|Forgetting the codomain')
teach('L6.2',
 'The kernel is the set of inputs erased by a map; the range is the set of outputs it can actually create. For T(v)=Av, solve Av=0 for the kernel and span the columns of A for the range. These sets can live in spaces of different dimensions.\nA linear map is one-to-one exactly when only zero is erased. It is onto exactly when its columns span the declared codomain. Rank-nullity counts the domain’s independent directions as visible output directions plus erased directions. A map can be onto without being one-to-one, especially when the domain has more dimensions than the codomain.',
 'If two inputs share an output, their difference lies in the kernel. A zero kernel therefore means no information collisions. The range is the span of basis images, and its dimension is rank; counting the remaining domain directions gives nullity.',
 'Placing kernel vectors in the output space|Confusing onto with one-to-one|Testing onto without naming the codomain')
teach('L6.3',
 'To build the standard matrix of a linear map, apply it to each standard basis vector and use those image vectors as columns. Linearity then guarantees the same matrix computes every input. For other bases, convert each basis image into the output basis’s coordinates before forming its column.\nComposition follows application order from right to left. If T acts first and S second, the matrix is [S][T]. Check the intermediate dimensions: the output space of T must be an acceptable input space for S. Test the resulting matrix on a simple vector to confirm both the order and interpretation.',
 'An input v=Σvⱼeⱼ maps to ΣvⱼT(eⱼ), exactly a matrix-column combination. Composing the two linear combinations gives the row-column product, so the matrix multiplication rule follows from the definition of a linear transformation.',
 'Putting basis images in rows|Reversing the order for S after T|Using standard coordinates when an output basis is specified')
teach('L6.4',
 'The same linear operator can look different in different bases. If P maps new coordinates to old coordinates, the new matrix is P⁻¹AP. Read the product as three actions: decode the input, apply the old transformation, then encode the output in the new basis.\nMatrices related this way are similar. They share determinant, trace, characteristic polynomial, and eigenvalues, although individual entries can differ. Similarity requires an invertible square P and a map from a space to itself; it is more specific than row equivalence. Invariants help check a calculation but do not prove similarity by themselves.',
 'Conjugation follows by applying coordinate conversion to both the input and output of the same map. The inverse factors cancel inside determinant products and powers, preserving intrinsic information while changing its coordinate description.',
 'Using PAP⁻¹ with the wrong coordinate convention|Confusing similarity with row equivalence|Assuming matching trace alone proves similarity')
teach('L7.1',
 'An eigenvector identifies a nonzero direction that stays on its original line under a transformation. Its eigenvalue is the scaling factor: positive preserves orientation, negative reverses it, and zero collapses that direction. The eigenvector itself may never be zero.\nRearrange Av=λv into (A−λI)v=0. A nonzero solution requires singularity, giving the characteristic equation. After finding each λ, solve that homogeneous system for its full eigenspace. Repeated roots need care: algebraic multiplicity counts repetitions of the root, while geometric multiplicity counts independent eigenvectors. Real matrices can have nonreal eigenvalues, so a real eigenspace is not guaranteed.',
 'The eigenvector equation becomes a homogeneous system; nontrivial solutions exist precisely when the determinant vanishes. Root multiplicity and null-space dimension measure different things, which explains why a repeated eigenvalue can have too few eigenvectors for a basis.',
 'Accepting the zero vector as an eigenvector|Assuming a repeated root gives two independent eigenvectors|Forgetting to solve for the eigenspace after finding eigenvalues')

teach('D1.1',
 'A differential equation describes a function through its rates of change. Begin by identifying dependent and independent variables. An ODE has one independent variable; a PDE involves partial derivatives with respect to multiple variables. Order is the highest derivative order. Linearity concerns the unknown function and its derivatives, not the complexity of coefficients in the independent variable.\nA general solution contains arbitrary constants; initial or boundary data select particular members. To verify a candidate, differentiate it enough times, substitute into the original equation, and check the data separately. State an interval where the expressions and equation are defined.',
 'Differentiation reveals whether a proposed function produces the prescribed rate. Checking an equation at only one point cannot verify a solution on an interval; checking the differential identity and all conditions can.',
 'Confusing order with polynomial degree|Calling an equation nonlinear because a coefficient contains sin x|Checking the initial value but not the equation')
teach('D2.2',
 'A separable equation has y′=g(x)h(y). Where h(y)≠0, place the y-expression with dy and the x-expression with dx, then integrate both sides. Include one arbitrary constant and apply any initial condition afterward. Logarithms from ∫dy/y require absolute values before exponentiation.\nBefore dividing by h(y), solve h(y)=0: those constant equilibrium solutions may be lost during division. A formula can also have poles or change branches; choose the interval containing the initial point on which the equation and selected solution make sense. Substitution and differentiation provide a final check.',
 'On intervals where separation is legitimate, the chain rule makes the derivative of an antiderivative of 1/h(y) equal to y′/h(y)=g(x). Integrating this identity explains separation without treating differentials as unexplained algebra.',
 'Losing constant solutions by dividing by h(y)|Dropping absolute values from logarithms|Ignoring an interval boundary where the solution blows up')
teach('D2.3',
 'Here homogeneous means scaling x and y together leaves the slope as a function of y/x. It does not mean zero forcing in a higher-order linear equation. Set v=y/x on an interval excluding x=0, so y=vx and the product rule gives y′=v+xv′.\nSubstitute both expressions into y′=F(y/x) to obtain xv′=F(v)−v. This is separable. Check roots of F(v)−v before division, integrate the remaining equation, and recover y=xv. Apply data to the recovered function and check the original equation, including its allowed x interval.',
 'The substitution encodes the ratio that controls the slope. Removing the direct y/x dependence leaves a function of v and a factor x, which can be separated. Constant ratios give straight-line solutions and must be retained.',
 'Writing y′=xv′ and forgetting v|Confusing this use of homogeneous with zero forcing|Dividing by F(v)−v without checking its zeros')
teach('D2.4',
 'An exact equation M dx+N dy=0 says the total change of a potential F is zero along solution curves. On a rectangle with continuous first partial derivatives, test Mᵧ=Nₓ. If the test fails, the equation is not exact in its current form.\nIntegrate M with respect to x while holding y fixed, and add g(y), not just a numerical constant. Differentiate the result with respect to y, compare with N, and solve for g′(y). Integrate once more and state F(x,y)=C. An initial point determines C. Check both partial derivatives; locally, the relation defines y(x) where Fᵧ≠0.',
 'The total differential is dF=Fₓdx+Fᵧdy. Equality of mixed partials motivates the exactness test, while the extra function g(y) captures information invisible to x-differentiation.',
 'Comparing Mₓ with Nᵧ|Using only a constant after partial integration|Adding independent arbitrary functions to both integrations')
teach('D2.5',
 'First divide by the coefficient of y′ so the equation reads y′+P(x)y=Q(x), on an interval where that coefficient is nonzero. The integrating factor μ=e^(∫P dx) turns the entire left side into (μy)′. Multiply every term, integrate μQ, and divide by μ.\nUse initial data after obtaining the family, or integrate from the initial point directly. A nonzero constant factor in μ cancels from the method, so choose the simplest convenient factor. Variable coefficients such as 1/x require an interval excluding zero. Differentiate the result to verify the original equation.',
 'The product rule requires μ′=Pμ. Solving that separable equation gives the integrating factor. Thus the method is designed to create a derivative we know how to integrate.',
 'Finding μ before normalizing the derivative coefficient|Forgetting to multiply the forcing by μ|Failing to divide the integrated result by μ')
teach('D4.1',
 'A higher-order linear equation combines y and its derivatives with coefficients depending only on x. Normalize by the leading coefficient on an interval where it does not vanish. Zero forcing gives a homogeneous equation; nonzero forcing gives a nonhomogeneous one.\nFor a regular nth-order homogeneous equation, the solution space has dimension n. An independent set of n solutions forms a fundamental set. For a forced equation, find one particular function yₚ and add the entire complementary family y꜀. The forced solution set usually does not contain zero and therefore is not itself a vector space.',
 'A linear differential operator preserves sums and constant multiples. Its kernel is the homogeneous solution space; if two functions solve the same forced equation, their difference lies in that kernel.',
 'Using the solution-space theorem where the leading coefficient vanishes|Calling a forced solution set a vector space|Omitting the complementary family')
teach('D4.1.1',
 'An nth-order IVP supplies n values of y and its first n−1 derivatives at the same initial point. Under continuous normalized coefficients and forcing, those data determine a unique solution throughout the regular interval. Differentiate the general family before applying derivative conditions.\nBoundary-value problems impose conditions at different points and behave differently: they can have one solution, none, or infinitely many. Substitute every endpoint into the same family and solve for its constants. A condition that becomes an identity supplies no new restriction; a contradiction means no member of the family works.',
 'Initial data fix all coordinates in the n-dimensional homogeneous family. Endpoint conditions can be dependent or incompatible, so the IVP uniqueness theorem cannot simply be transferred to boundary data.',
 'Replacing a function endpoint value by a derivative value|Assuming every boundary-value problem is unique|Applying uniqueness across a singular coefficient')
teach('D4.1.2',
 'Solution functions are independent when no constant combination vanishes identically on the interval. A relation at one x-value is not enough. A visible constant multiple proves dependence immediately. Otherwise, form the Wronskian using functions in the first row, first derivatives in the second, and successive derivatives below.\nA nonzero Wronskian at one point proves independence. For solutions of the same regular homogeneous linear ODE, a zero Wronskian and nonzero Wronskian obey stronger all-or-nothing results. For arbitrary differentiable functions, an identically zero Wronskian alone need not prove dependence; use a direct relation or appropriate theorem.',
 'A dependence relation also holds after differentiation. The resulting coefficient system has the Wronskian matrix; an invertible matrix forces all coefficients to zero, proving independence.',
 'Using variable coefficients in a dependence relation|Treating one zero Wronskian value as a general dependence proof|Computing the determinant in the wrong row order')
teach('D4.1.3',
 'A fundamental set supplies all homogeneous solutions through constant combinations. For a second-order equation, two independent functions are needed; repeating a function does not create a new direction. Initial data then choose the constants.\nFor L[y]=g, write y=y꜀+yₚ. Superposition also helps with several forcing terms: if L[p₁]=g₁ and L[p₂]=g₂, then L[p₁+p₂]=g₁+g₂. This does not mean two solutions of the same forced equation can be added without changing the forcing. Distinguish a general complementary family from one particular response.',
 'Linearity gives L[y꜀+yₚ]=0+g. Conversely, subtracting a particular response from any forced solution leaves a homogeneous solution, so the decomposition captures the whole solution set.',
 'Adding arbitrary constants to an already fixed particular solution|Assuming the sum of two solutions of the same forced equation has the same forcing|Using dependent functions as a fundamental set')
teach('D4.3',
 'For constant coefficients, try y=eʳˣ. Each derivative multiplies by r, so the ODE reduces to a characteristic polynomial. Distinct real roots give separate exponentials. A root r repeated m times gives eʳˣ, xeʳˣ, through xᵐ⁻¹eʳˣ.\nA conjugate pair α±iβ gives real terms eᵅˣcos βx and eᵅˣsin βx. Build enough independent terms to match the equation’s order before applying conditions. Differentiate the completed family and check all data. A repeated root requires new forms, not repeated copies of the same exponential.',
 'Exponentials convert differentiation into scalar multiplication. Repeated factors need generalized solution forms, while Euler’s complex exponential identity converts conjugate modes into real sine and cosine terms.',
 'Using only one term for a repeated root|Dropping the real exponential envelope for complex roots|Including fewer constants than the equation order')
teach('D4.4',
 'Undetermined coefficients works for constant-coefficient linear equations with polynomial, exponential, sine/cosine forcing and finite sums/products of those types. Solve the complementary equation first. Choose a full trial family matching the forcing, including lower polynomial powers and both trigonometric partners.\nCheck whether the trial overlaps the complementary family. If so, multiply the entire trial by x enough times to remove the overlap. Differentiate, substitute into the original equation, and equate coefficients. For several forcing pieces, solve each particular response separately and add them. Finally include the complementary family if a general solution is requested.',
 'The chosen finite family is closed under differentiation, making substitution an algebraic coefficient problem. Resonance means the operator erases an unadjusted trial; extra powers of x supply a new independent response.',
 'Trying undetermined coefficients for arbitrary forcing such as tan x|Omitting lower polynomial powers or the sine/cosine partner|Forgetting the resonance multiplier')
teach('D4.5',
 'The symbol D represents differentiation, so D²y means y″ and a polynomial L(D) is a linear combination of derivatives. It is not a square of y′. For constant coefficients, factor L(D) like an ordinary polynomial and connect its roots to exponential solutions.\nFor an exponential eʳˣ, L(D)eʳˣ=L(r)eʳˣ. This is a useful shortcut for evaluating a trial. Constant-coefficient operator factors commute, but variable coefficients do not generally commute with D: D(xy)=xy′+y differs from xDy. Keep this distinction when manipulating operators.',
 'Repeated differentiation of an exponential multiplies by repeated powers of r. Polynomial combinations of derivatives therefore act through the same polynomial evaluated at r. The product rule explains the failure of variable-coefficient commutation.',
 'Interpreting D²y as (y′)²|Commuting variable coefficients past D|Factoring without keeping every operator term')
teach('D4.6',
 'An annihilator turns a specific forcing into zero. A degree-n polynomial is killed by Dⁿ⁺¹; eᵃˣ by D−a; sin bx and cos bx by D²+b². Products with polynomial factors require repeated annihilator factors.\nApply the annihilator to both sides of L(D)y=g. The enlarged homogeneous equation suggests possible response terms, including resonance powers. Remove terms already belonging to the original complementary family and use the remaining terms as a particular trial. Determine its coefficients by substituting into the original forced equation; the enlarged equation alone has lost the forcing amplitude.',
 'Applying an annihilator deliberately removes information about the forcing. Its roots reveal the right trial space, but only the original equation can recover the coefficients that reproduce the actual input.',
 'Using Dⁿ for a degree-n polynomial|Keeping all enlarged homogeneous constants as particular coefficients|Checking only the annihilated equation')
teach('D6.1',
 'A Cauchy–Euler equation pairs y″ with x² and y′ with x. Use a power trial y=xᵐ, whose derivatives keep every term proportional to xᵐ. The second derivative contributes m(m−1), not m². Work on an interval excluding x=0.\nDistinct real auxiliary roots give powers xᵐ. A repeated root gives xᵐ and xᵐln|x|. Complex roots α±iβ give |x|ᵅ times cosine and sine of βln|x|; the examples use x>0 to avoid branch ambiguity. Apply conditions within the selected interval and verify with the chain rule.',
 'The substitution u=ln x for x>0 turns the Euler equation into a constant-coefficient equation. Powers in x correspond to exponentials in u, explaining logarithmic factors and oscillations in ln x.',
 'Using eᵐˣ as the Euler trial|Replacing m(m−1) by m²|Crossing x=0 without addressing the singular equation')
teach('D6.2',
 'A power series records a function through coefficients of powers about a center. Convergence has a radius: inside it, termwise differentiation and integration are valid; at endpoints, test convergence separately. The Maclaurin coefficient is f⁽ⁿ⁾(0)/n!, not just the derivative.\nFor a series solution of an ODE, assume y=Σcₙxⁿ, differentiate, shift indices so both sides use the same power, and compare coefficients. Initial data determine the first coefficients; a recurrence determines the rest. Recognize a familiar function when possible, but retain the recurrence reasoning and the interval of convergence.',
 'Equality of convergent power series on a neighborhood forces matching coefficients. Analytic coefficients around an ordinary point support local analytic solutions; singular points may require methods beyond an ordinary power-series ansatz.',
 'Comparing coefficients before aligning powers|Forgetting the factorial in Taylor coefficients|Assuming endpoints are included because the radius is known')
teach('D7.1',
 'The Laplace transform replaces a time function by an integral depending on s. The damping factor e⁻ˢᵗ must dominate growth for the improper integral to converge. Piecewise continuity and an exponential-order bound provide standard sufficient conditions, not a claim that every function transforms.\nLearn basic pairs from the definition: constants yield 1/s, exponentials shift that denominator, powers give factorials, and sine/cosine produce quadratic denominators. Use linearity to transform sums. Track the convergence half-plane along with the algebraic expression, especially when positive exponential growth is present.',
 'Integration packages all nonnegative-time behavior into F(s). Integration by parts produces algebraic derivative rules with initial data, which is why the transform can simplify initial-value problems.',
 'Using the time variable in the final transform|Omitting a factorial for a power|Ignoring whether the improper integral converges')
teach('D7.2',
 'Inverting a transform means recognizing time functions hidden in an algebraic expression. Simplify the rational expression first: divide if necessary, factor denominators, complete squares, and split into partial fractions. Each numerator must match the corresponding table entry.\nDistinct linear factors give separate simple fractions; repeated factors require every power up to the repetition. Quadratic denominators may need a constant and linear numerator, yielding sine and cosine pieces. Use linearity after decomposition, and transform your proposed function back to verify the result. For sufficiently regular exponential-order functions, inversion is unique apart from immaterial point values.',
 'Partial fractions rewrite the same transform as a sum of elementary pairs. Uniqueness justifies matching those pairs, while forward transformation independently checks algebraic signs and coefficient factors.',
 'Omitting terms for repeated denominator factors|Confusing sine and cosine numerators|Applying inverse transforms to factors as though they were separate products')
teach('D7.3',
 'Two shifts act in different domains. Multiplication by eᵃᵗ replaces every s in F with s−a. A time delay u(t−a)f(t−a) multiplies the transform by e⁻ᵃˢ. Rewrite an unshifted function inside a step so its argument uses elapsed time before using the delay theorem.\nMultiplication by t has another rule: transform differentiation, L{tf}=−F′(s). Higher powers give higher s-derivatives with alternating signs. Distinguish these from transforms of time derivatives. For piecewise functions, build step expressions interval by interval and check the resulting values on each interval.',
 'The exponential shift combines exponents in the defining integral. A change of integration variable t=u+a creates the delay factor. Differentiating the kernel e⁻ˢᵗ with respect to s produces −t, explaining transform derivatives.',
 'Shifting only the denominator|Delaying the step but not the function argument|Confusing a time derivative with an s-derivative')
teach('D7.4',
 'A time derivative becomes sF(s) minus an initial value; second and higher derivatives include successive initial derivatives. Accumulation from zero divides by s. These rules turn differential and integral operations into algebra while retaining starting data.\nConvolution is a time integral of one function against a reversed shifted copy of another; its transform is a product. A product of transforms therefore inverts to convolution, not pointwise multiplication. For periodic inputs, integrate over one full period and divide by 1−e⁻ᵀˢ. Include zero pieces when identifying the full period even though they contribute no integral.',
 'Integration by parts yields derivative identities and their boundary terms. Exchanging integration order gives the convolution theorem. Splitting a periodic integral into repeated periods produces a geometric series and the periodic denominator.',
 'Dropping initial-value terms|Inverting a product as a pointwise product|Using only the nonzero part as the period length')
teach('D7.5',
 'To solve an IVP, transform every term with its initial values, collect all Y(s) terms, and solve the resulting algebraic equation. Simplify Y using partial fractions, square completion, and shifting rules before taking the inverse. Keep the independent variable consistent throughout.\nFor delayed or piecewise forcing, represent the input with steps and delay the complete response. Check the solution separately before and after each transition, along with continuity and the specified initial data. At a jump in forcing, derivatives may have one-sided values; the ODE is interpreted on the open pieces unless a distributional formulation is specified.',
 'The transform encodes initial conditions directly in derivative formulas. Solving for Y determines the unique regular IVP response, while inverse transforms restore a function that can be independently checked in the original equation.',
 'Solving for Y before collecting all its terms|Forgetting to delay every occurrence of t|Checking only the transformed algebra and not the time solution')
teach('D8.3',
 'A system tracks several quantities whose rates may depend on one another. List state variables in a fixed order and evaluate every rate at the same current state. A derivative vector is a direction of change, not the state itself.\nA higher-order equation becomes a first-order system by introducing one state per derivative below the highest order. For y″+ay′+by=0, use x₁=y and x₂=y′, then x₁′=x₂ and x₂′=−bx₁−ax₂. Triangular systems can be solved sequentially: solve an independent component first and use it as forcing for the next equation.',
 'The state records enough information to determine the next rates. Differentiating its definitions and using the original highest-derivative equation proves the first-order system carries the same solution information.',
 'Mixing state order between equations|Treating a rate vector as the next state|Forgetting initial derivative data when introducing states')
teach('D8.5',
 'Write a linear system as X′=A(t)X+F(t). Row i of A gives coefficients in equation i; column j belongs to state variable j. Terms depending only on time form F, not extra columns of A. A zero F gives a homogeneous system.\nDifferentiate vector solutions componentwise and check every row equation. A fundamental matrix has independent homogeneous solution columns and is invertible on a regular interval. Its product with a constant coordinate vector gives the homogeneous general solution. Changing the order of states requires consistently rearranging rows, columns, data, and forcing.',
 'Matrix multiplication is precisely the collection of row equations. Linearity of the system preserves constant combinations of homogeneous solution vectors, making a fundamental matrix a time-dependent basis for all homogeneous solutions.',
 'Transposing the coefficient matrix|Putting forcing into a state-variable coefficient|Changing state order in only one part of the model')
teach('D8.6',
 'For X′=AX with constant A, try X=eˡᵗv. Substitution gives Av=λv, linking differential systems to eigenvalues. Each independent eigenvector supplies an exponential mode. Distinct real eigenvalues give separate real modes.\nComplex conjugate pairs produce real sine/cosine vector solutions with an exponential envelope. Repeated eigenvalues require checking the eigenspace: if too few independent eigenvectors exist, generalized eigenvectors introduce polynomial factors in t. Apply the initial vector to the complete independent family and verify X′=AX. Triangular systems also allow a direct sequential check of repeated-root formulas.',
 'The exponential trial separates the time factor from a constant direction. Missing eigenvectors in a repeated eigenspace signal a nilpotent coupling, whose exponential introduces factors such as t eˡᵗ rather than another identical mode.',
 'Using a zero eigenvector|Assuming every repeated eigenvalue supplies a full eigenbasis|Dropping coupled sine/cosine signs when forming real solutions')
teach('D9.2',
 'Euler’s method follows a tangent slope for one short step: evaluate f at the current approximate point, multiply by h, and add that increment. Then update x and recompute the slope. Keep a table of xₙ, yₙ, f(xₙ,yₙ), and the next estimate to avoid reusing old information.\nImproved Euler (Heun) first predicts an endpoint with Euler, then averages the starting and predicted endpoint slopes. A smaller step usually reduces truncation error, but stability matters: for y′=λy, Euler multiplies by 1+hλ each step. A decaying exact solution can have growing numerical estimates if that multiplier has magnitude above 1.',
 'The differential equation gives local slope, and a short tangent segment approximates the curve. Euler has first-order global accuracy under standard smoothness conditions; Heun’s averaged slope improves it to second order, but neither replaces error and stability checks.',
 'Using the starting slope for every step|Treating an approximation as an exact value|Choosing a large step without checking stability')

extra_formulas = {
 'L1.1': [('Solution criteria',r'\operatorname{rank}(A)=\operatorname{rank}([A|b])\ \Longleftrightarrow\ Ax=b\text{ is consistent}')],
 'L1.2': [('Free parameters in a consistent system',r'\#\text{ free variables}=n-\operatorname{rank}(A)')],
 'L2.1': [('Transpose',r'(A^T)_{ji}=a_{ij},\quad(AB)^T=B^TA^T')],
 'L2.2': [('Identity and product transpose',r'I_mA=AI_n=A,\quad(AB)^T=B^TA^T')],
 'L2.3': [('Two-by-two inverse',r'\begin{bmatrix}a&b\\c&d\end{bmatrix}^{-1}=\frac1{ad-bc}\begin{bmatrix}d&-b\\-c&a\end{bmatrix},\quad ad-bc\ne0')],
 'L2.4': [('Undo successive operations',r'(E_2E_1)^{-1}=E_1^{-1}E_2^{-1}')],
 'L2.6': [('Production balance',r'q=Cq+d\quad\Longrightarrow\quad q=(I-C)^{-1}d')],
 'L3.1': [('Two-by-two determinant and cofactor signs',r'\det\begin{bmatrix}a&b\\c&d\end{bmatrix}=ad-bc,\quad C_{ij}=(-1)^{i+j}M_{ij}')],
 'L3.2': [('Operation factors',r'\det(\text{swap}(A))=-\det A,\quad\det(\text{scale one row by }c)=c\det A')],
 'L3.3': [('Scaling and inverse',r'\det(cA)=c^n\det A,\quad\det(A^{-1})=1/\det A')],
 'L3.4': [('Adjugate identity',r'A\operatorname{adj}(A)=(\det A)I,\quad A^{-1}=\operatorname{adj}(A)/\det A')],
 'L4.1': [('Component operations',r'(u+v)_i=u_i+v_i,\quad(cu)_i=cu_i')],
 'L4.2': [('Addition axioms',r'u+v=v+u,\quad(u+v)+w=u+(v+w),\quad v+0=v,\quad v+(-v)=0'),('Scalar axioms',r'1v=v,\quad a(bv)=(ab)v,\quad a(u+v)=au+av,\quad(a+b)v=av+bv')],
 'L4.3': [('Homogeneous constraints define a subspace',r'W=\ker A=\{v:Av=0\}')],
 'L4.4': [('Independence criterion',r'Ac=0\text{ has only }c=0\quad\Longleftrightarrow\quad\text{columns of }A\text{ are independent}')],
 'L4.5': [('Basis coordinate equation',r'B[v]_{\mathcal B}=v,\quad\dim P_n=n+1')],
 'L4.6': [('Consistency and full solution set',r'\operatorname{rank}A=\operatorname{rank}[A|b],\quad x=x_p+z,\ z\in\ker A')],
 'L4.7': [('Basis matrix conversion',r'P_{\mathcal C\leftarrow\mathcal B}=C^{-1}B')],
 'L4.8': [('Symmetric matrix coordinates',r'\begin{bmatrix}a&b\\b&c\end{bmatrix}=a\begin{bmatrix}1&0\\0&0\end{bmatrix}+b\begin{bmatrix}0&1\\1&0\end{bmatrix}+c\begin{bmatrix}0&0\\0&1\end{bmatrix}')],
 'L5.1': [('Length, distance, and Cauchy–Schwarz',r'\|v\|=\sqrt{v\cdot v},\quad d(u,v)=\|u-v\|,\quad|u\cdot v|\le\|u\|\|v\|')],
 'L5.2': [('Function inner product and norm',r'\langle f,g\rangle=\int_a^b f(t)g(t)\,dt,\quad\|f\|=\sqrt{\langle f,f\rangle}')],
 'L5.3': [('Coordinates in an orthonormal basis',r'v=\sum_j\langle v,e_j\rangle e_j')],
 'L6.1': [('Necessary zero test',r'T(0)=0\quad\text{for every linear }T')],
 'L6.2': [('Dimension and injectivity',r'\operatorname{rank}T+\operatorname{nullity}T=\dim V,\quad T\text{ one-to-one}\iff\ker T=\{0\}')],
 'L6.3': [('Matrix in general domain and codomain bases',r'[T]_{\mathcal C\leftarrow\mathcal B}=\begin{bmatrix}[T(b_1)]_{\mathcal C}&\cdots&[T(b_n)]_{\mathcal C}\end{bmatrix}')],
 'L6.4': [('Similarity invariants',r'\det(P^{-1}AP)=\det A,\quad\operatorname{tr}(P^{-1}AP)=\operatorname{tr}A')],
 'L7.1': [('Eigenspace and multiplicities',r'E_\lambda=\ker(A-\lambda I),\quad1\le\dim E_\lambda\le\text{algebraic multiplicity}')],
 'D1.1': [('General linear form',r'a_n(x)y^{(n)}+\cdots+a_1(x)y\prime+a_0(x)y=g(x)')],
 'D2.2': [('Equilibria',r'y\prime=g(x)h(y),\quad h(c)=0\Longrightarrow y(x)=c')],
 'D2.3': [('Separated substitution equation',r'y\prime=F(y/x)\Longrightarrow x\frac{dv}{dx}=F(v)-v')],
 'D2.4': [('Total differential',r'dF=F_x\,dx+F_y\,dy=0\Longrightarrow F(x,y)=C')],
 'D2.5': [('Complete integrating-factor solution',r'y=\mu^{-1}\left(\int\mu(x)Q(x)\,dx+C\right)')],
 'D4.1': [('Forced solution decomposition',r'y=y_c+y_p,\quad L[y_c]=0,\quad L[y_p]=g')],
 'D4.1.1': [('Second-order data at one point',r'y(x_0)=y_0,\quad y\prime(x_0)=y_1')],
 'D4.1.2': [('Two-function Wronskian',r'W(f,g)=fg\prime-gf\prime')],
 'D4.1.3': [('Superposition with forcing',r'L[ap_1+bp_2]=ag_1+bg_2\quad\text{if }L[p_i]=g_i')],
 'D4.3': [('Repeated roots and conjugate roots',r'y_r=e^{rx}\sum_{j=0}^{m-1}C_jx^j,\quad y_{\alpha\pm i\beta}=e^{\alpha x}(A\cos\beta x+B\sin\beta x)')],
 'D4.4': [('Resonance-adjusted trial',r'y_p=x^m e^{ax}\big(P_n(x)\cos bx+Q_n(x)\sin bx\big)')],
 'D4.5': [('Exponential operator evaluation',r'L(D)e^{rx}=L(r)e^{rx}')],
 'D4.6': [('Basic annihilators',r'D^{n+1}[x^n]=0,\quad(D-a)e^{ax}=0,\quad(D^2+b^2)\sin bx=0')],
 'D6.1': [('Auxiliary polynomial and repeated root',r'am(m-1)+bm+c=0,\quad y_{\text{repeated}}=x^m(C_1+C_2\ln x),\ x>0')],
 'D6.2': [('Series derivatives',r'y\prime=\sum_{n=0}^\infty(n+1)c_{n+1}x^n,\quad y\prime\prime=\sum_{n=0}^\infty(n+2)(n+1)c_{n+2}x^n')],
 'D7.1': [('Basic pairs',r'\mathcal L\{1\}=1/s,\quad\mathcal L\{t^n\}=n!/s^{n+1},\quad\mathcal L\{\sin bt\}=b/(s^2+b^2)')],
 'D7.2': [('Sine and cosine pairs',r'\mathcal L^{-1}\{b/(s^2+b^2)\}=\sin bt,\quad\mathcal L^{-1}\{s/(s^2+b^2)\}=\cos bt')],
 'D7.3': [('Delay and transform derivatives',r'\mathcal L\{u(t-a)f(t-a)\}=e^{-as}F(s),\quad\mathcal L\{t^nf(t)\}=(-1)^nF^{(n)}(s)')],
 'D7.4': [('Second derivative, convolution, and periodicity',r'\mathcal L\{f\prime\prime\}=s^2F-sf(0)-f\prime(0),\quad\mathcal L\{f*g\}=FG'),('Periodic transform',r'F(s)=\frac{\int_0^T e^{-st}f(t)dt}{1-e^{-sT}}')],
 'D7.5': [('First-order IVP in transform form',r'y\prime+ay=g,\ y(0)=y_0\Longrightarrow Y(s)=\frac{G(s)+y_0}{s+a}')],
 'D8.3': [('Second-order to first-order',r'y\prime\prime+ay\prime+by=g\Longrightarrow x_1\prime=x_2,\ x_2\prime=g-ax_2-bx_1')],
 'D8.5': [('Fundamental matrix',r'\Phi\prime=A\Phi,\quad X=\Phi(t)C')],
 'D8.6': [('Eigenvector mode',r'Av=\lambda v\Longrightarrow X(t)=e^{\lambda t}v,\quad X\prime=AX')],
 'D9.2': [('Heun predictor and corrector',r'\widetilde y_{n+1}=y_n+hf(x_n,y_n),\quad y_{n+1}=y_n+\frac h2\big(f(x_n,y_n)+f(x_{n+1},\widetilde y_{n+1})\big)')],
}

def build():
    result = []
    for topic in topics:
        canonical = topic['courseId']+'-'+topic['section'].replace('.','-')
        lesson_id = old_ids.get(canonical, canonical)
        course = 'L' if topic['courseId']=='linear-algebra' else 'D'
        explanation, reasoning, mistakes = notes[course+topic['section']]
        definitions = [st(term.capitalize()+': '+glossary[term]) for term in topic['concepts']]
        if lesson_id in legacy:
            previous = legacy[lesson_id]
            exercises, examples = list(previous['exercises']), list(previous['examples'])
            if lesson_id=='projection':
                for mode in range(3):
                    problem=la_problem('5.2',mode+1,mode)
                    eid=f'projection-{11+mode}'
                    audit.append({'id':eid,'assertions':problem.pop('_proofs')})
                    exercises.append({'id':eid,'lessonId':lesson_id,'difficulty':mode+1,**problem})
                    example=la_problem('5.2',mode+5,mode)
                    audit.append({'id':f'projection-example-{4+mode}','assertions':example.pop('_proofs')})
                    examples.append({'title':example['prompt'],'difficulty':mode+1,'steps':[st(example['prompt'],example['math']),*example['solutionSteps']]})
        else:
            maker = la_problem if course=='L' else de_problem
            exercises = []
            for i in range(10):
                mode=3 if course=='D' and topic['section'] in ['7.2','7.3','7.4'] and i in [3,7] else i%3
                problem = maker(topic['section'],i//3+1,mode)
                exercise_id = f'{lesson_id}-{i+1}'
                audit.append({'id':exercise_id,'assertions':problem.pop('_proofs')})
                exercises.append({'id':exercise_id,'lessonId':lesson_id,'difficulty':1 if i<3 else 2 if i<7 else 3,**problem})
            examples = []
            for i in range(3):
                problem = maker(topic['section'],i+5,i)
                audit.append({'id':f'{lesson_id}-example-{i+1}','assertions':problem.pop('_proofs')})
                examples.append({'title':problem['prompt'],'difficulty':i+1,'steps':[st(problem['prompt'],problem['math']),*problem['solutionSteps']]})
        # References identify matching readings, not the provenance of original problems.
        source = topic.get('source')
        if canonical == 'differential-equations-7-3': source={'fileName':'7.2.pdf','pageNumbers':[4,5,6,7,8]}
        if canonical == 'differential-equations-4-4': source={'fileName':'4.3.pdf','pageNumbers':[7,8,9]}
        result.append({'id':lesson_id,'courseId':topic['courseId'],'chapter':topic['chapter'],'section':topic['section'],
            'title':topic['title'],'description':topic['mainIdea'],'difficulty':'beginner' if topic['section'].startswith(('1.','2.')) else 'intermediate',
            'keywords':[*topic['concepts'],*({'systems':['RREF','row reduction'],'eigenvalues':['eigenvalues','eigenvectors'],'linear-ode':['ODE','integrating factor','dy/dx']} .get(lesson_id,[]))],
            'prerequisites':[old_ids.get(p,p) for p in topic['prerequisites']],
            'learningObjectives':[topic['mainIdea'],'Define '+', '.join(topic['concepts'][:3])+'.','Work through the examples and check your own solution against the original conditions.'],
            'estimatedMinutes':35 if topic['section'].startswith(('1.','2.')) else 45,
            'sourceReferences':[{**source,'section':topic['section']}] if source else [],
            'provenance':'supplementary-original','reviewStatus':'verified','bigIdea':explanation,
            'definitions':definitions,'reasoning':reasoning,'formulas':([st('Core relationship and method for this section.',topic['formula'])] if topic.get('formula') else [])+[st(label,formula) for label,formula in extra_formulas[course+topic['section']]],
            'examples':examples,'exercises':exercises,'mistakes':mistakes,
            'summary':topic['mainIdea']+' '+reasoning,
            **({'visualization':legacy[lesson_id]['visualization']} if lesson_id in legacy and legacy[lesson_id].get('visualization') else {})})
    assert len(result)==51 and sum(l['courseId']=='linear-algebra' for l in result)==27
    assert sum(l['courseId']=='differential-equations' for l in result)==24
    expand_linear(result,audit,P,st,latex)
    enrich_examples(result,audit,st)
    expand_starters(result,audit,st)
    assert sum(len(l['exercises']) for l in result)==567
    ids={l['id'] for l in result}
    assert all(p in ids for l in result for p in l['prerequisites'])
    Path('src/content/course-lessons.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    Path('docs/curriculum-verification.json').write_text(json.dumps({'tool':'SymPy '+S.__version__,'newProblemsChecked':len(audit),'checks':audit},indent=2)+'\n')
    print(f'Built {len(result)} lessons, {sum(len(l["examples"]) for l in result)} examples, {sum(len(l["exercises"]) for l in result)} exercises; {len(audit)} new problems passed symbolic checks.')

if __name__ == '__main__': build()
