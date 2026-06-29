import { useAuth } from '../../auth/useAuth'
import './Incoming.css'

export function Incoming() {
  const { user, signOut } = useAuth()

  return (
    <div className="incoming-page">
      <h1>Chào, {user?.username}!</h1>
      <p>Trang gợi ý món ăn (/reels) đang được phát triển.</p>
      <button className="btn btn-secondary" onClick={signOut}>
        Đăng xuất
      </button>
    </div>
  )
}
