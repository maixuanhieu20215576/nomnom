import { useEffect } from 'react'
import { NavLink, Outlet } from 'react-router-dom'
import './AdminLayout.css'

export function AdminLayout() {
  useEffect(() => {
    document.getElementById('root')?.classList.add('is-admin')
    return () => document.getElementById('root')?.classList.remove('is-admin')
  }, [])

  return (
    <div className="admin-shell">
      <aside className="admin-sidebar">
        <div className="admin-sidebar-brand">
          <div className="admin-sidebar-brand-icon">🍗</div>
          <h1>NomNom Admin</h1>
        </div>
        <nav className="admin-nav">
          <NavLink
            to="/admin/dishes"
            className={({ isActive }) => `admin-nav-link${isActive ? ' active' : ''}`}
          >
            Quản lý món ăn
          </NavLink>
        </nav>
      </aside>
      <main className="admin-main">
        <Outlet />
      </main>
    </div>
  )
}
