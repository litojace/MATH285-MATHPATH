import {defineConfig} from '@playwright/test';

export default defineConfig({
 testDir:'./tests',testMatch:'**/*.spec.ts',workers:2,fullyParallel:true,
 use:{baseURL:'http://127.0.0.1:5190',headless:true,
  launchOptions:{...(process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE?{executablePath:process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE}:{}),args:['--no-sandbox']}},
 webServer:{command:'npm run preview -- --port 5190 --strictPort',url:'http://127.0.0.1:5190',reuseExistingServer:!process.env.CI},
});
