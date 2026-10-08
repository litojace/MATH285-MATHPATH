import {test,expect} from '@playwright/test';
import {readFileSync} from 'node:fs';
import type {Lesson} from '../src/types/content';
const curriculum=JSON.parse(readFileSync(new URL('../src/content/course-lessons.json',import.meta.url),'utf8')) as Lesson[];

for(const width of [320,1440]){
 test.describe(`${width}px curriculum`,()=>{
  test.use({viewport:{width,height:950}});
  test('shows the actual full course counts',async({page})=>{
   await page.goto('/');
   await expect(page.locator('.course-meta').filter({hasText:'27 lessons'})).toHaveCount(1);
   await expect(page.locator('.course-meta').filter({hasText:'24 lessons'})).toHaveCount(1);
   for(const [course,count] of [['linear-algebra',27],['differential-equations',24]] as const){
    await page.goto(`/courses/${course}`);
    await expect(page.locator('.curriculum-row')).toHaveCount(count);
    expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);
   }
  });
  for(const lesson of curriculum){
   test(`${lesson.courseId} ${lesson.section}: learn, practice, solutions`,async({page})=>{
    const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));
    await page.goto(`/lessons/${lesson.id}`);
    await expect(page.getByRole('heading',{level:1,name:lesson.title,exact:true})).toBeVisible();
    await expect(page.getByRole('button',{name:'Tutor mode',exact:true})).toHaveCount(0);
    if(lesson.methodGuide){
     const guide=page.getByRole('region',{name:'Detailed method guide'});
     await expect(guide.locator('.method-guide-part')).toHaveCount(3);
     await expect(page.locator('.source-references')).toContainText('LINEAR PROFESSOR V.pdf');
     await page.locator('details.example').evaluateAll(examples=>examples.forEach(example=>example.setAttribute('open','')));
     await expect(page.locator('.katex-error')).toHaveCount(0);
    }
    expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);
    await page.getByRole('button',{name:'Practice & solutions',exact:true}).click();
    await expect(page.locator('article.exercise')).toHaveCount(lesson.exercises.length);
    await expect(page.locator('.solution')).toHaveCount(0);
    const answered=lesson.exercises.find(e=>e.answerType==='numeric'||e.answerType==='matrix'||e.answerType==='multiple-choice');
    if(answered){
     const card=page.locator('article.exercise').nth(lesson.exercises.findIndex(e=>e.id===answered.id));
     if(answered.answerType==='multiple-choice'){
      await card.getByRole('radio',{name:String(answered.answer),exact:true}).check();
     }else{
      const answer=Array.isArray(answered.answer)?answered.answer.map(row=>row.join(',')).join(';'):String(answered.answer);
      await page.locator(`#${answered.id}`).fill(answer);
     }
     await card.getByRole('button',{name:'Check answer',exact:true}).click();
     await expect(card.getByRole('status')).toHaveClass(/success/);
    }
    await page.getByRole('button',{name:'Show Step-by-Step Solution',exact:true}).evaluateAll(buttons=>buttons.forEach(button=>(button as HTMLButtonElement).click()));
    await expect(page.locator('.solution')).toHaveCount(lesson.exercises.length);
    await expect(page.locator('.katex-error')).toHaveCount(0);
    expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);
    expect(errors).toEqual([]);
   });
  }
 });
}
