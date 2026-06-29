const API_BASE = '/api'
const TOKEN_STORAGE_KEY = 'nomnom_access_token'

export class ApiError extends Error {
  constructor(message, status) {
    super(message)
    this.status = status
  }
}

function authHeaders() {
  const token = localStorage.getItem(TOKEN_STORAGE_KEY)
  return token ? { Authorization: `Bearer ${token}` } : {}
}

function handleUnauthorized(status) {
  if (status === 401) {
    localStorage.removeItem(TOKEN_STORAGE_KEY)
    localStorage.removeItem('nomnom_user')
  }
}

async function request(path, options = {}) {
  const res = await fetch(`${API_BASE}${path}`, {
    method: options.method ?? 'GET',
    headers: { 'Content-Type': 'application/json', ...authHeaders() },
    body: options.body ? JSON.stringify(options.body) : undefined,
  })

  const data = await res.json().catch(() => null)

  if (!res.ok) {
    handleUnauthorized(res.status)
    throw new ApiError(data?.detail ?? 'Đã có lỗi xảy ra', res.status)
  }

  return data
}

async function requestFormData(path, formData) {
  const res = await fetch(`${API_BASE}${path}`, {
    method: 'POST',
    headers: authHeaders(),
    body: formData,
  })

  const data = await res.json().catch(() => null)

  if (!res.ok) {
    handleUnauthorized(res.status)
    throw new ApiError(data?.detail ?? 'Đã có lỗi xảy ra', res.status)
  }

  return data
}

export function login(payload) {
  return request('/auth/login', { method: 'POST', body: payload })
}

export function signUp(payload) {
  return request('/auth/sign-up', { method: 'POST', body: payload })
}

export function uploadImage(file) {
  const formData = new FormData()
  formData.append('file', file)
  return requestFormData('/images/upload', formData)
}

export function listDishes(page = 1, pageSize = 20) {
  return request(`/dishes?page=${page}&page_size=${pageSize}`)
}

export function getDish(dishId) {
  return request(`/dishes/${dishId}`)
}

export function createDish(payload) {
  return request('/dishes', { method: 'POST', body: payload })
}

export function getDishJob(jobId) {
  return request(`/dishes/jobs/${jobId}`)
}

export function getRecommendedDishIds(page = 1, pageSize = 10) {
  return request(`/dishes/recommended?page=${page}&page_size=${pageSize}`)
}

export function setReaction(dishId, reactioned) {
  return request('/reaction', { method: 'POST', body: { dish_id: dishId, reactioned } })
}

export function stopInteraction(dishId, timeSpentOnPostMs) {
  return request('/stop-interaction', {
    method: 'POST',
    body: { dish_id: dishId, time_spent_on_post_ms: timeSpentOnPostMs },
  })
}
