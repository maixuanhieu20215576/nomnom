import { Navigate, Route, BrowserRouter, Routes } from 'react-router-dom'
import { AuthProvider } from './auth/AuthContext'
import { useAuth } from './auth/useAuth'
import { Login } from './pages/Login/Login'
import { Incoming } from './pages/Incoming/Incoming'
import { AdminLayout } from './pages/Admin/AdminLayout'
import { DishManagement } from './pages/Admin/DishManagement/DishManagement'

function RequireAuth({ children }) {
  const { user } = useAuth()
  if (!user) return <Navigate to="/login" replace />
  return children
}

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route
            path="/incoming"
            element={
              <RequireAuth>
                <Incoming />
              </RequireAuth>
            }
          />
          <Route path="/admin" element={<AdminLayout />}>
            <Route path="dishes" element={<DishManagement />} />
            <Route index element={<Navigate to="/admin/dishes" replace />} />
          </Route>
          <Route path="/" element={<Navigate to="/login" replace />} />
          <Route path="*" element={<Navigate to="/login" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  )
}

export default App
