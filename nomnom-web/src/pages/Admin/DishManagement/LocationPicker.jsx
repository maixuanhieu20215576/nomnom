import L from 'leaflet'
import { useEffect } from 'react'
import { MapContainer, Marker, TileLayer, useMap, useMapEvents } from 'react-leaflet'
import 'leaflet/dist/leaflet.css'
import markerIcon2x from 'leaflet/dist/images/marker-icon-2x.png'
import markerIcon from 'leaflet/dist/images/marker-icon.png'
import markerShadow from 'leaflet/dist/images/marker-shadow.png'

delete L.Icon.Default.prototype._getIconUrl
L.Icon.Default.mergeOptions({
  iconRetinaUrl: markerIcon2x,
  iconUrl: markerIcon,
  shadowUrl: markerShadow,
})

const DEFAULT_CENTER = [10.7769, 106.7009] // Ho Chi Minh City

function ClickHandler({ onPick }) {
  useMapEvents({
    click(e) {
      onPick(e.latlng.lat, e.latlng.lng)
    },
  })
  return null
}

function RecenterOnChange({ latitude, longitude }) {
  const map = useMap()
  useEffect(() => {
    if (latitude != null && longitude != null) {
      map.flyTo([latitude, longitude], 15)
    }
  }, [latitude, longitude, map])
  return null
}

export function LocationPicker({ latitude, longitude, onChange }) {
  const hasPosition = latitude != null && longitude != null
  const center = hasPosition ? [latitude, longitude] : DEFAULT_CENTER

  return (
    <div className="cd-map">
      <MapContainer center={center} zoom={hasPosition ? 15 : 12} style={{ height: '100%', width: '100%' }}>
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution='&copy; OpenStreetMap contributors'
        />
        <ClickHandler onPick={onChange} />
        <RecenterOnChange latitude={latitude} longitude={longitude} />
        {hasPosition && <Marker position={[latitude, longitude]} />}
      </MapContainer>
    </div>
  )
}
