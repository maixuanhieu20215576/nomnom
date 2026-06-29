import { useRef, useState } from 'react'
import { createDish, uploadImage } from '../../../api/client'
import { AddressAutocomplete } from './AddressAutocomplete'
import { LocationPicker } from './LocationPicker'
import { SearchableSelect } from './SearchableSelect'
import './CreateDishDialog.css'

const MAX_IMAGES = 5

const MATERIAL_TAGS = ['pork', 'beef', 'chicken', 'duck', 'vegetables', 'noodle', 'seafood', 'rice', 'fish', 'fruit']
const TASTE_TAGS = ['spicy', 'sweet', 'bitter', 'neutral', 'salty', 'sour', 'savory', 'greasy']
const DISTRICTS = [
  'Đống Đa',
  'Hai Bà Trưng',
  'Cầu Giấy',
  'Hoàn Kiếm',
  'Ba Đình',
  'Tây Hồ',
  'Thanh Xuân',
  'Hoàng Mai',
  'Nam Từ Liêm',
  'Bắc Từ Liêm',
  'Hà Đông',
]
const COUNTRIES = [
  { value: 'viet', label: 'Việt Nam' },
  { value: 'thai', label: 'Thái Lan' },
  { value: 'korean', label: 'Hàn Quốc' },
  { value: 'europe', label: 'Châu Âu' },
  { value: 'japan', label: 'Nhật Bản' },
  { value: 'china', label: 'Trung Quốc' },
  { value: 'other', label: 'Khác' },
]

function toggleTag(list, tag) {
  return list.includes(tag) ? list.filter((t) => t !== tag) : [...list, tag]
}

export function CreateDishDialog({ onClose, onCreated }) {
  const fileInputRef = useRef(null)

  const [name, setName] = useState('')
  const [description, setDescription] = useState('')
  const [addressText, setAddressText] = useState('')
  const [district, setDistrict] = useState('')
  const [price, setPrice] = useState('')
  const [rating, setRating] = useState('5')
  const [country, setCountry] = useState('')
  const [materialTag, setMaterialTag] = useState([])
  const [tasteTag, setTasteTag] = useState([])
  const [latitude, setLatitude] = useState(null)
  const [longitude, setLongitude] = useState(null)

  const [images, setImages] = useState([]) // { previewUrl, objectName, uploading }
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState('')

  function handlePickLocation(lat, lng) {
    setLatitude(lat)
    setLongitude(lng)
  }

  function handleAddressSelect({ addressText: selectedAddress, latitude: lat, longitude: lng }) {
    setAddressText(selectedAddress)
    setLatitude(lat)
    setLongitude(lng)
  }

  async function handleFilesSelected(e) {
    const files = Array.from(e.target.files ?? [])
    e.target.value = ''
    const availableSlots = MAX_IMAGES - images.length
    const filesToUpload = files.slice(0, availableSlots)

    const pendingEntries = filesToUpload.map((file) => ({
      previewUrl: URL.createObjectURL(file),
      objectName: null,
      uploading: true,
    }))
    setImages((prev) => [...prev, ...pendingEntries])

    for (let i = 0; i < filesToUpload.length; i++) {
      const file = filesToUpload[i]
      const entry = pendingEntries[i]
      try {
        const data = await uploadImage(file)
        setImages((prev) =>
          prev.map((img) => (img === entry ? { ...img, objectName: data.object_name, uploading: false } : img)),
        )
      } catch {
        setImages((prev) => prev.filter((img) => img !== entry))
        setError(`Tải ảnh "${file.name}" thất bại`)
      }
    }
  }

  function removeImage(index) {
    setImages((prev) => prev.filter((_, i) => i !== index))
  }

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')

    if (!name.trim() || !description.trim()) {
      setError('Vui lòng nhập tên và mô tả món ăn')
      return
    }
    if (latitude == null || longitude == null) {
      setError('Vui lòng chọn vị trí trên bản đồ')
      return
    }
    if (images.some((img) => img.uploading)) {
      setError('Vui lòng chờ ảnh tải lên xong')
      return
    }

    setSubmitting(true)
    try {
      await createDish({
        name: name.trim(),
        description: description.trim(),
        address_text: addressText.trim() || null,
        district: district.trim() || null,
        price: price ? Number(price) : null,
        material_tag: materialTag.length ? materialTag : null,
        taste_tag: tasteTag.length ? tasteTag : null,
        country: country || null,
        location: { latitude, longitude },
        rating: Number(rating),
        image_object_names: images.map((img) => img.objectName),
      })
      onCreated()
    } catch {
      setError('Tạo món ăn thất bại, vui lòng thử lại')
      setSubmitting(false)
    }
  }

  return (
    <div className="cd-overlay" onClick={onClose}>
      <div className="cd-sheet" onClick={(e) => e.stopPropagation()}>
        <div className="cd-header">
          <h2>Thêm món ăn</h2>
          <button className="cd-close" onClick={onClose} aria-label="Đóng">
            ×
          </button>
        </div>

        <form onSubmit={handleSubmit} className="cd-grid">
          <div className="cd-field full">
            <label htmlFor="dish-name">Tên món ăn</label>
            <input id="dish-name" value={name} onChange={(e) => setName(e.target.value)} />
          </div>

          <div className="cd-field full">
            <label htmlFor="dish-desc">Mô tả</label>
            <textarea id="dish-desc" value={description} onChange={(e) => setDescription(e.target.value)} />
          </div>

          <div className="cd-field full">
            <label htmlFor="dish-address">Địa chỉ</label>
            <AddressAutocomplete
              value={addressText}
              onChange={setAddressText}
              onSelect={handleAddressSelect}
            />
          </div>

          <div className="cd-field">
            <label htmlFor="dish-district">Khu vực / Quận</label>
            <SearchableSelect
              id="dish-district"
              value={district}
              options={DISTRICTS}
              placeholder="Chọn quận..."
              onChange={setDistrict}
            />
          </div>

          <div className="cd-field">
            <label htmlFor="dish-price">Giá (VND)</label>
            <input
              id="dish-price"
              type="number"
              min="0"
              value={price}
              onChange={(e) => setPrice(e.target.value)}
            />
          </div>

          <div className="cd-field full">
            <label htmlFor="dish-rating">Đánh giá (1-5)</label>
            <input
              id="dish-rating"
              type="number"
              min="1"
              max="5"
              step="0.1"
              value={rating}
              onChange={(e) => setRating(e.target.value)}
            />
          </div>

          <div className="cd-field full">
            <label htmlFor="dish-country">Quốc gia</label>
            <select id="dish-country" value={country} onChange={(e) => setCountry(e.target.value)}>
              <option value="">Chọn quốc gia</option>
              {COUNTRIES.map((c) => (
                <option key={c.value} value={c.value}>
                  {c.label}
                </option>
              ))}
            </select>
          </div>

          <div className="cd-field full">
            <label>Nguyên liệu</label>
            <div className="cd-tag-group">
              {MATERIAL_TAGS.map((tag) => (
                <button
                  type="button"
                  key={tag}
                  className={`cd-tag-chip${materialTag.includes(tag) ? ' selected' : ''}`}
                  onClick={() => setMaterialTag((prev) => toggleTag(prev, tag))}
                >
                  {tag}
                </button>
              ))}
            </div>
          </div>

          <div className="cd-field full">
            <label>Vị</label>
            <div className="cd-tag-group">
              {TASTE_TAGS.map((tag) => (
                <button
                  type="button"
                  key={tag}
                  className={`cd-tag-chip${tasteTag.includes(tag) ? ' selected' : ''}`}
                  onClick={() => setTasteTag((prev) => toggleTag(prev, tag))}
                >
                  {tag}
                </button>
              ))}
            </div>
          </div>

          <div className="cd-field full">
            <label>Vị trí quán (click trên bản đồ để chọn)</label>
            <LocationPicker latitude={latitude} longitude={longitude} onChange={handlePickLocation} />
            {latitude != null && (
              <span className="cd-coords">
                Đã chọn: {latitude.toFixed(5)}, {longitude.toFixed(5)}
              </span>
            )}
          </div>

          <div className="cd-field full">
            <label>Hình ảnh (tối đa {MAX_IMAGES})</label>
            <div className="cd-images">
              {images.map((img, index) => (
                <div className="cd-image-slot" key={img.previewUrl}>
                  <img src={img.previewUrl} alt="" />
                  {img.uploading && <span className="cd-image-uploading">Đang tải...</span>}
                  <button type="button" className="cd-image-remove" onClick={() => removeImage(index)}>
                    ×
                  </button>
                </div>
              ))}
              {images.length < MAX_IMAGES && (
                <div className="cd-image-slot add" onClick={() => fileInputRef.current?.click()}>
                  +
                </div>
              )}
            </div>
            <input
              ref={fileInputRef}
              type="file"
              accept="image/*"
              multiple
              hidden
              onChange={handleFilesSelected}
            />
          </div>

          {error && <p className="cd-error">{error}</p>}

          <div className="cd-footer cd-field full">
            <button type="button" className="btn btn-secondary" onClick={onClose}>
              Hủy
            </button>
            <button type="submit" className="btn btn-primary" disabled={submitting}>
              {submitting ? 'Đang lưu...' : 'Lưu món ăn'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
