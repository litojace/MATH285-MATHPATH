import {test,expect} from '@playwright/test';

for(const width of [320,1440]){
 test(`lesson navigation and back to top at ${width}px`,async({page})=>{
  await page.setViewportSize({width,height:900});
  await page.goto('/lessons/linear-algebra-1-1');
  const top=page.getByRole('button',{name:'Back to top',exact:true});
  await expect(top).toHaveCount(0);
  await page.evaluate(()=>window.scrollTo({top:1000,behavior:'instant'}));
  await expect(top).toBeVisible();
  const bounds=await top.boundingBox();
  expect(bounds!.x+bounds!.width).toBeLessThanOrEqual(width);
  expect(bounds!.y+bounds!.height).toBeLessThanOrEqual(900);
  await top.click();
  await expect.poll(()=>page.evaluate(()=>scrollY)).toBe(0);
  await expect(top).toHaveCount(0);
  await expect(page.locator('main')).toBeFocused();
  const adjacent=page.getByRole('navigation',{name:'Adjacent lessons'});
  await adjacent.getByRole('link',{name:/Next lesson/}).click();
  await expect(page).toHaveURL(/\/lessons\/systems$/);
  await expect.poll(()=>page.evaluate(()=>scrollY)).toBe(0);
  await expect(page.getByRole('heading',{level:1})).toBeInViewport();
  await adjacent.getByRole('link',{name:/Previous lesson/}).click();
  await expect(page).toHaveURL(/\/lessons\/linear-algebra-1-1$/);
  await expect.poll(()=>page.evaluate(()=>scrollY)).toBe(0);
 });
}

test('back to top respects reduced motion and preserves anchor navigation',async({page})=>{
 await page.emulateMedia({reducedMotion:'reduce'});
 await page.goto('/library');
 await page.getByRole('link',{name:'Source status'}).click();
 await expect(page).toHaveURL(/\/library#sources$/);
 await expect(page.locator('#sources')).toBeInViewport();
 await page.getByRole('button',{name:'Back to top',exact:true}).click();
 expect(await page.evaluate(()=>scrollY)).toBe(0);
 await expect(page.locator('main')).toBeFocused();
});
