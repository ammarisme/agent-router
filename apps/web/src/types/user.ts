export interface UserProfile {
  id: string
  email: string
  name: string
  avatar?: string
  bio?: string
  location?: string
  website?: string
  createdAt: Date
  updatedAt: Date
}

export interface UserPreferences {
  theme: 'light' | 'dark' | 'system'
  language: string
  notifications: {
    email: boolean
    push: boolean
    sms: boolean
  }
}
