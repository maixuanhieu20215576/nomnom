import { useRef, useState } from 'react'

const NOMINATIM_URL = 'https://nominatim.openstreetmap.org/search'
const DEBOUNCE_MS = 400

export function AddressAutocomplete({ value, onChange, onSelect }) {
  const [suggestions, setSuggestions] = useState([])
  const [open, setOpen] = useState(false)
  const debounceRef = useRef(null)
  const containerRef = useRef(null)

  function handleBlur(e) {
    if (containerRef.current && containerRef.current.contains(e.relatedTarget)) return
    setOpen(false)
  }

  function handleInputChange(text) {
    onChange(text)

    if (debounceRef.current) clearTimeout(debounceRef.current)

    if (text.trim().length < 3) {
      setSuggestions([])
      return
    }

    debounceRef.current = setTimeout(async () => {
      try {
        const params = new URLSearchParams({
          q: text,
          format: 'json',
          addressdetails: '1',
          limit: '5',
          countrycodes: 'vn',
        })
        const res = await fetch(`${NOMINATIM_URL}?${params}`)
        const data = await res.json()
        setSuggestions(data)
        setOpen(true)
      } catch {
        setSuggestions([])
      }
    }, DEBOUNCE_MS)
  }

  function handleSelect(item) {
    onSelect({
      addressText: item.display_name,
      latitude: Number(item.lat),
      longitude: Number(item.lon),
    })
    setSuggestions([])
    setOpen(false)
  }

  return (
    <div className="combo" ref={containerRef} onBlur={handleBlur}>
      <input
        id="dish-address"
        value={value}
        onChange={(e) => handleInputChange(e.target.value)}
        onFocus={() => suggestions.length > 0 && setOpen(true)}
        autoComplete="off"
        placeholder="Nhập địa chỉ quán..."
      />
      {open && suggestions.length > 0 && (
        <ul className="combo-options">
          {suggestions.map((item) => (
            <li key={item.place_id} tabIndex={-1} onMouseDown={() => handleSelect(item)}>
              {item.display_name}
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
