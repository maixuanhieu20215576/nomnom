const API_BASE = '/api'

export class ApiError extends Error {
  constructor(message, status) {
    super(message)
    this.status = status
  }
}

async function request(path, options = {}) {
  const res = await fetch(`${API_BASE}${path}`, {
    method: options.method ?? 'GET',
    headers: { 'Content-Type': 'application/json' },
    body: options.body ? JSON.stringify(options.body) : undefined,
  })

  const data = await res.json().catch(() => null)

  if (!res.ok) {
    throw new ApiError(data?.detail ?? 'Đã có lỗi xảy ra', res.status)
  }

  return data
}

async function requestFormData(path, formData) {
  const res = await fetch(`${API_BASE}${path}`, {
    method: 'POST',
    body: formData,
  })

  const data = await res.json().catch(() => null)

  if (!res.ok) {
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
