import React, { createContext, useContext, useState, useEffect } from 'react'

interface User {
  id: number
  username: string
  email: string
  first_name?: string
  last_name?: string
}

interface AuthContextType {
  user: User | null
  accessToken: string | null
  refreshToken: string | null
  login: (username: string, password: string) => Promise<void>
  register: (username: string, email: string, password: string, password2: string) => Promise<void>
  logout: () => void
  isAuthenticated: boolean
  isLoading: boolean
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api'

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [accessToken, setAccessToken] = useState<string | null>(localStorage.getItem('accessToken'))
  const [refreshToken, setRefreshToken] = useState<string | null>(localStorage.getItem('refreshToken'))
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    if (accessToken) {
      fetchUser()
    } else {
      setIsLoading(false)
    }
  }, [])

  const fetchUser = async () => {
    if (!accessToken) {
      setIsLoading(false)
      return
    }

    try {
      const response = await fetch(`${API_BASE}/auth/user/`, {
        headers: {
          'Authorization': `Bearer ${accessToken}`,
        },
      })

      if (response.ok) {
        const userData = await response.json()
        setUser(userData)
        setIsLoading(false)
      } else if (response.status === 401) {
        // Token might be expired, try to refresh
        await refreshAccessToken()
      } else {
        // Other error, clear auth
        logout()
        setIsLoading(false)
      }
    } catch (error) {
      console.error('Failed to fetch user:', error)
      logout()
      setIsLoading(false)
    }
  }

  const refreshAccessToken = async () => {
    if (!refreshToken) {
      logout()
      setIsLoading(false)
      return
    }

    try {
      const response = await fetch(`${API_BASE}/auth/token/refresh/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ refresh: refreshToken }),
      })

      if (response.ok) {
        const data = await response.json()
        setAccessToken(data.access)
        localStorage.setItem('accessToken', data.access)
        
        if (data.refresh) {
          setRefreshToken(data.refresh)
          localStorage.setItem('refreshToken', data.refresh)
        }
        
        // Try fetching user again with new token
        const userResponse = await fetch(`${API_BASE}/auth/user/`, {
          headers: {
            'Authorization': `Bearer ${data.access}`,
          },
        })

        if (userResponse.ok) {
          const userData = await userResponse.json()
          setUser(userData)
        } else {
          logout()
        }
      } else {
        logout()
      }
    } catch (error) {
      console.error('Failed to refresh token:', error)
      logout()
    } finally {
      setIsLoading(false)
    }
  }

  const login = async (username: string, password: string) => {
    const response = await fetch(`${API_BASE}/auth/login/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ username, password }),
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Login failed')
    }

    const data = await response.json()
    setAccessToken(data.access)
    setRefreshToken(data.refresh)
    localStorage.setItem('accessToken', data.access)
    localStorage.setItem('refreshToken', data.refresh)

    // Fetch user profile with the new token
    const userResponse = await fetch(`${API_BASE}/auth/user/`, {
      headers: {
        'Authorization': `Bearer ${data.access}`,
      },
    })

    if (userResponse.ok) {
      const userData = await userResponse.json()
      setUser(userData)
    } else {
      throw new Error('Failed to fetch user profile')
    }
  }

  const register = async (username: string, email: string, password: string, password2: string) => {
    const response = await fetch(`${API_BASE}/auth/register/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ username, email, password, password2 }),
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(Object.values(error).flat().join(' ') || 'Registration failed')
    }

    // Auto-login after registration
    await login(username, password)
  }

  const logout = () => {
    setUser(null)
    setAccessToken(null)
    setRefreshToken(null)
    localStorage.removeItem('accessToken')
    localStorage.removeItem('refreshToken')
  }

  const value = {
    user,
    accessToken,
    refreshToken,
    login,
    register,
    logout,
    isAuthenticated: !!user,
    isLoading,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
