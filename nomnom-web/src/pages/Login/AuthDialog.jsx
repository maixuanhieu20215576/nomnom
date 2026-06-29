import { useState } from 'react'
import { login, signUp, ApiError } from '../../api/client'

export function AuthDialog({ onClose, onSuccess }) {
  const [mode, setMode] = useState('login')
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  function switchMode(nextMode) {
    setMode(nextMode)
    setError('')
  }

  async function handleSubmit(e) {
    e.preventDefault()
    if (!username.trim() || !password) {
      setError('Vui lòng nhập đầy đủ thông tin')
      return
    }

    setLoading(true)
    setError('')
    try {
      const data =
        mode === 'login'
          ? await login({ is_guest: false, username, password })
          : await signUp({ username, password })
      onSuccess(data.user)
    } catch (err) {
      if (err instanceof ApiError) {
        setError(
          mode === 'login'
            ? 'Tên đăng nhập hoặc mật khẩu không đúng'
            : err.status === 409
              ? 'Tên đăng nhập đã được sử dụng'
              : err.message,
        )
      } else {
        setError('Không thể kết nối tới server')
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="dialog-overlay" onClick={onClose}>
      <div className="dialog-sheet" onClick={(e) => e.stopPropagation()}>
        <div className="dialog-header">
          <h2>{mode === 'login' ? 'Đăng nhập' : 'Đăng ký'}</h2>
          <button className="dialog-close" onClick={onClose} aria-label="Đóng">
            ×
          </button>
        </div>

        <form onSubmit={handleSubmit} className="auth-form">
          <div className="field">
            <label htmlFor="username">Tên người dùng</label>
            <input
              id="username"
              type="text"
              autoComplete="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              autoFocus
            />
          </div>

          <div className="field">
            <label htmlFor="password">Mật khẩu</label>
            <input
              id="password"
              type="password"
              autoComplete={mode === 'login' ? 'current-password' : 'new-password'}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>

          {error && <p className="error-text">{error}</p>}

          <div className="dialog-footer">
            <button type="submit" className="btn btn-primary" disabled={loading}>
              {loading ? 'Đang xử lý...' : mode === 'login' ? 'Đăng nhập' : 'Đăng ký'}
            </button>

            <p className="dialog-switch">
              {mode === 'login' ? (
                <>
                  Chưa có tài khoản?{' '}
                  <button type="button" className="btn-link" onClick={() => switchMode('signup')}>
                    Đăng ký
                  </button>
                </>
              ) : (
                <>
                  Đã có tài khoản?{' '}
                  <button type="button" className="btn-link" onClick={() => switchMode('login')}>
                    Đăng nhập
                  </button>
                </>
              )}
            </p>
          </div>
        </form>
      </div>
    </div>
  )
}
