const SLOT_LABELS = {
  weapon: '武器',
  helmet: '头盔',
  armor: '护甲',
  boots: '鞋子',
  ring: '戒指'
}

const RARITY_LABELS = {
  white: '白',
  green: '绿',
  blue: '蓝',
  purple: '紫',
  gold: '金',
  red: '红'
}

const TALENT_TIER_LABELS = {
  common: '普通',
  uncommon: '优良',
  excellent: '卓越',
  rare: '罕见',
  transcendent: '超凡',
  mythic: '绝世'
}

const EFFECT_LABELS = {
  attack_pct: '攻击',
  defense_pct: '防御',
  max_hp_pct: '生命',
  move_speed_pct: '移速',
  drop_rate_pct: '掉宝',
  gold_pct: '金币',
  exp_pct: '经验',
  treasure_mimic_chance_pct: '宝箱怪',
  rift_drop_rate_pct: '秘境掉宝',
  all_stats_pct: '全属性'
}

const state = {
  snapshot: null,
  tickInFlight: false,
  animationFrame: 0,
  lastRenderAt: 0,
  loadedAssets: 0
}

const ASSET_PATHS = {
  heroIdle: '/web/assets/sprites/hero_idle.png',
  heroWalkA: '/web/assets/sprites/hero_walk_a.png',
  heroWalkB: '/web/assets/sprites/hero_walk_b.png',
  heroHit: '/web/assets/sprites/hero_hit.png',
  slimeRest: '/web/assets/sprites/slime_rest.png',
  slimeWalkA: '/web/assets/sprites/slime_walk_a.png',
  slimeWalkB: '/web/assets/sprites/slime_walk_b.png',
  thornRest: '/web/assets/sprites/thorn_rest.png',
  thornWalkA: '/web/assets/sprites/thorn_walk_a.png',
  impIdle: '/web/assets/sprites/imp_idle.png',
  impJump: '/web/assets/sprites/imp_jump.png',
  guardIdle: '/web/assets/sprites/guard_idle.png',
  guardAttack: '/web/assets/sprites/guard_attack.png',
  flyA: '/web/assets/sprites/fly_a.png',
  flyB: '/web/assets/sprites/fly_b.png',
  beeA: '/web/assets/sprites/bee_a.png',
  beeB: '/web/assets/sprites/bee_b.png',
  bossA: '/web/assets/sprites/boss_a.png',
  bossB: '/web/assets/sprites/boss_b.png',
  mushroom: '/web/assets/sprites/wild_mushroom.png',
  mimicClosed: '/web/assets/sprites/mimic_closed.png',
  mimicOpen: '/web/assets/sprites/mimic_open.png',
  bgForest: '/web/assets/backgrounds/forest_trees.png',
  bgForestFade: '/web/assets/backgrounds/forest_fade.png',
  bgCave: '/web/assets/backgrounds/cave_mushrooms.png',
  bgCastle: '/web/assets/backgrounds/castle_hills.png',
  bgClouds: '/web/assets/backgrounds/clouds.png',
  bgSky: '/web/assets/backgrounds/sky.png',
  groundGrass: '/web/assets/sprites/ground_grass.png',
  groundStone: '/web/assets/sprites/ground_stone.png',
  groundDirt: '/web/assets/sprites/ground_dirt.png',
  blockGrass: '/web/assets/sprites/block_grass.png',
  blockStone: '/web/assets/sprites/block_stone.png',
  brickGrey: '/web/assets/sprites/brick_grey.png',
  bush: '/web/assets/sprites/bush.png',
  rock: '/web/assets/sprites/rock.png'
}

const assetImages = {}

Object.entries(ASSET_PATHS).forEach(([key, path]) => {
  const image = new Image()
  image.decoding = 'async'
  image.onload = () => {
    state.loadedAssets += 1
  }
  image.src = path
  assetImages[key] = image
})

const canvas = document.querySelector('#gameCanvas')
const ctx = canvas.getContext('2d')

const els = {
  statusText: document.querySelector('#statusText'),
  goldText: document.querySelector('#goldText'),
  levelText: document.querySelector('#levelText'),
  hpText: document.querySelector('#hpText'),
  attackText: document.querySelector('#attackText'),
  defenseText: document.querySelector('#defenseText'),
  powerText: document.querySelector('#powerText'),
  modeText: document.querySelector('#modeText'),
  riftStateText: document.querySelector('#riftStateText'),
  enterRiftButton: document.querySelector('#enterRiftButton'),
  leaveRiftButton: document.querySelector('#leaveRiftButton'),
  tickButton: document.querySelector('#tickButton'),
  equipBestButton: document.querySelector('#equipBestButton'),
  resetButton: document.querySelector('#resetButton'),
  riftThemeText: document.querySelector('#riftThemeText'),
  riftProgressBar: document.querySelector('#riftProgressBar'),
  unlockedFloorText: document.querySelector('#unlockedFloorText'),
  recommendedPowerText: document.querySelector('#recommendedPowerText'),
  minionProgressText: document.querySelector('#minionProgressText'),
  mimicPityText: document.querySelector('#mimicPityText'),
  mimicPityBar: document.querySelector('#mimicPityBar'),
  mimicChanceText: document.querySelector('#mimicChanceText'),
  pityRemainingText: document.querySelector('#pityRemainingText'),
  talentScrollText: document.querySelector('#talentScrollText'),
  talentList: document.querySelector('#talentList'),
  talentCatalogText: document.querySelector('#talentCatalogText'),
  equippedList: document.querySelector('#equippedList'),
  inventoryList: document.querySelector('#inventoryList'),
  marketList: document.querySelector('#marketList'),
  eventList: document.querySelector('#eventList')
}

function api(path, options = {}) {
  return fetch(path, {
    method: options.method || 'GET',
    headers: {
      'content-type': 'application/json'
    },
    body: options.body ? JSON.stringify(options.body) : undefined
  }).then(async (response) => {
    const data = await response.json()
    if (!response.ok) {
      throw new Error(data.error || `HTTP ${response.status}`)
    }
    return data
  })
}

function resizeCanvas() {
  const rect = canvas.getBoundingClientRect()
  const dpr = window.devicePixelRatio || 1
  canvas.width = Math.round(rect.width * dpr)
  canvas.height = Math.round(rect.height * dpr)
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0)
}

function setStatus(text, online = true) {
  els.statusText.textContent = text
  els.statusText.style.color = online ? '#9fb0a6' : '#ff9f7f'
}

function refresh() {
  return api('/snapshot')
    .then((snapshot) => {
      applySnapshot(snapshot)
      setStatus('已连接')
    })
    .catch((error) => {
      setStatus(error.message || '连接失败', false)
    })
}

function tick(seconds = 1) {
  if (state.tickInFlight) {
    return Promise.resolve()
  }
  state.tickInFlight = true
  return api('/tick', {
    method: 'POST',
    body: { seconds }
  })
    .then((snapshot) => {
      applySnapshot(snapshot)
      setStatus(snapshot.mode === 'rift' ? '秘境推进中' : '挂机中')
    })
    .catch((error) => {
      setStatus(error.message || '推进失败', false)
    })
    .finally(() => {
      state.tickInFlight = false
    })
}

function postAction(path, body, statusText) {
  return api(path, {
    method: 'POST',
    body
  })
    .then((result) => {
      applySnapshot(result.snapshot || result)
      setStatus(statusText)
    })
    .catch((error) => {
      setStatus(error.message || '操作失败', false)
    })
}

function applySnapshot(snapshot) {
  state.snapshot = snapshot
  const hero = snapshot.hero
  const rift = snapshot.rift
  const treasure = snapshot.treasure || {}
  const active = rift.active
  const minionsRequired = active ? rift.minions_required : 0
  const minionsDefeated = active ? rift.minions_defeated : 0
  const progress = active
    ? (rift.state === 'boss' ? 100 : Math.round((minionsDefeated / Math.max(1, minionsRequired)) * 72))
    : 0

  els.goldText.textContent = hero.gold
  els.levelText.textContent = hero.level
  els.hpText.textContent = `${hero.hp} / ${hero.max_hp}`
  els.attackText.textContent = hero.attack
  els.defenseText.textContent = hero.defense
  els.powerText.textContent = rift.hero_power
  els.modeText.textContent = snapshot.mode === 'rift' ? '秘境' : '森林'
  els.riftStateText.textContent = describeRiftState(rift)
  els.enterRiftButton.disabled = active
  els.enterRiftButton.textContent = `进入 ${rift.unlocked_floor} 层秘境`
  els.leaveRiftButton.disabled = !active
  els.riftThemeText.textContent = active ? themeLabel(rift.theme) : '随机主题'
  els.unlockedFloorText.textContent = rift.unlocked_floor
  els.recommendedPowerText.textContent = rift.recommended_power
  els.minionProgressText.textContent = active ? `${minionsDefeated} / ${minionsRequired}` : '-'
  els.riftProgressBar.style.width = `${progress}%`
  els.mimicPityText.textContent = `${treasure.mimics_defeated_since_red || 0} / ${treasure.pity_threshold || 0}`
  els.mimicPityBar.style.width = `${Math.round((treasure.pity_progress || 0) * 100)}%`
  els.mimicChanceText.textContent = `${((treasure.mimic_chance || 0) * 100).toFixed(1)}%`
  els.pityRemainingText.textContent = treasure.pity_remaining || treasure.pity_threshold || 0

  renderEquipped(hero.equipped || {})
  renderTalents(hero.talents || [], hero.talent_scrolls || 0, snapshot.talent || {})
  renderInventory(hero.inventory || [])
  renderMarket((snapshot.market && snapshot.market.active) || [], hero.id)
  renderEvents(snapshot.events || [])
}

function describeRiftState(rift) {
  if (!rift.active) {
    return `推荐战力 ${rift.recommended_power}`
  }
  if (rift.state === 'boss') {
    return `${themeLabel(rift.theme)} ${rift.floor} 层 Boss`
  }
  return `${themeLabel(rift.theme)} ${rift.floor} 层 小怪 ${rift.minions_defeated}/${rift.minions_required}`
}

function renderTalents(talents, scrolls, talentMeta) {
  els.talentScrollText.textContent = `卷轴 ${scrolls}`
  els.talentCatalogText.textContent = `目录 ${talentMeta.total_catalog_count || 0} 个 · 每级 150 个`
  if (!talents.length) {
    els.talentList.innerHTML = '<div class="empty">暂无天赋</div>'
    return
  }
  els.talentList.innerHTML = talents
    .map((talent) => {
      const locked = talent.tier === 'mythic'
      const disabled = scrolls <= 0 || locked
      return `
        <article class="talent tier-${talent.tier}">
          <div class="item-main">
            <span class="item-name">${escapeHtml(talent.name)}</span>
            <span class="talent-tier">${talentTierLabel(talent.tier)}</span>
          </div>
          <div class="item-sub">${escapeHtml(talent.description)} · ${effectLine(talent.effects)}</div>
          <div class="item-actions">
            <button data-action="evolve-talent" data-id="${talent.id}" ${disabled ? 'disabled' : ''}>${locked ? '已绝世' : '进化'}</button>
          </div>
        </article>
      `
    })
    .join('')
}

function renderEquipped(equipped) {
  const items = Object.keys(equipped).map((slot) => equipped[slot])
  if (!items.length) {
    els.equippedList.innerHTML = '<div class="empty">暂无装备</div>'
    return
  }
  const bonuses = (state.snapshot && state.snapshot.hero && state.snapshot.hero.set_bonuses) || []
  els.equippedList.innerHTML = items.map((item) => itemHtml(item, '')).join('') + renderSetBonuses(bonuses)
}

function renderInventory(items) {
  if (!items.length) {
    els.inventoryList.innerHTML = '<div class="empty">背包是空的，继续砍怪试试。</div>'
    return
  }
  els.inventoryList.innerHTML = items
    .map((item) => itemHtml(item, `
      <div class="item-actions">
        <button data-action="equip" data-id="${item.id}">穿戴</button>
        <button class="muted" data-action="list" data-id="${item.id}" data-price="${Math.max(20, item.score * 2)}">挂售</button>
      </div>
    `))
    .join('')
}

function renderMarket(listings, heroId) {
  if (!listings.length) {
    els.marketList.innerHTML = '<div class="empty">暂无挂单</div>'
    return
  }
  els.marketList.innerHTML = listings
    .map((listing) => {
      const item = listing.item
      const own = listing.seller_id === heroId
      return `
        <article class="item rarity-${item.rarity}">
          <div class="item-main">
            <span class="item-name">${escapeHtml(item.name)}</span>
            <span class="price">${listing.price} 金</span>
          </div>
          <div class="item-sub">${own ? '我的挂单' : listing.seller_id} · ${slotLabel(item.slot)} · 评分 ${item.score}</div>
          ${specialLine(item)}
          <div class="item-actions">
            <button data-action="buy" data-id="${listing.id}" ${own ? 'disabled' : ''}>购买</button>
          </div>
        </article>
      `
    })
    .join('')
}

function renderEvents(events) {
  els.eventList.innerHTML = events
    .slice(-16)
    .reverse()
    .map((event) => `<div class="event ${event.kind}">${escapeHtml(event.message)}</div>`)
    .join('')
}

function itemHtml(item, actions) {
  return `
    <article class="item rarity-${item.rarity}${item.special ? ' special' : ''}">
      <div class="item-main">
        <span class="item-name">${escapeHtml(item.name)}</span>
        <span class="score">${item.score}</span>
      </div>
      <div class="item-sub">${slotLabel(item.slot)} · ${rarityLabel(item.rarity)} · Lv.${item.level} · 攻 ${item.attack} 防 ${item.defense} 命 ${item.max_hp}</div>
      ${specialLine(item)}
      ${actions}
    </article>
  `
}

function specialLine(item) {
  if (!item.special) {
    return ''
  }
  return `
    <div class="set-line">
      <span class="badge">特殊套装</span>
      ${escapeHtml(item.set_name || 'Unknown Set')} · ${escapeHtml(item.set_piece || '')}
      <small>${bonusText(item.set_bonus)}</small>
    </div>
  `
}

function renderSetBonuses(bonuses) {
  if (!bonuses.length) {
    return ''
  }
  return bonuses
    .map((bonus) => `
      <div class="set-bonus">
        ${escapeHtml(bonus.set_name || '套装')} ${bonus.pieces}/${bonus.pieces_required}
        <small>${bonusText(bonus)}</small>
      </div>
    `)
    .join('')
}

function bonusText(bonus) {
  if (!bonus) {
    return ''
  }
  const parts = []
  if (bonus.attack) parts.push(`攻 +${bonus.attack}`)
  if (bonus.defense) parts.push(`防 +${bonus.defense}`)
  if (bonus.max_hp) parts.push(`命 +${bonus.max_hp}`)
  return parts.join(' · ')
}

function effectLine(effects) {
  return Object.keys(effects || {})
    .map((key) => `${EFFECT_LABELS[key] || key} +${(effects[key] * 100).toFixed(1)}%`)
    .join(' · ')
}

function talentTierLabel(tier) {
  return TALENT_TIER_LABELS[tier] || tier
}

function slotLabel(slot) {
  return SLOT_LABELS[slot] || slot
}

function rarityLabel(rarity) {
  return RARITY_LABELS[rarity] || rarity
}

function themeLabel(theme) {
  return {
    forest: '森林',
    cave: '山洞',
    sky: '天空',
    castle: '城堡'
  }[theme] || theme
}

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
}

function assetImage(key) {
  const image = assetImages[key]
  if (!image || !image.complete || image.naturalWidth <= 0) {
    return null
  }
  return image
}

function drawSprite(key, x, y, width, height, flip = false) {
  const image = assetImage(key)
  if (!image) {
    return false
  }
  ctx.save()
  if (flip) {
    ctx.translate(x + width, y)
    ctx.scale(-1, 1)
    ctx.drawImage(image, 0, 0, width, height)
  } else {
    ctx.drawImage(image, x, y, width, height)
  }
  ctx.restore()
  return true
}

function drawSpriteBottom(key, centerX, bottomY, width, height, flip = false) {
  return drawSprite(key, centerX - width / 2, bottomY - height, width, height, flip)
}

function drawCover(key, x, y, width, height, alpha = 1) {
  const image = assetImage(key)
  if (!image) {
    return false
  }
  const scale = Math.max(width / image.naturalWidth, height / image.naturalHeight)
  const drawWidth = image.naturalWidth * scale
  const drawHeight = image.naturalHeight * scale
  ctx.save()
  ctx.globalAlpha = alpha
  ctx.drawImage(image, x + (width - drawWidth) / 2, y + (height - drawHeight) / 2, drawWidth, drawHeight)
  ctx.restore()
  return true
}

function drawTiledSprite(key, x, y, width, height, tileSize, offset = 0) {
  const image = assetImage(key)
  if (!image) {
    return false
  }
  const startX = x - ((offset % tileSize) + tileSize) % tileSize
  for (let tx = startX; tx < x + width + tileSize; tx += tileSize) {
    ctx.drawImage(image, tx, y, tileSize, tileSize)
  }
  return true
}

function draw(timestamp) {
  state.animationFrame += 1
  state.lastRenderAt = timestamp
  const snapshot = state.snapshot
  const rect = canvas.getBoundingClientRect()
  renderScene(snapshot, rect.width, rect.height)
  window.requestAnimationFrame(draw)
}

function renderScene(snapshot, width, height) {
  const scene = snapshot && snapshot.scene
  const biome = scene ? scene.biome : 'forest'
  const cameraX = scene && scene.camera ? scene.camera.x : 0
  const groundY = Math.round(height * 0.72)
  const worldScale = Math.max(0.78, Math.min(1.32, width / 720))

  drawBackground(biome, width, height)
  if (scene) {
    drawDecorations(scene.decorations || [], cameraX, groundY, worldScale, width, 'back', biome)
    drawGround(biome, width, height, groundY, cameraX, worldScale)
    drawDecorations(scene.decorations || [], cameraX, groundY, worldScale, width, 'front', biome)
    drawEntities(scene.entities || [], cameraX, groundY, worldScale)
  } else {
    drawGround('forest', width, height, groundY, 0, worldScale)
    centeredText(width, height, '等待后端连接')
  }
}

function drawAssetBackground(biome, width, height) {
  if (biome === 'cave') {
    if (!drawCover('bgCave', 0, 0, width, height)) {
      return false
    }
    ctx.fillStyle = 'rgba(10, 9, 14, 0.46)'
    ctx.fillRect(0, 0, width, height)
    ctx.fillStyle = 'rgba(132, 205, 255, 0.16)'
    for (let x = 30; x < width; x += 130) {
      drawCrystal(x, height * 0.56, 1.2)
    }
    drawStalactites(width)
    return true
  }

  if (biome === 'sky') {
    if (!drawCover('bgSky', 0, 0, width, height)) {
      return false
    }
    drawCover('bgClouds', 0, 0, width, height * 0.6, 0.88)
    ctx.fillStyle = 'rgba(255,255,255,0.72)'
    drawCloud(90, 78, 1.2)
    drawCloud(width * 0.62, 112, 1)
    drawFloatingIsland(width * 0.28, height * 0.5, 1.2)
    drawFloatingIsland(width * 0.74, height * 0.45, 0.9)
    return true
  }

  if (biome === 'castle') {
    if (!drawCover('bgCastle', 0, 0, width, height)) {
      return false
    }
    ctx.fillStyle = 'rgba(33, 35, 43, 0.54)'
    ctx.fillRect(0, 0, width, height)
    drawCastleWall(width, height)
    return true
  }

  if (!drawCover('bgForest', 0, 0, width, height)) {
    return false
  }
  drawCover('bgForestFade', 0, 0, width, height, 0.52)
  ctx.fillStyle = 'rgba(255, 238, 170, 0.5)'
  ctx.beginPath()
  ctx.arc(width - 76, 66, 28, 0, Math.PI * 2)
  ctx.fill()
  return true
}

function drawBackground(biome, width, height) {
  if (drawAssetBackground(biome, width, height)) {
    return
  }

  if (biome === 'cave') {
    const grad = ctx.createLinearGradient(0, 0, 0, height)
    grad.addColorStop(0, '#151827')
    grad.addColorStop(0.5, '#2c2432')
    grad.addColorStop(1, '#16120f')
    ctx.fillStyle = grad
    ctx.fillRect(0, 0, width, height)
    ctx.fillStyle = 'rgba(132, 205, 255, 0.18)'
    for (let x = 30; x < width; x += 130) {
      drawCrystal(x, height * 0.56, 1.2)
    }
    drawStalactites(width)
    return
  }

  if (biome === 'sky') {
    const grad = ctx.createLinearGradient(0, 0, 0, height)
    grad.addColorStop(0, '#4d95df')
    grad.addColorStop(0.55, '#dbefff')
    grad.addColorStop(1, '#b9d982')
    ctx.fillStyle = grad
    ctx.fillRect(0, 0, width, height)
    ctx.fillStyle = 'rgba(255,255,255,0.72)'
    drawCloud(90, 78, 1.2)
    drawCloud(width * 0.62, 112, 1)
    drawFloatingIsland(width * 0.28, height * 0.5, 1.2)
    drawFloatingIsland(width * 0.74, height * 0.45, 0.9)
    return
  }

  if (biome === 'castle') {
    const grad = ctx.createLinearGradient(0, 0, 0, height)
    grad.addColorStop(0, '#293346')
    grad.addColorStop(0.52, '#6a6670')
    grad.addColorStop(1, '#2a2524')
    ctx.fillStyle = grad
    ctx.fillRect(0, 0, width, height)
    drawCastleWall(width, height)
    return
  }

  const sky = ctx.createLinearGradient(0, 0, 0, height)
  sky.addColorStop(0, '#8ec5df')
  sky.addColorStop(0.5, '#d8c47e')
  sky.addColorStop(1, '#314f35')
  ctx.fillStyle = sky
  ctx.fillRect(0, 0, width, height)
  ctx.fillStyle = 'rgba(255, 238, 170, 0.66)'
  ctx.beginPath()
  ctx.arc(width - 76, 66, 28, 0, Math.PI * 2)
  ctx.fill()
  ctx.fillStyle = '#4e6f4b'
  drawRidge(width, height * 0.45, [10, 42, 70, 28, 80, 48, 84])
  ctx.fillStyle = '#294f3a'
  drawRidge(width, height * 0.55, [28, 58, 22, 72, 36, 86, 48])
}

function drawGround(biome, width, height, groundY, cameraX, worldScale) {
  const grad = ctx.createLinearGradient(0, groundY, 0, height)
  if (biome === 'cave') {
    grad.addColorStop(0, '#4b3a32')
    grad.addColorStop(1, '#1a1412')
  } else if (biome === 'sky') {
    grad.addColorStop(0, '#85ad52')
    grad.addColorStop(1, '#5b4a2e')
  } else if (biome === 'castle') {
    grad.addColorStop(0, '#706b67')
    grad.addColorStop(1, '#332d2a')
  } else {
    grad.addColorStop(0, '#4b6a30')
    grad.addColorStop(0.35, '#5b4a2d')
    grad.addColorStop(1, '#2c2119')
  }
  ctx.fillStyle = grad
  ctx.fillRect(0, groundY, width, height - groundY)
  const tileKey = biome === 'cave' || biome === 'castle'
    ? 'groundStone'
    : biome === 'sky'
      ? 'groundGrass'
      : 'groundDirt'
  const tileSize = Math.max(46, Math.min(72, Math.round(width / 15)))
  const offset = cameraX * worldScale
  const tiled = drawTiledSprite(tileKey, 0, groundY - tileSize * 0.35, width, tileSize, tileSize, offset)
  if (tiled && biome === 'forest') {
    drawTiledSprite('groundGrass', 0, groundY - tileSize * 0.82, width, tileSize, tileSize, offset)
  }
  ctx.strokeStyle = 'rgba(245, 236, 214, 0.32)'
  ctx.lineWidth = 2
  ctx.beginPath()
  ctx.moveTo(0, groundY + 1)
  ctx.lineTo(width, groundY + 1)
  ctx.stroke()
}

function drawDecorations(decorations, cameraX, groundY, worldScale, width, layer, biome) {
  decorations.forEach((decor) => {
    if (decor.layer !== layer) {
      return
    }
    const x = worldX(decor.x, cameraX, worldScale)
    if (x < -120 || x > width + 120) {
      return
    }
    const scale = (decor.scale || 1) * (layer === 'back' ? 0.82 : 1)
    if (drawDecorationSprite(decor.kind, biome, x, groundY, scale, layer)) {
      return
    }
    if (biome === 'cave') {
      if (decor.kind === 'crystal' || decor.kind === 'glow_mushroom') {
        drawCrystal(x, groundY + 6, scale)
      } else {
        drawStone(x, groundY + 6, scale)
      }
    } else if (biome === 'sky') {
      if (decor.kind === 'cloud_bank') {
        drawCloud(x, groundY - 96 * scale, scale)
      } else {
        drawFloatingIsland(x, groundY - 86 * scale, scale)
      }
    } else if (biome === 'castle') {
      drawCastleDecor(x, groundY + 6, scale, decor.kind)
    } else if (decor.kind === 'pine') {
      drawPine(x, groundY + 6, scale)
    } else if (decor.kind === 'oak') {
      drawOak(x, groundY + 8, scale)
    } else if (decor.kind === 'fern') {
      drawFern(x, groundY + 6, scale)
    } else if (decor.kind === 'stump') {
      drawStump(x, groundY + 8, scale)
    } else {
      drawMushrooms(x, groundY + 8, scale)
    }
  })
}

function drawDecorationSprite(kind, biome, x, groundY, scale, layer) {
  if (biome === 'forest') {
    if (kind === 'fern') {
      return drawSpriteBottom('bush', x, groundY + 9, 46 * scale, 38 * scale)
    }
    if (kind === 'stump') {
      return drawSpriteBottom('rock', x, groundY + 8, 42 * scale, 32 * scale)
    }
    if (kind.includes('mushroom')) {
      return drawSpriteBottom('mushroom', x, groundY + 6, 35 * scale, 40 * scale)
    }
  }
  if (biome === 'cave' && (kind === 'stalagmite' || kind === 'dark_column')) {
    return drawSpriteBottom('rock', x, groundY + 6, 48 * scale, 34 * scale)
  }
  if (biome === 'sky' && kind === 'floating_rock') {
    return drawSpriteBottom('blockGrass', x, groundY - 58 * scale, 52 * scale, 52 * scale)
  }
  if (biome === 'castle' && layer === 'front') {
    return drawSpriteBottom('brickGrey', x, groundY + 4, 54 * scale, 54 * scale)
  }
  return false
}

function drawEntities(entities, cameraX, groundY, worldScale) {
  entities.forEach((entity) => {
    const x = worldX(entity.position.x, cameraX, worldScale)
    const bob = Math.sin(state.animationFrame / 10) * (entity.state === 'walk' ? 2.5 : 1.2)
    if (entity.type === 'hero') {
      drawHero(x, groundY + bob, entity)
    } else {
      drawMonster(x, groundY + bob, entity)
    }
  })
}

function animatedFrame(a, b, speed = 18) {
  return Math.floor(state.animationFrame / speed) % 2 === 0 ? a : b
}

function monsterSpriteKey(entity) {
  if (entity.role === 'boss') {
    return animatedFrame('bossA', 'bossB', 22)
  }
  const name = entity.name || ''
  if (name.includes('thorn')) return animatedFrame('thornRest', 'thornWalkA', 20)
  if (name.includes('moss_imp')) return animatedFrame('impIdle', 'impJump', 18)
  if (name.includes('mushroom')) return 'mushroom'
  if (name.includes('bark') || name.includes('guard') || name.includes('knight') || name.includes('squire')) {
    return animatedFrame('guardIdle', 'guardAttack', 24)
  }
  if (name.includes('bat') || name.includes('wisp')) return animatedFrame('flyA', 'flyB', 12)
  if (name.includes('harpy') || name.includes('mote')) return animatedFrame('beeA', 'beeB', 12)
  return animatedFrame('slimeWalkA', 'slimeWalkB', 18)
}

function drawHero(x, y, entity) {
  drawHealthBar(x - 24, y - 84, 50, 7, entity.hp, entity.max_hp, '#5fd18b')
  const frame = entity.state === 'combat'
    ? animatedFrame('heroHit', 'heroIdle', 16)
    : animatedFrame('heroWalkA', 'heroWalkB', 14)
  if (drawSpriteBottom(frame, x, y + 2, 58, 82, false)) {
    ctx.strokeStyle = '#dce4e6'
    ctx.lineWidth = 4
    ctx.beginPath()
    ctx.moveTo(x + 18, y - 44)
    ctx.lineTo(x + 42, y - 60)
    ctx.stroke()
    return
  }
  ctx.fillStyle = '#223b44'
  roundRect(x - 13, y - 48, 26, 33, 6)
  ctx.fill()
  ctx.fillStyle = '#f0bf99'
  ctx.beginPath()
  ctx.arc(x, y - 60, 13, 0, Math.PI * 2)
  ctx.fill()
  ctx.fillStyle = '#3d2d20'
  ctx.fillRect(x - 13, y - 73, 26, 10)
  ctx.fillStyle = '#2a5588'
  ctx.fillRect(x - 10, y - 18, 8, 18)
  ctx.fillRect(x + 4, y - 18, 8, 18)
  ctx.strokeStyle = '#dce4e6'
  ctx.lineWidth = 4
  ctx.beginPath()
  ctx.moveTo(x + 14, y - 45)
  ctx.lineTo(x + 36, y - 61)
  ctx.stroke()
}

function drawMonster(x, y, entity) {
  if (entity.role === 'treasure_mimic') {
    drawTreasureMimic(x, y, entity)
    return
  }
  const boss = entity.role === 'boss'
  const scale = boss ? 1.45 : 1
  drawHealthBar(x - 26 * scale, y - 60 * scale, 52 * scale, 7, entity.hp, entity.max_hp, boss ? '#ffca55' : '#ff6b6b')
  const key = monsterSpriteKey(entity)
  const name = entity.name || ''
  const width = boss ? 94 : name.includes('mushroom') ? 48 : 66
  const height = boss ? 92 : name.includes('mushroom') ? 56 : 58
  const flightLift = name.includes('bat') || name.includes('wisp') || name.includes('harpy') || name.includes('mote') ? 26 : 0
  if (drawSpriteBottom(key, x, y - flightLift + 3, width, height, true)) {
    if (boss) {
      ctx.strokeStyle = 'rgba(255, 202, 85, 0.72)'
      ctx.lineWidth = 3
      ctx.beginPath()
      ctx.ellipse(x, y - 45, 46, 34, 0, 0, Math.PI * 2)
      ctx.stroke()
    }
    return
  }
  ctx.fillStyle = boss ? '#7d3f61' : monsterColor(entity.name)
  ctx.beginPath()
  ctx.ellipse(x, y - 24 * scale, 26 * scale, 20 * scale, 0, 0, Math.PI * 2)
  ctx.fill()
  ctx.fillStyle = '#141817'
  ctx.fillRect(x - 10 * scale, y - 30 * scale, 4 * scale, 4 * scale)
  ctx.fillRect(x + 7 * scale, y - 30 * scale, 4 * scale, 4 * scale)
  if (boss) {
    ctx.strokeStyle = '#ffca55'
    ctx.lineWidth = 3
    ctx.beginPath()
    ctx.moveTo(x - 18 * scale, y - 46 * scale)
    ctx.lineTo(x - 30 * scale, y - 68 * scale)
    ctx.moveTo(x + 18 * scale, y - 46 * scale)
    ctx.lineTo(x + 30 * scale, y - 68 * scale)
    ctx.stroke()
  }
}

function drawTreasureMimic(x, y, entity) {
  drawHealthBar(x - 31, y - 66, 62, 7, entity.hp, entity.max_hp, '#ffca55')
  const key = animatedFrame('mimicClosed', 'mimicOpen', 20)
  if (drawSpriteBottom(key, x, y + 2, 66, 66, false)) {
    ctx.fillStyle = '#1a1511'
    ctx.fillRect(x - 16, y - 30, 5, 5)
    ctx.fillRect(x + 11, y - 30, 5, 5)
    ctx.strokeStyle = '#d9d1c3'
    ctx.lineWidth = 3
    ctx.beginPath()
    ctx.moveTo(x - 20, y - 8)
    ctx.lineTo(x - 30, y)
    ctx.moveTo(x + 20, y - 8)
    ctx.lineTo(x + 30, y)
    ctx.stroke()
    return
  }
  ctx.fillStyle = '#6a3f23'
  roundRect(x - 28, y - 42, 56, 34, 7)
  ctx.fill()
  ctx.fillStyle = '#9a5a2e'
  roundRect(x - 30, y - 54, 60, 20, 8)
  ctx.fill()
  ctx.fillStyle = '#ffca55'
  ctx.fillRect(x - 5, y - 44, 10, 16)
  ctx.strokeStyle = '#ffca55'
  ctx.lineWidth = 3
  ctx.beginPath()
  ctx.moveTo(x - 26, y - 35)
  ctx.lineTo(x + 26, y - 35)
  ctx.stroke()
  ctx.fillStyle = '#1a1511'
  ctx.fillRect(x - 16, y - 29, 5, 5)
  ctx.fillRect(x + 11, y - 29, 5, 5)
  ctx.strokeStyle = '#d9d1c3'
  ctx.lineWidth = 3
  ctx.beginPath()
  ctx.moveTo(x - 20, y - 8)
  ctx.lineTo(x - 30, y)
  ctx.moveTo(x + 20, y - 8)
  ctx.lineTo(x + 30, y)
  ctx.stroke()
}

function monsterColor(name) {
  if (name.includes('mimic')) return '#b77936'
  if (name.includes('bat') || name.includes('wisp')) return '#7484d6'
  if (name.includes('guard') || name.includes('knight')) return '#9a8c7a'
  if (name.includes('crystal')) return '#69c6d7'
  if (name.includes('harpy')) return '#d79863'
  if (name.includes('slime')) return '#5db7a3'
  return '#728e42'
}

function drawHealthBar(x, y, width, height, hp, maxHp, color) {
  const ratio = Math.max(0, Math.min(1, hp / Math.max(1, maxHp)))
  ctx.fillStyle = 'rgba(12,18,16,0.72)'
  roundRect(x, y, width, height, height / 2)
  ctx.fill()
  ctx.fillStyle = color
  roundRect(x, y, width * ratio, height, height / 2)
  ctx.fill()
}

function drawRidge(width, baseY, offsets) {
  ctx.beginPath()
  ctx.moveTo(0, baseY)
  const step = width / (offsets.length - 1)
  offsets.forEach((offset, index) => ctx.lineTo(index * step, baseY - offset))
  ctx.lineTo(width, baseY + 120)
  ctx.lineTo(0, baseY + 120)
  ctx.closePath()
  ctx.fill()
}

function drawCloud(x, y, scale) {
  ctx.beginPath()
  ctx.arc(x, y, 15 * scale, 0, Math.PI * 2)
  ctx.arc(x + 20 * scale, y - 7 * scale, 21 * scale, 0, Math.PI * 2)
  ctx.arc(x + 44 * scale, y, 16 * scale, 0, Math.PI * 2)
  ctx.fill()
}

function drawFloatingIsland(x, y, scale) {
  ctx.fillStyle = '#638a46'
  ctx.beginPath()
  ctx.ellipse(x, y, 42 * scale, 14 * scale, 0, 0, Math.PI * 2)
  ctx.fill()
  ctx.fillStyle = '#5b412f'
  ctx.beginPath()
  ctx.moveTo(x - 32 * scale, y + 7 * scale)
  ctx.lineTo(x, y + 45 * scale)
  ctx.lineTo(x + 34 * scale, y + 7 * scale)
  ctx.closePath()
  ctx.fill()
}

function drawStalactites(width) {
  ctx.fillStyle = '#29242a'
  for (let x = 0; x < width + 80; x += 78) {
    ctx.beginPath()
    ctx.moveTo(x, 0)
    ctx.lineTo(x + 28, 0)
    ctx.lineTo(x + 14, 62 + (x % 3) * 16)
    ctx.closePath()
    ctx.fill()
  }
}

function drawCastleWall(width, height) {
  ctx.fillStyle = 'rgba(45, 48, 54, 0.72)'
  for (let x = -40; x < width + 80; x += 90) {
    ctx.fillRect(x, height * 0.28, 70, height * 0.38)
    ctx.fillStyle = 'rgba(255, 202, 85, 0.18)'
    ctx.fillRect(x + 22, height * 0.38, 18, 42)
    ctx.fillStyle = 'rgba(45, 48, 54, 0.72)'
  }
}

function drawPine(x, y, scale) {
  ctx.fillStyle = '#4a3321'
  ctx.fillRect(x - 4 * scale, y - 58 * scale, 8 * scale, 58 * scale)
  ctx.fillStyle = '#1f5a3d'
  triangle(x, y - 112 * scale, 42 * scale, 64 * scale)
  ctx.fillStyle = '#2f8052'
  triangle(x, y - 72 * scale, 54 * scale, 64 * scale)
}

function drawOak(x, y, scale) {
  ctx.fillStyle = '#5a3924'
  ctx.fillRect(x - 5 * scale, y - 68 * scale, 10 * scale, 68 * scale)
  ctx.fillStyle = '#2f7444'
  ctx.beginPath()
  ctx.arc(x, y - 82 * scale, 32 * scale, 0, Math.PI * 2)
  ctx.arc(x - 24 * scale, y - 68 * scale, 22 * scale, 0, Math.PI * 2)
  ctx.arc(x + 24 * scale, y - 68 * scale, 24 * scale, 0, Math.PI * 2)
  ctx.fill()
}

function drawFern(x, y, scale) {
  ctx.strokeStyle = '#6ab04c'
  ctx.lineWidth = 3 * scale
  for (let i = -2; i <= 2; i += 1) {
    ctx.beginPath()
    ctx.moveTo(x, y)
    ctx.quadraticCurveTo(x + i * 8 * scale, y - 18 * scale, x + i * 18 * scale, y - 30 * scale)
    ctx.stroke()
  }
}

function drawStump(x, y, scale) {
  ctx.fillStyle = '#7a4b2a'
  ctx.fillRect(x - 14 * scale, y - 22 * scale, 28 * scale, 22 * scale)
  ctx.fillStyle = '#ad7744'
  ctx.beginPath()
  ctx.ellipse(x, y - 22 * scale, 15 * scale, 7 * scale, 0, 0, Math.PI * 2)
  ctx.fill()
}

function drawMushrooms(x, y, scale) {
  drawMushroom(x - 9 * scale, y, scale, '#d95043')
  drawMushroom(x + 8 * scale, y + 1 * scale, scale * 0.9, '#d9b342')
}

function drawMushroom(x, y, scale, color) {
  ctx.fillStyle = '#f4d9af'
  ctx.fillRect(x - 3 * scale, y - 12 * scale, 6 * scale, 12 * scale)
  ctx.fillStyle = color
  ctx.beginPath()
  ctx.arc(x, y - 12 * scale, 10 * scale, Math.PI, 0)
  ctx.closePath()
  ctx.fill()
}

function drawCrystal(x, y, scale) {
  ctx.fillStyle = 'rgba(108, 207, 232, 0.7)'
  ctx.beginPath()
  ctx.moveTo(x, y - 48 * scale)
  ctx.lineTo(x + 18 * scale, y - 15 * scale)
  ctx.lineTo(x + 8 * scale, y)
  ctx.lineTo(x - 12 * scale, y)
  ctx.lineTo(x - 20 * scale, y - 18 * scale)
  ctx.closePath()
  ctx.fill()
}

function drawStone(x, y, scale) {
  ctx.fillStyle = '#4b4650'
  ctx.beginPath()
  ctx.ellipse(x, y - 16 * scale, 24 * scale, 16 * scale, 0, 0, Math.PI * 2)
  ctx.fill()
}

function drawCastleDecor(x, y, scale, kind) {
  if (kind === 'banner' || kind === 'torch') {
    ctx.fillStyle = kind === 'torch' ? '#ffb347' : '#7c2f43'
    ctx.fillRect(x - 7 * scale, y - 62 * scale, 14 * scale, 42 * scale)
  } else {
    ctx.fillStyle = '#6a6668'
    ctx.fillRect(x - 22 * scale, y - 64 * scale, 44 * scale, 64 * scale)
    ctx.fillStyle = '#2e2d32'
    ctx.fillRect(x - 10 * scale, y - 38 * scale, 20 * scale, 38 * scale)
  }
}

function triangle(x, y, width, height) {
  ctx.beginPath()
  ctx.moveTo(x, y)
  ctx.lineTo(x - width / 2, y + height)
  ctx.lineTo(x + width / 2, y + height)
  ctx.closePath()
  ctx.fill()
}

function roundRect(x, y, width, height, radius) {
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

function centeredText(width, height, text) {
  ctx.fillStyle = 'rgba(12,18,16,0.62)'
  roundRect(width / 2 - 90, height / 2 - 22, 180, 44, 8)
  ctx.fill()
  ctx.fillStyle = '#f5ecd6'
  ctx.font = '16px sans-serif'
  ctx.textAlign = 'center'
  ctx.fillText(text, width / 2, height / 2 + 6)
}

function worldX(x, cameraX, worldScale) {
  return Math.round((x - cameraX) * worldScale + 56)
}

els.enterRiftButton.addEventListener('click', () => {
  const snapshot = state.snapshot
  if (!snapshot) {
    return
  }
  postAction('/rift/enter', { floor: snapshot.rift.unlocked_floor }, '进入秘境')
})

els.leaveRiftButton.addEventListener('click', () => {
  postAction('/rift/leave', {}, '已离开秘境')
})

els.tickButton.addEventListener('click', () => tick(10))

els.equipBestButton.addEventListener('click', () => {
  postAction('/equip-best', {}, '已自动装备')
})

els.resetButton.addEventListener('click', () => {
  postAction('/reset', {}, '已重置')
})

els.inventoryList.addEventListener('click', (event) => {
  const button = event.target.closest('button')
  if (!button) {
    return
  }
  const action = button.dataset.action
  const itemId = button.dataset.id
  if (action === 'equip') {
    postAction('/equip-item', { item_id: itemId }, '已穿戴')
  }
  if (action === 'list') {
    const defaultPrice = button.dataset.price || '30'
    const price = window.prompt('挂售价格', defaultPrice)
    const parsed = Number.parseInt(price, 10)
    if (Number.isFinite(parsed) && parsed > 0) {
      postAction('/market/list', { item_id: itemId, price: parsed }, '已挂售')
    }
  }
})

els.talentList.addEventListener('click', (event) => {
  const button = event.target.closest('button[data-action="evolve-talent"]')
  if (!button || button.disabled) {
    return
  }
  postAction('/talent/evolve', { talent_id: button.dataset.id }, '天赋已进化')
})

els.marketList.addEventListener('click', (event) => {
  const button = event.target.closest('button[data-action="buy"]')
  if (!button || button.disabled) {
    return
  }
  postAction('/market/buy', { listing_id: button.dataset.id }, '购买成功')
})

window.addEventListener('resize', resizeCanvas)
resizeCanvas()
refresh()
window.requestAnimationFrame(draw)
setInterval(() => tick(1), 1000)
