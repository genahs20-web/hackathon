import { api } from "./api";
import { clearTokens, setTokens } from "./storage";

export interface LoginResponse {
  access_token: string;
  refresh_token: string;
  expires_in: number;
}

export interface CurrentUser {
  customer_id: string;
  email: string;
  name: string;
  role: string;
}

export async function login(email: string, password: string): Promise<LoginResponse> {
  const response = await api.post<LoginResponse>("/auth/login", { email, password });
  setTokens(response.data.access_token, response.data.refresh_token);
  return response.data;
}

export async function register(email: string, password: string, name: string, organization?: string) {
  return api.post("/auth/register", { email, password, name, organization });
}

export async function getCurrentUser(): Promise<CurrentUser> {
  const response = await api.get<CurrentUser>("/auth/me");
  return response.data;
}

export function logout(): void {
  clearTokens();
  window.location.href = "/login";
}
