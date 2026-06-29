import { useCallback, useEffect, useState } from 'react'
import { listDishes } from '../../../api/client'
import { CreateDishDialog } from './CreateDishDialog'
import './DishManagement.css'

const PAGE_SIZE = 20

const COUNTRY_LABELS = {
  viet: 'Việt Nam',
  thai: 'Thái Lan',
  korean: 'Hàn Quốc',
  europe: 'Châu Âu',
  japan: 'Nhật Bản',
  china: 'Trung Quốc',
  other: 'Khác',
}

function formatPrice(price) {
  if (price == null) return '—'
  return `${Number(price).toLocaleString('vi-VN')}đ`
}

export function DishManagement() {
  const [dishes, setDishes] = useState([])
  const [total, setTotal] = useState(0)
  const [page, setPage] = useState(1)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [dialogOpen, setDialogOpen] = useState(false)

  const loadDishes = useCallback(async (targetPage) => {
    setError('')
    try {
      const data = await listDishes(targetPage, PAGE_SIZE)
      setDishes(data.items)
      setTotal(data.total)
      setPage(data.page)
    } catch {
      setError('Không thể tải danh sách món ăn')
    } finally {
      setLoading(false)
    }
  }, [])

  const goToPage = useCallback(
    (targetPage) => {
      setLoading(true)
      loadDishes(targetPage)
    },
    [loadDishes],
  )

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect -- initial fetch on mount
    goToPage(1)
  }, [goToPage])

  function handleCreated() {
    setDialogOpen(false)
    goToPage(1)
  }

  const totalPages = Math.max(1, Math.ceil(total / PAGE_SIZE))

  return (
    <div>
      <div className="admin-page-header">
        <h2>Quản lý món ăn</h2>
        <button className="btn btn-primary btn-inline" onClick={() => setDialogOpen(true)}>
          + Thêm món ăn
        </button>
      </div>

      <div className="dish-table-wrapper">
        {loading ? (
          <div className="empty-state">Đang tải...</div>
        ) : error ? (
          <div className="empty-state">{error}</div>
        ) : dishes.length === 0 ? (
          <div className="empty-state">Chưa có món ăn nào. Hãy thêm món đầu tiên.</div>
        ) : (
          <table className="dish-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Tên món</th>
                <th>Khu vực</th>
                <th>Quốc gia</th>
                <th>Giá</th>
                <th>Đánh giá TB</th>
                <th>Ngày tạo</th>
              </tr>
            </thead>
            <tbody>
              {dishes.map((dish) => (
                <tr key={dish.id}>
                  <td>{dish.id}</td>
                  <td>{dish.name}</td>
                  <td>{dish.district ?? dish.address_text ?? '—'}</td>
                  <td>{dish.country ? COUNTRY_LABELS[dish.country] : '—'}</td>
                  <td>{formatPrice(dish.price)}</td>
                  <td>{dish.avg_rating ?? '—'}</td>
                  <td>{new Date(dish.created_at).toLocaleDateString('vi-VN')}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {!loading && !error && dishes.length > 0 && (
        <div className="pagination">
          <span>
            Trang {page} / {totalPages} ({total} món)
          </span>
          <button disabled={page <= 1} onClick={() => goToPage(page - 1)}>
            Trước
          </button>
          <button disabled={page >= totalPages} onClick={() => goToPage(page + 1)}>
            Sau
          </button>
        </div>
      )}

      {dialogOpen && (
        <CreateDishDialog onClose={() => setDialogOpen(false)} onCreated={handleCreated} />
      )}
    </div>
  )
}
