// Split only at the current mathematical level: never inside a fraction,
// matrix, exponent, or paired delimiter.
export function splitMath(math:string,tokens:string[],keep=false):string[]{
 math=math.replace(/\\ +/g,' ');
 const parts:string[]=[];let start=0,braces=0,environments=0,fences=0,parens=0;
 for(let i=0;i<math.length;i++){
  const tail=math.slice(i);
  const environment=tail.match(/^\\(begin|end)\{[^}]+\}/);
  if(environment){environments+=environment[1]==='begin'?1:-1;i+=environment[0].length-1;continue;}
  if(/^\\left(?![a-zA-Z])/.test(tail)){fences++;i+=5;continue;}
  if(/^\\right(?![a-zA-Z])/.test(tail)){fences--;i+=6;continue;}
  if(math[i]==='{'&&math[i-1]!=='\\')braces++;
  if(math[i]==='}'&&math[i-1]!=='\\')braces--;
  if(!fences&&math[i]==='(')parens++;
  if(!fences&&math[i]===')')parens--;
  if(braces||environments||fences||parens)continue;
  const token=tokens.find(t=>tail.startsWith(t));
  if(!token)continue;
  if(token.length===1&&math[i-1]==='\\')continue;
  if((token==='+'||token==='-')&&['_','^'].includes(math[i-1]))continue;
  // A leading sign or operator belongs to this line.
  if(!math.slice(start,i).trim()){if(!keep)start=i+token.length;i+=token.length-1;continue;}
  parts.push(math.slice(start,i).trim());start=keep?i:i+token.length;i+=token.length-1;
 }
 parts.push(math.slice(start).trim());return parts.filter(Boolean);
}

const separators=['\\qquad','\\quad',';',',',':'];
const relations=['\\Longrightarrow','\\Rightarrow','\\Longleftrightarrow','\\iff','\\longrightarrow','\\rightarrow','\\leftrightarrow','\\leftarrow','\\le','\\ge','='];
export function verticalMath(math:string):string[]{
 math=math.replace(/\\(?:big|Big|bigg|Bigg)[lr]?([()[\]])/g,(_command,delimiter)=>['(','['].includes(delimiter)?'\\left'+delimiter:'\\right'+delimiter);
 return splitMath(math,separators).flatMap(part=>{
  // Each equality or implication gets its own continuation line.
  const lines=splitMath(part,relations,true);
  return lines.map(line=>stackLists(line));
 });
}

function stackLists(math:string):string{
 // A tuple or set stays enclosed in its original delimiters, with its
 // entries arranged vertically rather than spread across one long row.
 const fences=/\\(left|right)(\\[{}]|[()[\]{}.|])/g;let output='',cursor=0;
 let first:RegExpExecArray|null;
 while((first=fences.exec(math))){
  if(first[1]!=='left')continue;
  let depth=1,last:RegExpExecArray|null=null,next:RegExpExecArray|null;
  while((next=fences.exec(math))){depth+=next[1]==='left'?1:-1;if(depth===0){last=next;break;}}
  if(!last)break;
  const body=math.slice(first.index+first[0].length,last.index);const entries=splitMath(body,[',']);
  output+=math.slice(cursor,first.index)+first[0]+(entries.length>1?`\\begin{gathered}${entries.map(stackLists).join('\\\\')}\\end{gathered}`:stackLists(body))+last[0];
  cursor=last.index+last[0].length;
 }
 return output+math.slice(cursor);
}

export type MathExpansion={lines:string[];definitions?:{label:string;lines:string[]}[]};
export function expandWideMath(math:string,level=1):MathExpansion|null{
 const grouped=verticalMath(math);
 if(grouped.length>1||grouped[0]!==math)return {lines:grouped};
 const relationsAndTerms=splitMath(math,[...relations,'+','-'],true);
 if(relationsAndTerms.length>1)return {lines:relationsAndTerms};

 // Wide matrices retain every entry and its position. The expression uses
 // a local matrix name, followed by one indexed entry per line.
 const definitions:{label:string;lines:string[]}[]=[];
 const named=math.replace(/\\begin\{(bmatrix|pmatrix|matrix|vmatrix|array)\}(?:\{([lcr|]+)\})?([\s\S]*?)\\end\{\1\}/g,(_original,kind,columns,body)=>{
  const number=definitions.length+1;const rows=body.split('\\\\').map((row:string)=>row.trim()).filter(Boolean);
  const entries=rows.map((row:string)=>splitMath(row,['&']));
  const name=`M_{${number}}`;
  const lines=entries.flatMap((row:string[],i:number)=>row.map((entry,j)=>`(${name})_{${i+1},${j+1}}=${entry}`));
  const divider=columns?.includes('|')?` The augmented divider follows column ${columns.split('|')[0].length}.`:'';
  definitions.push({label:`Matrix M${number}: ${rows.length} rows × ${entries[0]?.length??0} columns.${divider}`,lines});
  return kind==='vmatrix'?` \\det ${name} `:` ${name} `;
 });
 if(definitions.length)return {lines:[named],definitions};


 const integral=math.match(/\\int((?:[_^](?:\{[^}]+\}|\\[a-zA-Z]+|[a-zA-Z0-9])){0,2})\s*([\s\S]+?)((?:\\[,;!])?\s*d\s*([a-z]))$/);
 if(integral){
  const name=String.raw`\mathsf{G}_{${level}}`;
  return {lines:[math.slice(0,integral.index)+String.raw`\int${integral[1]} ${name}\,d${integral[4]}`],definitions:[{label:`For this integral, G${level} is the integrand.`,lines:[name+'='+integral[2]]}]};
 }

 const cases=math.match(/\\begin\{cases\}([\s\S]*?)\\end\{cases\}/);
 if(cases){
  const lines=cases[1].split('\\\\').flatMap(row=>{
   const [value,condition]=row.split('&');return [String.raw`\text{When }${condition??''}`,String.raw`\mathsf{P}=${value.replace(/,$/,'')}`];
  });
  return {lines:[math.replace(cases[0],String.raw`\mathsf{P}`)],definitions:[{label:'Piecewise value P: select the value for the condition that holds.',lines}]};
 }

 // Name a long subexpression locally rather than squeeze it into one line.
 // Its complete definition follows immediately and can itself be reflowed.
 const tuples=math.replace(/\(([^()]*,[^()]*)\)\^T/g,(_all,body)=>`\\begin{bmatrix}${splitMath(body,[',']).join('\\\\')}\\end{bmatrix}`).replace(/\(([^()]*,[^()]*)\)/g,(_all,body)=>`\\left(\\begin{gathered}${splitMath(body,[',']).join('\\\\')}\\end{gathered}\\right)`);
 if(tuples!==math)return {lines:[tuples]};
 const group=findLongGroup(math);
 if(group){
  const name=String.raw`\mathsf{E}_{${level}}`;
  return {lines:[math.slice(0,group.start)+'{'+name+'}'+math.slice(group.end)],definitions:[{label:'For this expression, E denotes the following complete quantity.',lines:[name+'='+group.body]}]};
 }

 const factors=splitMath(math,['\\cdot','\\times'],true);
 if(factors.length>1)return {lines:factors};
 const determinants=splitMath(math,['\\det'],true);
 if(determinants.length>2)return {lines:determinants.map((part,i)=>i>1?'\\cdot '+part:part).filter(Boolean)};

 // Reflow long numerators, denominators, exponents, and parenthesized sums.
 const nested=wrapGroups(math);
 if(nested!==math)return {lines:[nested]};

 const text=math.replace(/\\text\{([^{}]+)\}/g,(original,body)=>{
  const words=body.trim().split(/\s+/);if(words.length<4)return original;
  const rows=[];for(let i=0;i<words.length;i+=3)rows.push(`\\text{${words.slice(i,i+3).join(' ')}}`);
  return `\\begin{gathered}${rows.join('\\\\')}\\end{gathered}`;
 });
 if(text!==math)return {lines:[text]};
 const textParts=splitMath(math,['\\text'],true);
 return textParts.length>1?{lines:textParts}:null;
}

function wrapGroups(math:string):string{
 let result='';
 for(let i=0;i<math.length;i++){
  if(math[i]!=='{'||math[i-1]==='\\'){result+=math[i];continue;}
  let end=i+1,depth=1;
  for(;end<math.length&&depth;end++){
   if(math[end]==='{'&&math[end-1]!=='\\')depth++;
   if(math[end]==='}'&&math[end-1]!=='\\')depth--;
  }
  const body=math.slice(i+1,end-1);
  const terms=splitMath(body,['+','-'],true);
  // Command names and short groups remain intact.
  result+='{'+(terms.length>1&&body.length>18?`\\begin{gathered}${terms.join('\\\\')}\\end{gathered}`:wrapGroups(body))+'}';i=end-1;
 }
 return result;
}


function findLongGroup(math:string):{start:number;end:number;body:string}|null{
 const left=/\\left(\\[{}]|[()[\]{}.|])/g;let match:RegExpExecArray|null;
 while((match=left.exec(math))){
  const fences=/\\(left|right)(\\[{}]|[()[\]{}.|])/g;fences.lastIndex=left.lastIndex;let level=1,next:RegExpExecArray|null;
  while((next=fences.exec(math))){level+=next[1]==='left'?1:-1;if(!level){
   const body=math.slice(left.lastIndex,next.index);
   if(body.length>8)return {start:match.index,end:next.index+next[0].length,body};break;
  }}
 }
 for(let start=0;start<math.length;start++){
  const opener=math[start];if(!['{','('].includes(opener)||math[start-1]==='\\')continue;
  if(opener==='('&&/\\(?:left|right)$/.test(math.slice(0,start)))continue;
  // These arguments are words or layout instructions, not quantities.
  if(opener==='{'&&/\\(?:text|operatorname|begin|end|mathsf)$/.test(math.slice(0,start))){
   let end=start+1,level=1;for(;end<math.length&&level;end++){if(math[end]==='{')level++;if(math[end]==='}')level--;}start=end-1;continue;
  }
  const close=opener==='{'?'}':')';let level=1,end=start+1;
  for(;end<math.length&&level;end++){
   if(math[end-1]==='\\')continue;
   if(math[end]===opener)level++;else if(math[end]===close)level--;
  }
  const body=math.slice(start+1,end-1);
  if(!level&&body.length>8)return {start:opener==='{'?start+1:start,end:opener==='{'?end-1:end,body};
 }
 return null;
}
