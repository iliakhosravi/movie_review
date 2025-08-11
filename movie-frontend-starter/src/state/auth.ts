import { create } from "zustand";

export type User = {
  id: number;
  name: string;
  last_name: string;
  email: string;
  phone_number: string;
};

type AuthState = {
  user: User | null;
  token: string | null;
  login: (payload: { user: User; token: string }) => void;
  logout: () => void;
  updateUser: (partial: Partial<User>) => void;
};

export const useAuthStore = create<AuthState>((set, get) => ({
  user: (() => {
    const raw = localStorage.getItem("user");
    return raw ? (JSON.parse(raw) as User) : null;
  })(),
  token: localStorage.getItem("token"),

  login: ({ user, token }) => {
    localStorage.setItem("user", JSON.stringify(user));
    localStorage.setItem("token", token);
    set({ user, token });
  },

  logout: () => {
    localStorage.removeItem("user");
    localStorage.removeItem("token");
    set({ user: null, token: null });
  },

  updateUser: (partial) => {
    const current = get().user;
    if (!current) return;
    const updated: User = { ...current, ...partial };
    localStorage.setItem("user", JSON.stringify(updated));
    set({ user: updated });
  },
}));
