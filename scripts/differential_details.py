"""Explicit intermediate calculations for course problem families.

The original problem proofs still verify each result. Additional symbolic
calculations are checked here before becoming student-facing steps.
"""
import sympy as S
x,y,t,s,r,A,B,C=S.symbols('x y t s r A B C',real=True)

def expand_problem(problem,section,k,mode,st):
    additions={}
    def before(needle,steps):additions[needle]=steps
    if section=='2.3' and mode==0:
        before('Replace both', [st('Scale each occurrence of both variables, including both factors in the mixed term.',rf'(\lambda x)^2+{k}(\lambda x)(\lambda y)+(\lambda y)^2'),st('Square the scaling factor and then collect its common power.',rf'\lambda^2x^2+{k}\lambda^2xy+\lambda^2y^2')])
    if section=='2.3' and mode==1:
        before('Substitution cancels',[st('Insert y=vx and y′=v+xv′ into both sides.',r'v+xv\prime=v+1'),st('Subtract v from both sides.',r'xv\prime=1'),st('Divide by x, which is nonzero on the stated interval.',r'v\prime=\frac1x'),st('Integrate with respect to x; on x>0 the antiderivative is ln x.',r'v=\int\frac1x\,dx=\ln x+C')])
        before('Recover y',[st('Undo the substitution y=vx.',r'y=x(\ln x+C)'),st('Insert x=1 into the initial condition and use ln 1=0.',rf'{k}=1(0+C)'),st('Solve the constant equation.',rf'C={k}')])
    if section=='2.3' and mode==2:
        before('Integration gives',[st('Let u=1−2v; then du=−2 dv.',r'\int\frac{dv}{1-2v}=-\frac12\int\frac{du}{u}'),st('Integrate both sides of the separated equation.',r'-\frac12\ln|1-2v|=\ln x+C'),st('Multiply by −2, exponentiate, and absorb the signed constant.',r'1-2v=Kx^{-2}'),st('Isolate v, multiply by x, and rename the arbitrary coefficient.',r'y=\frac x2+\frac{C_1}{x}')])
        before('Use the initial',[st('Substitute x=1 into the family.',rf'\frac{{{k+1}}}2=\frac12+C_1'),st('Subtract one half from both sides.',rf'C_1=\frac{{{k}}}2')])
    if section=='2.4':
        F=[x*x+k*x*y+y*y,x*y+k*x*x,x*x*y+y*y+k*x][mode];M=S.diff(F,x);N=S.diff(F,y);I=S.integrate(M,x);g=S.simplify(N-S.diff(I,y))
        before('Integrate M',[st('Integrate each x-dependent term separately; any y factor is constant during this integration.',rf'\int({S.latex(M)})\,dx={S.latex(I)}'),st('Include an unknown function of y, since its x-derivative is zero.',r'\frac{\partial}{\partial x}g(y)=0')])
        before('Differentiate this',[st('Compute the y-partial derivative of the part already integrated.',rf'\frac{{\partial}}{{\partial y}}({S.latex(I)})={S.latex(S.diff(I,y))}'),st('Subtract that derivative from N to isolate the missing derivative.',rf'g\prime(y)=({S.latex(N)})-({S.latex(S.diff(I,y))})={S.latex(g)}')])
        before('Integrate g',[st('Integrate with respect to y; a remaining additive constant is absorbed into the final level constant.',rf'g(y)=\int({S.latex(g)})\,dy={S.latex(S.integrate(g,y))}')])
        assert S.simplify(I+S.integrate(g,y)-F)==0
    if section=='4.1.1' and mode in [0,1]:
        before('Integrate twice' if mode==0 else 'The general family',[st('Integrate y″=0 once; the derivative is an arbitrary constant.',r'y\prime=C_1'),st('Integrate once more to recover y, introducing a second constant.',r'y=C_1x+C_2')])
        if mode==0:before('The position condition',[st('Insert x=0 into the position condition.',rf'{k}=C_1(0)+C_2'),st('Differentiate the general family before using the velocity condition.',r'y\prime=C_1'),st('Insert x=0 into the velocity condition.',rf'{k+1}=C_1')])
        else:before('Use the second',[st('Insert the second endpoint into the same solution family.',rf'{k+4}=2C_1+{k}'),st('Subtract the already determined constant from both sides.',r'4=2C_1'),st('Divide both sides by two.',r'C_1=2')])
    if section=='4.1.2' and mode!=1:
        f,g=(S.exp(x),S.exp((k+1)*x)) if mode==0 else (S.cos(k*x),S.sin(k*x));f1=S.diff(f,x);g1=S.diff(g,x);wr=S.simplify(f*g1-g*f1)
        before('Compute the determinant',[st('Form the first product, using f and the derivative of g.',rf'fg\prime=({S.latex(f)})({S.latex(g1)})={S.latex(f*g1)}'),st('Form the second product, using g and the derivative of f.',rf'gf\prime=({S.latex(g)})({S.latex(f1)})={S.latex(g*f1)}'),st('Subtract the second product; for trigonometric functions use sin²+cos²=1.',rf'W=({S.latex(f*g1)})-({S.latex(g*f1)})={S.latex(wr)}')])
    if section=='4.1.3' and mode==0:
        f=k*S.exp(x)+(k+1)*S.exp(-x)
        before('Differentiate twice',[st('Differentiate the first exponential term.',rf'\frac{{d}}{{dx}}({k}e^x)={k}e^x'),st('Differentiate the negative-exponent term; its inner derivative is −1.',rf'\frac{{d}}{{dx}}({k+1}e^{{-x}})=-{k+1}e^{{-x}}'),st('Collect the first derivative.',rf'y\prime={S.latex(S.diff(f,x))}'),st('Differentiate again; the two negative signs in the second term cancel.',rf'y\prime\prime={S.latex(S.diff(f,x,2))}')])
    if section=='4.4':
        trial=[A*S.exp(2*x),A*x*x+B*x+C,A*x*S.sin(x)][mode]
        before(['Substitute the trial','Substitute and collect','Use yₚ=Ax'][mode],[st('Write the trial with its undetermined coefficients.',rf'y_p={S.latex(trial)}'),st('Compute its first derivative before the second derivative.',rf'y_p\prime={S.latex(S.diff(trial,x))}'),st('Differentiate once more, applying the product rule when needed.',rf'y_p\prime\prime={S.latex(S.diff(trial,x,2))}')])
        if mode==0:before('Match the coefficient',[st('Cancel the common nonzero exponential on both sides.',rf'3A={k}'),st('Divide both sides by the coefficient of A.',rf'A=\frac{{{k}}}3')])
        if mode==1:before('Match quadratic',[st('Equal polynomials have matching coefficients at each power.',rf'A={k},\quad B=0,\quad C+2A=0'),st('Insert A into the constant equation and subtract 2A.',rf'C+{2*k}=0\Rightarrow C=-{2*k}')])
    if section=='4.5' and mode==0:
        f=x**3+k*x
        before('D² means',[st('First apply the power rule to both terms of f.',rf'Df=3x^2+{k}'),st('Differentiate the result; the constant derivative is zero.',r'D^2f=6x+0')])
        before('Subtract the first',[st('Put parentheses around the full first derivative before subtracting.',rf'6x-(3x^2+{k})'),st('Distribute the negative sign to every term inside the parentheses.',rf'6x-3x^2-{k}')])
    if section=='4.6' and mode==0:
        before('Differentiating that many',[st(f'After derivative {j}, the power is reduced by one more.',rf'D^{{{j}}}x^{{{k}}}={S.latex(S.diff(x**k,x,j))}') for j in range(1,k+1)])
    if section=='4.6' and mode==2:
        trial=A*x*S.exp(x)
        before('Substitute into',[st('Differentiate the trial using the product rule.',rf'y_p\prime={S.latex(S.diff(trial,x))}'),st('Differentiate each product once more.',rf'y_p\prime\prime={S.latex(S.diff(trial,x,2))}'),st('Subtract the trial from its second derivative; the Ax eˣ terms cancel.',r'y_p\prime\prime-y_p=2Ae^x'),st('Cancel eˣ and divide both sides by 2.',rf'2A={k}\Rightarrow A=\frac{{{k}}}2')])
    if section=='6.1':
        before('Use y=x' if mode in [0,2] else 'Form the auxiliary',[st('Differentiate the power trial once.',r'y=x^r,\quad y\prime=rx^{r-1}'),st('Differentiate again using the power rule.',r'y\prime\prime=r(r-1)x^{r-2}'),st('The coefficient powers make all three terms multiples of xʳ.',r'x^2y\prime\prime=r(r-1)x^r,\quad xy\prime=rx^r'),st('Divide by xʳ, which is nonzero for x>0, to obtain the auxiliary polynomial.')])
    if section=='6.2' and mode==0:
        before('Evaluate k',[st(f'For n={j}, evaluate the numerator and factorial separately.',rf'c_{{{j}}}=\frac{{{k}^{{{j}}}}}{{{j}!}}=\frac{{{k**j}}}{{{S.factorial(j)}}}={S.latex(S.Rational(k**j,S.factorial(j)))}') for j in range(4)])
    if section=='6.2' and mode==2:
        before('Shift the derivative',[st('Write the assumed series explicitly.',r'y=\sum_{n=0}^\infty c_nx^n'),st('Differentiate each term; the n=0 term vanishes.',r'y\prime=\sum_{n=1}^\infty nc_nx^{n-1}'),st('Reindex so the first exponent is zero.',r'y\prime=\sum_{n=0}^\infty(n+1)c_{n+1}x^n'),st('Write the right side with matching exponents.',rf'{k}y=\sum_{{n=0}}^\infty {k}c_nx^n')])
        before('Start with c₀',[st('The initial condition gives c₀=1. Use the recurrence one index at a time.',rf'c_1={k}c_0={k}'),st('At n=1 divide by 2.',rf'c_2=\frac{{{k}c_1}}2=\frac{{{k*k}}}2'),st('At n=2 divide by 3; the accumulated denominator is 3!.',rf'c_3=\frac{{{k}c_2}}3=\frac{{{k**3}}}6')])
    if section=='7.1' and mode==0:
        before('Combine exponential',[st('Insert the function into the defining integral and combine exponents.',rf'F(s)=\int_0^\infty e^{{-(s+{k})t}}\,dt'),st('Integrate with a finite upper limit before taking a limit.',rf'F(s)=\lim_{{T\to\infty}}\left[\frac{{-e^{{-(s+{k})t}}}}{{s+{k}}}\right]_0^T'),st('For s+k>0 the upper-end exponential tends to zero; subtract the lower-end value.',rf'F(s)=0-\frac{{-1}}{{s+{k}}}=\frac1{{s+{k}}}')])
    if section=='7.1' and mode==1:
        power=k%3+1
        before('Repeated integration',[st('For the integral of tⁿ e⁻ˢᵗ, choose u=tⁿ and dv=e⁻ˢᵗdt.',r'du=nt^{n-1}dt,\quad v=-\frac{e^{-st}}s'),st('The boundary term is zero for n>0 and s>0, leaving a recurrence.',r'I_n=\frac ns I_{n-1},\quad I_0=\frac1s')]+[st(f'Reduce the power from {j} to {j-1}.',rf'I_{{{j}}}=\frac{{{j}}}s I_{{{j-1}}}=\frac{{{S.factorial(j)}}}{{s^{{{j+1}}}}}') for j in range(1,power+1)])
    if section=='7.1' and mode==2:
        before('Integrating the sine',[st('Use integration by parts with u=sin(kt), dv=e⁻ˢᵗdt; the sine endpoint term is zero.',rf'I=\frac{{{k}}}s J,\quad J=\int_0^\infty e^{{-st}}\cos({k}t)\,dt'),st('Integrate J by parts; the lower-end cosine contributes 1/s.',rf'J=\frac1s-\frac{{{k}}}s I'),st('Substitute J back into I.',rf'I=\frac{{{k}}}{{s^2}}-\frac{{{k*k}}}{{s^2}}I'),st('Collect the I terms, multiply by s², and divide.',rf'(s^2+{k*k})I={k}\Rightarrow I=\frac{{{k}}}{{s^2+{k*k}}}')])
    if section=='7.2' and mode==2:
        before('Decompose into',[st('Assign unknown constants to the two distinct factors.',rf'\frac1{{(s+{k})(s+{k+1})}}=\frac A{{s+{k}}}+\frac B{{s+{k+1}}}'),st('Multiply through by the common denominator.',rf'1=A(s+{k+1})+B(s+{k})'),st('Set s to the first root so the B term vanishes.',rf's=-{k}\Rightarrow 1=A'),st('Set s to the second root so the A term vanishes.',rf's=-{k+1}\Rightarrow 1=-B\Rightarrow B=-1')])
        assert S.simplify(1/((s+k)*(s+k+1))-(1/(s+k)-1/(s+k+1)))==0
    if section=='7.3' and mode==2:
        before('Differentiate and negate',[st('Write the transform as a negative power and use the chain rule.',rf'F(s)=(s+{k})^{{-1}}'),st('The derivative of the inner expression is 1.',rf'F\prime(s)=-(s+{k})^{{-2}}'),st('Negate the derivative as required by the transform identity.',rf'-F\prime(s)=\frac1{{(s+{k})^2}}')])
    if section=='7.4' and mode==0:
        before('Simplify',[st('Insert the known F(s) into the derivative identity.',rf'\mathcal L\{{f\prime\}}=\frac{{{k}s}}{{s+1}}-{k}'),st('Give both terms the same denominator.',rf'\mathcal L\{{f\prime\}}=\frac{{{k}s-{k}(s+1)}}{{s+1}}'),st('Expand the numerator and cancel the s terms.',rf'{k}s-{k}s-{k}=-{k}')])
    if section=='7.5' and mode in [0,1]:
        factor='s+2' if mode==0 else 's^2+1'
        before('Solve the algebraic' if mode==0 else 'Isolate the transform',[st('Move the initial-value term to the right side.',rf'({factor})Y={k}'),st('Divide both sides by the full coefficient of Y.',rf'Y=\frac{{{k}}}{{{factor}}}')])
    if section=='8.3' and mode==2:
        before('Integrate and apply',[st('Integrate the product derivative on the left.',r'e^ty=\int2e^{2t}\,dt'),st('The exponential integral is e²ᵗ because its derivative is 2e²ᵗ.',r'e^ty=e^{2t}+C'),st('Divide through by the integrating factor eᵗ.',r'y=e^t+Ce^{-t}'),st('Insert t=0 into the initial condition.',rf'{k}=1+C\Rightarrow C={k-1}')])
    expanded=[]
    for step in problem['solutionSteps']:
        for needle,steps in additions.items():
            if step['text'].startswith(needle):expanded+=steps
        expanded.append(step)
    problem['solutionSteps']=expanded
    return problem
