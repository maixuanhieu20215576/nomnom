import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { login, ApiError } from '../../api/client'
import { useAuth } from '../../auth/useAuth'
import { AuthDialog } from './AuthDialog'
import './Login.css'

export function Login() {
  const navigate = useNavigate()
  const { signIn } = useAuth()
  const [dialogOpen, setDialogOpen] = useState(false)
  const [guestLoading, setGuestLoading] = useState(false)
  const [guestError, setGuestError] = useState('')

  function handleAuthSuccess(user, accessToken) {
    signIn(user, accessToken)
    setDialogOpen(false)
    navigate('/reels', { replace: true })
  }

  async function handleGuestBrowse() {
    setGuestLoading(true)
    setGuestError('')
    try {
      const data = await login({ is_guest: true })
      signIn(data.user, data.access_token)
      navigate('/reels', { replace: true })
    } catch (err) {
      setGuestError(err instanceof ApiError ? err.message : 'Không thể kết nối tới server')
    } finally {
      setGuestLoading(false)
    }
  }

  return (
    <div className="login-page">
      <div className="login-brand">
        <div className="login-brand-logo">🍗</div>
        <h1>NomNom</h1>
        <p>Khám phá món ăn dành riêng cho bạn</p>
      </div>

      <div className="login-actions">
        {guestError && <p className="error-text">{guestError}</p>}
        <button className="btn btn-primary" onClick={() => setDialogOpen(true)}>
          Đăng nhập
        </button>
        <button className="btn btn-secondary" onClick={handleGuestBrowse} disabled={guestLoading}>
          {guestLoading ? 'Đang vào...' : 'Duyệt ẩn danh'}
        </button>
      </div>

      {dialogOpen && (
        <AuthDialog onClose={() => setDialogOpen(false)} onSuccess={handleAuthSuccess} />
      )}
    </div>
  )
}
