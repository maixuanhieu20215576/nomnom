import { AnimatePresence, motion } from 'framer-motion'
import { useEffect, useRef, useState } from 'react'
import { stopInteraction } from '../../api/client'
import { useIsMobile } from '../../hooks/useIsMobile'
import { DishCard } from './DishCard'
import { useDishFeed } from './useDishFeed'
import './Reels.css'

const SWIPE_THRESHOLD = 50

const dishVariants = {
  enter: (direction) => ({ y: direction > 0 ? '100%' : '-100%' }),
  center: { y: 0 },
  exit: (direction) => ({ y: direction > 0 ? '-100%' : '100%' }),
}

export function Reels() {
  const { currentDish, hasNext, hasPrev, goNext, goPrev, loading, error } = useDishFeed()
  const isMobile = useIsMobile()
  const dragStart = useRef(null)
  const viewingRef = useRef({ dishId: null, startedAt: null })
  const [imageIndex, setImageIndex] = useState(0)
  const [imageDirection, setImageDirection] = useState(1)
  const [renderedDishId, setRenderedDishId] = useState(currentDish?.id)
  const [direction, setDirection] = useState(1)

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
    setImageDirection(delta)
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
      if (deltaY > SWIPE_THRESHOLD && hasNext) {
        setDirection(1)
        goNext()
      } else if (deltaY < -SWIPE_THRESHOLD && hasPrev) {
        setDirection(-1)
        goPrev()
      }
    }
  }

  function handleGoNext() {
    setDirection(1)
    goNext()
  }

  function handleGoPrev() {
    setDirection(-1)
    goPrev()
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
      <AnimatePresence initial={false} custom={direction} mode="popLayout">
        {!loading && currentDish && (
          <motion.div
            key={currentDish.id}
            className="reels-dish-slide"
            custom={direction}
            variants={dishVariants}
            initial="enter"
            animate="center"
            exit="exit"
            transition={{ duration: 0.28, ease: 'easeInOut' }}
          >
            <DishCard
              dish={currentDish}
              imageIndex={imageIndex}
              imageDirection={imageDirection}
              onPrevImage={() => goToImage(-1)}
              onNextImage={() => goToImage(1)}
              hasPrevImage={imageIndex > 0}
              hasNextImage={imageIndex < images.length - 1}
            />
          </motion.div>
        )}
      </AnimatePresence>
      {!loading && !currentDish && !error && <p className="reels-status">Không có món ăn nào</p>}

      {!isMobile && (
        <div className="reels-dish-nav">
          <button
            className="dish-card-arrow-btn"
            onClick={handleGoPrev}
            disabled={!hasPrev}
            aria-label="Món trước"
          >
            ▲
          </button>
          <button
            className="dish-card-arrow-btn"
            onClick={handleGoNext}
            disabled={!hasNext}
            aria-label="Món tiếp theo"
          >
            ▼
          </button>
        </div>
      )}
    </div>
  )
}
