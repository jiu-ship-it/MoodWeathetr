const DEV_BASE_URL = "http://127.0.0.1:5000";

// 在 Vercel 中可通过环境变量覆盖后端地址
const PROD_BASE_URL = process.env.VUE_APP_API_BASE_URL || "https://your-backend.railway.app";

export const BASE_URL = process.env.NODE_ENV === "production" ? PROD_BASE_URL : DEV_BASE_URL;
