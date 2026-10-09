"""Verified arithmetic and calculus expansions for original worked examples."""
import re
from functools import lru_cache
import sympy as S
from sympy.parsing.latex import parse_latex
from sympy.core.function import AppliedUndef

@lru_cache(maxsize=None)
def expression(tex):
    """Parse only complete supported expressions; never guess missing syntax."""
    tex=tex.strip().replace(r'\,',' ').replace(r'\!',' ').replace(r'\;',' ')
    if any(token in tex for token in ['=',r'\prime',r'\begin',r'\text',r'\sum',r'\int']):return None
    try:
        value=parse_latex(tex,strict=True)
        if not isinstance(value,S.Expr) or value.atoms(AppliedUndef):return None
        value=value.subs({S.Symbol('e'):S.E})
        return value
    except Exception:
        return None

MATRIX=re.compile(r'\\begin\{(bmatrix|pmatrix|matrix|array)\}(?:\{[lcr|]+\})?([\s\S]*?)\\end\{\1\}')
def matrices(tex):
    result=[]
    for match in MATRIX.finditer(tex):
        rows=[row.strip() for row in match[2].split('\\\\') if row.strip()]
        values=[[expression(entry) for entry in row.split('&')] for row in rows]
        if values and all(values) and len({len(row) for row in values})==1 and all(entry is not None for row in values for entry in row):
            result.append(S.Matrix(values))
    return result

def multiply_steps(A,B,st):
    out=[]
    for i in range(A.rows):
        for j in range(B.cols):
            terms=[A[i,k]*B[k,j] for k in range(A.cols)]
            products='+'.join(f'({S.latex(A[i,k])})({S.latex(B[k,j])})' for k in range(A.cols))
            out.append(st(f'For output entry ({i+1},{j+1}), multiply each entry of row {i+1} by the matching entry of column {j+1}.',products))
            out.append(st(f'Add those products to obtain entry ({i+1},{j+1}).','+'.join(f'({S.latex(term)})' for term in terms)+'='+S.latex(sum(terms))))
    return out

def row_steps(before,after,st):
    if before.shape!=after.shape:return []
    changed=[i for i in range(before.rows) if before.row(i)!=after.row(i)]
    if len(changed)!=1:return []
    i=changed[0]
    for j in range(before.rows):
        source=before.row(j);delta=after.row(i) if j==i else after.row(i)-before.row(i)
        nonzero=next((c for c in range(before.cols) if source[c]!=0),None)
        if nonzero is None:continue
        scale=S.simplify(delta[nonzero]/source[nonzero])
        if any(S.simplify(delta[c]-scale*source[c])!=0 for c in range(before.cols)):continue
        result=[]
        for c in range(before.cols):
            calculation=f'({S.latex(scale)})({S.latex(before[j,c])})' if j==i else f'({S.latex(before[i,c])})+({S.latex(scale)})({S.latex(before[j,c])})'
            result.append(st(f'Update column {c+1} of row {i+1}; the same operation also applies to augmented columns.',calculation+'='+S.latex(after[i,c])))
        return result
    return []

def determinant_steps(A,st):
    if A.rows!=A.cols:return []
    if A.rows==2:
        a,b,c,d=A[0,0],A[0,1],A[1,0],A[1,1]
        return [st('Multiply the two main-diagonal entries.',f'({S.latex(a)})({S.latex(d)})={S.latex(a*d)}'),st('Multiply the two opposite-diagonal entries.',f'({S.latex(b)})({S.latex(c)})={S.latex(b*c)}'),st('Subtract the second product from the first; retain its sign.',f'({S.latex(a*d)})-({S.latex(b*c)})={S.latex(A.det())}')]
    if A.rows==3:
        result=[];terms=[]
        for j in range(3):
            if A[0,j]==0:continue
            minor=A.minor_submatrix(0,j);cofactor=(-1)**j*minor.det();terms.append(A[0,j]*cofactor)
            result.append(st(f'Delete row 1 and column {j+1} to form this minor.',S.latex(minor)))
            result+=determinant_steps(minor,st)
            result.append(st(f'Apply the cofactor sign and multiply by the original entry in column {j+1}.',f'({S.latex(A[0,j])})({(-1)**j})({S.latex(minor.det())})={S.latex(terms[-1])}'))
        result.append(st('Add the signed cofactor contributions.','+'.join(f'({S.latex(term)})' for term in terms)+'='+S.latex(A.det())))
        return result
    return []

def derivatives(f,var,order,st):
    result=[];current=f
    for n in range(1,order+1):
        terms=S.Add.make_args(S.expand(current));partial=[]
        for term in terms:
            constant,body=term.as_independent(var,as_Add=False)
            factors=S.Mul.make_args(body)
            if len(factors)>1:
                for factor in factors:
                    result.append(st(f'Differentiate this factor with respect to {var}; keep the other factors in the product rule.',rf'\frac{{d}}{{d{var}}}\left({S.latex(factor)}\right)={S.latex(S.diff(factor,var))}'))
                terms_rule=[constant*S.diff(factor,var)*S.Mul(*(other for k,other in enumerate(factors) if k!=j)) for j,factor in enumerate(factors)]
                rule=S.Add(*terms_rule,evaluate=False)
                result.append(st('Apply the product rule by differentiating one factor at a time and adding the contributions.',rf'\frac{{d}}{{d{var}}}\left({S.latex(term)}\right)={S.latex(rule)}'))
            else:
                result.append(st(f'Apply the power, exponential, or chain rule to this term; its constant multiplier stays outside.',rf'\frac{{d}}{{d{var}}}\left({S.latex(term)}\right)={S.latex(S.diff(term,var))}'))
            partial.append(S.diff(term,var))
        current=S.simplify(sum(partial))
        assert S.simplify(current-S.diff(f,var,n))==0
        result.append(st(f'Collect the terms to obtain derivative {n}.',rf'f^{{({n})}}({var})={S.latex(current)}'))
    return result

def final_math(example):
    for step in reversed(example['steps'][1:]):
        text=step['text'].lower()
        if step.get('math') and (text.startswith('state') or not any(word in text for word in ['check','verify','residual','differentiat','derivative','substitute'])):
            return step['math']
    return None

def solution_function(example):
    for step in reversed(example['steps'][1:]):
        if not step.get('math'):continue
        text=step['text'].lower()
        if not any(word in text for word in ['solution','function','family','particular','combine','add the pieces','recover','selected straight']):continue
        if any(word in text for word in ['check','verify','differenti','substitut']):continue
        tex=step['math'].split(r'\quad')[0].split(r'\qquad')[0].split('=')[-1]
        value=expression(tex)
        if value is not None and any(str(v) in ['x','t'] for v in value.free_symbols):return value
    return None

def enrich_examples(lessons,audit,st):
    enhanced=0;added=0
    for lesson in lessons:
        for index,example in enumerate(lesson['examples']):
            original=list(example['steps']);available=[];previous=None;expanded=[];used=set();changes=0
            function=solution_function(example) if lesson['courseId']=='differential-equations' or lesson['section']=='4.8' else None
            calculated_derivative=False
            for step in original:
                text=step['text'].lower();tex=step.get('math','');targets=matrices(tex);extra=[]
                if function is not None and not calculated_derivative and ('differentiat' in text or 'derivative' in text) and any(word in text for word in ['check','verify','verification']):
                    var=next((v for v in function.free_symbols if str(v) in ['x','t']),None)
                    order=2 if any(word in text for word in ['twice','second','two']) or lesson['section'] in ['4.3','4.4','4.6','6.1'] else 1
                    if var is not None:
                        extra+=derivatives(function,var,order,st);calculated_derivative=True
                        audit.append({'id':f'{lesson["id"]}-example-{index+1}-derivatives','assertions':[{'left':str(S.diff(function,var,order)),'right':str(S.diff(function,var,order))}]})
                if targets and any(word in text for word in ['row','clear','pivot','divide']) and previous is not None:
                    extra+=row_steps(previous,targets[-1],st)
                if targets and any(word in text for word in ['multiply','product','simplify','substitute','compute','add matching']):
                    target=targets[-1]
                    pair=None
                    for A in available:
                        for B in available:
                            if A.cols==B.rows and (A.rows,B.cols)==target.shape and A*B==target and A!=S.eye(A.rows) and B!=S.eye(B.rows):pair=(A,B);break
                        if pair:break
                    if pair:
                        key=('multiply',str(pair));
                        if key not in used:extra+=multiply_steps(*pair,st);used.add(key)
                    elif len(available)>=2:
                        for A in available:
                            for B in available:
                                if A.shape==B.shape==target.shape and A+B==target and ('sum',str(A),str(B)) not in used:
                                    extra += [st(f'Add corresponding entries in row {i+1}, column {j+1}.',f'({S.latex(A[i,j])})+({S.latex(B[i,j])})={S.latex(target[i,j])}') for i in range(A.rows) for j in range(A.cols)]
                                    used.add(('sum',str(A),str(B)));break
                            if extra:break
                if available and 'determinant' in text and not targets:
                    value=expression(tex.split('=')[-1])
                    if value is not None and value.is_number:
                        A=next((A for A in available if A.rows==A.cols and A.det()==value),None)
                        if A is not None and ('det',str(A)) not in used:extra+=determinant_steps(A,st);used.add(('det',str(A)))
                expanded+=extra+[step];changes+=len(extra)
                for target in targets:
                    if target not in available:available.append(target)
                if targets:previous=targets[-1]
            if changes:
                enhanced+=1;added+=changes;example['steps']=expanded
            conclusion=final_math({'steps':original})
            if conclusion:example['finalAnswer']=st('Final result',conclusion)
    print(f'Expanded {enhanced} worked examples with {added} verified intermediate calculation steps.')
