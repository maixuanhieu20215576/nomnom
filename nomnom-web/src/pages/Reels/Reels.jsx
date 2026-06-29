import { useEffect, useRef, useState } from 'react'
import { stopInteraction } from '../../api/client'
import { DishCard } from './DishCard'
import { useDishFeed } from './useDishFeed'
import './Reels.css'

const SWIPE_THRESHOLD = 50

export function Reels() {
  const { currentDish, hasNext, hasPrev, goNext, goPrev, loading, error } = useDishFeed()
  const dragStart = useRef(null)
  const viewingRef = useRef({ dishId: null, startedAt: null })
  const [imageIndex, setImageIndex] = useState(0)
  const [renderedDishId, setRenderedDishId] = useState(currentDish?.id)

  const images = currentDish?.image_urls?.length ? currentDish.image_urls : [null]

  if (currentDish?.id !== renderedDishId) {
    setRenderedDishId(currentDish?.id)
    setImageIndex(0)
  }

  useEffect(() => {
    const dishId = currentDish?.id ?? null
    const previous = viewingRef.current

    if (previous.dishId != null && previous.dishId !== dishId) {
      const timeSpentOnPostMs = Date.now() - previous.startedAt
      stopInteraction(previous.dishId, timeSpentOnPostMs).catch(() => {})
    }

    viewingRef.current = { dishId, startedAt: Date.now() }
  }, [currentDish?.id])

  useEffect(() => {
    return () => {
      const { dishId, startedAt } = viewingRef.current
      if (dishId != null) {
        stopInteraction(dishId, Date.now() - startedAt).catch(() => {})
      }
    }
  }, [])

  function goToImage(delta) {
    setImageIndex((idx) => Math.min(Math.max(idx + delta, 0), images.length - 1))
  }

  function handleDragStart(clientX, clientY) {
    dragStart.current = { x: clientX, y: clientY }
  }

  function handleDragEnd(clientX, clientY) {
    if (dragStart.current == null) return
    const deltaX = dragStart.current.x - clientX
    const deltaY = dragStart.current.y - clientY
    dragStart.current = null

    if (Math.abs(deltaX) > Math.abs(deltaY)) {
      if (deltaX > SWIPE_THRESHOLD) goToImage(1)
      else if (deltaX < -SWIPE_THRESHOLD) goToImage(-1)
    } else {
      if (deltaY > SWIPE_THRESHOLD && hasNext) goNext()
      else if (deltaY < -SWIPE_THRESHOLD && hasPrev) goPrev()
    }
  }

  return (
    <div
      className="reels-page"
      onTouchStart={(e) => handleDragStart(e.touches[0].clientX, e.touches[0].clientY)}
      onTouchEnd={(e) => handleDragEnd(e.changedTouches[0].clientX, e.changedTouches[0].clientY)}
      onMouseDown={(e) => handleDragStart(e.clientX, e.clientY)}
      onMouseUp={(e) => handleDragEnd(e.clientX, e.clientY)}
    >
      {loading && <p className="reels-status">Đang tải...</p>}
      {!loading && error && !currentDish && <p className="reels-status">{error}</p>}
      {!loading && currentDish && (
        <DishCard
          key={currentDish.id}
          dish={currentDish}
          imageIndex={imageIndex}
          onPrevImage={() => goToImage(-1)}
          onNextImage={() => goToImage(1)}
          hasPrevImage={imageIndex > 0}
          hasNextImage={imageIndex < images.length - 1}
        />
      )}
      {!loading && !currentDish && !error && <p className="reels-status">Không có món ăn nào</p>}

      <div className="reels-dish-nav">
        <button
          className="dish-card-arrow-btn"
          onClick={goPrev}
          disabled={!hasPrev}
          aria-label="Món trước"
        >
          ▲
        </button>
        <button
          className="dish-card-arrow-btn"
          onClick={goNext}
          disabled={!hasNext}
          aria-label="Món tiếp theo"
        >
          ▼
        </button>
      </div>
    </div>
  )
}
