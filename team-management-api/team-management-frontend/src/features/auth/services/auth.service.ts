import api from "../../../api/axios";

import type {
    LoginRequest,
    RegisterRequest,
    AuthResponse,

} from "../types/auth.types"

export async function register(
    data: RegisterRequest
) {
    const response = await api.post(
        "auth/register",
        data
    );

    return response.data;
}

export async function login(
  data: LoginRequest
): Promise<AuthResponse> {

  const response = await api.post(
    "/auth/login",
    data
  );

  return response.data;
}
    
