import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import { getDish, getRecommendedDishIds } from '../../api/client'

const PAGE_SIZE = 10
const PREFETCH_THRESHOLD = 3
const CACHE_BEHIND = 3

function preloadImage(url) {
  if (!url) return
  const img = new Image()
  img.src = url
}

export function useDishFeed() {
  const [dishIds, setDishIds] = useState([])
  const [currentIndex, setCurrentIndex] = useState(0)
  const [dishCache, setDishCache] = useState(new Map())
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const nextPageRef = useRef(1)
  const fetchingIdsRef = useRef(new Set())
  const idsPageLoadingRef = useRef(false)

  const fetchDish = useCallback(async (dishId) => {
    if (dishCache.has(dishId) || fetchingIdsRef.current.has(dishId)) return
    fetchingIdsRef.current.add(dishId)
    try {
      const dish = await getDish(dishId)
      setDishCache((prev) => {
        const next = new Map(prev)
        next.set(dishId, dish)
        return next
      })
      preloadImage(dish.image_urls?.[0])
    } catch {
      // ignore individual dish fetch failures; UI will just keep showing a loading state for it
    } finally {
      fetchingIdsRef.current.delete(dishId)
    }
  }, [dishCache])

  const loadMoreIds = useCallback(async () => {
    if (idsPageLoadingRef.current) return
    idsPageLoadingRef.current = true
    try {
      const data = await getRecommendedDishIds(nextPageRef.current, PAGE_SIZE)
      nextPageRef.current += 1
      setDishIds((prev) => [...prev, ...data.ids])
    } catch {
      setError('Không thể tải thêm món ăn')
    } finally {
      idsPageLoadingRef.current = false
    }
  }, [])

  useEffect(() => {
    let cancelled = false
    async function init() {
      setLoading(true)
      try {
        const data = await getRecommendedDishIds(1, PAGE_SIZE)
        nextPageRef.current = 2
        if (!cancelled) setDishIds(data.ids)
      } catch {
        if (!cancelled) setError('Không thể tải danh sách món ăn')
      } finally {
        if (!cancelled) setLoading(false)
      }
    }
    init()
    return () => {
      cancelled = true
    }
  }, [])

  useEffect(() => {
    if (dishIds.length === 0) return

    async function syncFeedWindow() {
      const currentId = dishIds[currentIndex]
      if (currentId != null) await fetchDish(currentId)

      const nextId = dishIds[currentIndex + 1]
      if (nextId != null) await fetchDish(nextId)

      if (dishIds.length - currentIndex <= PREFETCH_THRESHOLD) {
        await loadMoreIds()
      }
    }

    syncFeedWindow()
  }, [dishIds, currentIndex, fetchDish, loadMoreIds])

  // Dishes more than CACHE_BEHIND positions behind the current one are dropped from view
  // without a separate effect, since this is pure derived state from dishIds/currentIndex.
  const visibleDishCache = useMemo(() => {
    const keepFrom = Math.max(currentIndex - CACHE_BEHIND, 0)
    const visibleIds = new Set(dishIds.slice(keepFrom))
    const next = new Map()
    for (const id of visibleIds) {
      if (dishCache.has(id)) next.set(id, dishCache.get(id))
    }
    return next
  }, [dishCache, dishIds, currentIndex])

  const goNext = useCallback(() => {
    setCurrentIndex((idx) => (idx + 1 < dishIds.length ? idx + 1 : idx))
  }, [dishIds.length])

  const goPrev = useCallback(() => {
    setCurrentIndex((idx) => (idx > 0 ? idx - 1 : idx))
  }, [])

  const currentDishId = dishIds[currentIndex]
  const currentDish = currentDishId != null ? visibleDishCache.get(currentDishId) : undefined

  return {
    currentDish,
    currentIndex,
    hasNext: currentIndex + 1 < dishIds.length,
    hasPrev: currentIndex > 0,
    goNext,
    goPrev,
    loading: loading && dishIds.length === 0,
    error,
  }
}
