import { useState } from 'react'
import { setReaction } from '../../api/client'

function formatPrice(price) {
  if (price == null) return null
  return `${Number(price).toLocaleString('vi-VN')}đ`
}

export function DishCard({ dish, imageIndex, onPrevImage, onNextImage, hasPrevImage, hasNextImage }) {
  const [liked, setLiked] = useState(dish.reactioned ?? false)
  const [reacting, setReacting] = useState(false)
  const [captionExpanded, setCaptionExpanded] = useState(false)

  const images = dish.image_urls?.length ? dish.image_urls : [null]

  async function handleToggleLike() {
    if (reacting) return
    const nextLiked = !liked
    setLiked(nextLiked)
    setReacting(true)
    try {
      await setReaction(dish.id, nextLiked)
    } catch {
      setLiked(!nextLiked)
    } finally {
      setReacting(false)
    }
  }

  return (
    <div className="dish-card">
      <div className="dish-card-images">
        {images[imageIndex] ? (
          <img
            src={images[imageIndex]}
            alt={dish.name}
            className="dish-card-image"
            draggable={false}
            onDragStart={(e) => e.preventDefault()}
          />
        ) : (
          <div className="dish-card-image dish-card-image-placeholder" />
        )}

        {images.length > 1 && (
          <div className="dish-card-image-dots">
            {images.map((_, i) => (
              <span key={i} className={`dish-card-dot ${i === imageIndex ? 'active' : ''}`} />
            ))}
          </div>
        )}

        {images.length > 1 && (
          <div className="dish-card-image-nav">
            <button
              className="dish-card-arrow-btn"
              onClick={onPrevImage}
              disabled={!hasPrevImage}
              aria-label="Ảnh trước"
            >
              ◀
            </button>
            <button
              className="dish-card-arrow-btn"
              onClick={onNextImage}
              disabled={!hasNextImage}
              aria-label="Ảnh tiếp theo"
            >
              ▶
            </button>
          </div>
        )}
      </div>

      <div
        className="dish-card-info"
        onClick={() => dish.description && setCaptionExpanded(true)}
      >
        <h2 className="dish-card-name">{dish.name}</h2>
        <div className="dish-card-meta">
          {dish.avg_rating != null && (
            <span className="dish-card-meta-item">★ {Number(dish.avg_rating).toFixed(1)}</span>
          )}
          {formatPrice(dish.price) && (
            <span className="dish-card-meta-item">{formatPrice(dish.price)}</span>
          )}
          {dish.address_text && (
            <span className="dish-card-meta-item dish-card-address">📍 {dish.address_text}</span>
          )}
        </div>
        {dish.description && <p className="dish-card-description">{dish.description}</p>}
      </div>

      <button
        className={`dish-card-like ${liked ? 'liked' : ''}`}
        onClick={handleToggleLike}
        disabled={reacting}
        aria-label={liked ? 'Bỏ thích' : 'Thích'}
      >
        ♥
      </button>

      {captionExpanded && (
        <div className="dish-card-caption-overlay" onClick={() => setCaptionExpanded(false)}>
          <div className="dish-card-caption-sheet" onClick={(e) => e.stopPropagation()}>
            <h2 className="dish-card-name">{dish.name}</h2>
            <div className="dish-card-caption-text">{dish.description}</div>
            <button className="btn btn-secondary" onClick={() => setCaptionExpanded(false)}>
              Đóng
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
