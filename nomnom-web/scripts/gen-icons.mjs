import sharp from 'sharp'
import { readFileSync } from 'fs'
import { fileURLToPath } from 'url'

const svg = readFileSync(new URL('../public/icon-source.svg', import.meta.url))

async function makeIcon(size, scale, name, bg = { r: 0, g: 0, b: 0, alpha: 0 }) {
  const contentSize = Math.round(size * scale)
  const contentBuffer = await sharp(svg).resize(contentSize, contentSize, { fit: 'contain' }).png().toBuffer()

  await sharp({
    create: { width: size, height: size, channels: 4, background: bg },
  })
    .composite([{ input: contentBuffer, gravity: 'center' }])
    .png()
    .toFile(fileURLToPath(new URL(`../public/${name}`, import.meta.url)))

  console.log('wrote', name)
}

await makeIcon(192, 1, 'icon-192.png')
await makeIcon(512, 1, 'icon-512.png')
await makeIcon(512, 0.7, 'icon-maskable-512.png', { r: 134, g: 59, b: 255, alpha: 1 })
