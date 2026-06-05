const RARITY_COLORS = {
  white: '#d8dde4',
  green: '#36b37e',
  blue: '#2684ff',
  purple: '#9b5cff',
  gold: '#ffab00',
  red: '#ff4d4f'
}

function createRenderer(canvas, ctx, size) {
  const state = {
    canvas,
    ctx,
    width: size.width,
    height: size.height,
    frame: 0
  }

  function resize(nextSize) {
    state.width = nextSize.width
    state.height = nextSize.height
  }

  function render(snapshot, statusText) {
    state.frame += 1
    const ctx = state.ctx
    const width = state.width
    const height = state.height
    const scene = snapshot && snapshot.scene
    const hero = snapshot && snapshot.hero
    const cameraX = scene && scene.camera ? scene.camera.x : 0
    const groundY = Math.round(height * 0.7)
    const worldScale = Math.max(0.7, Math.min(1.35, width / 420))

    drawBackground(ctx, width, height, state.frame)
    drawDecorations(ctx, scene, cameraX, groundY, worldScale, width, 'back')
    drawGround(ctx, width, height, groundY)
    drawDecorations(ctx, scene, cameraX, groundY, worldScale, width, 'front')
    drawEntities(ctx, scene, cameraX, groundY, worldScale, state.frame)
    drawFloatingLoot(ctx, snapshot, width)

    if (!snapshot) {
      drawCenteredText(ctx, width, height, statusText || 'API offline')
    }

    if (hero) {
      drawProgress(ctx, hero, width)
    }
  }

  return {
    resize,
    render
  }
}

function drawBackground(ctx, width, height, frame) {
  const sky = ctx.createLinearGradient(0, 0, 0, height)
  sky.addColorStop(0, '#91c7dd')
  sky.addColorStop(0.46, '#d9c486')
  sky.addColorStop(1, '#335235')
  ctx.fillStyle = sky
  ctx.fillRect(0, 0, width, height)

  ctx.fillStyle = 'rgba(255, 238, 170, 0.62)'
  ctx.beginPath()
  ctx.arc(width - 54, 48, 21, 0, Math.PI * 2)
  ctx.fill()

  const drift = (frame % 240) / 240
  ctx.fillStyle = 'rgba(255, 255, 255, 0.28)'
  drawCloud(ctx, 42 + drift * 36, 52, 0.9)
  drawCloud(ctx, width * 0.58 - drift * 28, 74, 0.75)

  ctx.fillStyle = '#4f6b50'
  drawRidge(ctx, width, height * 0.44, [0, 28, 52, 20, 64, 36, 70])
  ctx.fillStyle = '#2d573d'
  drawRidge(ctx, width, height * 0.52, [24, 46, 22, 62, 30, 76, 42])
}

function drawRidge(ctx, width, baseY, offsets) {
  ctx.beginPath()
  ctx.moveTo(0, baseY)
  const step = width / (offsets.length - 1)
  offsets.forEach((offset, index) => {
    ctx.lineTo(index * step, baseY - offset)
  })
  ctx.lineTo(width, baseY + 90)
  ctx.lineTo(0, baseY + 90)
  ctx.closePath()
  ctx.fill()
}

function drawCloud(ctx, x, y, scale) {
  ctx.beginPath()
  ctx.arc(x, y, 12 * scale, 0, Math.PI * 2)
  ctx.arc(x + 14 * scale, y - 5 * scale, 16 * scale, 0, Math.PI * 2)
  ctx.arc(x + 31 * scale, y, 12 * scale, 0, Math.PI * 2)
  ctx.fill()
}

function drawGround(ctx, width, height, groundY) {
  const ground = ctx.createLinearGradient(0, groundY, 0, height)
  ground.addColorStop(0, '#4b6a30')
  ground.addColorStop(0.32, '#5b4a2d')
  ground.addColorStop(1, '#2c2119')
  ctx.fillStyle = ground
  ctx.fillRect(0, groundY, width, height - groundY)

  ctx.strokeStyle = 'rgba(230, 211, 144, 0.35)'
  ctx.lineWidth = 2
  ctx.beginPath()
  ctx.moveTo(0, groundY + 1)
  ctx.lineTo(width, groundY + 1)
  ctx.stroke()
}

function drawDecorations(ctx, scene, cameraX, groundY, worldScale, width, layer) {
  if (!scene || !scene.decorations) {
    return
  }
  scene.decorations.forEach((decor) => {
    if (decor.layer !== layer) {
      return
    }
    const x = worldToScreenX(decor.x, cameraX, worldScale)
    const scale = (decor.scale || 1) * (layer === 'back' ? 0.8 : 1)
    if (x < -100 || x > width + 100) {
      return
    }
    if (decor.kind === 'pine') {
      drawPine(ctx, x, groundY + 6, scale)
    } else if (decor.kind === 'oak') {
      drawOak(ctx, x, groundY + 8, scale)
    } else if (decor.kind === 'fern') {
      drawFern(ctx, x, groundY + 6, scale)
    } else if (decor.kind === 'stump') {
      drawStump(ctx, x, groundY + 8, scale)
    } else {
      drawMushrooms(ctx, x, groundY + 8, scale)
    }
  })
}

function drawPine(ctx, x, y, scale) {
  ctx.fillStyle = '#4a3321'
  ctx.fillRect(x - 4 * scale, y - 58 * scale, 8 * scale, 58 * scale)
  ctx.fillStyle = '#1d5a3b'
  drawTriangle(ctx, x, y - 112 * scale, 38 * scale, 62 * scale)
  ctx.fillStyle = '#287049'
  drawTriangle(ctx, x, y - 88 * scale, 46 * scale, 66 * scale)
  ctx.fillStyle = '#2f8052'
  drawTriangle(ctx, x, y - 60 * scale, 52 * scale, 58 * scale)
}

function drawOak(ctx, x, y, scale) {
  ctx.fillStyle = '#5a3924'
  ctx.fillRect(x - 5 * scale, y - 68 * scale, 10 * scale, 68 * scale)
  ctx.fillStyle = '#2f7444'
  ctx.beginPath()
  ctx.arc(x, y - 86 * scale, 31 * scale, 0, Math.PI * 2)
  ctx.arc(x - 22 * scale, y - 70 * scale, 23 * scale, 0, Math.PI * 2)
  ctx.arc(x + 23 * scale, y - 68 * scale, 25 * scale, 0, Math.PI * 2)
  ctx.fill()
}

function drawFern(ctx, x, y, scale) {
  ctx.strokeStyle = '#6ab04c'
  ctx.lineWidth = 3 * scale
  for (let i = -2; i <= 2; i += 1) {
    ctx.beginPath()
    ctx.moveTo(x, y)
    ctx.quadraticCurveTo(x + i * 7 * scale, y - 18 * scale, x + i * 17 * scale, y - 27 * scale)
    ctx.stroke()
  }
}

function drawStump(ctx, x, y, scale) {
  ctx.fillStyle = '#7a4b2a'
  ctx.fillRect(x - 13 * scale, y - 21 * scale, 26 * scale, 21 * scale)
  ctx.fillStyle = '#ad7744'
  ctx.beginPath()
  ctx.ellipse(x, y - 21 * scale, 14 * scale, 7 * scale, 0, 0, Math.PI * 2)
  ctx.fill()
}

function drawMushrooms(ctx, x, y, scale) {
  drawMushroom(ctx, x - 8 * scale, y, scale * 0.85, '#d95043')
  drawMushroom(ctx, x + 7 * scale, y + 1 * scale, scale, '#d9b342')
}

function drawMushroom(ctx, x, y, scale, capColor) {
  ctx.fillStyle = '#f4d9af'
  ctx.fillRect(x - 3 * scale, y - 12 * scale, 6 * scale, 12 * scale)
  ctx.fillStyle = capColor
  ctx.beginPath()
  ctx.arc(x, y - 12 * scale, 10 * scale, Math.PI, 0)
  ctx.closePath()
  ctx.fill()
}

function drawTriangle(ctx, x, y, width, height) {
  ctx.beginPath()
  ctx.moveTo(x, y)
  ctx.lineTo(x - width / 2, y + height)
  ctx.lineTo(x + width / 2, y + height)
  ctx.closePath()
  ctx.fill()
}

function drawEntities(ctx, scene, cameraX, groundY, worldScale, frame) {
  if (!scene || !scene.entities) {
    return
  }
  scene.entities.forEach((entity) => {
    const x = worldToScreenX(entity.position.x, cameraX, worldScale)
    const bob = Math.sin(frame / 10) * (entity.state === 'walk' ? 2.5 : 1.2)
    if (entity.type === 'hero') {
      drawHero(ctx, x, groundY + bob, entity)
    } else {
      drawMonster(ctx, x, groundY + bob, entity)
    }
  })
}

function drawHero(ctx, x, y, entity) {
  drawHealthBar(ctx, x - 22, y - 78, 46, 6, entity.hp, entity.max_hp, '#36b37e')

  ctx.fillStyle = '#23434a'
  ctx.fillRect(x - 11, y - 45, 22, 31)
  ctx.fillStyle = '#f3c19b'
  ctx.beginPath()
  ctx.arc(x, y - 55, 12, 0, Math.PI * 2)
  ctx.fill()
  ctx.fillStyle = '#443323'
  ctx.fillRect(x - 12, y - 68, 24, 9)
  ctx.fillStyle = '#284d7c'
  ctx.fillRect(x - 8, y - 17, 7, 17)
  ctx.fillRect(x + 3, y - 17, 7, 17)

  ctx.strokeStyle = '#d7dde5'
  ctx.lineWidth = 3
  ctx.beginPath()
  ctx.moveTo(x + 13, y - 43)
  ctx.lineTo(x + 31, y - 57)
  ctx.stroke()
  ctx.fillStyle = '#b6c1c9'
  ctx.beginPath()
  ctx.arc(x + 34, y - 60, 7, 0.3, Math.PI * 1.35)
  ctx.lineTo(x + 34, y - 60)
  ctx.fill()
}

function drawMonster(ctx, x, y, entity) {
  drawHealthBar(ctx, x - 24, y - 58, 48, 6, entity.hp, entity.max_hp, '#ff6b6b')

  if (entity.name === 'thorn_boar') {
    ctx.fillStyle = '#7b5745'
    roundedRect(ctx, x - 24, y - 34, 48, 27, 13)
    ctx.fill()
    ctx.fillStyle = '#f0d6aa'
    drawTriangle(ctx, x - 30, y - 25, 12, 12)
    drawTriangle(ctx, x + 30, y - 25, 12, 12)
  } else if (entity.name === 'bark_guard') {
    ctx.fillStyle = '#704a2d'
    roundedRect(ctx, x - 18, y - 52, 36, 45, 7)
    ctx.fill()
    ctx.strokeStyle = '#3d291a'
    ctx.lineWidth = 2
    ctx.beginPath()
    ctx.moveTo(x - 10, y - 43)
    ctx.lineTo(x + 8, y - 16)
    ctx.stroke()
  } else if (entity.name === 'wild_mushroom') {
    drawMushroom(ctx, x, y - 4, 2, '#c64d48')
    ctx.fillStyle = '#3a2c29'
    ctx.fillRect(x - 5, y - 24, 3, 3)
    ctx.fillRect(x + 5, y - 24, 3, 3)
  } else {
    ctx.fillStyle = entity.name === 'moss_imp' ? '#708c42' : '#5db7a3'
    ctx.beginPath()
    ctx.ellipse(x, y - 22, 25, 18, 0, 0, Math.PI * 2)
    ctx.fill()
    ctx.fillStyle = '#17231e'
    ctx.fillRect(x - 9, y - 27, 4, 4)
    ctx.fillRect(x + 7, y - 27, 4, 4)
  }
}

function drawHealthBar(ctx, x, y, width, height, hp, maxHp, color) {
  const ratio = maxHp > 0 ? Math.max(0, Math.min(1, hp / maxHp)) : 0
  ctx.fillStyle = 'rgba(18, 24, 22, 0.72)'
  roundedRect(ctx, x, y, width, height, 3)
  ctx.fill()
  ctx.fillStyle = color
  roundedRect(ctx, x, y, width * ratio, height, 3)
  ctx.fill()
}

function drawProgress(ctx, hero, width) {
  const barWidth = Math.min(220, width - 32)
  const ratio = hero.exp_to_next_level > 0 ? hero.exp / hero.exp_to_next_level : 0
  ctx.fillStyle = 'rgba(16, 25, 22, 0.48)'
  roundedRect(ctx, 16, 14, barWidth, 8, 4)
  ctx.fill()
  ctx.fillStyle = '#ffcf5a'
  roundedRect(ctx, 16, 14, barWidth * Math.max(0, Math.min(1, ratio)), 8, 4)
  ctx.fill()
}

function drawFloatingLoot(ctx, snapshot, width) {
  if (!snapshot || !snapshot.events) {
    return
  }
  const loot = snapshot.events.slice().reverse().find((event) => event.kind === 'loot')
  if (!loot) {
    return
  }
  ctx.fillStyle = RARITY_COLORS[loot.data.rarity] || '#ffffff'
  ctx.font = '13px sans-serif'
  ctx.textAlign = 'center'
  ctx.fillText(loot.message, width / 2, 42)
}

function drawCenteredText(ctx, width, height, text) {
  ctx.fillStyle = 'rgba(12, 18, 16, 0.58)'
  roundedRect(ctx, width / 2 - 78, height / 2 - 18, 156, 36, 6)
  ctx.fill()
  ctx.fillStyle = '#f4f0df'
  ctx.font = '14px sans-serif'
  ctx.textAlign = 'center'
  ctx.fillText(text, width / 2, height / 2 + 5)
}

function roundedRect(ctx, x, y, width, height, radius) {
  const r = Math.min(radius, width / 2, height / 2)
  ctx.beginPath()
  ctx.moveTo(x + r, y)
  ctx.lineTo(x + width - r, y)
  ctx.quadraticCurveTo(x + width, y, x + width, y + r)
  ctx.lineTo(x + width, y + height - r)
  ctx.quadraticCurveTo(x + width, y + height, x + width - r, y + height)
  ctx.lineTo(x + r, y + height)
  ctx.quadraticCurveTo(x, y + height, x, y + height - r)
  ctx.lineTo(x, y + r)
  ctx.quadraticCurveTo(x, y, x + r, y)
  ctx.closePath()
}

function worldToScreenX(x, cameraX, worldScale) {
  return Math.round((x - cameraX) * worldScale + 20)
}

module.exports = {
  createRenderer,
  RARITY_COLORS
}
