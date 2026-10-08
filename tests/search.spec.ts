import {test,expect} from '@playwright/test';

for(const width of [320,620,1440]){
 test(`scrollable live suggestions and prerequisite cards at ${width}px`,async({page})=>{
  await page.setViewportSize({width,height:900});
  await page.goto('/search');
  const input=page.getByRole('combobox',{name:'Search all lesson content'});
  await input.fill('m');
  const list=page.getByRole('listbox',{name:'Search suggestions'});
  await expect(list).toBeVisible();
  expect(await list.getByRole('option').count()).toBeGreaterThan(4);
  expect(await list.evaluate(el=>el.scrollHeight>el.clientHeight)).toBe(true);
  const bounds=await list.boundingBox();
  expect(bounds!.x).toBeGreaterThanOrEqual(0);
  expect(bounds!.x+bounds!.width).toBeLessThanOrEqual(width);
  await list.hover();
  await page.mouse.wheel(0,450);
  await expect.poll(()=>list.evaluate(el=>el.scrollTop)).toBeGreaterThan(0);
  await expect(list).toBeVisible();
  await input.press('ArrowUp');
  const last=list.getByRole('option').last();
  await expect(last).toHaveAttribute('aria-selected','true');
  const destination=await last.getAttribute('href');
  await input.press('Enter');
  await expect(page).toHaveURL(new RegExp(`${destination}$`));
  await page.goto('/lessons/linear-algebra-6-4');
  const prerequisites=page.getByRole('region',{name:'Recommended prerequisites'});
  await prerequisites.scrollIntoViewIfNeeded();
  await expect(prerequisites).toBeVisible();
  expect(await prerequisites.getByRole('link').count()).toBeGreaterThan(0);
  expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);
  await page.screenshot({path:`/tmp/mathpath-prerequisites-${width}.png`});
  const first=prerequisites.getByRole('link').first();
  const prerequisiteUrl=await first.getAttribute('href');
  await first.click();
  await expect(page).toHaveURL(new RegExp(`${prerequisiteUrl}$`));
 });
}

test('header and home suggestions open, clear, and navigate',async({page})=>{
 await page.setViewportSize({width:1440,height:1000});
 await page.goto('/');
 const header=page.locator('.desktop-search');
 const input=header.getByRole('combobox');
 await input.fill('eigen');
 await header.getByRole('option',{name:/Eigenvalues and Eigenvectors/}).click();
 await expect(page).toHaveURL(/\/lessons\/eigenvalues$/);
 await page.goto('/');
 const hero=page.locator('.search-wrap.large');
 await hero.getByRole('combobox').fill('m');
 await expect(hero.getByRole('listbox')).toBeVisible();
 const dropdown=await hero.locator('.suggestions').boundingBox();
 expect(dropdown!.y).toBeGreaterThanOrEqual(0);
 expect(dropdown!.y+dropdown!.height).toBeLessThanOrEqual(1000);
 await page.screenshot({path:'/tmp/mathpath-search-desktop.png'});
 await hero.getByRole('combobox').press('Escape');
 await expect(hero.getByRole('listbox')).toHaveCount(0);
 await hero.getByRole('combobox').click();
 await hero.getByRole('button',{name:'Clear search input'}).click();
 await expect(hero.getByRole('combobox')).toBeFocused();
 await expect(hero.getByRole('combobox')).toHaveValue('');
 await hero.getByRole('combobox').fill('integrating factor');
 await hero.getByRole('link',{name:'See all results'}).click();
 await expect(page).toHaveURL(/\/search\?q=integrating%20factor$/);
 await expect(page.getByRole('combobox',{name:'Search all lesson content'})).toHaveValue('integrating factor');
});

test('page search handles no matches, outside clicks, and submission',async({page})=>{
 await page.goto('/search');
 const input=page.getByRole('combobox',{name:'Search all lesson content'});
 await input.fill('zzzzzz');
 await expect(page.locator('.suggestions-empty')).toBeVisible();
 await page.getByRole('heading',{level:1}).click();
 await expect(page.locator('.suggestions')).toHaveCount(0);
 await input.fill('matrix');
 await expect(page.getByRole('listbox')).toBeVisible();
 await input.press('Enter');
 await expect(page).toHaveURL(/\/search\?q=matrix$/);
 await expect(page.getByRole('listbox')).toHaveCount(0);
});
