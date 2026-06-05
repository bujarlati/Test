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

const FALLBACK_GEAR_PALETTES = {
  white: { primary: '#d8dde4', accent: '#8f9aa4', glow: '#d8dde4' },
  green: { primary: '#5fd18b', accent: '#2f8f5c', glow: '#36b37e' },
  blue: { primary: '#68b7ff', accent: '#2b78c2', glow: '#2684ff' },
  purple: { primary: '#b779ff', accent: '#7543bd', glow: '#9b5cff' },
  gold: { primary: '#ffdc7d', accent: '#b98221', glow: '#ffca55' },
  red: { primary: '#ff7a7c', accent: '#9e2e3a', glow: '#ff4d4f' }
}

const PROFILE_STORAGE_KEY = 'idleForestProfile'
const SETTINGS_STORAGE_KEY = 'idleForestSettings'
const SIMULATION_STEP_SECONDS = 0.125
const SIMULATION_TICK_MS = 125
const VISUAL_SNAP_DISTANCE = 96
const CAMERA_DAMPING = 18
const LOOT_FLOAT_DURATION_MS = 2400
const ATTACK_EFFECT_DURATION_MS = 520
const DEFAULT_SETTINGS = {
  paused: false,
  volume: 0.7,
  language: 'zh-CN'
}

const UI_TEXT = {
  'zh-CN': {
    settings: '设置',
    close: '关闭',
    newCharacter: '新角色',
    gold: '金币',
    level: '等级',
    exp: '经验',
    hp: '生命',
    attack: '攻击',
    defense: '防御',
    attackSpeed: '攻速',
    hpRegen: '回复',
    power: '战力',
    seconds: '秒',
    forest: '森林',
    deepForest: '深林',
    idle: '挂机中',
    connecting: '连接中',
    waitingCreate: '等待创建角色',
    loadingLocal: '读取本地角色',
    connected: '已连接',
    recommendedPower: '推荐战力',
    normalIdle: '普通挂机',
    enterRift: '进入秘境',
    leaveRift: '离开秘境',
    pushTen: '推进 10 秒',
    deepenForest: '深入森林',
    continueDeepen: '继续深入',
    retreatForest: '远离森林',
    equipBest: '自动装备',
    reset: '重置',
    pauseLabel: '暂停',
    paused: '已暂停',
    resumed: '继续冒险',
    volume: '音量',
    language: '语言',
    emptySlot: '空缺',
    waitingDrop: '等待掉落',
    noEquipment: '暂无装备',
    emptyInventory: '背包是空的，继续砍怪试试。',
    equip: '穿戴',
    list: '挂售',
    marketEmpty: '暂无挂单',
    mine: '我的挂单',
    buy: '购买',
    score: '评分',
    priceGold: '金',
    specialSet: '特殊套装',
    catalog: '目录',
    perLevel: '每级 150 点经验',
    talentScrolls: '卷轴',
    noTalents: '暂无天赋',
    evolve: '进化',
    maxed: '已绝世',
    randomTheme: '随机主题',
    rift: '秘境',
    minion: '小怪',
    reviveIn: '复活中',
    lootFallback: '掉落',
    nameRequired: '请输入角色名',
    rollFirst: '请先 Roll 天赋',
    rollPrompt: '先 Roll 一组天赋',
    rolled: '已 Roll 出初始天赋',
    createSuccess: '已创建角色',
    createFail: '创建失败',
    rollFail: 'Roll 失败',
    profileInvalid: '本地角色失效，请重新创建',
    resetConfirm: '重新创建角色会清除当前本地角色。继续吗？',
    listPrice: '挂售价格',
    actionFail: '操作失败'
  },
  'en-US': {
    settings: 'Settings',
    close: 'Close',
    newCharacter: 'New Hero',
    gold: 'Gold',
    level: 'Level',
    exp: 'EXP',
    hp: 'HP',
    attack: 'Attack',
    defense: 'Defense',
    attackSpeed: 'Atk Speed',
    hpRegen: 'Regen',
    power: 'Power',
    seconds: 'sec',
    forest: 'Forest',
    deepForest: 'Deep Forest',
    idle: 'Idling',
    connecting: 'Connecting',
    waitingCreate: 'Create a hero',
    loadingLocal: 'Loading local hero',
    connected: 'Connected',
    recommendedPower: 'Recommended Power',
    normalIdle: 'Forest idle',
    enterRift: 'Enter Rift',
    leaveRift: 'Leave Rift',
    pushTen: 'Advance 10s',
    deepenForest: 'Go Deeper',
    continueDeepen: 'Go Deeper',
    retreatForest: 'Retreat',
    equipBest: 'Equip Best',
    reset: 'Reset',
    pauseLabel: 'Pause',
    paused: 'Paused',
    resumed: 'Adventure resumed',
    volume: 'Volume',
    language: 'Language',
    emptySlot: 'Empty',
    waitingDrop: 'Waiting for drop',
    noEquipment: 'No gear equipped',
    emptyInventory: 'Inventory is empty. Keep fighting.',
    equip: 'Equip',
    list: 'List',
    marketEmpty: 'No listings',
    mine: 'My listing',
    buy: 'Buy',
    score: 'Score',
    priceGold: 'g',
    specialSet: 'Special Set',
    catalog: 'Catalog',
    perLevel: '150 EXP per level',
    talentScrolls: 'Scrolls',
    noTalents: 'No talents',
    evolve: 'Evolve',
    maxed: 'Mythic',
    randomTheme: 'Random theme',
    rift: 'Rift',
    minion: 'Minion',
    reviveIn: 'Reviving',
    lootFallback: 'Loot',
    nameRequired: 'Enter a hero name',
    rollFirst: 'Roll talents first',
    rollPrompt: 'Roll a talent set first',
    rolled: 'Starting talents rolled',
    createSuccess: 'Hero created',
    createFail: 'Create failed',
    rollFail: 'Roll failed',
    profileInvalid: 'Local hero expired. Please create again.',
    resetConfirm: 'Creating a new hero clears the current local hero. Continue?',
    listPrice: 'Listing price',
    actionFail: 'Action failed'
  }
}

const state = {
  snapshot: null,
  previousSnapshot: null,
  settings: { ...DEFAULT_SETTINGS },
  equipmentTranslations: {},
  tickInFlight: false,
  gameReady: false,
  selectedGender: 'male',
  creationDraft: null,
  tickTimer: null,
  lastRenderAt: 0,
  loadedAssets: 0,
  lootFloaters: [],
  seenLootEventKeys: new Set(),
  attackEffects: [],
  seenAttackEventKeys: new Set(),
  visual: {
    entities: [],
    cameraX: 0,
    cameraY: 0,
    ready: false,
    cameraReady: false
  }
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
  expText: document.querySelector('#expText'),
  expProgressBar: document.querySelector('#expProgressBar'),
  hpText: document.querySelector('#hpText'),
  attackText: document.querySelector('#attackText'),
  defenseText: document.querySelector('#defenseText'),
  attackSpeedText: document.querySelector('#attackSpeedText'),
  hpRegenText: document.querySelector('#hpRegenText'),
  powerText: document.querySelector('#powerText'),
  modeText: document.querySelector('#modeText'),
  riftStateText: document.querySelector('#riftStateText'),
  enterRiftButton: document.querySelector('#enterRiftButton'),
  leaveRiftButton: document.querySelector('#leaveRiftButton'),
  reviveText: document.querySelector('#reviveText'),
  tickButton: document.querySelector('#tickButton'),
  deepenForestButton: document.querySelector('#deepenForestButton'),
  retreatForestButton: document.querySelector('#retreatForestButton'),
  equipBestButton: document.querySelector('#equipBestButton'),
  resetButton: document.querySelector('#resetButton'),
  settingsButton: document.querySelector('#settingsButton'),
  settingsPanel: document.querySelector('#settingsPanel'),
  settingsCloseButton: document.querySelector('#settingsCloseButton'),
  pauseToggle: document.querySelector('#pauseToggle'),
  volumeSlider: document.querySelector('#volumeSlider'),
  languageSelect: document.querySelector('#languageSelect'),
  newCharacterButton: document.querySelector('#newCharacterButton'),
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
  equipmentSlotList: document.querySelector('#equipmentSlotList'),
  equippedList: document.querySelector('#equippedList'),
  inventoryList: document.querySelector('#inventoryList'),
  marketList: document.querySelector('#marketList'),
  eventList: document.querySelector('#eventList'),
  profileGate: document.querySelector('#profileGate'),
  profileAvatar: document.querySelector('#profileAvatar'),
  characterNameInput: document.querySelector('#characterNameInput'),
  genderMaleButton: document.querySelector('#genderMaleButton'),
  genderFemaleButton: document.querySelector('#genderFemaleButton'),
  rollTalentButton: document.querySelector('#rollTalentButton'),
  confirmCharacterButton: document.querySelector('#confirmCharacterButton'),
  rollCountText: document.querySelector('#rollCountText'),
  creationTalentList: document.querySelector('#creationTalentList'),
  profileStatusText: document.querySelector('#profileStatusText')
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

function currentLanguage() {
  return state.settings.language === 'en-US' ? 'en-US' : 'zh-CN'
}

function t(key) {
  const lang = currentLanguage()
  return (UI_TEXT[lang] && UI_TEXT[lang][key]) || UI_TEXT['zh-CN'][key] || key
}

function loadStoredSettings() {
  try {
    const raw = window.localStorage.getItem(SETTINGS_STORAGE_KEY)
    const parsed = raw ? (JSON.parse(raw) || {}) : {}
    return {
      ...DEFAULT_SETTINGS,
      ...parsed,
      language: parsed.language === 'en-US' ? 'en-US' : 'zh-CN',
      volume: Number.isFinite(Number(parsed.volume)) ? clamp(Number(parsed.volume), 0, 1) : DEFAULT_SETTINGS.volume
    }
  } catch (error) {
    return { ...DEFAULT_SETTINGS }
  }
}

function saveSettings() {
  window.localStorage.setItem(SETTINGS_STORAGE_KEY, JSON.stringify(state.settings))
}

function applySettings() {
  if (els.pauseToggle) {
    els.pauseToggle.checked = Boolean(state.settings.paused)
  }
  if (els.volumeSlider) {
    els.volumeSlider.value = String(Math.round(Number(state.settings.volume || 0) * 100))
  }
  if (els.languageSelect) {
    els.languageSelect.value = currentLanguage()
  }
  document.documentElement.lang = currentLanguage()
  setMasterVolume(state.settings.volume)
  applyStaticTranslations()
  if (state.snapshot) {
    applySnapshot(state.snapshot)
  }
  setStatus(state.settings.paused ? t('paused') : statusForSnapshot(state.snapshot), true)
}

function applyStaticTranslations() {
  setText('#settingsButton', t('settings'))
  setText('#settingsTitle', t('settings'))
  setText('#settingsCloseButton', t('close'))
  setText('#newCharacterButton', t('newCharacter'))
  setText('.resource small', t('gold'))
  setText('.hero-strip .stat:nth-child(1) span', t('level'))
  setText('.hero-strip .stat:nth-child(2) span', t('exp'))
  setText('.hero-strip .stat:nth-child(3) span', t('hp'))
  setText('.hero-strip .stat:nth-child(4) span', t('attack'))
  setText('.hero-strip .stat:nth-child(5) span', t('defense'))
  setText('.hero-strip .stat:nth-child(6) span', t('attackSpeed'))
  setText('.hero-strip .stat:nth-child(7) span', t('hpRegen'))
  setText('.hero-strip .stat:nth-child(8) span', t('power'))
  setText('#tickButton', t('pushTen'))
  setText('#equipBestButton', t('equipBest'))
  setText('#resetButton', t('reset'))
  setText('#rollTalentButton', currentLanguage() === 'zh-CN' ? 'Roll 天赋' : 'Roll Talents')
  setText('#confirmCharacterButton', currentLanguage() === 'zh-CN' ? '确认角色' : 'Confirm Hero')
  const rows = document.querySelectorAll('.setting-row span')
  if (rows[0]) rows[0].textContent = t('pauseLabel')
  if (rows[1]) rows[1].textContent = t('volume')
  if (rows[2]) rows[2].textContent = t('language')
  if (els.rollCountText && !state.creationDraft) {
    els.rollCountText.textContent = remainingRollsText(3)
  }
  if (state.creationDraft) {
    els.rollCountText.textContent = remainingRollsText(state.creationDraft.rolls_remaining || 0)
    renderCreationTalents(state.creationDraft.talents || [])
  } else if (els.creationTalentList && els.profileGate && !els.profileGate.classList.contains('hidden')) {
    renderCreationTalents()
  }
}

function setText(selector, text) {
  const element = document.querySelector(selector)
  if (element) {
    element.textContent = text
  }
}

function toggleSettingsPanel(show) {
  if (!els.settingsPanel) {
    return
  }
  els.settingsPanel.classList.toggle('hidden', !show)
  els.settingsPanel.setAttribute('aria-hidden', show ? 'false' : 'true')
}

function togglePause(paused) {
  state.settings.paused = Boolean(paused)
  saveSettings()
  applySettings()
}

function setMasterVolume(value) {
  const volume = clamp(Number(value), 0, 1)
  state.settings.volume = volume
  document.documentElement.style.setProperty('--master-volume', String(volume))
}

function loadEquipmentTranslations() {
  return fetch('/web/i18n/equipment.json')
    .then((response) => response.ok ? response.json() : {})
    .then((translations) => {
      state.equipmentTranslations = translations || {}
      if (state.snapshot) {
        applySnapshot(state.snapshot)
      }
    })
    .catch(() => {
      state.equipmentTranslations = {}
    })
}

function translateItemName(itemOrName) {
  const name = typeof itemOrName === 'string' ? itemOrName : itemOrName && itemOrName.name
  if (!name) {
    return ''
  }
  const exact = translateEquipmentTerm(name)
  if (exact !== name) {
    return exact
  }
  const match = String(name).match(/^(.+?)\s+Lv\.(\d+)$/)
  if (!match) {
    return name
  }
  const translatedBase = match[1]
    .split(/\s+/)
    .map((part) => translateEquipmentTerm(part))
    .join(currentLanguage() === 'zh-CN' ? '' : ' ')
  return `${translatedBase} Lv.${match[2]}`
}

function translateEquipmentTerm(term) {
  const entry = state.equipmentTranslations[String(term)] || null
  if (!entry) {
    return String(term)
  }
  return entry[currentLanguage()] || entry['zh-CN'] || entry['en-US'] || String(term)
}

function translateEventMessage(event) {
  if (isLootEvent(event)) {
    const data = event.data || {}
    return `+1 ${translateItemName(data.item_name || event.message || t('lootFallback'))}`
  }
  return event.message
}

function clamp(value, min, max) {
  if (!Number.isFinite(value)) {
    return min
  }
  return Math.max(min, Math.min(max, value))
}

function setStatus(text, online = true) {
  els.statusText.textContent = text
  els.statusText.style.color = online ? '#9fb0a6' : '#ff9f7f'
}

function statusForSnapshot(snapshot) {
  if (snapshot && snapshot.hero && snapshot.hero.reviving) {
    return `${t('reviveIn')} ${Math.ceil(Number(snapshot.hero.revive_remaining || 0))} ${t('seconds')}`
  }
  if (snapshot && snapshot.mode === 'rift') {
    return `${t('rift')} ${t('idle')}`
  }
  const depth = Number(snapshot && snapshot.forest && snapshot.forest.depth)
  return depth > 1 ? `${t('deepForest')} ${depth}` : t('idle')
}

function refresh() {
  return api('/snapshot')
    .then((snapshot) => {
      applySnapshot(snapshot)
      setStatus(statusForSnapshot(snapshot))
    })
    .catch((error) => {
      setStatus(error.message || t('actionFail'), false)
    })
}

function tick(seconds = 1) {
  if (!state.gameReady || state.tickInFlight || state.settings.paused) {
    return Promise.resolve()
  }
  state.tickInFlight = true
  return api('/tick', {
    method: 'POST',
    body: { seconds }
  })
    .then((snapshot) => {
      applySnapshot(snapshot)
      setStatus(statusForSnapshot(snapshot))
    })
    .catch((error) => {
      setStatus(error.message || t('actionFail'), false)
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
      const snapshot = result.snapshot || result
      applySnapshot(snapshot)
      setStatus(snapshot.hero && snapshot.hero.reviving ? statusForSnapshot(snapshot) : statusText)
    })
    .catch((error) => {
      setStatus(error.message || t('actionFail'), false)
    })
}

function loadStoredProfile() {
  try {
    const raw = window.localStorage.getItem(PROFILE_STORAGE_KEY)
    return raw ? JSON.parse(raw) : null
  } catch (error) {
    return null
  }
}

function saveStoredProfile(profile) {
  window.localStorage.setItem(PROFILE_STORAGE_KEY, JSON.stringify(profile))
}

function clearStoredProfile() {
  window.localStorage.removeItem(PROFILE_STORAGE_KEY)
}

function setProfileStatus(text, ok = true) {
  els.profileStatusText.textContent = text
  els.profileStatusText.style.color = ok ? '#9fb0a6' : '#ff9f7f'
}

function remainingRollsText(count) {
  return currentLanguage() === 'zh-CN' ? `剩余 ${count} 次` : `${count} rolls left`
}

function showProfileGate(show) {
  els.profileGate.classList.toggle('hidden', !show)
}

function setGender(gender) {
  state.selectedGender = gender
  els.genderMaleButton.classList.toggle('active', gender === 'male')
  els.genderFemaleButton.classList.toggle('active', gender === 'female')
  els.profileAvatar.classList.toggle('female', gender === 'female')
}

function profileName() {
  return els.characterNameInput.value.trim()
}

function renderCreationTalents(talents = []) {
  if (!talents.length) {
    els.creationTalentList.innerHTML = `<div class="empty">${t('rollPrompt')}</div>`
    return
  }
  els.creationTalentList.innerHTML = talents
    .map((talent) => `
      <article class="creation-talent tier-${talent.tier}">
        <div class="item-main">
          <span class="item-name">${escapeHtml(talent.name)}</span>
          <span class="talent-tier">${talentTierLabel(talent.tier)}</span>
        </div>
        <div class="item-sub">${escapeHtml(talent.description)} · ${effectLine(talent.effects)}</div>
      </article>
    `)
    .join('')
}

function rollCreationTalents() {
  const name = profileName()
  if (!name) {
    setProfileStatus(t('nameRequired'), false)
    return
  }
  els.rollTalentButton.disabled = true
  api('/profile/roll', {
    method: 'POST',
    body: { name, gender: state.selectedGender }
  })
    .then((draft) => {
      state.creationDraft = draft
      renderCreationTalents(draft.talents || [])
      els.rollCountText.textContent = remainingRollsText(draft.rolls_remaining)
      els.rollTalentButton.disabled = draft.rolls_remaining <= 0
      els.confirmCharacterButton.disabled = false
      setProfileStatus(t('rolled'))
    })
    .catch((error) => {
      setProfileStatus(error.message || t('rollFail'), false)
      els.rollTalentButton.disabled = false
    })
}

function confirmCharacter() {
  const draft = state.creationDraft
  if (!draft || !draft.talents || draft.talents.length !== 3) {
    setProfileStatus(t('rollFirst'), false)
    return
  }
  const profile = {
    name: draft.name,
    gender: draft.gender,
    talent_ids: draft.talents.map((talent) => talent.id),
    talents: draft.talents
  }
  els.confirmCharacterButton.disabled = true
  api('/profile/confirm', {
    method: 'POST',
    body: {
      name: profile.name,
      gender: profile.gender,
      talent_ids: profile.talent_ids
    }
  })
    .then((result) => {
      saveStoredProfile(profile)
      startGame(result.snapshot)
      setStatus(t('createSuccess'))
    })
    .catch((error) => {
      setProfileStatus(error.message || t('createFail'), false)
      els.confirmCharacterButton.disabled = false
    })
}

function startGame(snapshot) {
  state.gameReady = true
  showProfileGate(false)
  if (snapshot) {
    applySnapshot(snapshot)
  }
  if (!state.tickTimer) {
    state.tickTimer = window.setInterval(() => tick(SIMULATION_STEP_SECONDS), SIMULATION_TICK_MS)
  }
}

function stopGameLoop() {
  state.gameReady = false
  if (state.tickTimer) {
    window.clearInterval(state.tickTimer)
    state.tickTimer = null
  }
  resetVisualSmoothing()
}

function resetVisualSmoothing() {
  state.visual.entities = []
  state.visual.cameraX = 0
  state.visual.cameraY = 0
  state.visual.ready = false
  state.visual.cameraReady = false
  state.lootFloaters = []
  state.seenLootEventKeys = new Set()
  state.attackEffects = []
  state.seenAttackEventKeys = new Set()
  state.lastRenderAt = 0
}

function bootstrapProfile() {
  renderCreationTalents()
  const stored = loadStoredProfile()
  if (!stored || !stored.talent_ids) {
    showProfileGate(true)
    setStatus(t('waitingCreate'))
    return Promise.resolve()
  }
  setStatus(t('loadingLocal'))
  return api('/profile/confirm', {
    method: 'POST',
    body: {
      name: stored.name,
      gender: stored.gender,
      talent_ids: stored.talent_ids
    }
  })
    .then((result) => {
      startGame(result.snapshot)
      setStatus(t('connected'))
    })
    .catch((error) => {
      clearStoredProfile()
      showProfileGate(true)
      setProfileStatus(error.message || t('profileInvalid'), false)
      setStatus(t('waitingCreate'), false)
    })
}

function applySnapshot(snapshot) {
  state.previousSnapshot = state.snapshot
  state.snapshot = snapshot
  snapVisualStateToSnapshot(snapshot)
  trackLootFloaters(snapshot.events || [], snapshot.scene)
  trackAttackEffects(snapshot.events || [], snapshot.scene)
  const hero = snapshot.hero
  const rift = snapshot.rift
  const treasure = snapshot.treasure || {}
  const forest = snapshot.forest || {}
  const forestDepth = Number(forest.depth || (snapshot.scene && snapshot.scene.forest_depth) || 1)
  const active = rift.active
  const minionsRequired = active ? rift.minions_required : 0
  const minionsDefeated = active ? rift.minions_defeated : 0
  const progress = active
    ? (rift.state === 'boss' ? 100 : Math.round((minionsDefeated / Math.max(1, minionsRequired)) * 72))
    : 0

  els.goldText.textContent = hero.gold
  els.levelText.textContent = hero.level
  els.expText.textContent = `${hero.exp} / ${hero.exp_to_next_level}`
  els.expProgressBar.style.width = `${Math.round((hero.exp_progress || 0) * 100)}%`
  els.hpText.textContent = `${hero.hp} / ${hero.max_hp}`
  els.attackText.textContent = hero.attack
  els.defenseText.textContent = hero.defense
  els.attackSpeedText.textContent = `${Number(hero.attack_speed || 0).toFixed(2)} / ${t('seconds')}`
  els.hpRegenText.textContent = `${Number(hero.hp_regen || 0).toFixed(1)} / ${t('seconds')}`
  els.powerText.textContent = forest.hero_power || rift.hero_power
  els.modeText.textContent = snapshot.mode === 'rift' ? t('rift') : forestDepth > 1 ? `${t('deepForest')} ${forestDepth}` : t('forest')
  els.riftStateText.textContent = describeRiftState(rift, forest, snapshot.mode)
  els.enterRiftButton.disabled = active
  els.enterRiftButton.textContent = `${t('enterRift')} ${rift.unlocked_floor}`
  els.leaveRiftButton.disabled = !active
  els.leaveRiftButton.textContent = t('leaveRift')
  els.deepenForestButton.disabled = active
  els.deepenForestButton.textContent = forestDepth > 1 ? `${t('continueDeepen')} ${forestDepth + 1}` : t('deepenForest')
  els.retreatForestButton.disabled = active || forestDepth <= 1
  els.retreatForestButton.textContent = forestDepth > 1 ? `${t('retreatForest')} ${forestDepth - 1}` : t('retreatForest')
  els.riftThemeText.textContent = active ? themeLabel(rift.theme) : t('randomTheme')
  els.unlockedFloorText.textContent = rift.unlocked_floor
  els.recommendedPowerText.textContent = snapshot.mode === 'rift' ? rift.recommended_power : (forest.recommended_power || rift.recommended_power)
  els.minionProgressText.textContent = active ? `${minionsDefeated} / ${minionsRequired}` : '-'
  els.riftProgressBar.style.width = `${progress}%`
  els.mimicPityText.textContent = `${treasure.mimics_defeated_since_red || 0} / ${treasure.pity_threshold || 0}`
  els.mimicPityBar.style.width = `${Math.round((treasure.pity_progress || 0) * 100)}%`
  els.mimicChanceText.textContent = `${((treasure.mimic_chance || 0) * 100).toFixed(1)}%`
  els.pityRemainingText.textContent = treasure.pity_remaining || treasure.pity_threshold || 0
  if (hero.reviving) {
    els.reviveText.textContent = `${t('reviveIn')} ${Math.ceil(Number(hero.revive_remaining || 0))} ${t('seconds')}`
    els.reviveText.classList.remove('hidden')
  } else {
    els.reviveText.classList.add('hidden')
  }

  renderEquipmentSlots(hero.equipment_slots || [], hero.equipped || {})
  renderEquipped(hero.equipped || {})
  renderTalents(hero.talents || [], hero.talent_scrolls || 0, snapshot.talent || {})
  renderInventory(hero.inventory || [])
  renderMarket((snapshot.market && snapshot.market.active) || [], hero.id)
  renderEvents(snapshot.events || [])
}

function describeRiftState(rift, forest, mode) {
  if (!rift.active) {
    const recommended = mode === 'rift' ? rift.recommended_power : (forest && forest.recommended_power) || rift.recommended_power
    return `${t('recommendedPower')} ${recommended}`
  }
  if (rift.state === 'boss') {
    return `${themeLabel(rift.theme)} ${rift.floor} Boss`
  }
  return `${themeLabel(rift.theme)} ${rift.floor} ${t('minion')} ${rift.minions_defeated}/${rift.minions_required}`
}

function renderTalents(talents, scrolls, talentMeta) {
  els.talentScrollText.textContent = `${t('talentScrolls')} ${scrolls}`
  els.talentCatalogText.textContent = `${t('catalog')} ${talentMeta.total_catalog_count || 0} · ${t('perLevel')}`
  if (!talents.length) {
    els.talentList.innerHTML = `<div class="empty">${t('noTalents')}</div>`
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
            <button data-action="evolve-talent" data-id="${talent.id}" ${disabled ? 'disabled' : ''}>${locked ? t('maxed') : t('evolve')}</button>
          </div>
        </article>
      `
    })
    .join('')
}

function renderEquipmentSlots(slots, equipped) {
  const normalized = slots.length
    ? slots
    : Object.keys(SLOT_LABELS).map((slot) => ({ slot, item: equipped[slot] || null }))
  els.equipmentSlotList.innerHTML = normalized
    .map(({ slot, item }) => {
      const empty = !item
      const itemName = item ? translateItemName(item) : ''
      return `
        <article class="equipment-slot ${empty ? 'empty-slot' : `rarity-${item.rarity}`}">
          <div class="slot-top">
            ${equipmentPreviewHtml(item)}
            <div class="slot-copy">
              <span class="slot-label">${slotLabel(slot)}</span>
              <span class="slot-state">${empty ? t('emptySlot') : escapeHtml(itemName)}</span>
              <span class="item-sub">${empty ? t('waitingDrop') : `${rarityLabel(item.rarity)} · Lv.${item.level}`}</span>
            </div>
          </div>
        </article>
      `
    })
    .join('')
}

function renderEquipped(equipped) {
  const items = Object.keys(equipped).map((slot) => equipped[slot])
  if (!items.length) {
    els.equippedList.innerHTML = `<div class="empty">${t('noEquipment')}</div>`
    return
  }
  const bonuses = (state.snapshot && state.snapshot.hero && state.snapshot.hero.set_bonuses) || []
  els.equippedList.innerHTML = items.map((item) => itemHtml(item, '')).join('') + renderSetBonuses(bonuses)
}

function renderInventory(items) {
  if (!items.length) {
    els.inventoryList.innerHTML = `<div class="empty">${t('emptyInventory')}</div>`
    return
  }
  els.inventoryList.innerHTML = items
    .map((item) => itemHtml(item, `
      <div class="item-actions">
        <button data-action="equip" data-id="${item.id}">${t('equip')}</button>
        <button class="muted" data-action="list" data-id="${item.id}" data-price="${Math.max(20, item.score * 2)}">${t('list')}</button>
      </div>
    `))
    .join('')
}

function renderMarket(listings, heroId) {
  if (!listings.length) {
    els.marketList.innerHTML = `<div class="empty">${t('marketEmpty')}</div>`
    return
  }
  els.marketList.innerHTML = listings
    .map((listing) => {
      const item = listing.item
      const own = listing.seller_id === heroId
      return `
        <article class="item rarity-${item.rarity}">
          <div class="item-visual">
              ${equipmentPreviewHtml(item)}
            <div class="item-copy">
              <div class="item-main">
                <span class="item-name">${escapeHtml(translateItemName(item))}</span>
                <span class="price">${listing.price} ${t('priceGold')}</span>
              </div>
              <div class="item-sub">${own ? t('mine') : listing.seller_id} · ${slotLabel(item.slot)} · ${t('score')} ${item.score}</div>
              ${specialLine(item)}
              <div class="item-actions">
                <button data-action="buy" data-id="${listing.id}" ${own ? 'disabled' : ''}>${t('buy')}</button>
              </div>
            </div>
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
    .map((event) => `<div class="event ${event.kind}">${escapeHtml(translateEventMessage(event))}</div>`)
    .join('')
}

function trackLootFloaters(events, scene) {
  if (!scene || !Array.isArray(events)) {
    return
  }
  const hero = (scene.entities || []).find((entity) => entity.type === 'hero')
  if (!hero || !hero.position) {
    return
  }
  events.forEach((event) => {
    if (!isLootEvent(event)) {
      return
    }
    const key = lootEventKey(event)
    if (state.seenLootEventKeys.has(key)) {
      return
    }
    state.seenLootEventKeys.add(key)
    if (!state.previousSnapshot) {
      return
    }
    state.lootFloaters.push({
      key,
      text: lootFloatText(event),
      rarity: (event.data && event.data.rarity) || 'white',
      x: Number(hero.position.x || 0) + 12,
      y: Number(hero.position.y || 0),
      createdAt: state.lastRenderAt || window.performance.now()
    })
  })
  if (state.seenLootEventKeys.size > 220) {
    state.seenLootEventKeys = new Set(Array.from(state.seenLootEventKeys).slice(-160))
  }
}

function isLootEvent(event) {
  return ['loot', 'rift_loot', 'special_loot', 'pity_special_loot'].includes(event.kind)
}

function lootEventKey(event) {
  const data = event.data || {}
  return `${event.tick}:${event.kind}:${data.item_id || event.message}`
}

function lootFloatText(event) {
  const data = event.data || {}
  return `+1 ${translateItemName(data.item_name || event.message || t('lootFallback'))}`
}

function trackAttackEffects(events, scene) {
  if (!scene || !Array.isArray(events)) {
    return
  }
  const hero = (scene.entities || []).find((entity) => entity.type === 'hero')
  const monster = (scene.entities || []).find((entity) => entity.type === 'monster')
  if (!hero || !hero.position) {
    return
  }
  events.forEach((event) => {
    if (event.kind !== 'hero_attack') {
      return
    }
    const key = attackEventKey(event)
    if (state.seenAttackEventKeys.has(key)) {
      return
    }
    state.seenAttackEventKeys.add(key)
    if (!state.previousSnapshot) {
      return
    }
    const weapon = hero.weapon || ((hero.equipped || {}).weapon)
    const targetX = monster && monster.position
      ? Number(monster.position.x || 0)
      : Number(hero.position.x || 0) + Number(hero.attack_range || 72)
    state.attackEffects.push({
      key,
      x: Number(hero.position.x || 0) + 24,
      y: Number(hero.position.y || 0),
      targetX,
      rarity: (weapon && weapon.rarity) || 'white',
      appearance: weapon ? equipmentAppearance(weapon) : null,
      damage: (event.data && event.data.damage) || 0,
      createdAt: state.lastRenderAt || window.performance.now()
    })
  })
  if (state.seenAttackEventKeys.size > 260) {
    state.seenAttackEventKeys = new Set(Array.from(state.seenAttackEventKeys).slice(-180))
  }
}

function attackEventKey(event) {
  const data = event.data || {}
  return `${event.tick}:${event.kind}:${data.monster_id || ''}:${data.damage || 0}`
}

function itemHtml(item, actions) {
  return `
    <article class="item rarity-${item.rarity}${item.special ? ' special' : ''}">
      <div class="item-visual">
        ${equipmentPreviewHtml(item)}
        <div class="item-copy">
          <div class="item-main">
            <span class="item-name">${escapeHtml(translateItemName(item))}</span>
            <span class="score">${item.score}</span>
          </div>
          <div class="item-sub">${itemStatLine(item)}</div>
          ${specialLine(item)}
          ${actions}
        </div>
      </div>
    </article>
  `
}

function equipmentPreviewHtml(item) {
  if (!item) {
    return '<span class="gear-preview gear-empty" aria-hidden="true"></span>'
  }
  const appearance = equipmentAppearance(item)
  const palette = appearance.palette || {}
  const style = [
    `--gear-primary:${safeColor(palette.primary, '#d8dde4')}`,
    `--gear-accent:${safeColor(palette.accent, '#8f9aa4')}`,
    `--gear-glow:${safeColor(palette.glow, '#d8dde4')}`
  ].join(';')
  const model = safeClassName(appearance.model)
  const slot = safeClassName(item.slot || appearance.slot)
  return `
    <span class="gear-preview gear-slot-${slot} gear-model-${model}${appearance.aura ? ' gear-aura' : ''}" style="${style}" aria-hidden="true">
      <span class="gear-core"></span>
      <span class="gear-edge"></span>
    </span>
  `
}

function equipmentAppearance(item) {
  if (item && item.appearance) {
    return item.appearance
  }
  const palette = FALLBACK_GEAR_PALETTES[(item && item.rarity) || 'white'] || FALLBACK_GEAR_PALETTES.white
  return {
    slot: (item && item.slot) || 'weapon',
    model: (item && item.weapon_type) || (item && item.slot) || 'blade',
    palette,
    aura: item && ['purple', 'gold', 'red'].includes(item.rarity),
    icon_shape: 'slash'
  }
}

function safeColor(value, fallback) {
  return /^#[0-9a-f]{3,6}$/i.test(String(value || '')) ? value : fallback
}

function safeClassName(value) {
  return String(value || 'gear').toLowerCase().replace(/[^a-z0-9_-]+/g, '-')
}

function itemStatLine(item) {
  const parts = [
    slotLabel(item.slot),
    rarityLabel(item.rarity),
    `Lv.${item.level}`,
    `${t('attack')} ${item.attack}`,
    `${t('defense')} ${item.defense}`,
    `${t('hp')} ${item.max_hp}`
  ]
  if (item.attack_speed) parts.push(`${t('attackSpeed')} ${Number(item.attack_speed).toFixed(2)}`)
  if (item.hp_regen) parts.push(`${t('hpRegen')} ${Number(item.hp_regen).toFixed(1)}`)
  if (item.attack_range) parts.push(`${currentLanguage() === 'zh-CN' ? '距离' : 'Range'} +${Number(item.attack_range).toFixed(0)}`)
  return parts.join(' · ')
}

function specialLine(item) {
  if (!item.special) {
    return ''
  }
  return `
    <div class="set-line">
      <span class="badge">${t('specialSet')}</span>
      ${escapeHtml(translateEquipmentTerm(item.set_name || 'Unknown Set'))} · ${escapeHtml(translateEquipmentTerm(item.set_piece || ''))}
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
        ${escapeHtml(translateEquipmentTerm(bonus.set_name || t('specialSet')))} ${bonus.pieces}/${bonus.pieces_required}
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
  if (bonus.attack) parts.push(`${t('attack')} +${bonus.attack}`)
  if (bonus.defense) parts.push(`${t('defense')} +${bonus.defense}`)
  if (bonus.max_hp) parts.push(`${t('hp')} +${bonus.max_hp}`)
  return parts.join(' · ')
}

function effectLine(effects) {
  return Object.keys(effects || {})
    .map((key) => `${effectLabel(key)} +${(effects[key] * 100).toFixed(1)}%`)
    .join(' · ')
}

function effectLabel(key) {
  if (currentLanguage() === 'en-US') {
    return {
      attack_pct: 'Attack',
      defense_pct: 'Defense',
      max_hp_pct: 'HP',
      move_speed_pct: 'Move Speed',
      drop_rate_pct: 'Drops',
      gold_pct: 'Gold',
      exp_pct: 'EXP',
      treasure_mimic_chance_pct: 'Mimic',
      rift_drop_rate_pct: 'Rift Drops',
      all_stats_pct: 'All Stats'
    }[key] || key
  }
  return EFFECT_LABELS[key] || key
}

function talentTierLabel(tier) {
  if (currentLanguage() === 'en-US') {
    return {
      common: 'Common',
      uncommon: 'Uncommon',
      excellent: 'Excellent',
      rare: 'Rare',
      transcendent: 'Transcendent',
      mythic: 'Mythic'
    }[tier] || tier
  }
  return TALENT_TIER_LABELS[tier] || tier
}

function slotLabel(slot) {
  if (currentLanguage() === 'en-US') {
    return {
      weapon: 'Weapon',
      helmet: 'Helmet',
      armor: 'Armor',
      boots: 'Boots',
      ring: 'Ring'
    }[slot] || slot
  }
  return SLOT_LABELS[slot] || slot
}

function rarityLabel(rarity) {
  if (currentLanguage() === 'en-US') {
    return {
      white: 'White',
      green: 'Green',
      blue: 'Blue',
      purple: 'Purple',
      gold: 'Gold',
      red: 'Red'
    }[rarity] || rarity
  }
  return RARITY_LABELS[rarity] || rarity
}

function themeLabel(theme) {
  if (currentLanguage() === 'en-US') {
    return {
      forest: 'Forest',
      deep_forest: 'Deep Forest',
      cave: 'Cave',
      sky: 'Sky',
      castle: 'Castle'
    }[theme] || theme
  }
  return {
    forest: '森林',
    deep_forest: '深林',
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

function drawBlendedSpriteBottom(a, b, centerX, bottomY, width, height, flip = false, speed = 260) {
  const amount = smoothstep(animationPhase(speed))
  const key = amount < 0.5 ? a : b
  return drawSpriteBottom(key, centerX, bottomY, width, height, flip)
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

function cloneEntity(entity) {
  return {
    ...entity,
    position: entity.position ? { ...entity.position } : entity.position
  }
}

function snapVisualStateToSnapshot(snapshot) {
  if (!snapshot || !snapshot.scene) {
    state.visual.ready = false
    state.visual.entities = []
    return
  }
  const currentEntities = state.visual.entities || []
  let shouldSnapCamera = !state.visual.ready
  state.visual.entities = (snapshot.scene.entities || []).map((entity) => {
    const current = currentEntities.find((candidate) => candidate.id === entity.id)
    const next = cloneEntity(entity)
    if (!current || !current.position || !next.position) {
      return next
    }
    const currentX = Number(current.position.x || 0)
    const nextX = Number(next.position.x || 0)
    if (Math.abs(nextX - currentX) > VISUAL_SNAP_DISTANCE) {
      if (entity.type === 'hero') {
        shouldSnapCamera = true
      }
      return next
    }
    next.position.x = currentX
    next.position.y = Number(current.position.y || next.position.y || 0)
    return next
  })
  state.visual.ready = true
  if (shouldSnapCamera) {
    const camera = snapshot.scene.camera || { x: 0, y: 0 }
    state.visual.cameraX = Number(camera.x || 0)
    state.visual.cameraY = Number(camera.y || 0)
    state.visual.cameraReady = true
  }
}

function advanceVisualState(seconds) {
  if (!state.visual.ready) {
    if (state.snapshot) {
      snapVisualStateToSnapshot(state.snapshot)
    }
    return
  }
  const hero = state.visual.entities.find((entity) => entity.type === 'hero')
  if (!hero || !hero.position) {
    return
  }
  const monster = state.visual.entities.find((entity) => entity.type === 'monster' && entity.position)
  const speed = Number((state.snapshot && state.snapshot.hero && state.snapshot.hero.speed) || hero.speed || 0)
  if ((hero.state === 'walk' || hero.state === 'approach') && Number.isFinite(speed) && speed > 0) {
    let nextX = Number(hero.position.x || 0) + speed * Math.max(0, seconds)
    if (monster) {
      const range = Number(hero.attack_range || (state.snapshot && state.snapshot.hero && state.snapshot.hero.attack_range) || 0)
      nextX = Math.min(nextX, Number(monster.position.x || nextX) - range)
    }
    const serverX = Number(state.snapshot && state.snapshot.hero && state.snapshot.hero.position && state.snapshot.hero.position.x)
    if (Number.isFinite(serverX)) {
      nextX = Math.min(nextX, serverX + VISUAL_SNAP_DISTANCE)
    }
    if (Number.isFinite(nextX)) {
      hero.position.x = Number(nextX.toFixed(3))
    }
  }
  applyCameraDamping(Math.max(0, Number(hero.position.x || 0) - 180), 0, seconds * 1000)
}

function visualSnapshot() {
  const snapshot = state.snapshot
  if (!snapshot || !snapshot.scene) {
    return snapshot
  }
  return {
    ...snapshot,
    scene: {
      ...snapshot.scene,
      camera: {
        ...(snapshot.scene.camera || {}),
        x: state.visual.cameraX,
        y: state.visual.cameraY
      },
      entities: (state.visual.entities || []).map(cloneEntity)
    }
  }
}

function applyCameraDamping(targetX, targetY, frameDelta) {
  if (!state.visual.cameraReady) {
    state.visual.cameraX = targetX
    state.visual.cameraY = targetY
    state.visual.cameraReady = true
  } else {
    const amount = 1 - Math.exp(-(Math.max(0, frameDelta) / 1000) * CAMERA_DAMPING)
    state.visual.cameraX = lerp(state.visual.cameraX, targetX, amount)
    state.visual.cameraY = lerp(state.visual.cameraY, targetY, amount)
  }
}

function smoothstep(value) {
  return value * value * (3 - 2 * value)
}

function lerp(a, b, amount) {
  return a + (b - a) * amount
}

function draw(timestamp) {
  const previousRenderAt = state.lastRenderAt || timestamp
  const frameDelta = Math.min(50, Math.max(0, timestamp - previousRenderAt))
  state.lastRenderAt = timestamp
  const rect = canvas.getBoundingClientRect()
  advanceVisualState(frameDelta / 1000)
  renderScene(visualSnapshot(), rect.width, rect.height)
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
    drawCombatRange(scene.entities || [], cameraX, groundY, worldScale)
    drawEntities(scene.entities || [], cameraX, groundY, worldScale)
    drawAttackEffects(scene, cameraX, groundY, worldScale)
    drawLootFloaters(scene, cameraX, groundY, worldScale)
  } else {
    drawGround('forest', width, height, groundY, 0, worldScale)
    centeredText(width, height, '等待后端连接')
  }
}

function drawCombatRange(entities, cameraX, groundY, worldScale) {
  const hero = entities.find((entity) => entity.type === 'hero')
  const monster = entities.find((entity) => entity.type === 'monster')
  if (!hero || !monster || !hero.attack_range) {
    return
  }
  const start = worldX(hero.position.x, cameraX, worldScale)
  const end = worldX(Number(hero.position.x) + Number(hero.attack_range), cameraX, worldScale)
  ctx.save()
  const width = Math.max(18, end - start - 20)
  const gradient = ctx.createLinearGradient(start + 18, 0, end, 0)
  gradient.addColorStop(0, 'rgba(255, 202, 85, 0)')
  gradient.addColorStop(0.5, 'rgba(255, 202, 85, 0.16)')
  gradient.addColorStop(1, 'rgba(255, 202, 85, 0)')
  ctx.fillStyle = gradient
  ctx.beginPath()
  ctx.ellipse(start + 18 + width / 2, groundY - 6, width / 2, 9, 0, 0, Math.PI * 2)
  ctx.fill()
  ctx.restore()
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
  if (biome === 'deep_forest') {
    ctx.fillStyle = 'rgba(5, 12, 12, 0.46)'
    ctx.fillRect(0, 0, width, height)
    drawDeepForestCanopy(width, height)
    return true
  }
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

  if (biome === 'deep_forest') {
    const grad = ctx.createLinearGradient(0, 0, 0, height)
    grad.addColorStop(0, '#06100d')
    grad.addColorStop(0.55, '#10251c')
    grad.addColorStop(1, '#1b1b18')
    ctx.fillStyle = grad
    ctx.fillRect(0, 0, width, height)
    drawDeepForestCanopy(width, height)
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

function drawDeepForestCanopy(width, height) {
  ctx.save()
  ctx.fillStyle = 'rgba(2, 8, 8, 0.52)'
  for (let x = -80; x < width + 120; x += 86) {
    ctx.beginPath()
    ctx.ellipse(x, height * 0.1 + (x % 3) * 12, 86, 42, 0, 0, Math.PI * 2)
    ctx.ellipse(x + 44, height * 0.16, 74, 38, 0, 0, Math.PI * 2)
    ctx.fill()
  }
  ctx.fillStyle = 'rgba(42, 86, 54, 0.38)'
  drawRidge(width, height * 0.48, [64, 96, 70, 116, 78, 122, 88])
  ctx.fillStyle = 'rgba(14, 36, 27, 0.58)'
  drawRidge(width, height * 0.6, [48, 92, 40, 104, 62, 118, 76])
  ctx.restore()
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
  } else if (biome === 'deep_forest') {
    grad.addColorStop(0, '#223b24')
    grad.addColorStop(0.35, '#3a2f28')
    grad.addColorStop(1, '#171515')
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
  if (tiled && (biome === 'forest' || biome === 'deep_forest')) {
    drawTiledSprite('groundGrass', 0, groundY - tileSize * 0.82, width, tileSize, tileSize, offset)
    if (biome === 'deep_forest') {
      ctx.fillStyle = 'rgba(3, 12, 9, 0.28)'
      ctx.fillRect(0, groundY - tileSize * 0.82, width, tileSize * 0.46)
    }
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
    } else if (biome === 'deep_forest') {
      if (decor.kind === 'dark_pine') {
        drawDarkPine(x, groundY + 8, scale)
      } else if (decor.kind === 'bramble') {
        drawBramble(x, groundY + 8, scale)
      } else if (decor.kind === 'shadow_fern') {
        drawShadowFern(x, groundY + 8, scale)
      } else if (decor.kind === 'pine') {
        drawPine(x, groundY + 6, scale * 1.15)
      } else if (decor.kind === 'oak') {
        drawOak(x, groundY + 8, scale * 1.12)
      } else {
        drawMushrooms(x, groundY + 8, scale)
      }
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
  if (biome === 'forest' || biome === 'deep_forest') {
    if (biome === 'deep_forest' && (kind === 'bramble' || kind === 'shadow_fern')) {
      return false
    }
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
    const bob = Math.sin((state.lastRenderAt || 0) / 160) * (entity.state === 'walk' || entity.state === 'approach' ? 2.5 : 1.2)
    if (entity.type === 'hero') {
      drawHero(x, groundY + bob, entity)
    } else {
      drawMonster(x, groundY + bob, entity)
    }
  })
}

function drawLootFloaters(scene, cameraX, groundY, worldScale) {
  const now = state.lastRenderAt || 0
  state.lootFloaters = state.lootFloaters.filter((floater) => now - floater.createdAt < LOOT_FLOAT_DURATION_MS)
  state.lootFloaters.forEach((floater) => {
    const age = Math.max(0, now - floater.createdAt)
    const progress = age / LOOT_FLOAT_DURATION_MS
    const alpha = progress < 0.18 ? progress / 0.18 : Math.max(0, 1 - progress)
    const x = worldX(floater.x, cameraX, worldScale)
    const y = groundY - 94 - progress * 46 + Math.sin((now + floater.x * 17) / 130) * 3
    const palette = FALLBACK_GEAR_PALETTES[floater.rarity] || FALLBACK_GEAR_PALETTES.white

    ctx.save()
    ctx.globalAlpha = alpha
    ctx.textAlign = 'center'
    ctx.font = '800 14px "Segoe UI", "Microsoft YaHei", sans-serif'
    ctx.lineWidth = 4
    ctx.strokeStyle = 'rgba(9, 15, 13, 0.72)'
    ctx.strokeText(floater.text, x, y)
    ctx.fillStyle = palette.glow
    ctx.fillText(floater.text, x, y)
    ctx.restore()
  })
}

function drawAttackEffects(scene, cameraX, groundY, worldScale) {
  const now = state.lastRenderAt || 0
  state.attackEffects = state.attackEffects.filter((effect) => now - effect.createdAt < ATTACK_EFFECT_DURATION_MS)
  state.attackEffects.forEach((effect) => {
    const age = Math.max(0, now - effect.createdAt)
    const progress = Math.min(1, age / ATTACK_EFFECT_DURATION_MS)
    const profile = attackEffectProfile(effect.rarity)
    const startX = worldX(effect.x, cameraX, worldScale)
    const targetX = worldX(effect.targetX, cameraX, worldScale)
    const reach = Math.max(48, Math.min(160, targetX - startX))
    const y = groundY - 44 - Math.sin(progress * Math.PI) * 8
    drawWeaponRarityBurst(startX, y, reach, progress, profile, effect)
  })
}

function attackEffectProfile(rarity) {
  const palette = FALLBACK_GEAR_PALETTES[rarity] || FALLBACK_GEAR_PALETTES.white
  return {
    palette,
    particles: {
      white: 5,
      green: 8,
      blue: 12,
      purple: 18,
      gold: 24,
      red: 34
    }[rarity] || 6,
    trails: {
      white: 1,
      green: 2,
      blue: 2,
      purple: 3,
      gold: 4,
      red: 5
    }[rarity] || 1,
    width: {
      white: 4,
      green: 5,
      blue: 6,
      purple: 7,
      gold: 8,
      red: 10
    }[rarity] || 4
  }
}

function drawWeaponRarityBurst(startX, y, reach, progress, profile, effect) {
  const slashProgress = smoothstep(progress)
  const slashX = startX + reach * slashProgress
  const alpha = Math.max(0, 1 - progress)
  const palette = profile.palette

  ctx.save()
  for (let trail = 0; trail < profile.trails; trail += 1) {
    const trailOffset = trail * 5
    ctx.globalAlpha = alpha * (0.22 + (profile.trails - trail) / profile.trails * 0.42)
    ctx.strokeStyle = trail % 2 === 0 ? palette.glow : palette.primary
    ctx.lineWidth = Math.max(2, profile.width - trail)
    ctx.lineCap = 'round'
    ctx.beginPath()
    ctx.moveTo(startX + trailOffset, y + 10 - trail * 2)
    ctx.quadraticCurveTo(
      startX + reach * 0.5,
      y - 24 - trail * 3,
      slashX + 18 - trailOffset,
      y - 3 + trail * 2
    )
    ctx.stroke()
  }
  ctx.restore()

  ctx.save()
  ctx.globalAlpha = alpha
  const gradient = ctx.createRadialGradient(slashX, y - 8, 2, slashX, y - 8, 34)
  gradient.addColorStop(0, palette.glow)
  gradient.addColorStop(1, 'rgba(255,255,255,0)')
  ctx.fillStyle = gradient
  ctx.beginPath()
  ctx.arc(slashX, y - 8, 34, 0, Math.PI * 2)
  ctx.fill()
  ctx.restore()

  ctx.save()
  for (let i = 0; i < profile.particles; i += 1) {
    const seed = i * 19 + String(effect.key || '').length * 7
    const spread = (pseudoRandom(seed) - 0.5) * 48
    const lift = pseudoRandom(seed + 3) * 34
    const travel = progress * (18 + pseudoRandom(seed + 9) * 42)
    const x = slashX + spread + travel
    const particleY = y - lift + Math.sin(progress * Math.PI + i) * 8
    ctx.globalAlpha = alpha * (0.35 + pseudoRandom(seed + 5) * 0.55)
    ctx.fillStyle = i % 3 === 0 ? palette.primary : i % 3 === 1 ? palette.glow : palette.accent
    ctx.beginPath()
    ctx.arc(x, particleY, 1.6 + pseudoRandom(seed + 11) * 2.8, 0, Math.PI * 2)
    ctx.fill()
    if (['purple', 'gold', 'red'].includes(effect.rarity) && i % 5 === 0) {
      ctx.strokeStyle = palette.glow
      ctx.lineWidth = 1.2
      ctx.strokeRect(x - 3, particleY - 3, 6, 6)
    }
  }
  ctx.restore()
}

function pseudoRandom(seed) {
  const value = Math.sin(seed * 12.9898) * 43758.5453
  return value - Math.floor(value)
}

function animatedFrame(a, b, speed = 260) {
  return Math.floor((state.lastRenderAt || 0) / speed) % 2 === 0 ? a : b
}

function animationPhase(speed = 260) {
  const cycle = ((state.lastRenderAt || 0) / speed) % 2
  return cycle < 1 ? cycle : 2 - cycle
}

function monsterSpriteFrames(entity) {
  if (entity.role === 'boss') {
    return ['bossA', 'bossB', 360]
  }
  const name = entity.name || ''
  if (name.includes('thorn')) return ['thornRest', 'thornWalkA', 320]
  if (name.includes('moss_imp')) return ['impIdle', 'impJump', 290]
  if (name.includes('mushroom')) return null
  if (name.includes('bark') || name.includes('guard') || name.includes('knight') || name.includes('squire')) {
    return ['guardIdle', 'guardAttack', 380]
  }
  if (name.includes('bat') || name.includes('wisp')) return ['flyA', 'flyB', 180]
  if (name.includes('harpy') || name.includes('mote')) return ['beeA', 'beeB', 180]
  return ['slimeWalkA', 'slimeWalkB', 290]
}

function monsterSpriteKey(entity) {
  if (entity.role === 'boss') {
    return animatedFrame('bossA', 'bossB', 360)
  }
  const name = entity.name || ''
  if (name.includes('thorn')) return animatedFrame('thornRest', 'thornWalkA', 320)
  if (name.includes('moss_imp')) return animatedFrame('impIdle', 'impJump', 290)
  if (name.includes('mushroom')) return 'mushroom'
  if (name.includes('bark') || name.includes('guard') || name.includes('knight') || name.includes('squire')) {
    return animatedFrame('guardIdle', 'guardAttack', 380)
  }
  if (name.includes('bat') || name.includes('wisp')) return animatedFrame('flyA', 'flyB', 180)
  if (name.includes('harpy') || name.includes('mote')) return animatedFrame('beeA', 'beeB', 180)
  return animatedFrame('slimeWalkA', 'slimeWalkB', 290)
}

function drawHero(x, y, entity) {
  const skeleton = createHeroSkeleton(x, y, entity)
  drawTalentAura(skeleton, entity)
  if (entity.state === 'reviving') {
    drawReviveAura(skeleton, entity)
  }
  drawHeroRig(skeleton, entity)
  drawEquippedBoots(skeleton, (entity.equipped || {}).boots)
  drawEquippedArmor(skeleton, (entity.equipped || {}).armor)
  drawEquippedRing(skeleton, (entity.equipped || {}).ring)
  drawEquippedHelmet(skeleton, (entity.equipped || {}).helmet)
  drawEquippedWeapon(skeleton, entity)
  drawEquippedParticleEffects(skeleton, entity)
  drawHeroHealthBar(skeleton, entity)
}

function drawHeroHealthBar(skeleton, entity) {
  drawHealthBar(skeleton.head.x - 29, skeleton.head.y - 24, 58, 7, entity.hp, entity.max_hp, '#5fd18b')
}

function createHeroSkeleton(x, y, entity) {
  const now = state.lastRenderAt || 0
  const female = entity.gender === 'female'
  const moving = entity.state === 'walk' || entity.state === 'approach'
  const combat = entity.state === 'combat'
  const stride = moving ? Math.sin(now / 145) : 0
  const counterStride = moving ? Math.sin(now / 145 + Math.PI) : 0
  const breathing = Math.sin(now / 420) * 1.2
  const swing = combat ? Math.sin(now / 95) : Math.sin(now / 240) * 0.35
  const shoulder = female ? 9 : 11
  const hip = female ? 10 : 12
  const reach = female ? 31 : 34
  const hips = { x, y: y - 28 + breathing * 0.15 }
  const torso = { x, y: y - 48 + breathing * 0.2 }
  const neck = { x: x + 1, y: y - 64 + breathing * 0.2 }
  const head = { x: x + 2, y: y - 76 + breathing * 0.2 }
  const rightShoulder = { x: x + shoulder, y: y - 58 + breathing * 0.2 }
  const leftShoulder = { x: x - shoulder, y: y - 57 + breathing * 0.2 }
  const rightElbow = {
    x: x + shoulder + 9 + (combat ? 4 : stride * 3),
    y: y - 47 + (combat ? -3 + swing * 2 : -stride * 2)
  }
  const leftElbow = {
    x: x - shoulder - 7 + counterStride * 2,
    y: y - 45 + counterStride * 2
  }
  const rightHand = {
    x: x + reach + (combat ? swing * 7 : stride * 2),
    y: y - 39 + (combat ? -8 + swing * 3 : stride * 2),
    angle: combat ? -0.9 + swing * 0.45 : -0.28 + stride * 0.1
  }
  const leftHand = {
    x: x - (female ? 20 : 22) + counterStride * 2,
    y: y - 39 + counterStride * 1.4,
    angle: -2.45 + counterStride * 0.1
  }
  return {
    hips,
    torso,
    neck,
    head,
    rightShoulder,
    leftShoulder,
    rightElbow,
    leftElbow,
    rightHand,
    leftHand,
    mainHand: rightHand,
    offHand: leftHand,
    rightKnee: { x: x + 8 + counterStride * 5, y: y - 14 },
    leftKnee: { x: x - 8 + stride * 5, y: y - 14 },
    rightFoot: { x: x + 11 + counterStride * 7, y: y - 1 },
    leftFoot: { x: x - 11 + stride * 7, y: y - 1 },
    hip
  }
}

function drawReviveAura(skeleton, entity) {
  const pulse = 0.5 + animationPhase(520) * 0.5
  ctx.save()
  ctx.strokeStyle = `rgba(255, 202, 85, ${0.28 + pulse * 0.32})`
  ctx.lineWidth = 3
  ctx.setLineDash([6, 6])
  ctx.beginPath()
  ctx.ellipse(skeleton.hips.x, skeleton.hips.y + 20, 34 + pulse * 8, 10 + pulse * 2, 0, 0, Math.PI * 2)
  ctx.stroke()
  ctx.setLineDash([])
  ctx.fillStyle = `rgba(255, 202, 85, ${0.08 + pulse * 0.08})`
  ctx.beginPath()
  ctx.ellipse(skeleton.torso.x, skeleton.torso.y - 8, 24 + pulse * 6, 42 + pulse * 4, 0, 0, Math.PI * 2)
  ctx.fill()
  ctx.restore()
}

function drawTalentAura(skeleton, entity) {
  const style = talentAuraStyle(entity)
  if (!style) {
    return
  }
  if (style.kind === 'lightning') {
    drawLightningAura(skeleton, style)
    return
  }
  if (style.kind === 'ward') {
    drawWardAura(skeleton, style)
    return
  }
  drawMoteAura(skeleton, style)
}

function talentAuraStyle(entity) {
  const effects = entity.talent_effects || {}
  const names = (entity.talents || []).map((talent) => talent.name || '').join('')
  if (effects.move_speed_pct || names.includes('雷') || names.includes('疾风')) {
    return {
      kind: 'lightning',
      color: '#68b7ff',
      secondary: '#ffca55',
      strength: Math.min(1.4, 0.72 + Number(effects.move_speed_pct || 0) * 3)
    }
  }
  if (effects.defense_pct || effects.max_hp_pct) {
    return {
      kind: 'ward',
      color: '#5fd18b',
      secondary: '#68b7ff',
      strength: Math.min(1.25, 0.66 + Number((effects.defense_pct || 0) + (effects.max_hp_pct || 0)) * 2)
    }
  }
  if (effects.attack_pct || effects.all_stats_pct) {
    return {
      kind: 'mote',
      color: '#ff7a7c',
      secondary: '#ffca55',
      strength: Math.min(1.25, 0.7 + Number((effects.attack_pct || 0) + (effects.all_stats_pct || 0)) * 2.5)
    }
  }
  if (effects.drop_rate_pct || effects.gold_pct || effects.exp_pct || effects.rift_drop_rate_pct) {
    return {
      kind: 'mote',
      color: '#ffca55',
      secondary: '#b779ff',
      strength: 0.78
    }
  }
  return null
}

function drawLightningAura(skeleton, style) {
  const now = state.lastRenderAt || 0
  const pulse = 0.45 + animationPhase(360) * 0.55
  ctx.save()
  ctx.globalAlpha = 0.42 + pulse * 0.25
  ctx.strokeStyle = style.color
  ctx.lineWidth = 2.5
  for (let i = 0; i < 4; i += 1) {
    const angle = now / 260 + i * Math.PI * 0.5
    const radius = (22 + i * 4) * style.strength
    const startX = skeleton.torso.x + Math.cos(angle) * radius
    const startY = skeleton.torso.y + Math.sin(angle * 1.7) * 20
    ctx.beginPath()
    ctx.moveTo(startX, startY)
    ctx.lineTo(startX + Math.cos(angle + 1.1) * 8, startY - 12)
    ctx.lineTo(startX + Math.cos(angle + 2.1) * 15, startY + 1)
    ctx.lineTo(startX + Math.cos(angle + 2.8) * 23, startY - 16)
    ctx.stroke()
  }
  ctx.strokeStyle = style.secondary
  ctx.lineWidth = 1.5
  ctx.beginPath()
  ctx.ellipse(skeleton.hips.x, skeleton.hips.y + 19, 31 * style.strength, 9, 0, 0, Math.PI * 2)
  ctx.stroke()
  ctx.restore()
}

function drawWardAura(skeleton, style) {
  const pulse = 0.5 + animationPhase(620) * 0.5
  ctx.save()
  ctx.strokeStyle = style.color
  ctx.lineWidth = 2
  ctx.globalAlpha = 0.28 + pulse * 0.25
  ctx.beginPath()
  ctx.ellipse(skeleton.torso.x, skeleton.torso.y - 4, 26 * style.strength, 43 * style.strength, 0, 0, Math.PI * 2)
  ctx.stroke()
  ctx.strokeStyle = style.secondary
  ctx.setLineDash([5, 9])
  ctx.beginPath()
  ctx.ellipse(skeleton.hips.x, skeleton.hips.y + 18, 34 * style.strength, 10, 0, 0, Math.PI * 2)
  ctx.stroke()
  ctx.restore()
}

function drawMoteAura(skeleton, style) {
  const now = state.lastRenderAt || 0
  ctx.save()
  for (let i = 0; i < 7; i += 1) {
    const angle = now / 420 + i * 0.9
    const radius = (18 + (i % 3) * 8) * style.strength
    const x = skeleton.torso.x + Math.cos(angle) * radius
    const y = skeleton.torso.y - 4 + Math.sin(angle * 1.3) * 32
    ctx.globalAlpha = 0.36 + animationPhase(520 + i * 30) * 0.28
    ctx.fillStyle = i % 2 === 0 ? style.color : style.secondary
    ctx.beginPath()
    ctx.arc(x, y, 2.2 + (i % 3), 0, Math.PI * 2)
    ctx.fill()
  }
  ctx.restore()
}

function drawHeroRig(skeleton, entity) {
  ctx.save()
  ctx.lineCap = 'round'
  ctx.lineJoin = 'round'
  drawRigLimb(skeleton.hips, skeleton.rightKnee, 8, '#243f52')
  drawRigLimb(skeleton.rightKnee, skeleton.rightFoot, 7, '#1c3343')
  drawRigLimb(skeleton.hips, skeleton.leftKnee, 8, '#20394b')
  drawRigLimb(skeleton.leftKnee, skeleton.leftFoot, 7, '#1a2f3e')
  drawRigBoot(skeleton.rightFoot)
  drawRigBoot(skeleton.leftFoot)
  drawRigLimb(skeleton.leftShoulder, skeleton.leftElbow, 7, '#2f6475')
  drawRigLimb(skeleton.leftElbow, skeleton.leftHand, 6, '#e8ad87')
  drawHeroTorso(skeleton, entity)
  drawRigLimb(skeleton.rightShoulder, skeleton.rightElbow, 7, '#356f82')
  drawRigLimb(skeleton.rightElbow, skeleton.rightHand, 6, '#efbd96')
  drawRigHand(skeleton.leftHand)
  drawRigHand(skeleton.rightHand)
  drawHeroHead(skeleton, entity)
  ctx.restore()
}

function drawHeroTorso(skeleton, entity) {
  const female = entity.gender === 'female'
  const armorTint = entity.weapon && entity.weapon.rarity === 'red' ? '#395472' : female ? '#6a4d75' : '#2e5d69'
  ctx.fillStyle = armorTint
  ctx.beginPath()
  ctx.moveTo(skeleton.leftShoulder.x - 3, skeleton.leftShoulder.y + 2)
  ctx.lineTo(skeleton.rightShoulder.x + 4, skeleton.rightShoulder.y + 1)
  ctx.lineTo(skeleton.hips.x + skeleton.hip + 1, skeleton.hips.y + 4)
  ctx.lineTo(skeleton.hips.x - skeleton.hip, skeleton.hips.y + 4)
  ctx.closePath()
  ctx.fill()
  ctx.strokeStyle = 'rgba(10, 21, 25, 0.42)'
  ctx.lineWidth = 3
  ctx.stroke()
  ctx.strokeStyle = 'rgba(230, 245, 239, 0.24)'
  ctx.lineWidth = 2
  ctx.beginPath()
  ctx.moveTo(skeleton.torso.x - 7, skeleton.torso.y - 9)
  ctx.lineTo(skeleton.torso.x + 8, skeleton.torso.y + 8)
  ctx.stroke()
}

function drawHeroHead(skeleton, entity) {
  const female = entity.gender === 'female'
  drawHeroBackHair(skeleton, entity)
  ctx.fillStyle = female ? '#f1b48f' : entity.name && entity.name.includes('Astra') ? '#f3c29f' : '#efbd96'
  ctx.beginPath()
  ctx.ellipse(skeleton.head.x, skeleton.head.y, 13, 14, 0, 0, Math.PI * 2)
  ctx.fill()
  drawHeroHair(skeleton, entity)
  drawHeroEye(skeleton, entity)
}

function drawHeroBackHair(skeleton, entity) {
  if (entity.gender !== 'female') {
    return
  }
  ctx.fillStyle = '#5b2f34'
  ctx.beginPath()
  ctx.ellipse(skeleton.head.x - 2, skeleton.head.y + 2, 15, 19, -0.08, 0, Math.PI * 2)
  ctx.ellipse(skeleton.head.x - 12, skeleton.head.y + 4, 6, 15, -0.22, 0, Math.PI * 2)
  ctx.ellipse(skeleton.head.x + 12, skeleton.head.y + 4, 6, 14, 0.22, 0, Math.PI * 2)
  ctx.fill()
}

function drawHeroHair(skeleton, entity) {
  const female = entity.gender === 'female'
  ctx.fillStyle = female ? '#5b2f34' : '#2e231b'
  ctx.beginPath()
  ctx.ellipse(skeleton.head.x - 1, skeleton.head.y - 10, female ? 15 : 14, female ? 8 : 7, -0.18, 0, Math.PI * 2)
  ctx.fill()
  if (!female) {
    return
  }
  ctx.fillStyle = '#6f3b42'
  ctx.beginPath()
  ctx.arc(skeleton.head.x - 14, skeleton.head.y - 3, 5, 0, Math.PI * 2)
  ctx.fill()
}

function drawHeroEye(skeleton, entity) {
  ctx.fillStyle = '#101817'
  ctx.fillRect(skeleton.head.x + 5, skeleton.head.y - 2, 4, 4)
}

function drawRigLimb(from, to, width, color) {
  ctx.strokeStyle = color
  ctx.lineWidth = width
  ctx.beginPath()
  ctx.moveTo(from.x, from.y)
  ctx.lineTo(to.x, to.y)
  ctx.stroke()
}

function drawRigHand(hand) {
  ctx.fillStyle = '#efbd96'
  ctx.beginPath()
  ctx.arc(hand.x, hand.y, 4.6, 0, Math.PI * 2)
  ctx.fill()
}

function drawRigBoot(foot) {
  ctx.fillStyle = '#172532'
  roundRect(foot.x - 8, foot.y - 3, 16, 6, 3)
  ctx.fill()
}

function drawEquippedArmor(skeleton, armor) {
  if (!armor) {
    return
  }
  const appearance = equipmentAppearance(armor)
  const palette = appearance.palette || FALLBACK_GEAR_PALETTES.white
  drawEquipmentGlow(skeleton.torso, appearance, 26, 33)
  ctx.save()
  ctx.fillStyle = palette.primary
  ctx.strokeStyle = palette.accent
  ctx.lineWidth = 2.5
  ctx.beginPath()
  ctx.moveTo(skeleton.leftShoulder.x - 1, skeleton.leftShoulder.y + 4)
  ctx.lineTo(skeleton.rightShoulder.x + 3, skeleton.rightShoulder.y + 3)
  ctx.lineTo(skeleton.hips.x + skeleton.hip + 3, skeleton.hips.y + 5)
  ctx.lineTo(skeleton.hips.x - skeleton.hip - 2, skeleton.hips.y + 5)
  ctx.closePath()
  ctx.fill()
  ctx.stroke()
  ctx.strokeStyle = 'rgba(255,255,255,0.42)'
  ctx.lineWidth = 1.8
  ctx.beginPath()
  ctx.moveTo(skeleton.torso.x, skeleton.torso.y - 14)
  ctx.lineTo(skeleton.torso.x, skeleton.torso.y + 14)
  ctx.moveTo(skeleton.torso.x - 10, skeleton.torso.y - 1)
  ctx.lineTo(skeleton.torso.x + 10, skeleton.torso.y - 1)
  ctx.stroke()
  ctx.restore()
}

function drawEquippedHelmet(skeleton, helmet) {
  if (!helmet) {
    return
  }
  const appearance = equipmentAppearance(helmet)
  const palette = appearance.palette || FALLBACK_GEAR_PALETTES.white
  drawEquipmentGlow(skeleton.head, appearance, 21, 23)
  ctx.save()
  ctx.strokeStyle = palette.accent
  ctx.fillStyle = palette.primary
  ctx.lineWidth = 2
  ctx.beginPath()
  ctx.ellipse(skeleton.head.x, skeleton.head.y - 8, 15, 9, -0.04, Math.PI, Math.PI * 2)
  ctx.lineTo(skeleton.head.x + 13, skeleton.head.y - 1)
  ctx.lineTo(skeleton.head.x - 12, skeleton.head.y - 1)
  ctx.closePath()
  ctx.fill()
  ctx.stroke()
  if (appearance.model === 'crown_helm') {
    ctx.fillStyle = palette.glow
    triangle(skeleton.head.x - 7, skeleton.head.y - 17, 8, 10)
    triangle(skeleton.head.x + 1, skeleton.head.y - 19, 8, 12)
    triangle(skeleton.head.x + 9, skeleton.head.y - 17, 8, 10)
  }
  ctx.restore()
}

function drawEquippedBoots(skeleton, boots) {
  if (!boots) {
    return
  }
  const appearance = equipmentAppearance(boots)
  const palette = appearance.palette || FALLBACK_GEAR_PALETTES.white
  ctx.save()
  ;[skeleton.rightFoot, skeleton.leftFoot].forEach((foot, index) => {
    ctx.fillStyle = palette.primary
    roundRect(foot.x - 9, foot.y - 5, 18, 8, 3)
    ctx.fill()
    ctx.strokeStyle = palette.accent
    ctx.lineWidth = 2
    ctx.stroke()
    if (appearance.model === 'winged_boots') {
      ctx.strokeStyle = palette.glow
      ctx.beginPath()
      ctx.moveTo(foot.x + (index === 0 ? 5 : -5), foot.y - 8)
      ctx.lineTo(foot.x + (index === 0 ? 15 : -15), foot.y - 14)
      ctx.lineTo(foot.x + (index === 0 ? 9 : -9), foot.y - 4)
      ctx.stroke()
    }
  })
  ctx.restore()
}

function drawEquippedRing(skeleton, ring) {
  if (!ring) {
    return
  }
  const appearance = equipmentAppearance(ring)
  const palette = appearance.palette || FALLBACK_GEAR_PALETTES.white
  drawEquipmentGlow(skeleton.offHand, appearance, 15, 15)
  ctx.save()
  ctx.strokeStyle = palette.glow
  ctx.lineWidth = 2
  ctx.beginPath()
  ctx.ellipse(skeleton.offHand.x, skeleton.offHand.y, 8, 4, -0.5, 0, Math.PI * 2)
  ctx.stroke()
  ctx.fillStyle = palette.primary
  ctx.beginPath()
  ctx.arc(skeleton.offHand.x + 5, skeleton.offHand.y - 4, 3, 0, Math.PI * 2)
  ctx.fill()
  ctx.restore()
}

function drawEquipmentGlow(anchor, appearance, width, height) {
  if (!appearance || !appearance.aura) {
    return
  }
  const palette = appearance.palette || FALLBACK_GEAR_PALETTES.white
  const pulse = 0.4 + animationPhase(560) * 0.6
  ctx.save()
  ctx.globalAlpha = 0.14 + pulse * 0.16
  ctx.fillStyle = palette.glow
  ctx.beginPath()
  ctx.ellipse(anchor.x, anchor.y, width * (0.9 + pulse * 0.2), height * (0.9 + pulse * 0.2), 0, 0, Math.PI * 2)
  ctx.fill()
  ctx.restore()
}

function drawEquippedParticleEffects(skeleton, entity) {
  const equipped = entity.equipped || {}
  const anchors = {
    weapon: skeleton.mainHand,
    helmet: skeleton.head,
    armor: skeleton.torso,
    boots: {
      x: (skeleton.leftFoot.x + skeleton.rightFoot.x) / 2,
      y: (skeleton.leftFoot.y + skeleton.rightFoot.y) / 2
    },
    ring: skeleton.offHand
  }
  Object.keys(equipped).forEach((slot) => {
    const item = equipped[slot]
    if (!item) {
      return
    }
    const appearance = equipmentAppearance(item)
    if (!appearance.aura && !['purple', 'gold', 'red'].includes(item.rarity)) {
      return
    }
    drawRarityParticle(anchors[slot] || skeleton.torso, item, slot)
  })
}

function drawRarityParticle(anchor, item, slot) {
  const appearance = equipmentAppearance(item)
  const palette = appearance.palette || FALLBACK_GEAR_PALETTES[item.rarity] || FALLBACK_GEAR_PALETTES.white
  const count = item.rarity === 'red' ? 8 : item.rarity === 'gold' ? 6 : 4
  const now = state.lastRenderAt || 0
  ctx.save()
  for (let i = 0; i < count; i += 1) {
    const orbit = now / (420 + i * 37) + i * 1.7
    const radius = slot === 'weapon' ? 12 + i * 1.4 : slot === 'boots' ? 18 : 10 + i * 1.2
    const x = anchor.x + Math.cos(orbit) * radius
    const y = anchor.y + Math.sin(orbit * 1.35) * (slot === 'boots' ? 5 : 14)
    ctx.globalAlpha = 0.28 + animationPhase(440 + i * 22) * 0.34
    ctx.fillStyle = i % 2 === 0 ? palette.glow : palette.primary
    ctx.beginPath()
    ctx.arc(x, y, item.rarity === 'red' ? 2.6 : 2, 0, Math.PI * 2)
    ctx.fill()
  }
  ctx.restore()
}

function drawEquippedWeapon(skeleton, entity) {
  const equipped = entity.equipped || {}
  if (equipped.weapon) {
    drawWeaponOnHand(skeleton.mainHand, equipped.weapon)
  } else if (entity.weapon) {
    drawWeaponOnHand(skeleton.mainHand, entity.weapon)
  }
  if (entity.offhand_weapon) {
    drawWeaponOnHand(skeleton.offHand, entity.offhand_weapon, true)
  }
}

function drawWeaponOnHand(hand, weapon, offhand = false) {
  const type = weapon.weapon_type || 'blade'
  const appearance = equipmentAppearance(weapon)
  const palette = appearance.palette || FALLBACK_GEAR_PALETTES.white
  const reach = type === 'spear' ? 66 : type === 'axe' ? 48 : 42
  const angle = offhand ? hand.angle + Math.PI : hand.angle
  ctx.save()
  ctx.translate(hand.x, hand.y)
  ctx.rotate(angle)
  if (appearance.aura) {
    ctx.strokeStyle = palette.glow
    ctx.globalAlpha = 0.28
    ctx.lineWidth = 10
    ctx.lineCap = 'round'
    ctx.beginPath()
    ctx.moveTo(2, 0)
    ctx.lineTo(reach + 12, 0)
    ctx.stroke()
    ctx.globalAlpha = 1
  }
  ctx.strokeStyle = appearance.model === 'wooden_blade' ? palette.accent : '#81532c'
  ctx.lineWidth = 5
  ctx.lineCap = 'round'
  ctx.beginPath()
  ctx.moveTo(-9, 0)
  ctx.lineTo(reach, 0)
  ctx.stroke()
  drawWeaponHead(type, reach, palette, appearance)
  ctx.restore()
}

function drawWeaponHead(type, reach, palette = FALLBACK_GEAR_PALETTES.white, appearance = {}) {
  if (type === 'spear') {
    ctx.fillStyle = palette.primary
    ctx.beginPath()
    ctx.moveTo(reach + 16, 0)
    ctx.lineTo(reach - 3, -8)
    ctx.lineTo(reach + 1, 8)
    ctx.closePath()
    ctx.fill()
    ctx.strokeStyle = palette.glow
    ctx.lineWidth = appearance.aura ? 2 : 1
    ctx.stroke()
    return
  }
  if (type === 'axe') {
    ctx.fillStyle = palette.primary
    ctx.beginPath()
    ctx.ellipse(reach + 1, -5, 14, 10, -0.28, 0, Math.PI * 2)
    ctx.fill()
    ctx.fillStyle = palette.accent
    ctx.fillRect(reach - 3, -13, 6, 24)
    return
  }
  ctx.strokeStyle = palette.primary
  ctx.lineWidth = 7
  ctx.beginPath()
  ctx.moveTo(reach * 0.25, 0)
  ctx.lineTo(reach + 9, 0)
  ctx.stroke()
  ctx.fillStyle = appearance.model === 'wooden_blade' ? '#f3d49b' : palette.glow
  ctx.beginPath()
  ctx.moveTo(reach + 18, 0)
  ctx.lineTo(reach + 4, -6)
  ctx.lineTo(reach + 6, 6)
  ctx.closePath()
  ctx.fill()
}

function drawMonster(x, y, entity) {
  if (entity.role === 'treasure_mimic') {
    drawTreasureMimic(x, y, entity)
    return
  }
  const boss = entity.role === 'boss'
  const scale = boss ? 1.45 : 1
  const threatStyle = monsterThreatStyle(entity)
  drawHealthBar(x - 26 * scale, y - 60 * scale, 52 * scale, 7, entity.hp, entity.max_hp, boss ? '#ffca55' : threatStyle.bar)
  const frames = monsterSpriteFrames(entity)
  const key = monsterSpriteKey(entity)
  const name = entity.name || ''
  const width = boss ? 94 : name.includes('mushroom') ? 48 : 66
  const height = boss ? 92 : name.includes('mushroom') ? 56 : 58
  const flightLift = name.includes('bat') || name.includes('wisp') || name.includes('harpy') || name.includes('mote') ? 26 : 0
  const flipTowardHero = monsterFacingFlip(entity)
  const drewMonster = frames
    ? drawBlendedSpriteBottom(frames[0], frames[1], x, y - flightLift + 3, width, height, flipTowardHero, frames[2])
    : drawSpriteBottom(key, x, y - flightLift + 3, width, height, flipTowardHero)
  if (drewMonster) {
    drawMonsterThreatOverlay(x, y - flightLift + 3, width, height, threatStyle)
    if (boss) {
      ctx.strokeStyle = 'rgba(255, 202, 85, 0.72)'
      ctx.lineWidth = 3
      ctx.beginPath()
      ctx.ellipse(x, y - 45, 46, 34, 0, 0, Math.PI * 2)
      ctx.stroke()
    }
    return
  }
  ctx.fillStyle = boss ? '#7d3f61' : threatStyle.body
  ctx.beginPath()
  ctx.ellipse(x, y - 24 * scale, 26 * scale, 20 * scale, 0, 0, Math.PI * 2)
  ctx.fill()
  ctx.fillStyle = threatStyle.eye
  ctx.fillRect(x - 10 * scale, y - 30 * scale, 4 * scale, 4 * scale)
  ctx.fillRect(x + 7 * scale, y - 30 * scale, 4 * scale, 4 * scale)
  if (threatStyle.threat > 1) {
    ctx.strokeStyle = threatStyle.aura
    ctx.lineWidth = 3
    ctx.beginPath()
    ctx.moveTo(x - 18 * scale, y - 42 * scale)
    ctx.lineTo(x - 26 * scale, y - 58 * scale)
    ctx.moveTo(x + 18 * scale, y - 42 * scale)
    ctx.lineTo(x + 26 * scale, y - 58 * scale)
    ctx.stroke()
  }
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

function monsterFacingFlip(entity) {
  return false
}

function monsterThreatStyle(entity) {
  const name = entity.name || ''
  const deep = entity.theme === 'deep_forest' || Number(entity.threat || 1) > 1
  if (!deep) {
    return {
      threat: 1,
      body: monsterColor(name),
      eye: '#141817',
      bar: '#ff6b6b',
      aura: 'rgba(20, 24, 23, 0)'
    }
  }
  if (name.includes('venom')) {
    return { threat: entity.threat || 1.3, body: '#475d2c', eye: '#d7ff78', bar: '#b6ff5f', aura: 'rgba(182, 255, 95, 0.42)' }
  }
  if (name.includes('bramble')) {
    return { threat: entity.threat || 1.3, body: '#51323b', eye: '#ffca55', bar: '#ff7a7c', aura: 'rgba(255, 122, 124, 0.42)' }
  }
  if (name.includes('ancient')) {
    return { threat: entity.threat || 1.3, body: '#3e4635', eye: '#ff4d4f', bar: '#ff4d4f', aura: 'rgba(255, 77, 79, 0.38)' }
  }
  return { threat: entity.threat || 1.3, body: '#283c46', eye: '#ff4d4f', bar: '#b779ff', aura: 'rgba(183, 121, 255, 0.42)' }
}

function drawMonsterThreatOverlay(x, bottomY, width, height, style) {
  if (!style || style.threat <= 1) {
    return
  }
  const topY = bottomY - height
  ctx.save()
  ctx.globalAlpha = 0.28
  ctx.fillStyle = style.aura
  ctx.beginPath()
  ctx.ellipse(x, topY + height * 0.58, width * 0.48, height * 0.42, 0, 0, Math.PI * 2)
  ctx.fill()
  ctx.globalAlpha = 1
  ctx.fillStyle = style.eye
  ctx.fillRect(x - width * 0.15, topY + height * 0.38, 4, 4)
  ctx.fillRect(x + width * 0.08, topY + height * 0.38, 4, 4)
  ctx.strokeStyle = style.aura
  ctx.lineWidth = 2
  ctx.beginPath()
  ctx.moveTo(x - width * 0.22, topY + height * 0.2)
  ctx.lineTo(x - width * 0.34, topY + height * 0.02)
  ctx.moveTo(x + width * 0.22, topY + height * 0.2)
  ctx.lineTo(x + width * 0.34, topY + height * 0.02)
  ctx.stroke()
  ctx.restore()
}

function drawTreasureMimic(x, y, entity) {
  drawHealthBar(x - 31, y - 66, 62, 7, entity.hp, entity.max_hp, '#ffca55')
  const key = animatedFrame('mimicClosed', 'mimicOpen', 320)
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
  if (name.includes('shadow')) return '#283c46'
  if (name.includes('bramble')) return '#51323b'
  if (name.includes('gloom')) return '#34415a'
  if (name.includes('venom')) return '#475d2c'
  if (name.includes('ancient')) return '#3e4635'
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

function drawDarkPine(x, y, scale) {
  ctx.fillStyle = '#231a16'
  ctx.fillRect(x - 5 * scale, y - 74 * scale, 10 * scale, 74 * scale)
  ctx.fillStyle = '#0d2f24'
  triangle(x, y - 140 * scale, 50 * scale, 78 * scale)
  ctx.fillStyle = '#134630'
  triangle(x, y - 92 * scale, 64 * scale, 76 * scale)
  ctx.fillStyle = 'rgba(104, 183, 255, 0.18)'
  ctx.beginPath()
  ctx.arc(x + 13 * scale, y - 82 * scale, 3 * scale, 0, Math.PI * 2)
  ctx.fill()
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

function drawBramble(x, y, scale) {
  ctx.strokeStyle = '#1d3928'
  ctx.lineWidth = 4 * scale
  for (let i = -3; i <= 3; i += 1) {
    ctx.beginPath()
    ctx.moveTo(x + i * 7 * scale, y)
    ctx.quadraticCurveTo(x + i * 10 * scale, y - 18 * scale, x + i * 18 * scale, y - 34 * scale)
    ctx.stroke()
  }
  ctx.fillStyle = '#7d2a3f'
  for (let i = -2; i <= 2; i += 1) {
    ctx.beginPath()
    ctx.arc(x + i * 12 * scale, y - (18 + Math.abs(i) * 3) * scale, 3 * scale, 0, Math.PI * 2)
    ctx.fill()
  }
}

function drawShadowFern(x, y, scale) {
  ctx.strokeStyle = '#143f31'
  ctx.lineWidth = 3 * scale
  for (let i = -4; i <= 4; i += 1) {
    ctx.beginPath()
    ctx.moveTo(x, y)
    ctx.quadraticCurveTo(x + i * 7 * scale, y - 22 * scale, x + i * 16 * scale, y - 42 * scale)
    ctx.stroke()
  }
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
  return (x - cameraX) * worldScale + 56
}

els.enterRiftButton.addEventListener('click', () => {
  const snapshot = state.snapshot
  if (!snapshot) {
    return
  }
  postAction('/rift/enter', { floor: snapshot.rift.unlocked_floor }, t('enterRift'))
})

els.leaveRiftButton.addEventListener('click', () => {
  postAction('/rift/leave', {}, t('leaveRift'))
})

els.tickButton.addEventListener('click', () => tick(10))

els.deepenForestButton.addEventListener('click', () => {
  resetVisualSmoothing()
  postAction('/forest/deepen', {}, t('deepenForest'))
})

els.retreatForestButton.addEventListener('click', () => {
  resetVisualSmoothing()
  postAction('/forest/retreat', {}, t('retreatForest'))
})

els.equipBestButton.addEventListener('click', () => {
  postAction('/equip-best', {}, t('equipBest'))
})

els.resetButton.addEventListener('click', () => {
  resetVisualSmoothing()
  postAction('/reset', {}, t('reset'))
})

els.settingsButton.addEventListener('click', () => toggleSettingsPanel(true))
els.settingsCloseButton.addEventListener('click', () => toggleSettingsPanel(false))
els.settingsPanel.addEventListener('click', (event) => {
  if (event.target === els.settingsPanel) {
    toggleSettingsPanel(false)
  }
})
els.pauseToggle.addEventListener('change', () => {
  togglePause(els.pauseToggle.checked)
})
els.volumeSlider.addEventListener('input', () => {
  setMasterVolume(Number(els.volumeSlider.value) / 100)
  saveSettings()
})
els.languageSelect.addEventListener('change', () => {
  state.settings.language = els.languageSelect.value === 'en-US' ? 'en-US' : 'zh-CN'
  saveSettings()
  applySettings()
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
    const price = window.prompt(t('listPrice'), defaultPrice)
    const parsed = Number.parseInt(price, 10)
    if (Number.isFinite(parsed) && parsed > 0) {
      postAction('/market/list', { item_id: itemId, price: parsed }, t('list'))
    }
  }
})

els.talentList.addEventListener('click', (event) => {
  const button = event.target.closest('button[data-action="evolve-talent"]')
  if (!button || button.disabled) {
    return
  }
  postAction('/talent/evolve', { talent_id: button.dataset.id }, t('evolve'))
})

els.marketList.addEventListener('click', (event) => {
  const button = event.target.closest('button[data-action="buy"]')
  if (!button || button.disabled) {
    return
  }
  postAction('/market/buy', { listing_id: button.dataset.id }, t('buy'))
})

els.genderMaleButton.addEventListener('click', () => setGender('male'))
els.genderFemaleButton.addEventListener('click', () => setGender('female'))
els.rollTalentButton.addEventListener('click', rollCreationTalents)
els.confirmCharacterButton.addEventListener('click', confirmCharacter)

els.newCharacterButton.addEventListener('click', () => {
  const shouldReset = window.confirm(t('resetConfirm'))
  if (!shouldReset) {
    return
  }
  stopGameLoop()
  clearStoredProfile()
  state.snapshot = null
  state.previousSnapshot = null
  state.creationDraft = null
  els.characterNameInput.value = ''
  els.rollCountText.textContent = remainingRollsText(3)
  els.rollTalentButton.disabled = false
  els.confirmCharacterButton.disabled = true
  renderCreationTalents()
  api('/profile/clear', { method: 'POST', body: {} }).catch(() => {})
  showProfileGate(true)
  setStatus(t('waitingCreate'))
})

window.addEventListener('resize', resizeCanvas)
resizeCanvas()
state.settings = loadStoredSettings()
applySettings()
setGender('male')
loadEquipmentTranslations()
bootstrapProfile()
window.requestAnimationFrame(draw)
