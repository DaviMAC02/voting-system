import { create } from "zustand";
import type { User } from "@/lib/types";
import api from "@/lib/api";

interface AuthState {
  token: string | null;
  user: User | null;
  setToken: (token: string) => void;
  setUser: (user: User) => void;
  logout: () => void;
  initialize: () => Promise<void>;
}

export const useAuth = create<AuthState>((set) => ({
  token: localStorage.getItem("token"),
  user: null,
  setToken: (token) => {
    localStorage.setItem("token", token);
    set({ token });
  },
  setUser: (user) => set({ user }),
  logout: () => {
    localStorage.removeItem("token");
    set({ token: null, user: null });
  },
  initialize: async () => {
    const token = localStorage.getItem("token");
    if (token) {
      try {
        const { data: userData } = await api.get("/users/me");
        set({ token, user: userData }); // Make sure to set both token and user
        // eslint-disable-next-line @typescript-eslint/no-unused-vars
      } catch (error) {
        localStorage.removeItem("token");
        set({ token: null, user: null });
      }
    }
  },
}));
