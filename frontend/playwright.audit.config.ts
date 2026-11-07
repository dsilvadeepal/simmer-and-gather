import {defineConfig} from '@playwright/test';
export default defineConfig({
 testDir:'./tests',testMatch:'architecture-audit.spec.ts',
 use:{...(process.env.CHROME_PATH?{launchOptions:{executablePath:process.env.CHROME_PATH}}:{}),baseURL:'http://127.0.0.1:5194'},
 webServer:{command:'npm run dev -- --port 5194',url:'http://127.0.0.1:5194',reuseExistingServer:false}
});
