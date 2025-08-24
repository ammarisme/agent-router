'use client'

import React, { createContext, useContext, useState, useEffect } from 'react'
import type { User, AuthSession } from '@/types/auth'

interface AuthContextType {
  user: User | null
  session: AuthSession | null
  isLoading: boolean
  signIn: (email: string, password: string) => Promise<void>
  signOut: () => Promise<void>
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [session, setSession] = useState<AuthSession | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  const signIn = async (email: string, password: string) => {
    // Authentication logic will be implemented here
    setIsLoading(true)
    try {
      // Sign in implementation
    } catch (error) {
      throw error
    } finally {
      setIsLoading(false)
    }
  }

  const signOut = async () => {
    // Sign out logic will be implemented here
    setUser(null)
    setSession(null)
  }

  useEffect(() => {
    // Initialize auth state
    setIsLoading(false)
  }, [])

  return (
    <AuthContext.Provider value={{ user, session, isLoading, signIn, signOut }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
