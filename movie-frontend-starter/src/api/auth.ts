import { useMutation } from "@tanstack/react-query";
import { api } from "./client";
import { z } from "zod";

const loginSchema = z.object({
  email: z.string().email(),
  password: z.string().min(6),
});
export type LoginInput = z.infer<typeof loginSchema>;

const signupSchema = z.object({
  name: z.string().min(1),
  last_name: z.string().min(1),
  phone_number: z.string().min(7),
  email: z.string().email(),
  password: z.string().min(6),
});
export type SignupInput = z.infer<typeof signupSchema>;

/** POST /login/ -> { id, name, last_name, email, phone_number, token } */
export function useLogin() {
  return useMutation({
    mutationFn: async (payload: LoginInput) => {
      const { data } = await api.post("/login/", payload);
      return data as {
        id: number;
        name: string;
        last_name: string;
        email: string;
        phone_number: string;
        token: string;
      };
    },
  });
}

/** POST /signup/ -> { id, name, last_name, phone_number, email } */
export function useSignup() {
  return useMutation({
    mutationFn: async (payload: SignupInput) => {
      const { data } = await api.post("/signup/", payload);
      return data as {
        id: number;
        name: string;
        last_name: string;
        phone_number: string;
        email: string;
      };
    },
  });
}

/** PATCH /me/ -> { id, name, last_name, email, phone_number } */
export function useUpdateMe() {
  return useMutation({
    mutationFn: async (
      payload: Partial<{
        name: string;
        last_name: string;
        phone_number: string;
      }>
    ) => {
      const { data } = await api.patch("/me/", payload);
      return data as {
        id: number;
        name: string;
        last_name: string;
        email: string;
        phone_number: string;
      };
    },
  });
}
