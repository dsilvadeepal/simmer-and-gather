import {defineConfig} from '@playwright/test';
export default defineConfig({testDir:'./tests',testMatch:'random-ux.spec.ts',timeout:180000,use:{channel:'chrome',baseURL:'http://127.0.0.1:5196'},webServer:{command:'npm run dev -- --port 5196',url:'http://127.0.0.1:5196',reuseExistingServer:false}});
