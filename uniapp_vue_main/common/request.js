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

function tryParseJson(value) {
  if (typeof value !== "string") return value;
  try {
    return JSON.parse(value);
  } catch (e) {
    return value;
  }
}

export function normalizeApiResponse(res) {
  const statusCode = Number(res && res.statusCode) || 0;
  const raw = tryParseJson(res && res.data);
  const isWrapped = raw && typeof raw === "object" && Object.prototype.hasOwnProperty.call(raw, "code") && Object.prototype.hasOwnProperty.call(raw, "data");

  if (isWrapped) {
    return {
      ok: Number(raw.code) === 0,
      statusCode,
      message: raw.message || "",
      data: raw.data
    };
  }

  return {
    ok: statusCode >= 200 && statusCode < 300,
    statusCode,
    message: (raw && (raw.error || raw.message)) || "",
    data: raw
  };
}

export async function apiRequestUnified(options) {
  const res = await apiRequest(options);
  return normalizeApiResponse(res);
}
