import { useEffect, useState } from 'react'
import { AuthContext } from './auth-context'
const STORAGE_KEY = 'nomnom_user'
const TOKEN_STORAGE_KEY = 'nomnom_access_token'

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => {
    const raw = localStorage.getItem(STORAGE_KEY)
    return raw ? JSON.parse(raw) : null
  })
  const [accessToken, setAccessToken] = useState(() => localStorage.getItem(TOKEN_STORAGE_KEY))

  useEffect(() => {
    if (user) {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(user))
    } else {
      localStorage.removeItem(STORAGE_KEY)
    }
  }, [user])

  useEffect(() => {
    if (accessToken) {
      localStorage.setItem(TOKEN_STORAGE_KEY, accessToken)
    } else {
      localStorage.removeItem(TOKEN_STORAGE_KEY)
    }
  }, [accessToken])

  function signIn(nextUser, nextAccessToken) {
    setUser(nextUser)
    setAccessToken(nextAccessToken)
  }

  function signOut() {
    setUser(null)
    setAccessToken(null)
  }

  return (
    <AuthContext.Provider value={{ user, accessToken, signIn, signOut }}>
      {children}
    </AuthContext.Provider>
  )
}
