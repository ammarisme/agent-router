export interface User {
  id: string
  email: string
  name: string
  role: UserRole
  avatar?: string
  emailVerified: boolean
  createdAt: Date
  updatedAt: Date
}

export type UserRole = 'admin' | 'user'

export interface AuthSession {
  user: User
  expires: Date
}

export interface SignInCredentials {
  email: string
  password: string
  rememberMe?: boolean
}

export interface SignUpData {
  email: string
  password: string
  confirmPassword: string
  name: string
  acceptTerms: boolean
}

export interface AuthError {
  code: string
  message: string
  field?: string
}
