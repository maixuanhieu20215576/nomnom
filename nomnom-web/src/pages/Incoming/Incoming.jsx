import { useNavigate } from 'react-router-dom'
import { useAuth } from '../../auth/useAuth'
import './Incoming.css'

export function Incoming() {
  const { user, signOut } = useAuth()
  const navigate = useNavigate()

  return (
    <div className="incoming-page">
      <h1>Chào, {user?.username}!</h1>
      <button className="btn btn-primary" onClick={() => navigate('/reels')}>
        Xem gợi ý món ăn
      </button>
      <button className="btn btn-secondary" onClick={signOut}>
        Đăng xuất
      </button>
    </div>
  )
}
