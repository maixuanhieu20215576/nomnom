import { useRef, useState } from 'react'

export function SearchableSelect({ id, value, options, placeholder, onChange }) {
  const [query, setQuery] = useState(value ?? '')
  const [open, setOpen] = useState(false)
  const containerRef = useRef(null)

  const filteredOptions = options.filter((option) =>
    option.toLowerCase().includes(query.toLowerCase()),
  )

  function handleSelect(option) {
    onChange(option)
    setQuery(option)
    setOpen(false)
  }

  function handleBlur(e) {
    if (containerRef.current && containerRef.current.contains(e.relatedTarget)) return
    setOpen(false)
    setQuery(value ?? '')
  }

  return (
    <div className="combo" ref={containerRef} onBlur={handleBlur}>
      <input
        id={id}
        value={query}
        placeholder={placeholder}
        autoComplete="off"
        onFocus={() => setOpen(true)}
        onChange={(e) => {
          setQuery(e.target.value)
          setOpen(true)
        }}
      />
      {open && (
        <ul className="combo-options">
          {filteredOptions.length === 0 ? (
            <li className="combo-empty">Không tìm thấy</li>
          ) : (
            filteredOptions.map((option) => (
              <li key={option} tabIndex={-1} onMouseDown={() => handleSelect(option)}>
                {option}
              </li>
            ))
          )}
        </ul>
      )}
    </div>
  )
}
