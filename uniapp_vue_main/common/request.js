import { BASE_URL } from "./config";

export function apiRequest(options) {
  const { url, method = "GET", data, header = {} } = options || {};
  const token = uni.getStorageSync("token");
  const finalHeader = {
    "Content-Type": "application/json",
    ...header
  };
  if (token) {
    finalHeader.Authorization = `Bearer ${token}`;
  }

  return new Promise((resolve, reject) => {
    uni.request({
      url: `${BASE_URL}${url}`,
      method,
      data,
      header: finalHeader,
      success: (res) => resolve(res),
      fail: (err) => reject(err)
    });
  });
}
