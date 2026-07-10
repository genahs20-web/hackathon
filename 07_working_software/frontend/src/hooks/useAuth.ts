import { useCallback, useEffect, useState } from "react";

import { type CurrentUser, getCurrentUser, login as loginRequest, logout as logoutRequest } from "../services/auth";
import { getAccessToken } from "../services/storage";

export function useAuth() {
  const [user, setUser] = useState<CurrentUser | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!getAccessToken()) {
      setLoading(false);
      return;
    }
    getCurrentUser()
      .then(setUser)
      .catch(() => setUser(null))
      .finally(() => setLoading(false));
  }, []);

  const login = useCallback(async (email: string, password: string) => {
    await loginRequest(email, password);
    const currentUser = await getCurrentUser();
    setUser(currentUser);
  }, []);

  const logout = useCallback(() => {
    setUser(null);
    logoutRequest();
  }, []);

  return { user, loading, isAuthenticated: Boolean(user), login, logout };
}
