const SLOT_LABELS = {
  weapon: '武器',
  helmet: '头盔',
  armor: '护甲',
  boots: '鞋子',
  ring: '\u6212\u6307\u5ba0\u7269'
}

const RARITY_LABELS = {
  white: '白',
  green: '绿',
  blue: '蓝',
  purple: '紫',
  gold: '金',
  red: '红',
  rainbow: '彩'
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
  red: { primary: '#ff7a7c', accent: '#9e2e3a', glow: '#ff4d4f' },
  rainbow: { primary: '#8effff', accent: '#ff78e6', glow: '#fff36a' }
}

const PROFILE_STORAGE_KEY = 'idleForestProfile'
const SESSION_STORAGE_KEY = 'idleForestSessionToken'
const SETTINGS_STORAGE_KEY = 'idleForestSettings'
const MAX_CHARACTER_SLOTS = 3
const SIMULATION_STEP_SECONDS = 0.125
const SIMULATION_TICK_MS = 125
const VISUAL_MAX_FRAME_DELTA_MS = 500
const VISUAL_SNAP_DISTANCE = 96
const WALK_PIXELS_PER_FRAME = 4
const WALK_FRAME_SEQUENCE = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
const HERO_CAMERA_OFFSET = 180
const HERO_CAMERA_LEAD_SECONDS = 0.22
const HERO_CAMERA_MAX_LEAD = 28
const HERO_CAMERA_MAX_LAG = 42
const CAMERA_DAMPING = 18
const VISUAL_ENTITY_DAMPING = 14
const MONSTER_SPAWN_SCREEN_BUFFER = 820
const COMBAT_VISUAL_RANGE_GRACE = 16
const LOOT_FLOAT_DURATION_MS = 2400
const ATTACK_EFFECT_DURATION_MS = 520
const PIXEL_ASSET_VERSION = 'assassin-v54'
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
    moveSpeed: '移速',
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
    buying: '购买中',
    cancelListing: '取消挂售',
    cancelingListing: '取消中',
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
    listingReady: '输入价格后确认挂售',
    confirmList: '确认挂售',
    cancel: '取消',
    invalidPrice: '请输入有效价格',
    actionFail: '操作失败',
    systemShop: '系统商城',
    systemShopEmpty: '系统商城暂时缺货',
    donation: '捐赠',
    donations: '捐赠',
    buyDonation: '购买捐赠',
    recycle: '回收',
    recycling: '回收中',
    recycleAll: '一键回收',
    sellSystem: '卖给系统',
    sellingSystem: '售出中',
    expandTalent: '捐赠解锁天赋',
    expandingTalent: '解锁中',
    shopBuy: '购买',
    shopBuying: '购买中'
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
    moveSpeed: 'Move Speed',
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
    buying: 'Buying',
    cancelListing: 'Cancel Listing',
    cancelingListing: 'Canceling',
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
    listingReady: 'Set a price and confirm',
    confirmList: 'Confirm',
    cancel: 'Cancel',
    invalidPrice: 'Enter a valid price',
    actionFail: 'Action failed',
    systemShop: 'System Shop',
    systemShopEmpty: 'System shop is empty',
    donation: 'Donation',
    donations: 'Donations',
    buyDonation: 'Buy Donation',
    recycle: 'Recycle',
    recycling: 'Recycling',
    recycleAll: 'Recycle All',
    sellSystem: 'Sell to System',
    sellingSystem: 'Selling',
    expandTalent: 'Unlock Talent',
    expandingTalent: 'Unlocking',
    shopBuy: 'Buy',
    shopBuying: 'Buying'
  }
}

const state = {
  snapshot: null,
  previousSnapshot: null,
  settings: { ...DEFAULT_SETTINGS },
  account: null,
  characters: [],
  activeCharacterId: null,
  equipmentTranslations: {},
  tickInFlight: false,
  tickQueuedSeconds: 0,
  gameReady: false,
  assetsReady: false,
  stageReady: false,
  stageLoadToken: 0,
  selectedGender: 'male',
  creationDraft: null,
  tickTimer: null,
  listingDraftItemId: null,
  listingDraftItem: null,
  inventoryRenderSignature: '',
  systemShopRenderSignature: '',
  marketRenderSignature: '',
  equipmentSlotsRenderSignature: '',
  equippedRenderSignature: '',
  talentsRenderSignature: '',
  eventsRenderSignature: '',
  marketActionInFlightIds: new Set(),
  inventoryActionInFlightIds: new Set(),
  systemShopActionInFlightSkus: new Set(),
  recycleAllInFlight: false,
  talentEvolutionInFlight: false,
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
    cameraTargetX: 0,
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
  rock: '/web/assets/sprites/rock.png',
  pixelHeroMaleAssassin: `/web/assets/pixel/v1/heroes/male/pixellab_shadow_assassin.png?v=${PIXEL_ASSET_VERSION}`,
  pixelHeroFemaleAssassin: `/web/assets/pixel/v1/heroes/female/pixellab_shadow_assassin.png?v=${PIXEL_ASSET_VERSION}`,
  pixelHeroMale: `/web/assets/pixel/v1/heroes/male/base.png?v=${PIXEL_ASSET_VERSION}`,
  pixelHeroFemale: `/web/assets/pixel/v1/heroes/female/base.png?v=${PIXEL_ASSET_VERSION}`,
  pixelSlime: `/web/assets/pixel/v1/monsters/common/slime.png?v=${PIXEL_ASSET_VERSION}`,
  pixelThorn: `/web/assets/pixel/v1/monsters/common/thorn.png?v=${PIXEL_ASSET_VERSION}`,
  pixelImp: `/web/assets/pixel/v1/monsters/common/imp.png?v=${PIXEL_ASSET_VERSION}`,
  pixelForestBoss: `/web/assets/pixel/v1/monsters/bosses/forest_boss.png?v=${PIXEL_ASSET_VERSION}`,
  equipmentWoodenBlade: `/web/assets/pixel/v1/equipment/wooden_blade.png?v=${PIXEL_ASSET_VERSION}`,
  equipmentBlade: `/web/assets/pixel/v1/equipment/blade.png?v=${PIXEL_ASSET_VERSION}`,
  equipmentAxe: `/web/assets/pixel/v1/equipment/axe.png?v=${PIXEL_ASSET_VERSION}`,
  equipmentSpear: `/web/assets/pixel/v1/equipment/spear.png?v=${PIXEL_ASSET_VERSION}`,
  equipmentVisorHelm: `/web/assets/pixel/v1/equipment/visor_helm.png?v=${PIXEL_ASSET_VERSION}`,
  equipmentCrownHelm: `/web/assets/pixel/v1/equipment/crown_helm.png?v=${PIXEL_ASSET_VERSION}`,
  equipmentLeatherMail: `/web/assets/pixel/v1/equipment/leather_mail.png?v=${PIXEL_ASSET_VERSION}`,
  equipmentPlateMail: `/web/assets/pixel/v1/equipment/plate_mail.png?v=${PIXEL_ASSET_VERSION}`,
  equipmentTravelBoots: `/web/assets/pixel/v1/equipment/travel_boots.png?v=${PIXEL_ASSET_VERSION}`,
  equipmentWingedBoots: `/web/assets/pixel/v1/equipment/winged_boots.png?v=${PIXEL_ASSET_VERSION}`,
  equipmentSproutPet: `/web/assets/pixel/v1/equipment/sprout_pet.png?v=${PIXEL_ASSET_VERSION}`,
  equipmentLeafPet: `/web/assets/pixel/v1/equipment/leaf_pet.png?v=${PIXEL_ASSET_VERSION}`,
  equipmentMoonCatPet: `/web/assets/pixel/v1/equipment/moon_cat_pet.png?v=${PIXEL_ASSET_VERSION}`,
  equipmentStarBunnyPet: `/web/assets/pixel/v1/equipment/star_bunny_pet.png?v=${PIXEL_ASSET_VERSION}`,
  equipmentSparkFoxPet: `/web/assets/pixel/v1/equipment/spark_fox_pet.png?v=${PIXEL_ASSET_VERSION}`,
  equipmentEmberFoxPet: `/web/assets/pixel/v1/equipment/ember_fox_pet.png?v=${PIXEL_ASSET_VERSION}`,
  talentLightningEffect: `/web/assets/pixel/v1/effects/talent_lightning.png?v=${PIXEL_ASSET_VERSION}`,
  talentFlameEffect: `/web/assets/pixel/v1/effects/talent_flame.png?v=${PIXEL_ASSET_VERSION}`,
  talentDragonEffect: `/web/assets/pixel/v1/effects/talent_dragon.png?v=${PIXEL_ASSET_VERSION}`
}

const EQUIPMENT_MODEL_ASSET_KEYS = {
  wooden_blade: 'equipmentWoodenBlade',
  blade: 'equipmentBlade',
  dagger: 'equipmentBlade',
  axe: 'equipmentAxe',
  heavy: 'equipmentAxe',
  spear: 'equipmentSpear',
  visor_helm: 'equipmentVisorHelm',
  crown_helm: 'equipmentCrownHelm',
  leather_mail: 'equipmentLeatherMail',
  plate_mail: 'equipmentPlateMail',
  travel_boots: 'equipmentTravelBoots',
  winged_boots: 'equipmentWingedBoots',
  sprout_pet: 'equipmentSproutPet',
  leaf_pet: 'equipmentLeafPet',
  moon_cat_pet: 'equipmentMoonCatPet',
  star_bunny_pet: 'equipmentStarBunnyPet',
  spark_fox_pet: 'equipmentSparkFoxPet',
  ember_fox_pet: 'equipmentEmberFoxPet'
}

const PIXEL_HERO_ACTIONS = {
  idle: { row: 0, frames: 8, frameMs: 120 },
  walk: { row: 1, frames: 8, frameMs: 82 },
  attack_unarmed: { row: 2, frames: 8, frameMs: 68 },
  attack_blade: { row: 3, frames: 8, frameMs: 64 },
  attack_dual: { row: 4, frames: 8, frameMs: 60 },
  attack_bow: { row: 5, frames: 8, frameMs: 76 },
  attack_spear: { row: 6, frames: 8, frameMs: 72 },
  attack_heavy: { row: 7, frames: 8, frameMs: 82 },
  hurt: { row: 8, frames: 4, frameMs: 90 },
  death: { row: 9, frames: 8, frameMs: 110 },
  revive: { row: 10, frames: 8, frameMs: 95 }
}

const MALE_ASSASSIN_ACTIONS = {
  idle: { row: 0, frames: 8, frameMs: 120 },
  walk: { row: 1, frames: 15, frameMs: 48 },
  attack_unarmed: { row: 2, frames: 8, frameMs: 68 },
  attack_blade: { row: 3, frames: 9, frameMs: 48 },
  attack_dual: { row: 4, frames: 9, frameMs: 46 },
  attack_bow: { row: 5, frames: 8, frameMs: 76 },
  attack_spear: { row: 6, frames: 8, frameMs: 72 },
  attack_heavy: { row: 7, frames: 8, frameMs: 82 },
  hurt: { row: 8, frames: 4, frameMs: 90 },
  death: { row: 9, frames: 8, frameMs: 110 },
  revive: { row: 10, frames: 8, frameMs: 95 }
}

const FEMALE_ASSASSIN_ACTIONS = {
  idle: { row: 0, frames: 5, frameMs: 78 },
  walk: { row: 1, frames: 12, frameMs: 44 },
  attack_unarmed: { row: 2, frames: 9, frameMs: 46 },
  attack_blade: { row: 3, frames: 9, frameMs: 44 },
  attack_dual: { row: 4, frames: 9, frameMs: 42 },
  attack_bow: { row: 5, frames: 9, frameMs: 52 },
  attack_spear: { row: 6, frames: 9, frameMs: 50 },
  attack_heavy: { row: 7, frames: 9, frameMs: 56 },
  hurt: { row: 8, frames: 5, frameMs: 70 },
  death: { row: 9, frames: 5, frameMs: 86 },
  revive: { row: 10, frames: 5, frameMs: 78 }
}

const PIXEL_MONSTER_ACTIONS = {
  idle: { row: 0, frames: 8, frameMs: 120 },
  walk: { row: 1, frames: 8, frameMs: 92 },
  attack: { row: 2, frames: 8, frameMs: 76 },
  hurt: { row: 3, frames: 4, frameMs: 90 },
  death: { row: 4, frames: 8, frameMs: 110 }
}

const ASSASSIN_EQUIPMENT_ANCHORS = {
  mainHand: [90, 68],
  offHand: [28, 73],
  ringHand: [28, 73],
  head: [73, 28],
  torso: [59, 58],
  halo: [73, 0],
  back: [34, 40],
  feetCenter: [57, 125]
}

const MALE_ASSASSIN_FRAME_ANCHORS = {
  walk: [[[90.3,68.1,0.84],[28.5,72.9,1.76],[126.2,108.5,0.84]],[[91.0,69.0,0.82],[29.9,74.2,1.71],[127.7,108.6,0.82]],[[89.8,71.7,0.91],[32.8,75.8,1.65],[122.7,114.4,0.91]],[[85.9,72.4,1.06],[34.3,75.4,1.6],[112.1,119.7,1.06]],[[88.5,70.4,1.01],[33.8,73.7,1.63],[117.3,116.1,1.01]],[[90.6,67.6,0.94],[32.7,71.5,1.71],[122.3,111.3,0.94]],[[93.4,67.8,0.89],[30.3,71.5,1.79],[127.6,109.6,0.89]],[[95.3,68.3,0.83],[29.1,73.2,1.89],[131.7,108.2,0.83]],[[95.0,70.1,0.83],[29.2,75.1,1.87],[131.5,109.9,0.83]],[[91.7,71.3,0.92],[30.9,75.7,1.8],[124.3,114.3,0.92]],[[88.2,70.7,1.09],[34.2,74.3,1.67],[113.3,118.5,1.09]],[[86.6,70.6,1.16],[38.5,73.2,1.54],[108.4,120.0,1.16]],[[84.5,70.9,1.27],[43.1,73.5,1.42],[100.5,122.4,1.27]],[[84.4,71.2,1.21],[38.6,74.1,1.56],[103.3,121.8,1.21]],[[87.6,70.3,1.02],[33.0,75.5,1.67],[115.8,116.4,1.02]]],
  attack_blade: [[[90.3,68.1,0.84],[28.5,72.9,1.76],[126.2,108.5,0.84]],[[69.1,19.2,-2.11],[28.2,73.0,1.77],[41.3,-27.1,-2.11]],[[112.6,48.6,0.44],[28.2,73.0,1.77],[161.6,71.5,0.44]],[[112.6,48.6,0.44],[28.2,73.0,1.77],[161.6,71.5,0.44]],[[111.4,89.6,0.96],[28.2,73.0,1.77],[142.3,133.8,0.96]],[[111.4,89.6,0.96],[28.2,73.0,1.77],[142.3,133.8,0.96]],[[112.6,48.6,0.44],[28.2,73.0,1.77],[161.6,71.5,0.44]],[[69.1,19.2,-2.11],[28.2,73.0,1.77],[41.3,-27.1,-2.11]],[[90.3,68.1,0.84],[28.5,72.9,1.76],[126.2,108.5,0.84]]],
  attack_dual: [[[90.3,68.1,0.84],[28.5,72.9,1.76],[126.2,108.5,0.84]],[[69.1,19.2,-2.11],[30.7,25.6,-2.45],[41.3,-27.1,-2.11]],[[112.6,48.6,0.44],[20.5,47.4,2.9],[161.6,71.5,0.44]],[[112.6,48.6,0.44],[20.5,47.4,2.9],[161.6,71.5,0.44]],[[111.4,89.6,0.96],[23.0,84.5,2.17],[142.3,133.8,0.96]],[[111.4,89.6,0.96],[23.0,84.5,2.17],[142.3,133.8,0.96]],[[112.6,48.6,0.44],[20.5,47.4,2.9],[161.6,71.5,0.44]],[[69.1,19.2,-2.11],[30.7,25.6,-2.45],[41.3,-27.1,-2.11]],[[90.3,68.1,0.84],[28.5,72.9,1.76],[126.2,108.5,0.84]]]
}

const FEMALE_ASSASSIN_EQUIPMENT_ANCHORS = {
  mainHand: [91, 72],
  offHand: [34, 73],
  ringHand: [38, 83],
  head: [64, 30],
  torso: [62, 70],
  halo: [64, 1],
  back: [42, 31],
  feetCenter: [61, 126]
}

const FEMALE_ASSASSIN_FRAME_ANCHORS = {
  walk: [[[95.2,59.0,0.74], [52.6,61.6,2.02], [135.0,95.5,0.74]], [[91.7,61.0,1.05], [59.7,63.6,1.78], [118.6,107.9,1.05]], [[83.0,62.8,1.52], [65.3,65.4,1.57], [85.5,116.7,1.52]], [[82.1,60.8,1.46], [76.6,60.5,1.12], [87.8,114.5,1.46]], [[83.4,61.0,1.35], [82.2,59.6,0.92], [95.0,113.8,1.35]], [[84.8,60.4,1.11], [81.7,57.9,0.79], [109.0,108.7,1.11]], [[80.6,61.3,1.51], [75.6,60.4,1.07], [83.7,115.2,1.51]], [[81.4,61.5,1.6], [67.5,63.7,1.47], [79.6,115.4,1.6]], [[85.7,62.6,1.39], [61.4,61.8,1.68], [95.6,115.7,1.39]], [[93.2,58.9,0.93], [55.8,59.2,1.87], [125.6,102.1,0.93]], [[96.6,57.9,0.76], [52.1,57.9,2.12], [135.9,95.0,0.76]], [[96.4,58.5,0.73], [52.3,60.7,2.07], [136.7,94.4,0.73]], [[91.8,61.3,0.99], [58.1,63.0,1.84], [121.5,106.4,0.99]], [[82.8,60.8,1.5], [66.3,63.6,1.48], [86.8,114.6,1.5]], [[94.9,58.5,0.84], [52.9,59.1,2.03], [130.8,98.9,0.84]], [[96.9,57.4,0.66], [51.5,59.9,2.09], [139.7,90.3,0.66]]],
  attack_blade: [
    [[95.7, 53.0, 0.79], [53.7, 53.9, -2.2], [133.9, 91.2, 0.79]],
    [[94.3, 52.1, 0.77], [54.1, 54.5, -2.2], [133.1, 89.7, 0.77]],
    [[89.8, 51.2, 0.65], [69.4, 57.4, -2.2], [132.7, 84.1, 0.65]],
    [[96.9, 43.5, 0.08], [76.5, 50.6, -2.2], [150.8, 47.7, 0.08]],
    [[104.6, 36.3, 0.08], [67.1, 55.6, -2.2], [158.5, 40.7, 0.08]],
    [[106.5, 34.8, 0.1], [64.0, 55.3, -2.2], [160.2, 40.4, 0.1]],
    [[106.0, 35.4, 0.08], [62.7, 53.6, -2.2], [159.8, 39.8, 0.08]],
    [[90.9, 43.8, 0.2], [90.0, 45.3, -2.2], [143.8, 54.8, 0.2]],
    [[95.8, 53.6, 0.81], [54.7, 54.8, -2.2], [132.9, 92.8, 0.81]]
  ],
  attack_dual: [
    [[95.7, 53.0, 0.79], [53.7, 53.9, -2.2], [133.9, 91.2, 0.79]],
    [[97.4, 53.3, 0.77], [50.3, 52.7, -2.2], [136.1, 90.9, 0.77]],
    [[99.5, 52.1, 0.64], [47.1, 47.4, -2.2], [142.8, 84.3, 0.64]],
    [[100.1, 48.4, 0.52], [38.0, 30.7, -2.2], [147.0, 75.0, 0.52]],
    [[82.6, 57.4, 0.08], [35.5, 19.3, -2.2], [136.4, 61.7, 0.08]],
    [[81.5, 46.2, -0.28], [39.2, 16.2, -2.2], [133.4, 31.4, -0.28]],
    [[78.2, 45.5, -0.13], [41.9, 17.0, -2.2], [131.7, 38.4, -0.13]],
    [[64.7, 46.2, 0.08], [39.9, 22.5, -2.2], [118.6, 50.5, 0.08]],
    [[86.0, 66.3, 1.0], [105.6, 64.5, 0.2], [115.0, 111.8, 1.0]]
  ]
}

const PIXEL_SPRITES = {
  heroes: {
    male_assassin: {
      key: 'pixelHeroMaleAssassin',
      frameWidth: 128,
      frameHeight: 128,
      drawWidth: 116,
      drawHeight: 116,
      anchors: ASSASSIN_EQUIPMENT_ANCHORS,
      frameAnchors: MALE_ASSASSIN_FRAME_ANCHORS,
      actions: MALE_ASSASSIN_ACTIONS
    },
    female_assassin: {
      key: 'pixelHeroFemaleAssassin',
      frameWidth: 128,
      frameHeight: 128,
      drawWidth: 116,
      drawHeight: 116,
      anchors: FEMALE_ASSASSIN_EQUIPMENT_ANCHORS,
      frameAnchors: FEMALE_ASSASSIN_FRAME_ANCHORS,
      actions: FEMALE_ASSASSIN_ACTIONS
    },
    male_base: {
      key: 'pixelHeroMale',
      frameWidth: 96,
      frameHeight: 96,
      drawWidth: 88,
      drawHeight: 88,
      actions: PIXEL_HERO_ACTIONS
    },
    female_base: {
      key: 'pixelHeroFemale',
      frameWidth: 96,
      frameHeight: 96,
      drawWidth: 88,
      drawHeight: 88,
      actions: PIXEL_HERO_ACTIONS
    }
  },
  monsters: {
    slime: {
      key: 'pixelSlime',
      frameWidth: 64,
      frameHeight: 64,
      drawWidth: 70,
      drawHeight: 70,
      actions: PIXEL_MONSTER_ACTIONS
    },
    thorn: {
      key: 'pixelThorn',
      frameWidth: 64,
      frameHeight: 64,
      drawWidth: 72,
      drawHeight: 72,
      actions: PIXEL_MONSTER_ACTIONS
    },
    imp: {
      key: 'pixelImp',
      frameWidth: 64,
      frameHeight: 64,
      drawWidth: 70,
      drawHeight: 70,
      actions: PIXEL_MONSTER_ACTIONS
    },
    forest_boss: {
      key: 'pixelForestBoss',
      frameWidth: 128,
      frameHeight: 128,
      drawWidth: 126,
      drawHeight: 126,
      actions: PIXEL_MONSTER_ACTIONS
    }
  }
}

const assetImages = {}
const assetLoadPromises = {}

Object.entries(ASSET_PATHS).forEach(([key, path]) => {
  const image = new Image()
  image.decoding = 'async'
  assetLoadPromises[key] = new Promise((resolve) => {
    image.onload = () => {
      state.loadedAssets += 1
      resolve({ key, ok: true })
    }
    image.onerror = () => resolve({ key, ok: false })
  })
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
  moveSpeedText: document.querySelector('#moveSpeedText'),
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
  listingPanel: document.querySelector('#listingPanel'),
  listingTitle: document.querySelector('#listingTitle'),
  listingCancelButton: document.querySelector('#listingCancelButton'),
  listingItemPreview: document.querySelector('#listingItemPreview'),
  listingPriceLabel: document.querySelector('#listingPriceLabel'),
  listingPriceInput: document.querySelector('#listingPriceInput'),
  listingConfirmButton: document.querySelector('#listingConfirmButton'),
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
  systemShopList: document.querySelector('#systemShopList'),
  recycleAllButton: document.querySelector('#recycleAllButton'),
  inventoryList: document.querySelector('#inventoryList'),
  marketList: document.querySelector('#marketList'),
  eventList: document.querySelector('#eventList'),
  profileGate: document.querySelector('#profileGate'),
  stageLoading: document.querySelector('#stageLoading'),
  stageLoadingText: document.querySelector('#stageLoadingText'),
  accountPanel: document.querySelector('#accountPanel'),
  accountUsernameInput: document.querySelector('#accountUsernameInput'),
  accountPasswordInput: document.querySelector('#accountPasswordInput'),
  loginButton: document.querySelector('#loginButton'),
  registerButton: document.querySelector('#registerButton'),
  accountStatusText: document.querySelector('#accountStatusText'),
  characterPanel: document.querySelector('#characterPanel'),
  accountNameText: document.querySelector('#accountNameText'),
  logoutButton: document.querySelector('#logoutButton'),
  characterSlotList: document.querySelector('#characterSlotList'),
  creationPanel: document.querySelector('#creationPanel'),
  cancelCreationButton: document.querySelector('#cancelCreationButton'),
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
  const headers = {
    'content-type': 'application/json'
  }
  const token = loadSessionToken()
  if (token) {
    headers['X-Session-Token'] = token
  }
  return fetch(path, {
    method: options.method || 'GET',
    headers,
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
    resetListRenderSignatures()
    applySnapshot(state.snapshot)
  }
  setStatus(state.settings.paused ? t('paused') : statusForSnapshot(state.snapshot), true)
}

function applyStaticTranslations() {
  setText('#settingsButton', t('settings'))
  setText('#settingsTitle', t('settings'))
  setText('#settingsCloseButton', t('close'))
  setText('#listingTitle', t('listPrice'))
  setText('#listingCancelButton', t('cancel'))
  setText('#listingPriceLabel', t('listPrice'))
  setText('#listingConfirmButton', t('confirmList'))
  setText('#newCharacterButton', t('newCharacter'))
  setText('.resource small', t('gold'))
  setText('.hero-strip .stat:nth-child(1) span', t('level'))
  setText('.hero-strip .stat:nth-child(2) span', t('exp'))
  setText('.hero-strip .stat:nth-child(3) span', t('hp'))
  setText('.hero-strip .stat:nth-child(4) span', t('attack'))
  setText('.hero-strip .stat:nth-child(5) span', t('defense'))
  setText('.hero-strip .stat:nth-child(6) span', t('moveSpeed'))
  setText('.hero-strip .stat:nth-child(7) span', t('attackSpeed'))
  setText('.hero-strip .stat:nth-child(8) span', t('hpRegen'))
  setText('.hero-strip .stat:nth-child(9) span', t('power'))
  setText('#tickButton', t('pushTen'))
  setText('#equipBestButton', t('equipBest'))
  setText('#resetButton', t('reset'))
  setText('#recycleAllButton', t('recycleAll'))
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

function resetListRenderSignatures() {
  state.inventoryRenderSignature = ''
  state.systemShopRenderSignature = ''
  state.marketRenderSignature = ''
  state.equipmentSlotsRenderSignature = ''
  state.equippedRenderSignature = ''
  state.talentsRenderSignature = ''
  state.eventsRenderSignature = ''
}

function openListingPanel(item) {
  if (!item || !els.listingPanel) {
    return
  }
  state.listingDraftItemId = item.id
  state.listingDraftItem = item
  els.listingItemPreview.innerHTML = itemHtml(item, '')
  els.listingPriceInput.value = String(Math.max(20, Number(item.score || 0) * 2))
  els.listingPanel.classList.remove('hidden')
  els.listingPanel.setAttribute('aria-hidden', 'false')
  window.requestAnimationFrame(() => {
    els.listingPriceInput.focus()
    els.listingPriceInput.select()
  })
  setStatus(t('listingReady'))
}

function closeListingPanel() {
  state.listingDraftItemId = null
  state.listingDraftItem = null
  if (!els.listingPanel) {
    return
  }
  els.listingPanel.classList.add('hidden')
  els.listingPanel.setAttribute('aria-hidden', 'true')
  els.listingItemPreview.innerHTML = ''
}

function submitListingDraft() {
  const itemId = state.listingDraftItemId
  const parsed = Number.parseInt(els.listingPriceInput.value, 10)
  if (!itemId || !Number.isFinite(parsed) || parsed <= 0) {
    setStatus(t('invalidPrice'), false)
    return
  }
  closeListingPanel()
  postAction('/market/list', { item_id: itemId, price: parsed }, t('list'))
}

function togglePause(paused) {
  state.settings.paused = Boolean(paused)
  if (state.settings.paused) {
    state.tickQueuedSeconds = 0
  }
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
        resetListRenderSignatures()
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
  if (!state.gameReady || state.settings.paused) {
    return Promise.resolve()
  }
  if (state.tickInFlight) {
    state.tickQueuedSeconds += Math.max(0, Number(seconds) || 0)
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
      if (state.gameReady && !state.settings.paused && state.tickQueuedSeconds > 0) {
        const queuedSeconds = Math.min(1, state.tickQueuedSeconds)
        state.tickQueuedSeconds = Math.max(0, state.tickQueuedSeconds - queuedSeconds)
        window.setTimeout(() => tick(queuedSeconds), 0)
      }
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

function loadSessionToken() {
  try {
    return window.localStorage.getItem(SESSION_STORAGE_KEY) || ''
  } catch (error) {
    return ''
  }
}

function saveSessionToken(token) {
  window.localStorage.setItem(SESSION_STORAGE_KEY, token)
}

function clearSessionToken() {
  window.localStorage.removeItem(SESSION_STORAGE_KEY)
}

function setAccountStatus(text, ok = true) {
  if (!els.accountStatusText) {
    return
  }
  els.accountStatusText.textContent = text
  els.accountStatusText.style.color = ok ? '#9fb0a6' : '#ff9f7f'
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

function setStageLoading(show) {
  if (!els.stageLoading) {
    return
  }
  els.stageLoading.classList.toggle('hidden', !show)
  canvas.setAttribute('aria-busy', show ? 'true' : 'false')
}

function updateStageLoading() {
  if (!state.gameReady) {
    setStageLoading(false)
    return
  }
  state.stageReady = Boolean(state.assetsReady && state.snapshot && state.visual.ready)
  setStageLoading(!state.stageReady)
}

function stageAssetKeysForSnapshot(snapshot) {
  const hero = snapshot && snapshot.hero
  const gender = hero && hero.gender
  const keys = [gender === 'female' ? 'pixelHeroFemaleAssassin' : 'pixelHeroMaleAssassin']
  const equipmentItems = Object.values((hero && hero.equipped) || {})
  ;[hero && hero.weapon, hero && hero.offhand_weapon].forEach((item) => {
    if (item) {
      equipmentItems.push(item)
    }
  })
  equipmentItems.forEach((item) => {
    if (!item) {
      return
    }
    const key = equipmentAssetKey(equipmentAppearance(item))
    if (key) {
      keys.push(key)
    }
  })
  return Array.from(new Set(keys))
}

function waitForStageAssets(snapshot, token) {
  return Promise.allSettled(
    stageAssetKeysForSnapshot(snapshot).map((key) => assetLoadPromises[key]).filter(Boolean)
  ).then(() => {
    if (state.stageLoadToken !== token) {
      return
    }
    state.assetsReady = true
    window.requestAnimationFrame(updateStageLoading)
  })
}

function showAccountPanel() {
  stopGameLoop()
  showProfileGate(true)
  els.accountPanel.classList.remove('hidden')
  els.characterPanel.classList.add('hidden')
  els.creationPanel.classList.add('hidden')
  setStatus(t('waitingCreate'))
}

function showCharacterPanel() {
  stopGameLoop()
  showProfileGate(true)
  els.accountPanel.classList.add('hidden')
  els.characterPanel.classList.remove('hidden')
  els.creationPanel.classList.add('hidden')
  renderCharacterSlots(state.characters)
  setStatus(t('waitingCreate'))
}

function showCreationPanel() {
  state.creationDraft = null
  els.characterNameInput.value = ''
  els.rollCountText.textContent = remainingRollsText(3)
  els.rollTalentButton.disabled = false
  els.confirmCharacterButton.disabled = true
  renderCreationTalents()
  els.creationPanel.classList.remove('hidden')
  setProfileStatus('')
}

function accountName() {
  return els.accountUsernameInput.value.trim()
}

function accountPassword() {
  return els.accountPasswordInput.value
}

function renderCharacterSlots(characters = []) {
  state.characters = characters
  if (els.accountNameText && state.account) {
    els.accountNameText.textContent = state.account.username
  }
  const bySlot = new Map(characters.map((character) => [Number(character.slot_index), character]))
  const slots = []
  for (let slot = 0; slot < MAX_CHARACTER_SLOTS; slot += 1) {
    const character = bySlot.get(slot)
    if (character) {
      const active = character.character_id === state.activeCharacterId
      slots.push(`
        <article class="character-slot ${active ? 'active' : ''}">
          <div>
            <strong>${escapeHtml(character.name)}</strong>
            <span>${character.gender === 'female' ? '女' : '男'} · Slot ${slot + 1}</span>
          </div>
          <div class="character-actions">
            <button type="button" data-action="select-character" data-id="${escapeHtml(character.character_id)}">进入</button>
            <button class="muted" type="button" data-action="delete-character" data-id="${escapeHtml(character.character_id)}">删除</button>
          </div>
        </article>
      `)
    } else {
      slots.push(`
        <article class="character-slot empty-slot">
          <div>
            <strong>空角色位</strong>
            <span>Slot ${slot + 1}</span>
          </div>
          <button type="button" data-action="create-character">创建角色</button>
        </article>
      `)
    }
  }
  els.characterSlotList.innerHTML = slots.join('')
}

function applyAccountState(accountState) {
  state.account = accountState.account || null
  state.characters = accountState.characters || []
  state.activeCharacterId = accountState.active_character_id || null
  renderCharacterSlots(state.characters)
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
      applyAccountState(result)
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
  state.settings.paused = false
  state.tickQueuedSeconds = 0
  state.assetsReady = false
  state.stageReady = false
  state.stageLoadToken += 1
  const stageLoadToken = state.stageLoadToken
  saveSettings()
  if (els.pauseToggle) {
    els.pauseToggle.checked = false
  }
  showProfileGate(false)
  els.creationPanel.classList.add('hidden')
  updateStageLoading()
  if (snapshot) {
    applySnapshot(snapshot)
    waitForStageAssets(snapshot, stageLoadToken)
  } else {
    state.assetsReady = true
    updateStageLoading()
  }
  if (!state.tickTimer) {
    state.tickTimer = window.setInterval(() => tick(SIMULATION_STEP_SECONDS), SIMULATION_TICK_MS)
  }
}

function stopGameLoop() {
  state.gameReady = false
  state.stageLoadToken += 1
  state.stageReady = false
  setStageLoading(false)
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
  state.visual.cameraTargetX = 0
  state.visual.ready = false
  state.visual.cameraReady = false
  state.lootFloaters = []
  state.seenLootEventKeys = new Set()
  state.attackEffects = []
  state.seenAttackEventKeys = new Set()
  state.lastRenderAt = 0
}

function submitAccount(path) {
  const username = accountName()
  const password = accountPassword()
  const isRegister = path.includes('register')
  if (!username || !password) {
    setAccountStatus(currentLanguage() === 'zh-CN' ? '请输入账号和密码' : 'Enter username and password', false)
    return
  }
  els.loginButton.disabled = true
  els.registerButton.disabled = true
  api(path, {
    method: 'POST',
    body: { username, password }
  })
    .then((result) => {
      saveSessionToken(result.session_token)
      applyAccountState(result)
      setAccountStatus(isRegister
        ? (currentLanguage() === 'zh-CN' ? '账号已创建' : 'Account created')
        : (currentLanguage() === 'zh-CN' ? '登录成功' : 'Logged in'))
      if (result.active_character_id && !isRegister) {
        return api('/snapshot').then((snapshot) => {
          startGame(snapshot)
          setStatus(t('connected'))
        })
      }
      showCharacterPanel()
      if (isRegister && !(result.characters || []).length) {
        showCreationPanel()
      }
      return null
    })
    .catch((error) => {
      clearSessionToken()
      setAccountStatus(error.message || t('actionFail'), false)
    })
    .finally(() => {
      els.loginButton.disabled = false
      els.registerButton.disabled = false
    })
}

function refreshAccount() {
  return api('/account')
    .then((accountState) => {
      if (!accountState.authenticated) {
        clearSessionToken()
        showAccountPanel()
        return accountState
      }
      applyAccountState(accountState)
      return accountState
    })
}

function selectCharacter(characterId) {
  return api('/characters/select', {
    method: 'POST',
    body: { character_id: characterId }
  })
    .then((result) => {
      applyAccountState(result)
      startGame(result.snapshot)
      setStatus(t('connected'))
    })
    .catch((error) => {
      setAccountStatus(error.message || t('actionFail'), false)
    })
}

function deleteCharacter(characterId) {
  const shouldDelete = window.confirm(currentLanguage() === 'zh-CN'
    ? '删除角色后会腾出角色位，确认删除吗？'
    : 'Delete this hero and free the slot?')
  if (!shouldDelete) {
    return
  }
  api('/characters/delete', {
    method: 'POST',
    body: { character_id: characterId }
  })
    .then((result) => {
      applyAccountState(result)
      showCharacterPanel()
      setAccountStatus(currentLanguage() === 'zh-CN' ? '角色已删除' : 'Hero deleted')
    })
    .catch((error) => {
      setAccountStatus(error.message || t('actionFail'), false)
    })
}

function logoutAccount() {
  clearSessionToken()
  state.account = null
  state.characters = []
  state.activeCharacterId = null
  state.snapshot = null
  state.previousSnapshot = null
  stopGameLoop()
  showAccountPanel()
}

function bootstrapProfile() {
  renderCreationTalents()
  setStatus(t('connecting'))
  if (!loadSessionToken()) {
    showAccountPanel()
    return Promise.resolve(null)
  }
  return refreshAccount()
    .then((accountState) => {
      if (!accountState.authenticated) {
        return null
      }
      if (accountState.active_character_id) {
        return api('/snapshot').then((snapshot) => {
          startGame(snapshot)
          setStatus(t('connected'))
        })
      }
      showCharacterPanel()
      return null
    })
    .catch((error) => {
      clearSessionToken()
      showAccountPanel()
      setAccountStatus(error.message || t('profileInvalid'), false)
      setStatus(t('waitingCreate'), false)
    })
}

function applySnapshot(snapshot) {
  state.previousSnapshot = state.snapshot
  state.snapshot = snapshot
  snapVisualStateToSnapshot(snapshot)
  updateStageLoading()
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
  els.moveSpeedText.textContent = `${Number(hero.speed || 0).toFixed(1)} / ${t('seconds')}`
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

  renderEquipmentSlots(hero.equipment_slots || [], hero.equipped || {}, false)
  renderEquipped(hero.equipped || {}, false)
  renderTalents(hero.talents || [], hero.talent_scrolls || 0, snapshot.talent || {}, false)
  renderSystemShop((snapshot.system_shop && snapshot.system_shop.items) || [], hero.gold || 0, false)
  renderInventory(hero.inventory || [], false)
  renderMarket((snapshot.market && snapshot.market.active) || [], hero.id, false)
  renderEvents(snapshot.events || [], false)
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

function renderTalents(talents, scrolls, talentMeta, force = true) {
  const signature = talentsSignature(talents, scrolls, talentMeta || {})
  if (!force && state.talentsRenderSignature === signature) {
    return
  }
  state.talentsRenderSignature = signature
  const donations = Number(talentMeta.donations || 0)
  els.talentScrollText.textContent = `${t('talentScrolls')} ${scrolls} · ${t('donations')} ${donations}`
  els.talentCatalogText.textContent = `${t('catalog')} ${talentMeta.total_catalog_count || 0} · ${t('perLevel')}`
  if (!talents.length) {
    els.talentList.innerHTML = `<div class="empty">${t('noTalents')}</div>`
    return
  }
  const expandDisabled = !talentMeta.can_expand || state.talentEvolutionInFlight
  const expandHtml = `
    <div class="talent-expand-row">
      <span>${t('donations')} ${donations} / ${talentMeta.donation_cost || 5}</span>
      <button data-action="expand-talent" ${expandDisabled ? 'disabled' : ''}>${state.talentEvolutionInFlight ? t('expandingTalent') : t('expandTalent')}</button>
    </div>
  `
  els.talentList.innerHTML = talents
    .map((talent) => {
      const locked = talent.tier === 'mythic'
      const disabled = scrolls <= 0 || locked || state.talentEvolutionInFlight
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
    .join('') + expandHtml
}

function renderCurrentTalents() {
  const snapshot = state.snapshot
  if (!snapshot || !snapshot.hero) {
    return
  }
  renderTalents(snapshot.hero.talents || [], snapshot.hero.talent_scrolls || 0, snapshot.talent || {})
}

function evolveTalent(button) {
  if (state.talentEvolutionInFlight) {
    return
  }
  state.talentEvolutionInFlight = true
  button.disabled = true
  renderCurrentTalents()
  postAction('/talent/evolve', { talent_id: button.dataset.id }, t('evolve'))
    .finally(() => {
      state.talentEvolutionInFlight = false
      renderCurrentTalents()
    })
}

function equipmentSlotsSignature(slots, equipped) {
  return JSON.stringify({
    slots: slots.map(({ slot, item }) => ({ slot, item: item ? itemSignature(item) : null })),
    equipped: Object.keys(equipped || {})
      .sort()
      .map((slot) => [slot, itemSignature(equipped[slot])])
  })
}

function equippedSignature(equipped) {
  return Object.keys(equipped || {})
    .sort()
    .map((slot) => `${slot}:${itemSignature(equipped[slot])}`)
    .join('|')
}

function talentsSignature(talents, scrolls, talentMeta) {
  return JSON.stringify({
    scrolls,
    donations: talentMeta.donations || 0,
    canExpand: !!talentMeta.can_expand,
    evolving: state.talentEvolutionInFlight,
    total: talentMeta.total_catalog_count || 0,
    talents: talents.map((talent) => ({
      id: talent.id,
      tier: talent.tier,
      name: talent.name,
      description: talent.description,
      effects: talent.effects
    }))
  })
}

function eventsSignature(events) {
  return events
    .slice(-16)
    .map((event) => JSON.stringify({ tick: event.tick, kind: event.kind, message: event.message, data: event.data || {} }))
    .join('|')
}

function renderEquipmentSlots(slots, equipped, force = true) {
  const normalized = slots.length
    ? slots
    : Object.keys(SLOT_LABELS).map((slot) => ({ slot, item: equipped[slot] || null }))
  const signature = equipmentSlotsSignature(normalized, equipped || {})
  if (!force && state.equipmentSlotsRenderSignature === signature) {
    return
  }
  state.equipmentSlotsRenderSignature = signature
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

function renderEquipped(equipped, force = true) {
  const signature = equippedSignature(equipped || {})
  if (!force && state.equippedRenderSignature === signature) {
    return
  }
  state.equippedRenderSignature = signature
  const items = Object.keys(equipped).map((slot) => equipped[slot])
  if (!items.length) {
    els.equippedList.innerHTML = `<div class="empty">${t('noEquipment')}</div>`
    return
  }
  const bonuses = (state.snapshot && state.snapshot.hero && state.snapshot.hero.set_bonuses) || []
  els.equippedList.innerHTML = items.map((item) => itemHtml(item, '')).join('') + renderSetBonuses(bonuses)
}

function itemSignature(item) {
  return JSON.stringify({
    id: item.id,
    name: item.name,
    slot: item.slot,
    rarity: item.rarity,
    level: item.level,
    attack: item.attack,
    defense: item.defense,
    max_hp: item.max_hp,
    attack_speed: item.attack_speed,
    hp_regen: item.hp_regen,
    attack_range: item.attack_range,
    weapon_type: item.weapon_type,
    owner_id: item.owner_id,
    score: item.score,
    special: item.special,
    set_id: item.set_id,
    set_name: item.set_name,
    set_piece: item.set_piece
  })
}

function inventorySignature(items) {
  return JSON.stringify({
    recycleAllInFlight: state.recycleAllInFlight,
    pending: Array.from(state.inventoryActionInFlightIds).sort(),
    items: items.map((item) => itemSignature(item))
  })
}

function expandTalentWithDonations(button) {
  if (state.talentEvolutionInFlight) {
    return
  }
  state.talentEvolutionInFlight = true
  button.disabled = true
  renderCurrentTalents()
  postAction('/talent/donate', {}, t('expandTalent'))
    .finally(() => {
      state.talentEvolutionInFlight = false
      renderCurrentTalents()
    })
}

function systemShopSignature(items, heroGold) {
  return JSON.stringify({
    heroGold,
    pending: Array.from(state.systemShopActionInFlightSkus).sort(),
    items: items.map((item) => ({
      sku: item.sku,
      name: item.name,
      kind: item.kind,
      slot: item.slot,
      rarity: item.rarity,
      level: item.level,
      price: item.price,
      affordable: item.affordable,
      description: item.description
    }))
  })
}

function marketSignature(listings, heroId) {
  return listings
    .map((listing) => JSON.stringify({
      id: listing.id,
      seller_id: listing.seller_id,
      own: listing.seller_id === heroId,
      price: listing.price,
      pending: state.marketActionInFlightIds.has(listing.id),
      item: itemSignature(listing.item)
    }))
    .join('|')
}

function renderSystemShop(items, heroGold, force = true) {
  if (!els.systemShopList) {
    return
  }
  const signature = systemShopSignature(items, heroGold)
  if (!force && state.systemShopRenderSignature === signature) {
    return
  }
  state.systemShopRenderSignature = signature
  if (!items.length) {
    els.systemShopList.innerHTML = `<div class="empty">${t('systemShopEmpty')}</div>`
    return
  }
  els.systemShopList.innerHTML = items
    .map((entry) => {
      const pending = state.systemShopActionInFlightSkus.has(entry.sku)
      const affordable = entry.affordable !== false && Number(heroGold || 0) >= Number(entry.price || 0)
      const rarity = entry.rarity || (entry.kind === 'donation' ? 'gold' : 'white')
      const token = entry.kind === 'donation' ? 'D' : slotLabel(entry.slot || '')
      const subLine = entry.kind === 'donation'
        ? t('buyDonation')
        : `${slotLabel(entry.slot)} · ${rarityLabel(entry.rarity)} · Lv.${entry.level || 1}`
      return `
        <article class="item shop-item rarity-${rarity}">
          <div class="item-visual">
            <div class="shop-token rarity-${rarity}">${escapeHtml(token)}</div>
            <div class="item-copy">
              <div class="item-main">
                <span class="item-name">${escapeHtml(entry.name || entry.sku)}</span>
                <span class="price">${entry.price || 0} ${t('priceGold')}</span>
              </div>
              <div class="item-sub">${subLine}</div>
              <div class="item-sub">${escapeHtml(entry.description || '')}</div>
              <div class="item-actions">
                <button data-action="system-shop-buy" data-sku="${escapeHtml(entry.sku)}" ${pending || !affordable ? 'disabled' : ''}>${pending ? t('shopBuying') : t('shopBuy')}</button>
              </div>
            </div>
          </div>
        </article>
      `
    })
    .join('')
}

function renderInventory(items, force = true) {
  if (state.listingDraftItemId && !items.some((item) => item.id === state.listingDraftItemId)) {
    closeListingPanel()
  }
  if (els.recycleAllButton) {
    els.recycleAllButton.disabled = !items.length || state.recycleAllInFlight
    els.recycleAllButton.textContent = state.recycleAllInFlight ? t('recycling') : t('recycleAll')
  }
  const signature = inventorySignature(items)
  if (!force && state.inventoryRenderSignature === signature) {
    return
  }
  state.inventoryRenderSignature = signature
  if (!items.length) {
    els.inventoryList.innerHTML = `<div class="empty">${t('emptyInventory')}</div>`
    return
  }
  els.inventoryList.innerHTML = items
    .map((item) => {
      const defaultPrice = Math.max(20, item.score * 2)
      const pending = state.inventoryActionInFlightIds.has(item.id)
      const actions = `
        <div class="item-actions">
          <button data-action="equip" data-id="${item.id}" ${pending ? 'disabled' : ''}>${t('equip')}</button>
          <button class="muted" data-action="list" data-id="${item.id}" data-price="${defaultPrice}" ${pending ? 'disabled' : ''}>${t('list')}</button>
          <button class="muted" data-action="recycle" data-id="${item.id}" ${pending ? 'disabled' : ''}>${pending ? t('recycling') : t('recycle')}</button>
        </div>
      `
      return itemHtml(item, actions)
    })
    .join('')
}

function renderMarket(listings, heroId, force = true) {
  const signature = marketSignature(listings, heroId)
  if (!force && state.marketRenderSignature === signature) {
    return
  }
  state.marketRenderSignature = signature
  if (!listings.length) {
    els.marketList.innerHTML = `<div class="empty">${t('marketEmpty')}</div>`
    return
  }
  els.marketList.innerHTML = listings
    .map((listing) => {
      const item = listing.item
      const own = listing.seller_id === heroId
      const pending = state.marketActionInFlightIds.has(listing.id)
      const actionButton = own
        ? `
          <button class="muted" data-action="cancel-listing" data-id="${listing.id}" ${pending ? 'disabled' : ''}>${pending ? t('cancelingListing') : t('cancelListing')}</button>
          <button data-action="sell-to-system" data-id="${listing.id}" ${pending ? 'disabled' : ''}>${pending ? t('sellingSystem') : t('sellSystem')} (${item.score})</button>
        `
        : `<button data-action="buy" data-id="${listing.id}" ${pending ? 'disabled' : ''}>${pending ? t('buying') : t('buy')}</button>`
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
                ${actionButton}
              </div>
            </div>
          </div>
        </article>
      `
    })
    .join('')
}

function renderEvents(events, force = true) {
  const signature = eventsSignature(events)
  if (!force && state.eventsRenderSignature === signature) {
    return
  }
  state.eventsRenderSignature = signature
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
    if (!isLootFloatEvent(event)) {
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
      rarity: lootFloatRarity(event),
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

function isLootFloatEvent(event) {
  return isLootEvent(event) || event.kind === 'gold_loss'
}

function lootEventKey(event) {
  const data = event.data || {}
  return `${event.tick}:${event.kind}:${data.item_id || data.gold_lost || event.message}`
}

function lootFloatText(event) {
  if (event.kind === 'gold_loss') {
    return goldLossFloatText(event)
  }
  const data = event.data || {}
  return `+1 ${translateItemName(data.item_name || event.message || t('lootFallback'))}`
}

function goldLossFloatText(event) {
  const data = event.data || {}
  return `-${Number(data.gold_lost || 0)} ${t('gold')}`
}

function lootFloatRarity(event) {
  if (event.kind === 'gold_loss') {
    return 'red'
  }
  return (event.data && event.data.rarity) || 'white'
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
  const slot = safeClassName(item.slot === 'ring' ? 'ring-pet' : item.slot || appearance.slot)
  const assetPath = equipmentAssetPath(appearance)
  const imageStyle = assetPath ? `;--gear-image:url('${assetPath.replace(/'/g, '%27')}')` : ''
  const imageClass = assetPath ? ' gear-has-image' : ''
  return `
    <span class="gear-preview gear-slot-${slot} gear-model-${model}${appearance.aura ? ' gear-aura' : ''}${imageClass}" style="${style}${imageStyle}" aria-hidden="true">
      <span class="gear-core"></span>
      <span class="gear-edge"></span>
    </span>
  `
}

function equipmentAppearance(item) {
  if (item && item.appearance) {
    if (item.slot === 'ring') {
      return {
        ...item.appearance,
        slot: 'ring',
        model: ringPetModel(item, item.appearance),
        icon_shape: 'pet'
      }
    }
    return item.appearance
  }
  const palette = FALLBACK_GEAR_PALETTES[(item && item.rarity) || 'white'] || FALLBACK_GEAR_PALETTES.white
  return {
    slot: (item && item.slot) || 'weapon',
    model: item && item.slot === 'ring' ? ringPetModel(item) : (item && item.weapon_type) || (item && item.slot) || 'blade',
    palette,
    aura: item && ['purple', 'gold', 'red', 'rainbow'].includes(item.rarity),
    icon_shape: item && item.slot === 'ring' ? 'pet' : 'slash'
  }
}

function ringPetModel(item, appearance = {}) {
  const existing = String((appearance && appearance.model) || '')
  if (existing.includes('pet')) {
    return existing
  }
  return {
    white: 'sprout_pet',
    green: 'leaf_pet',
    blue: 'moon_cat_pet',
    purple: 'star_bunny_pet',
    gold: 'spark_fox_pet',
    red: 'ember_fox_pet',
    rainbow: 'ember_fox_pet'
  }[(item && item.rarity) || 'white'] || 'sprout_pet'
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
      ring: 'Ring Pet'
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

function equipmentAssetKey(appearance) {
  return EQUIPMENT_MODEL_ASSET_KEYS[String((appearance && appearance.model) || '').toLowerCase()] || null
}

function equipmentAssetPath(appearance) {
  const key = equipmentAssetKey(appearance)
  return key ? ASSET_PATHS[key] : ''
}

function equipmentSpriteImage(appearance) {
  const key = equipmentAssetKey(appearance)
  return key ? assetImage(key) : null
}

function drawEquipmentSprite(appearance, x, y, width, height, options = {}) {
  const image = equipmentSpriteImage(appearance)
  if (!image) {
    return false
  }
  const anchorX = Number.isFinite(options.anchorX) ? options.anchorX : width / 2
  const anchorY = Number.isFinite(options.anchorY) ? options.anchorY : height / 2
  const alpha = Number.isFinite(options.alpha) ? options.alpha : 1
  const scaleX = Number.isFinite(options.scaleX) ? options.scaleX : 1
  const scaleY = Number.isFinite(options.scaleY) ? options.scaleY : 1
  ctx.save()
  ctx.translate(x, y)
  if (Number.isFinite(options.rotation) && options.rotation !== 0) {
    ctx.rotate(options.rotation)
  }
  if (options.flipX) {
    ctx.scale(-1, 1)
  }
  ctx.scale(scaleX, scaleY)
  ctx.globalAlpha *= alpha
  ctx.drawImage(image, -anchorX, -anchorY, width, height)
  ctx.restore()
  return true
}

function drawWingEquipmentSprite(appearance, anchor, width, height, rareScale = 1, alpha = 1) {
  const image = equipmentSpriteImage(appearance)
  if (!image) {
    return false
  }
  const now = state.lastRenderAt || 0
  const wingFlap = Math.sin(now / 150)
  const flapScaleX = 0.98 + Math.abs(wingFlap) * 0.08
  const flapScaleY = 1.02 + wingFlap * 0.1
  ctx.save()
  ctx.translate(anchor.x - width * 0.04, anchor.y - 22 * rareScale)
  ctx.rotate(-0.03 - wingFlap * 0.06)
  ctx.scale(flapScaleX, flapScaleY)
  ctx.globalAlpha *= alpha
  ctx.drawImage(image, -width * 0.72, -height * 0.54, width, height)
  ctx.restore()
  return true
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

function movingEntity(entity) {
  return entity && (entity.state === 'walk' || entity.state === 'approach' || entity.visualCombatApproach)
}

function accumulateWalkDistance(entity, fromX, toX) {
  if (!entity) {
    return
  }
  if (!movingEntity(entity)) {
    entity.visualWalkDistance = 0
    return
  }
  const delta = Math.abs(Number(toX || 0) - Number(fromX || 0))
  if (!Number.isFinite(delta) || delta <= 0) {
    return
  }
  entity.visualWalkDistance = Number((Number(entity.visualWalkDistance || 0) + delta).toFixed(3))
}

function walkCycleFrame(entity, frameCount) {
  const sequence = walkFrameSequence(frameCount)
  const distance = Math.max(0, Number(entity && entity.visualWalkDistance || 0))
  return sequence[Math.floor(distance / WALK_PIXELS_PER_FRAME) % sequence.length] || 0
}

function walkFrameSequence(frameCount) {
  const maxFrame = Math.max(0, Number(frameCount || 1) - 1)
  const sequence = WALK_FRAME_SEQUENCE.filter((frame) => frame <= maxFrame)
  return sequence.length ? sequence : [0]
}

function spriteSheetFrameInfo(sprite, actionName, entity) {
  if (!sprite || !sprite.actions) {
    return null
  }
  const action = sprite.actions[actionName] || sprite.actions.idle
  if (!action) {
    return null
  }
  const frameCount = Math.max(1, Number(action.frames || 1))
  const frameMs = Math.max(1, Number(action.frameMs || 100))
  const timedFrame = Math.floor((state.lastRenderAt || 0) / frameMs) % frameCount
  const frame = actionName === 'walk' ? walkCycleFrame(entity, frameCount) : timedFrame
  return {
    action,
    frame,
    frameCount,
    frameMs
  }
}

function drawSpriteSheetFrameBottom(sprite, actionName, centerX, bottomY, flip = false, entity = null) {
  if (!sprite || !sprite.key) {
    return false
  }
  const image = assetImage(sprite.key)
  if (!image) {
    return false
  }
  const frameInfo = spriteSheetFrameInfo(sprite, actionName, entity)
  if (!frameInfo) {
    return false
  }
  const action = frameInfo.action
  const frameWidth = Number(sprite.frameWidth || image.naturalWidth)
  const frameHeight = Number(sprite.frameHeight || image.naturalHeight)
  const frame = frameInfo.frame
  const sourceX = frame * frameWidth
  const sourceY = Number(action.row || 0) * frameHeight
  const drawWidth = Number(sprite.drawWidth || frameWidth)
  const drawHeight = Number(sprite.drawHeight || frameHeight)
  const x = centerX - drawWidth / 2
  const y = bottomY - drawHeight
  ctx.save()
  ctx.imageSmoothingEnabled = false
  if (flip) {
    ctx.translate(x + drawWidth, y)
    ctx.scale(-1, 1)
    ctx.drawImage(image, sourceX, sourceY, frameWidth, frameHeight, 0, 0, drawWidth, drawHeight)
  } else {
    ctx.drawImage(image, sourceX, sourceY, frameWidth, frameHeight, x, y, drawWidth, drawHeight)
  }
  ctx.restore()
  return true
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
    position: entity.position ? { ...entity.position } : entity.position,
    visualTarget: entity.visualTarget ? { ...entity.visualTarget } : entity.visualTarget,
    visualWalkDistance: Number(entity.visualWalkDistance || 0)
  }
}

function clonePosition(position) {
  return position ? { x: Number(position.x || 0), y: Number(position.y || 0) } : null
}

function approachVisualPosition(current, target, maxStep) {
  const currentValue = Number(current || 0)
  const targetValue = Number(target || 0)
  if (!Number.isFinite(currentValue) || !Number.isFinite(targetValue)) {
    return Number.isFinite(targetValue) ? targetValue : currentValue
  }
  const delta = targetValue - currentValue
  if (Math.abs(delta) <= maxStep) {
    return targetValue
  }
  return currentValue + Math.sign(delta) * maxStep
}

function spawnVisualPosition(entity, snapshot, currentEntities) {
  const target = clonePosition(entity.position)
  if (!target || entity.type !== 'monster') {
    return target
  }
  const currentHero = currentEntities.find((candidate) => candidate.type === 'hero' && candidate.position)
  const snapshotHero = snapshot.scene.entities.find((candidate) => candidate.type === 'hero' && candidate.position)
  const heroX = Number((currentHero && currentHero.position && currentHero.position.x)
    || (snapshotHero && snapshotHero.position && snapshotHero.position.x)
    || 0)
  if (!Number.isFinite(heroX)) {
    return target
  }
  return {
    ...target,
    x: Math.max(target.x, heroX + MONSTER_SPAWN_SCREEN_BUFFER)
  }
}

function transitioningIntoCombatRange(current, next) {
  if (!current || !next || next.type !== 'hero' || next.state !== 'combat' || !movingEntity(current)) {
    return false
  }
  const currentX = Number(current.position && current.position.x)
  const targetX = Number(next.position && next.position.x)
  return Number.isFinite(currentX) && Number.isFinite(targetX) && currentX < targetX - 0.5
}

function combatVisualRangeGrace(hero) {
  const range = Number(hero && hero.attack_range || 0)
  if (!Number.isFinite(range)) {
    return COMBAT_VISUAL_RANGE_GRACE
  }
  return Math.max(COMBAT_VISUAL_RANGE_GRACE, range * 0.45)
}

function visibleMonsterWithinAttackRange(hero, monster) {
  if (!hero || !monster || !hero.position || !monster.position) {
    return false
  }
  const heroX = Number(hero.position.x)
  const monsterX = Number(monster.position.x)
  const range = Number(hero.attack_range || 0)
  if (!Number.isFinite(heroX) || !Number.isFinite(monsterX) || !Number.isFinite(range)) {
    return false
  }
  const visualGrace = combatVisualRangeGrace(hero)
  return monsterX - heroX <= Math.max(0, range) + visualGrace
}

function clearVisualCombatApproach(hero, monster = null) {
  if (!hero || !hero.visualCombatApproach) {
    return
  }
  if (visibleMonsterWithinAttackRange(hero, monster)) {
    hero.visualCombatApproach = false
    hero.visualWalkDistance = 0
    return
  }
  if (!hero.position || !hero.visualTarget) {
    return
  }
  const targetX = Number(hero.visualTarget.x)
  const currentX = Number(hero.position.x)
  if (!Number.isFinite(targetX) || !Number.isFinite(currentX) || currentX < targetX - 0.5) {
    return
  }
  hero.position.x = Number(targetX.toFixed(3))
  hero.visualCombatApproach = false
  hero.visualWalkDistance = 0
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
    next.visualTarget = clonePosition(entity.position)
    if (current) {
      next.visualWalkDistance = Number(current.visualWalkDistance || 0)
    }
    if (!current || !current.position || !next.position) {
      const spawnPosition = spawnVisualPosition(next, snapshot, currentEntities)
      if (spawnPosition) {
        next.position = spawnPosition
      }
      return next
    }
    const currentX = Number(current.position.x || 0)
    const nextX = Number(next.position.x || 0)
    if (transitioningIntoCombatRange(current, next)) {
      next.position.x = currentX
      next.position.y = Number(current.position.y || next.position.y || 0)
      next.visualCombatApproach = true
      return next
    }
    if (next.type === 'hero' && movingEntity(next)) {
      next.position.x = currentX
      next.position.y = Number(current.position.y || next.position.y || 0)
      return next
    }
    if (Math.abs(nextX - currentX) > VISUAL_SNAP_DISTANCE) {
      next.position.x = approachVisualPosition(currentX, nextX, VISUAL_SNAP_DISTANCE)
      next.position.y = Number(current.position.y || next.position.y || 0)
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
    state.visual.cameraTargetX = Number(camera.x || 0)
    state.visual.cameraReady = true
  }
}

function syncCameraToHeroBounds(cameraX, heroX) {
  const nextCameraX = Math.max(0, Number(cameraX || 0))
  if (!Number.isFinite(heroX)) {
    return nextCameraX
  }
  const center = Math.max(0, heroX - HERO_CAMERA_OFFSET)
  const minCameraX = Math.max(0, center - HERO_CAMERA_MAX_LAG)
  const maxCameraX = Math.max(0, center + HERO_CAMERA_MAX_LEAD)
  return Math.max(minCameraX, Math.min(maxCameraX, nextCameraX))
}

function visualCameraTarget(hero, speed, seconds, visualStep = null) {
  const snapshotTargetX = Math.max(0, Number(hero && hero.visualTarget && hero.visualTarget.x || 0) - HERO_CAMERA_OFFSET)
  const heroX = Number(hero && hero.position && hero.position.x || 0)
  if (movingEntity(hero) && Number.isFinite(speed) && speed > 0) {
    const fallbackCameraStep = speed * Math.max(0, seconds)
    const cameraStep = Number.isFinite(visualStep) ? Math.max(0, Number(visualStep)) : fallbackCameraStep
    const nextCameraX = state.visual.cameraX + cameraStep
    return syncCameraToHeroBounds(nextCameraX, heroX)
  }
  return Math.max(0, Number.isFinite(heroX) ? heroX - HERO_CAMERA_OFFSET : snapshotTargetX)
}

function advanceMovingVisualCamera(cameraTargetX) {
  const targetX = Number(cameraTargetX || 0)
  state.visual.cameraTargetX = Number.isFinite(targetX) ? targetX : 0
  state.visual.cameraX = state.visual.cameraTargetX
  state.visual.cameraY = 0
}

function advanceRestingVisualCamera(cameraTargetX, seconds) {
  const targetX = Number(cameraTargetX || 0)
  state.visual.cameraTargetX = Number.isFinite(targetX) ? targetX : 0
  applyCameraDamping(state.visual.cameraTargetX, 0, seconds * 1000)
}

function shouldSkipMovingEntityLerp(entity) {
  return entity && entity.type === 'hero' && movingEntity(entity)
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
  const amount = 1 - Math.exp(-(Math.max(0, seconds)) * VISUAL_ENTITY_DAMPING)
  let heroVisualStep = 0
  if (movingEntity(hero) && Number.isFinite(speed) && speed > 0) {
    let nextX = Number(hero.position.x || 0) + speed * Math.max(0, seconds)
    if (monster) {
      const range = Number(hero.attack_range || (state.snapshot && state.snapshot.hero && state.snapshot.hero.attack_range) || 0)
      const monsterTargetX = Number((monster.visualTarget && monster.visualTarget.x) || monster.position.x || nextX)
      nextX = Math.min(nextX, monsterTargetX - range)
    }
    if (Number.isFinite(nextX)) {
      const previousX = Number(hero.position.x || 0)
      hero.position.x = Number(nextX.toFixed(3))
      heroVisualStep = Math.max(0, hero.position.x - previousX)
      accumulateWalkDistance(hero, previousX, hero.position.x)
    }
  }
  for (const entity of state.visual.entities) {
    if (!entity.position || !entity.visualTarget) {
      continue
    }
    const targetX = Number(entity.visualTarget.x || entity.position.x || 0)
    const targetY = Number(entity.visualTarget.y || entity.position.y || 0)
    const currentX = Number(entity.position.x || 0)
    const currentY = Number(entity.position.y || 0)
    if (shouldSkipMovingEntityLerp(entity)) {
      entity.position.y = Number(lerp(currentY, targetY, amount).toFixed(3))
      continue
    }
    entity.position.x = Number(lerp(currentX, targetX, amount).toFixed(3))
    entity.position.y = Number(lerp(currentY, targetY, amount).toFixed(3))
    accumulateWalkDistance(entity, currentX, entity.position.x)
  }
  clearVisualCombatApproach(hero, monster)
  const cameraTargetX = visualCameraTarget(hero, speed, seconds, heroVisualStep)
  if (movingEntity(hero)) {
    advanceMovingVisualCamera(cameraTargetX)
  } else {
    advanceRestingVisualCamera(cameraTargetX, seconds)
  }
}

function visualCameraOffset(cameraX) {
  const offset = Number(cameraX || 0)
  return Number.isFinite(offset) ? offset : 0
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

window.__idleForestDebug = function idleForestDebug() {
  const visualHero = (state.visual.entities || []).find((entity) => entity.type === 'hero')
  const visualMonster = (state.visual.entities || []).find((entity) => entity.type === 'monster')
  const snapshotHero = state.snapshot && state.snapshot.scene
    ? (state.snapshot.scene.entities || []).find((entity) => entity.type === 'hero')
    : null
  const snapshotMonster = state.snapshot && state.snapshot.scene
    ? (state.snapshot.scene.entities || []).find((entity) => entity.type === 'monster')
    : null
  const visualDistance = visualHero && visualMonster && visualHero.position && visualMonster.position
    ? Number((Number(visualMonster.position.x || 0) - Number(visualHero.position.x || 0)).toFixed(2))
    : null
  const snapshotDistance = snapshotHero && snapshotMonster && snapshotHero.position && snapshotMonster.position
    ? Number((Number(snapshotMonster.position.x || 0) - Number(snapshotHero.position.x || 0)).toFixed(2))
    : null
  const visualHeroX = visualHero && visualHero.position ? Number(Number(visualHero.position.x || 0).toFixed(2)) : null
  const visualMonsterX = visualMonster && visualMonster.position ? Number(Number(visualMonster.position.x || 0).toFixed(2)) : null
  const snapshotHeroX = snapshotHero && snapshotHero.position ? Number(Number(snapshotHero.position.x || 0).toFixed(2)) : null
  const snapshotMonsterX = snapshotMonster && snapshotMonster.position ? Number(Number(snapshotMonster.position.x || 0).toFixed(2)) : null
  return {
    gameReady: state.gameReady,
    tickInFlight: state.tickInFlight,
    tickQueuedSeconds: Number(state.tickQueuedSeconds.toFixed(3)),
    tickTimerActive: Boolean(state.tickTimer),
    paused: Boolean(state.settings.paused),
    snapshotTick: state.snapshot && state.snapshot.time ? state.snapshot.time.tick : null,
    snapshotHeroState: snapshotHero && snapshotHero.state,
    snapshotHeroX,
    snapshotMonsterX,
    snapshotDistance,
    visualHeroState: visualHero && visualHero.state,
    visualHeroX,
    visualMonsterX,
    visualCombatApproach: Boolean(visualHero && visualHero.visualCombatApproach),
    visualDistance,
    visualSpeed: visualHero && visualHero.speed,
    attackRange: visualHero && visualHero.attack_range,
    combatVisualGrace: visualHero ? combatVisualRangeGrace(visualHero) : null,
    attackEffects: state.attackEffects.length,
    lastRenderAt: state.lastRenderAt
  }
}

function updateIdleForestDebugDataset() {
  if (!document || !document.documentElement || !window.__idleForestDebug) {
    return
  }
  document.documentElement.dataset.idleDebug = JSON.stringify(window.__idleForestDebug())
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
  const frameDelta = Math.min(VISUAL_MAX_FRAME_DELTA_MS, Math.max(0, timestamp - previousRenderAt))
  state.lastRenderAt = timestamp
  const rect = canvas.getBoundingClientRect()
  advanceVisualState(frameDelta / 1000)
  updateIdleForestDebugDataset()
  renderScene(visualSnapshot(), rect.width, rect.height)
  window.requestAnimationFrame(draw)
}

function renderScene(snapshot, width, height) {
  const scene = snapshot && snapshot.scene
  const biome = scene ? scene.biome : 'forest'
  const cameraX = scene && scene.camera ? scene.camera.x : 0
  const visualCameraX = visualCameraOffset(cameraX)
  const groundY = Math.round(height * 0.72)
  const worldScale = Math.max(0.78, Math.min(1.32, width / 720))

  drawBackground(biome, width, height)
  if (scene) {
    drawDecorations(scene.decorations || [], visualCameraX, groundY, worldScale, width, 'back', biome)
    drawGround(biome, width, height, groundY, visualCameraX, worldScale)
    drawDecorations(scene.decorations || [], visualCameraX, groundY, worldScale, width, 'front', biome)
    drawCombatRange(scene.entities || [], visualCameraX, groundY, worldScale)
    drawEntities(scene.entities || [], visualCameraX, groundY, worldScale)
    drawAttackEffects(scene, visualCameraX, groundY, worldScale)
    drawLootFloaters(scene, visualCameraX, groundY, worldScale)
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
  if (drawSmoothGroundTexture(biome, width, height, groundY, cameraX, worldScale)) {
    ctx.strokeStyle = 'rgba(245, 236, 214, 0.24)'
    ctx.lineWidth = 2
    ctx.beginPath()
    ctx.moveTo(0, groundY + 1)
    ctx.lineTo(width, groundY + 1)
    ctx.stroke()
    return
  }
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
      red: 34,
      rainbow: 44
    }[rarity] || 6,
    trails: {
      white: 1,
      green: 2,
      blue: 2,
      purple: 3,
      gold: 4,
      red: 5,
      rainbow: 6
    }[rarity] || 1,
    width: {
      white: 4,
      green: 5,
      blue: 6,
      purple: 7,
      gold: 8,
      red: 10,
      rainbow: 12
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
    if (['purple', 'gold', 'red', 'rainbow'].includes(effect.rarity) && i % 5 === 0) {
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

function heroWeaponProfile(entity) {
  const equipped = (entity && entity.equipped) || {}
  const main = equipped.weapon || (entity && entity.weapon) || null
  const offhand = (entity && entity.offhand_weapon) || equipped.offhand_weapon || null
  const rawType = String((main && main.weapon_type) || 'unarmed').toLowerCase()
  const type = rawType.includes('bow')
    ? 'bow'
    : rawType.includes('spear') || rawType.includes('pole') || rawType.includes('staff')
      ? 'spear'
      : rawType.includes('axe') || rawType.includes('hammer') || rawType.includes('heavy') || rawType.includes('great')
        ? 'heavy'
        : rawType.includes('dual') || rawType.includes('dagger_pair')
          ? 'dual'
          : rawType.includes('dagger') || rawType.includes('blade') || rawType.includes('sword')
            ? 'blade'
            : rawType
  return {
    main,
    offhand,
    type,
    dual: Boolean(offhand) || type === 'dual'
  }
}

function weaponAnimationType(profile) {
  if (!profile || !profile.main) return 'attack_unarmed'
  if (profile.dual) return 'attack_dual'
  if (profile.type === 'bow') return 'attack_bow'
  if (profile.type === 'spear') return 'attack_spear'
  if (profile.type === 'heavy') return 'attack_heavy'
  return 'attack_blade'
}

function pixelHeroAction(entity, weaponProfile = heroWeaponProfile(entity)) {
  if (!entity) return 'idle'
  if (entity.state === 'reviving') return 'revive'
  if (Number(entity.hp || 0) <= 0) return 'death'
  if (entity.visualCombatApproach) return 'walk'
  if (entity.state === 'combat') {
    if (entity.gender === 'female') {
      return weaponProfile && weaponProfile.dual ? 'attack_dual' : 'attack_blade'
    }
    return weaponAnimationType(weaponProfile)
  }
  if (entity.state === 'walk' || entity.state === 'approach') return 'walk'
  return 'idle'
}

function pixelHeroRenderInfo(skeleton, entity) {
  const key = entity.gender === 'female' ? 'female_assassin' : 'male_assassin'
  const sprite = PIXEL_SPRITES.heroes[key]
  if (!sprite) {
    return false
  }
  const weaponProfile = heroWeaponProfile(entity)
  const actionName = pixelHeroAction(entity, weaponProfile)
  const frameInfo = spriteSheetFrameInfo(sprite, actionName, entity)
  const bottomY = Math.max(skeleton.leftFoot.y, skeleton.rightFoot.y) + 4
  return {
    sprite,
    actionName,
    centerX: skeleton.hips.x + 1,
    bottomY,
    frame: frameInfo ? frameInfo.frame : 0,
    anchors: heroEquipmentAnchorsForFrame(skeleton, entity, actionName, frameInfo ? frameInfo.frame : 0, sprite)
  }
}

function drawPixelHero(skeleton, entity, renderInfo = null) {
  const info = renderInfo || pixelHeroRenderInfo(skeleton, entity)
  if (!info) {
    return false
  }
  const drew = drawSpriteSheetFrameBottom(
    info.sprite,
    info.actionName,
    info.centerX,
    info.bottomY,
    false,
    entity
  )
  if (!drew) {
    return false
  }
  return {
    actionName: info.actionName,
    frame: info.frame,
    anchors: info.anchors
  }
}

function heroEquipmentAnchorsForFrame(skeleton, entity, actionName, frame, sprite) {
  const source = heroFrameSkeletonAnchorPoints(actionName, frame, sprite)
    || heroPixelAnchorPoints(actionName, frame, sprite.anchors, sprite.actions && sprite.actions[actionName])
    || heroPixelHandPoints(actionName, frame, entity && entity.gender === 'female')
  const centerX = skeleton.hips.x + 1
  const bottomY = Math.max(skeleton.leftFoot.y, skeleton.rightFoot.y) + 4
  const frameWidth = Number(sprite.frameWidth || 96)
  const frameHeight = Number(sprite.frameHeight || 96)
  const drawWidth = Number(sprite.drawWidth || frameWidth)
  const drawHeight = Number(sprite.drawHeight || frameHeight)
  const x = centerX - drawWidth / 2
  const y = bottomY - drawHeight
  const scaleX = drawWidth / frameWidth
  const scaleY = drawHeight / frameHeight
  const sourceScaleX = source.frameBased ? 1 : frameWidth / 96
  const sourceScaleY = source.frameBased ? 1 : frameHeight / 96
  const mapPoint = (point) => ({
    x: x + point.x * sourceScaleX * scaleX,
    y: y + point.y * sourceScaleY * scaleY,
    angle: point.angle
  })
  const mainHand = mapPoint(source.rightHand)
  const offHand = mapPoint(source.leftHand)
  return {
    ...skeleton,
    rightHand: mainHand,
    leftHand: offHand,
    mainHand,
    offHand,
    ringHand: mapPoint(source.ringHand || source.leftHand),
    head: mapPoint(source.head),
    torso: mapPoint(source.torso),
    halo: mapPoint(source.halo || { x: source.head.x, y: source.head.y - 14, angle: 0 }),
    back: mapPoint(source.back || { x: source.torso.x - 12, y: source.torso.y, angle: 0 }),
    feetCenter: mapPoint(source.feetCenter || { x: 48, y: 92, angle: 0 }),
    weaponTip: mapPoint(source.weaponTip)
  }
}

function heroFrameSkeletonAnchorPoints(actionName, frame, sprite) {
  const frameAnchors = sprite && sprite.frameAnchors
  if (!frameAnchors) {
    return null
  }
  const aliases = [actionName]
  if (actionName.startsWith('attack_') && actionName !== 'attack_bow') {
    aliases.push('attack_blade')
  }
  const sequence = aliases.map((name) => frameAnchors[name]).find((value) => Array.isArray(value))
  if (!sequence || !sequence.length) {
    return null
  }
  const [mainRaw, offRaw, tipRaw] = sequence[Math.abs(frame) % sequence.length]
  const triplet = (value) => ({ x: value[0], y: value[1], angle: value[2] || 0 })
  const basePoint = (name, fallback, angle = 0) => {
    const value = sprite.anchors && sprite.anchors[name] ? sprite.anchors[name] : fallback
    return { x: value[0], y: value[1], angle }
  }
  const mainHand = triplet(mainRaw)
  const offHand = triplet(offRaw)
  return {
    frameBased: true,
    leftHand: offHand,
    rightHand: mainHand,
    ringHand: basePoint('ringHand', [38, 83]),
    head: basePoint('head', [64, 30]),
    torso: basePoint('torso', [62, 70]),
    halo: basePoint('halo', [64, 1]),
    back: basePoint('back', [42, 31]),
    feetCenter: basePoint('feetCenter', [61, 126]),
    weaponTip: tipRaw ? triplet(tipRaw) : {
      x: mainHand.x + Math.cos(mainHand.angle) * 54,
      y: mainHand.y + Math.sin(mainHand.angle) * 54,
      angle: mainHand.angle
    }
  }
}

function heroPixelAnchorPoints(actionName, frame, anchors, action) {
  if (!anchors) {
    return null
  }
  const frameCount = Math.max(1, Number(action && action.frames || 8))
  const phase = (frame / Math.max(1, frameCount - 1)) * Math.PI * 2
  const attack = actionName.startsWith('attack')
  const attackProgress = attack ? Math.min(1, frame / Math.max(1, frameCount - 1)) : 0
  const attackEase = attack ? smoothstep(attackProgress) : 0
  const swing = attack ? Math.sin(attackProgress * Math.PI) : 0
  const bob = Math.sin(phase) * 1.2
  const point = (name, fallback, dx = 0, dy = 0, angle = 0) => {
    const value = anchors[name] || fallback
    return {
      x: value[0] + dx,
      y: value[1] + dy,
      angle
    }
  }
  const bowAttack = actionName === 'attack_bow'
  const mainAngle = attack
    ? bowAttack
      ? -0.08
      : -1.35 + attackEase * 1.7
    : -0.18
  const offAngle = attack && actionName === 'attack_dual' ? -2.6 + attackEase * 0.7 : -2.35
  const mainHand = point(
    'mainHand',
    [82, 75],
    attack ? -7 * swing + attackEase * 7 : 0,
    attack ? -13 * swing + attackEase * 7 : bob,
    mainAngle
  )
  const offHandDrift = attack ? 4 + swing * 6 - attackEase * 2 : Math.sin(phase) * 1.4
  const offHandLift = attack ? -7 + swing * 4 : bob * 0.6
  const offHand = point('offHand', [47, 78], offHandDrift, offHandLift, offAngle)
  const ringHandDrift = attack ? 1 + swing * 2 : Math.sin(phase) * 1.2
  const ringHandLift = attack ? -4 + swing * 2 : bob * 0.6
  const ringHand = point('ringHand', [53, 68], ringHandDrift, ringHandLift, offAngle)
  return {
    frameBased: true,
    leftHand: offHand,
    rightHand: mainHand,
    ringHand,
    head: point('head', [64, 34], 0, bob * 0.4, 0),
    torso: point('torso', [62, 70], 0, bob * 0.35, 0),
    halo: point('halo', [64, 23], 0, bob * 0.25, 0),
    back: point('back', [49, 70], -Math.max(0, swing) * 2, bob * 0.2, 0),
    feetCenter: point('feetCenter', [64, 120], 0, 0, 0),
    weaponTip: {
      x: mainHand.x + Math.cos(mainHand.angle) * 54,
      y: mainHand.y + Math.sin(mainHand.angle) * 54,
      angle: mainHand.angle
    }
  }
}

function heroPixelHandPoints(actionName, frame) {
  const phase = (frame / 8) * Math.PI * 2
  const breath = Math.round(Math.sin(phase) * 1)
  const stride = Math.round(Math.sin(phase) * 5)
  const torsoY = 45 + breath
  const headY = 29 + breath
  const attackCurve = [0, 3, 9, 15, 18, 10, 4, 0][frame] || 0
  const attacking = actionName.startsWith('attack_')
  const lean = attacking ? Math.round(attackCurve / 5) : actionName === 'hurt' ? -5 : 0
  let leftHand = {
    x: 31 + lean - (actionName === 'walk' ? stride / 3 : 0),
    y: torsoY + 16,
    angle: -2.45
  }
  let rightHand = {
    x: 63 + lean + (actionName === 'walk' ? stride / 3 : 0),
    y: torsoY + 14,
    angle: -0.28
  }

  if (actionName === 'attack_unarmed') {
    rightHand = { x: 66 + lean + attackCurve, y: torsoY + 12 - attackCurve / 6, angle: -0.35 }
    leftHand = { x: 34 + lean, y: torsoY + 11, angle: -2.2 }
  } else if (actionName === 'attack_blade') {
    rightHand = { x: 63 + lean + attackCurve, y: torsoY + 9 - attackCurve / 5, angle: -0.72 }
    leftHand = { x: 33 + lean, y: torsoY + 17, angle: -2.32 }
  } else if (actionName === 'attack_dual') {
    rightHand = { x: 61 + lean + attackCurve, y: torsoY + 8 - attackCurve / 5, angle: -0.82 }
    leftHand = { x: 35 + lean + attackCurve / 2, y: torsoY + 20 + attackCurve / 9, angle: -2.95 }
  } else if (actionName === 'attack_bow') {
    rightHand = { x: 39 + lean - attackCurve / 5, y: torsoY + 5, angle: -0.08 }
    leftHand = { x: 65 + lean + attackCurve / 3, y: torsoY + 7, angle: -0.08 }
  } else if (actionName === 'attack_spear') {
    rightHand = { x: 54 + lean + attackCurve / 2, y: torsoY + 13, angle: -0.2 }
    leftHand = { x: 72 + lean + attackCurve, y: torsoY + 8 - attackCurve / 8, angle: -0.2 }
  } else if (actionName === 'attack_heavy') {
    rightHand = { x: 56 + lean + attackCurve / 2, y: torsoY - 4 + attackCurve / 5, angle: -1.18 }
    leftHand = { x: 43 + lean + attackCurve / 3, y: torsoY - 3 + attackCurve / 5, angle: -1.18 }
  }

  return {
    leftHand,
    rightHand,
    head: { x: 49 + lean, y: headY - 1, angle: 0 },
    torso: { x: 48 + lean, y: torsoY + 12, angle: 0 },
    weaponTip: {
      x: rightHand.x + Math.cos(rightHand.angle) * 52,
      y: rightHand.y + Math.sin(rightHand.angle) * 52,
      angle: rightHand.angle
    }
  }
}

function drawHero(x, y, entity) {
  const skeleton = createHeroSkeleton(x, y, entity)
  drawMovementTrail(x, y, entity)
  drawTalentAura(skeleton, entity)
  if (entity.state === 'reviving') {
    drawReviveAura(skeleton, entity)
  }
  const pixelInfo = pixelHeroRenderInfo(skeleton, entity)
  const equipmentSkeleton = pixelInfo && pixelInfo.anchors ? pixelInfo.anchors : skeleton
  drawEquippedFootCircle(equipmentSkeleton, (entity.equipped || {}).boots)
  drawEquippedWings(equipmentSkeleton, (entity.equipped || {}).armor)
  const drewPixelHero = drawPixelHero(skeleton, entity, pixelInfo)
  if (!drewPixelHero) {
    drawHeroRig(skeleton, entity)
  }
  drawEquippedHalo(equipmentSkeleton, (entity.equipped || {}).helmet)
  drawRingPet(equipmentSkeleton, (entity.equipped || {}).ring)
  drawEquippedWeapon(equipmentSkeleton, entity)
  drawEquippedParticleEffects(equipmentSkeleton, entity)
  drawHeroHealthBar(equipmentSkeleton, entity)
}

function movementIntensity(entity) {
  const speed = Number(
    entity.speed ||
    (state.snapshot && state.snapshot.hero && state.snapshot.hero.speed) ||
    0
  )
  return Math.max(0, Math.min(1, (speed - 38) / 70))
}

function drawMovementTrail(x, groundY, entity) {
  const intensity = movementIntensity(entity)
  if (intensity <= 0 || (entity.state !== 'walk' && entity.state !== 'approach')) {
    return
  }
  const pulse = 0.75 + Math.sin((state.lastRenderAt || 0) / 90) * 0.25
  ctx.save()
  ctx.globalAlpha = (0.12 + intensity * 0.2) * pulse
  ctx.strokeStyle = '#c7f0d0'
  ctx.lineWidth = 1.5 + intensity * 1.5
  ctx.lineCap = 'round'
  for (let index = 0; index < 4; index += 1) {
    const offset = 18 + index * 13
    const lift = 16 + index * 4
    ctx.beginPath()
    ctx.moveTo(x - offset, groundY - lift)
    ctx.quadraticCurveTo(x - offset - 18, groundY - lift - 11, x - offset - 36, groundY - lift + 2)
    ctx.stroke()
  }
  ctx.restore()
}

function drawHeroHealthBar(skeleton, entity) {
  const anchor = heroHealthBarAnchor(skeleton)
  drawHealthBar(anchor.x - 29, anchor.y, 58, 7, entity.hp, entity.max_hp, '#5fd18b')
}

function heroHealthBarAnchor(skeleton) {
  const head = skeleton.head || skeleton.halo || skeleton.torso || { x: 0, y: 0 }
  const halo = haloAnchorFromSkeleton(skeleton)
  return {
    x: head.x,
    y: Math.min(head.y - 92, halo.y - 26)
  }
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
    halo: { x: head.x, y: head.y - 18, angle: 0 },
    back: { x: torso.x - 16, y: torso.y + 1, angle: 0 },
    feetCenter: { x, y: y + 1, angle: 0 },
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
  drawPixellabTalentAura(skeleton, style)
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
  if (effects.all_stats_pct || names.includes('龙')) {
    return {
      kind: 'dragon',
      assetKey: 'talentDragonEffect',
      color: '#ffca55',
      secondary: '#ff78e6',
      strength: Math.min(1.42, 0.78 + Number(effects.all_stats_pct || 0) * 4.2)
    }
  }
  if (effects.attack_pct || names.includes('火')) {
    return {
      kind: 'flame',
      assetKey: 'talentFlameEffect',
      color: '#ff7a7c',
      secondary: '#ffca55',
      strength: Math.min(1.36, 0.74 + Number(effects.attack_pct || 0) * 3.2)
    }
  }
  if (effects.move_speed_pct || names.includes('雷') || names.includes('疾风')) {
    return {
      kind: 'lightning',
      assetKey: 'talentLightningEffect',
      color: '#68b7ff',
      secondary: '#ffca55',
      strength: Math.min(1.4, 0.72 + Number(effects.move_speed_pct || 0) * 3)
    }
  }
  if (effects.defense_pct || effects.max_hp_pct) {
    return {
      kind: 'ward',
      assetKey: 'talentFlameEffect',
      color: '#5fd18b',
      secondary: '#68b7ff',
      strength: Math.min(1.25, 0.66 + Number((effects.defense_pct || 0) + (effects.max_hp_pct || 0)) * 2)
    }
  }
  if (effects.attack_pct || effects.all_stats_pct) {
    return {
      kind: 'mote',
      assetKey: 'talentDragonEffect',
      color: '#ff7a7c',
      secondary: '#ffca55',
      strength: Math.min(1.25, 0.7 + Number((effects.attack_pct || 0) + (effects.all_stats_pct || 0)) * 2.5)
    }
  }
  if (effects.drop_rate_pct || effects.gold_pct || effects.exp_pct || effects.rift_drop_rate_pct) {
    return {
      kind: 'mote',
      assetKey: 'talentDragonEffect',
      color: '#ffca55',
      secondary: '#b779ff',
      strength: 0.78
    }
  }
  return null
}

function drawPixellabTalentAura(skeleton, style) {
  const image = style.assetKey ? assetImages[style.assetKey] : null
  if (!image || !image.complete || image.naturalWidth <= 0) {
    return false
  }
  const now = state.lastRenderAt || 0
  const pulse = 0.5 + animationPhase(style.kind === 'lightning' ? 460 : 720) * 0.5
  const size = (style.kind === 'dragon' ? 122 : 108) * style.strength * (0.96 + pulse * 0.08)
  const yOffset = style.kind === 'dragon' ? 2 : 4
  const spin = style.kind === 'lightning'
    ? Math.sin(now / 220) * 0.16
    : (now / (style.kind === 'flame' ? 1700 : 2300)) * (style.kind === 'dragon' ? -1 : 1)
  ctx.save()
  ctx.translate(skeleton.torso.x, skeleton.torso.y + yOffset)
  ctx.rotate(spin)
  ctx.globalAlpha = style.kind === 'dragon' ? 0.58 : 0.48
  ctx.drawImage(image, -size / 2, -size / 2, size, size)
  ctx.restore()
  return true
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

function drawSmoothGroundTexture(biome, width, height, groundY, cameraX, worldScale) {
  if (biome !== 'forest' && biome !== 'deep_forest') {
    return false
  }
  const scroll = cameraX * worldScale * 0.35
  const groundScuffSpacing = 92
  ctx.save()
  ctx.fillStyle = biome === 'deep_forest' ? 'rgba(76, 92, 58, 0.16)' : 'rgba(105, 132, 67, 0.18)'
  for (let x = -groundScuffSpacing - (scroll % groundScuffSpacing); x < width + groundScuffSpacing; x += groundScuffSpacing) {
    const y = groundY + 16 + Math.sin((x + scroll) * 0.018) * 5
    ctx.beginPath()
    ctx.ellipse(x, y, 34, 5, -0.12, 0, Math.PI * 2)
    ctx.fill()
  }
  ctx.strokeStyle = biome === 'deep_forest' ? 'rgba(93, 120, 69, 0.24)' : 'rgba(122, 155, 80, 0.26)'
  ctx.lineWidth = 2
  for (let layer = 0; layer < 3; layer += 1) {
    const layerScroll = scroll * (0.45 + layer * 0.18)
    const y = groundY + 28 + layer * 22
    ctx.beginPath()
    ctx.moveTo(0, y)
    for (let x = -24; x <= width + 24; x += 24) {
      ctx.lineTo(x, y + Math.sin((x + layerScroll) * 0.024 + layer * 1.7) * (3 + layer))
    }
    ctx.stroke()
  }
  ctx.fillStyle = biome === 'deep_forest' ? 'rgba(18, 42, 27, 0.38)' : 'rgba(40, 83, 44, 0.34)'
  for (let x = -72 - ((scroll * 0.72) % 72); x < width + 72; x += 72) {
    const bladeBase = groundY - 5 + Math.sin((x + scroll) * 0.03) * 2
    ctx.fillRect(x, bladeBase, 22, 4)
    ctx.fillRect(x + 27, bladeBase + 3, 16, 3)
  }
  ctx.restore()
  return true
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

function drawEquippedWings(skeleton, armor) {
  if (!armor) {
    return
  }
  const appearance = equipmentAppearance(armor)
  const palette = appearance.palette || FALLBACK_GEAR_PALETTES.white
  const anchor = skeleton.back || skeleton.torso
  const pulse = 0.55 + animationPhase(680) * 0.45
  const rareScale = armor.rarity === 'red' ? 1.24 : armor.rarity === 'gold' ? 1.14 : armor.rarity === 'purple' ? 1.08 : 1
  const spread = 52 * rareScale + pulse * 6
  const lift = 58 * rareScale
  drawEquipmentGlow(anchor, appearance, 68 * rareScale, 76 * rareScale)
  const wingWidth = 188 * rareScale
  const wingHeight = 126 * rareScale
  if (drawWingEquipmentSprite(appearance, anchor, wingWidth, wingHeight, rareScale, 0.82 + pulse * 0.1)) {
    if (['purple', 'gold', 'red', 'rainbow'].includes(armor.rarity)) {
      drawWingSparks(anchor, palette, armor.rarity, spread)
    }
    return
  }
  ctx.save()
  ctx.globalAlpha = 0.66
  ctx.fillStyle = palette.primary
  ctx.strokeStyle = palette.glow
  ctx.lineWidth = armor.rarity === 'white' ? 1.4 : 2.2
  ;[-1, 1].forEach((side) => {
    ctx.beginPath()
    ctx.moveTo(anchor.x + side * 3, anchor.y - 4)
    ctx.bezierCurveTo(
      anchor.x + side * spread * 0.42,
      anchor.y - lift,
      anchor.x + side * spread,
      anchor.y - lift * 0.65,
      anchor.x + side * (spread + 8),
      anchor.y - 4
    )
    ctx.bezierCurveTo(
      anchor.x + side * spread * 0.58,
      anchor.y + 6,
      anchor.x + side * spread * 0.28,
      anchor.y + 18,
      anchor.x + side * 3,
      anchor.y + 8
    )
    ctx.closePath()
    ctx.fill()
    ctx.stroke()
    ctx.strokeStyle = palette.accent
    ctx.lineWidth = 1.4
    for (let line = 0; line < 3; line += 1) {
      ctx.beginPath()
      ctx.moveTo(anchor.x + side * 7, anchor.y + line * 4)
      ctx.quadraticCurveTo(
        anchor.x + side * (18 + line * 8),
        anchor.y - 11 - line * 9,
        anchor.x + side * (spread - line * 4),
        anchor.y - 3 + line * 5
      )
      ctx.stroke()
    }
  })
  if (['purple', 'gold', 'red', 'rainbow'].includes(armor.rarity)) {
    drawWingSparks(anchor, palette, armor.rarity, spread)
  }
  ctx.restore()
}

function drawEquippedHalo(skeleton, helmet) {
  if (!helmet) {
    return
  }
  const appearance = equipmentAppearance(helmet)
  const palette = appearance.palette || FALLBACK_GEAR_PALETTES.white
  const anchor = haloAnchorFromSkeleton(skeleton)
  const pulse = 0.5 + animationPhase(520) * 0.5
  const radiusX = helmet.rarity === 'red' ? 29 : helmet.rarity === 'gold' ? 26 : 22
  const radiusY = helmet.rarity === 'red' ? 10 : 8
  drawEquipmentGlow(anchor, appearance, radiusX * 1.4, radiusY + 20)
  const now = state.lastRenderAt || 0
  const haloSpin = now / (helmet.rarity === 'red' || helmet.rarity === 'gold' ? 520 : 680)
  const haloPulse = 0.98 + pulse * 0.12
  const haloWidth = appearance.model === 'crown_helm' ? 78 : 68
  const haloHeight = appearance.model === 'crown_helm' ? 28 : 22
  if (drawEquipmentSprite(appearance, anchor.x, anchor.y, haloWidth, haloHeight, {
    alpha: 0.94,
    scaleX: haloPulse,
    scaleY: 0.98 + pulse * 0.07
  })) {
    drawHaloBurst(anchor, palette, haloSpin, haloWidth, haloHeight, helmet.rarity, pulse)
    return
  }
  ctx.save()
  ctx.strokeStyle = palette.glow
  ctx.lineWidth = helmet.rarity === 'white' ? 2 : 2.7
  ctx.globalAlpha = 0.82
  ctx.beginPath()
  ctx.ellipse(anchor.x, anchor.y, radiusX + pulse * 2.4, radiusY + pulse, -0.08, 0, Math.PI * 2)
  ctx.stroke()
  ctx.globalAlpha = 0.32
  ctx.strokeStyle = palette.primary
  ctx.beginPath()
  ctx.ellipse(anchor.x, anchor.y + 1.5, radiusX * 0.72, radiusY * 0.62, -0.08, 0, Math.PI * 2)
  ctx.stroke()
  if (appearance.model === 'crown_helm' || ['gold', 'red', 'rainbow'].includes(helmet.rarity)) {
    ctx.globalAlpha = 0.78
    ctx.fillStyle = palette.glow
    for (let i = -2; i <= 2; i += 1) {
      triangle(anchor.x + i * 8, anchor.y - 15 - Math.abs(i) * 2, 5, 9 + (2 - Math.abs(i)) * 2)
    }
  }
  ctx.restore()
}

function drawEquippedFootCircle(skeleton, boots) {
  if (!boots) {
    return
  }
  const appearance = equipmentAppearance(boots)
  const palette = appearance.palette || FALLBACK_GEAR_PALETTES.white
  const anchor = skeleton.feetCenter || {
    x: (skeleton.leftFoot.x + skeleton.rightFoot.x) / 2,
    y: (skeleton.leftFoot.y + skeleton.rightFoot.y) / 2
  }
  const pulse = 0.45 + animationPhase(620) * 0.55
  const radiusX = boots.rarity === 'red' ? 34 : boots.rarity === 'gold' ? 30 : 25
  const radiusY = boots.rarity === 'red' ? 9 : 7
  const now = state.lastRenderAt || 0
  const auraSpin = now / (boots.rarity === 'rainbow' ? 760 : boots.rarity === 'red' || boots.rarity === 'gold' ? 980 : 1220)
  const auraWidth = radiusX * 3.7
  const auraHeight = Math.max(58, radiusY * 7.2)
  const auraPulse = 0.98 + pulse * 0.08
  if (drawEquipmentSprite(appearance, anchor.x, anchor.y + 8, auraWidth, auraHeight, {
    alpha: 0.84 + pulse * 0.08,
    scaleX: auraPulse,
    scaleY: auraPulse
  })) {
    drawFootAuraOrbit(anchor, palette, auraSpin, auraWidth, auraHeight, boots.rarity)
    return
  }
  ctx.save()
  ctx.globalAlpha = 0.16 + pulse * 0.14
  ctx.fillStyle = palette.glow
  ctx.beginPath()
  ctx.ellipse(anchor.x, anchor.y + 5, radiusX + pulse * 4, radiusY + pulse * 1.5, 0, 0, Math.PI * 2)
  ctx.fill()
  ctx.globalAlpha = 0.78
  ctx.strokeStyle = palette.primary
  ctx.lineWidth = 2
  ctx.beginPath()
  ctx.ellipse(anchor.x, anchor.y + 5, radiusX, radiusY, 0, 0, Math.PI * 2)
  ctx.stroke()
  ctx.strokeStyle = palette.accent
  ctx.lineWidth = 1.5
  for (let i = 0; i < 5; i += 1) {
    const angle = (i / 5) * Math.PI * 2 + (state.lastRenderAt || 0) / 900
    ctx.beginPath()
    ctx.arc(anchor.x + Math.cos(angle) * radiusX * 0.62, anchor.y + 5 + Math.sin(angle) * radiusY * 0.62, 2.2, 0, Math.PI * 2)
    ctx.stroke()
  }
  ctx.restore()
}

function haloAnchorFromSkeleton(skeleton) {
  const head = skeleton.head || skeleton.halo || skeleton.torso
  if (!head) {
    return { x: 0, y: 0, angle: 0 }
  }
  const halo = skeleton.halo || head
  const horizontalDrift = Math.max(-6, Math.min(6, Number((halo.x || head.x) - head.x) * 0.35))
  const verticalGap = skeleton.frameBased ? 72 : 42
  return {
    x: head.x + horizontalDrift + 1,
    y: head.y - verticalGap,
    angle: 0
  }
}

function drawHaloBurst(anchor, palette, spin, haloWidth, haloHeight, rarity, pulse) {
  const count = rarity === 'red' ? 12 : rarity === 'gold' ? 10 : 8
  const radiusX = haloWidth * 0.43
  const radiusY = haloHeight * 0.38
  ctx.save()
  ctx.globalAlpha = 0.26 + pulse * 0.22
  ctx.strokeStyle = palette.glow
  ctx.lineWidth = rarity === 'white' ? 1.4 : 2
  ctx.beginPath()
  ctx.ellipse(anchor.x, anchor.y, haloWidth * (0.48 + pulse * 0.05), haloHeight * (0.45 + pulse * 0.05), -0.06, 0, Math.PI * 2)
  ctx.stroke()
  for (let i = 0; i < count; i += 1) {
    const angle = spin + (i / count) * Math.PI * 2
    const x = anchor.x + Math.cos(angle) * radiusX
    const y = anchor.y - 1 + Math.sin(angle) * radiusY
    const trailX = anchor.x + Math.cos(angle - 0.32) * radiusX
    const trailY = anchor.y - 1 + Math.sin(angle - 0.32) * radiusY
    ctx.globalAlpha = 0.18 + animationPhase(320 + i * 13) * 0.34
    ctx.strokeStyle = i % 2 === 0 ? palette.glow : palette.primary
    ctx.lineWidth = rarity === 'red' ? 2.2 : 1.6
    ctx.beginPath()
    ctx.moveTo(trailX, trailY)
    ctx.lineTo(x, y)
    ctx.stroke()
    ctx.globalAlpha = 0.5 + animationPhase(360 + i * 19) * 0.5
    ctx.fillStyle = i % 2 === 0 ? palette.glow : palette.primary
    ctx.beginPath()
    ctx.arc(x, y, rarity === 'red' ? 3.1 : rarity === 'gold' ? 2.7 : 2.2, 0, Math.PI * 2)
    ctx.fill()
  }
  for (let i = 0; i < 6; i += 1) {
    const angle = spin * 0.7 + i * (Math.PI * 2 / 6)
    const x = anchor.x + Math.cos(angle) * (haloWidth * 0.53)
    const y = anchor.y + Math.sin(angle) * (haloHeight * 0.5)
    ctx.globalAlpha = 0.2 + pulse * 0.28
    ctx.strokeStyle = palette.glow
    ctx.lineWidth = 1.2
    ctx.beginPath()
    ctx.moveTo(x - Math.cos(angle) * 3, y - Math.sin(angle) * 3)
    ctx.lineTo(x + Math.cos(angle) * 7, y + Math.sin(angle) * 7)
    ctx.stroke()
  }
  ctx.restore()
}

function drawFootAuraOrbit(anchor, palette, spin, auraWidth, auraHeight, rarity) {
  const count = rarity === 'red' ? 9 : rarity === 'gold' ? 8 : 6
  const radiusX = auraWidth * 0.34
  const radiusY = auraHeight * 0.26
  ctx.save()
  ctx.lineWidth = rarity === 'white' ? 1.2 : 1.8
  for (let i = 0; i < count; i += 1) {
    const angle = spin + (i / count) * Math.PI * 2
    const x = anchor.x + Math.cos(angle) * radiusX
    const y = anchor.y + 8 + Math.sin(angle) * radiusY
    ctx.globalAlpha = 0.34 + animationPhase(480 + i * 17) * 0.42
    ctx.fillStyle = i % 2 === 0 ? palette.glow : palette.primary
    ctx.beginPath()
    ctx.arc(x, y, rarity === 'red' ? 2.8 : 2.2, 0, Math.PI * 2)
    ctx.fill()
  }
  ctx.restore()
}

function drawWingSparks(anchor, palette, rarity, spread) {
  const count = rarity === 'red' ? 9 : rarity === 'gold' ? 7 : 5
  const now = state.lastRenderAt || 0
  for (let i = 0; i < count; i += 1) {
    const side = i % 2 === 0 ? -1 : 1
    const phase = now / (520 + i * 31) + i
    const x = anchor.x + side * (16 + (i % 4) * (spread / 7)) + Math.cos(phase) * 4
    const y = anchor.y - 26 + Math.sin(phase * 1.4) * 18
    ctx.globalAlpha = 0.28 + animationPhase(360 + i * 20) * 0.36
    ctx.fillStyle = i % 3 === 0 ? palette.glow : palette.primary
    ctx.beginPath()
    ctx.arc(x, y, rarity === 'red' ? 2.5 : 2, 0, Math.PI * 2)
    ctx.fill()
  }
  ctx.globalAlpha = 1
}

function drawRingPet(skeleton, ring) {
  if (!ring) {
    return
  }
  const appearance = equipmentAppearance(ring)
  const anchor = ringPetAnchor(skeleton.ringHand || skeleton.offHand)
  drawEquipmentGlow(anchor, appearance, 18, 16)
  const petSize = ring.rarity === 'red' ? 38 : ring.rarity === 'gold' ? 36 : 34
  const now = state.lastRenderAt || 0
  const petHop = Math.sin(now / 210)
  const petSquash = Math.max(0, petHop) * 0.08
  if (drawEquipmentSprite(appearance, anchor.x, anchor.y + 2 - Math.max(0, petHop) * 2.6, petSize, petSize, {
    alpha: 1,
    rotation: Math.sin(now / 290) * 0.1,
    scaleX: 1 + petSquash,
    scaleY: 1 - petSquash * 0.7
  })) {
    if (['purple', 'gold', 'red', 'rainbow'].includes(ring.rarity)) {
      const palette = appearance.palette || FALLBACK_GEAR_PALETTES.white
      drawPetSparkles(anchor, palette, ring.rarity, 0.5 + animationPhase(580) * 0.5)
    }
    return
  }
  drawPetBody(anchor, appearance, ring)
}

function ringPetAnchor(hand) {
  const bob = Math.sin((state.lastRenderAt || 0) / 260) * 2
  return {
    x: hand.x + 2,
    y: hand.y - 3 + bob,
    angle: hand.angle
  }
}

function drawPetBody(anchor, appearance, ring) {
  const palette = appearance.palette || FALLBACK_GEAR_PALETTES.white
  const rarity = (ring && ring.rarity) || 'white'
  const model = String(appearance.model || '')
  const scale = rarity === 'red' ? 1.14 : rarity === 'gold' ? 1.08 : 1
  const bodyColor = model.includes('fox') ? '#f0a45f' : model.includes('bunny') ? '#f0d4ef' : model.includes('cat') ? '#c9d8ee' : palette.primary
  const bellyColor = model.includes('fox') ? '#ffe1b2' : model.includes('bunny') ? '#fff0fb' : '#eef6f1'
  const earColor = model.includes('fox') ? '#d96c43' : palette.accent
  const pulse = 0.5 + animationPhase(580) * 0.5

  ctx.save()
  ctx.globalAlpha = 0.26
  ctx.fillStyle = palette.glow
  ctx.beginPath()
  ctx.ellipse(anchor.x, anchor.y + 13 * scale, 13 * scale, 5 * scale, 0, 0, Math.PI * 2)
  ctx.fill()

  ctx.globalAlpha = 1
  ctx.fillStyle = bodyColor
  ctx.strokeStyle = palette.accent
  ctx.lineWidth = 1.6
  ctx.beginPath()
  ctx.ellipse(anchor.x, anchor.y + 3, 12 * scale, 10 * scale, 0, 0, Math.PI * 2)
  ctx.fill()
  ctx.stroke()

  ctx.fillStyle = bellyColor
  ctx.beginPath()
  ctx.ellipse(anchor.x + 1, anchor.y + 6, 5 * scale, 4 * scale, 0, 0, Math.PI * 2)
  ctx.fill()

  ctx.fillStyle = earColor
  if (model.includes('bunny')) {
    roundPetEar(anchor.x - 7 * scale, anchor.y - 10 * scale, 4 * scale, 11 * scale, -0.22)
    roundPetEar(anchor.x + 6 * scale, anchor.y - 10 * scale, 4 * scale, 11 * scale, 0.18)
  } else {
    triangle(anchor.x - 7 * scale, anchor.y - 8 * scale, 8 * scale, 11 * scale)
    triangle(anchor.x + 7 * scale, anchor.y - 8 * scale, 8 * scale, 11 * scale)
  }

  ctx.fillStyle = model.includes('fox') ? '#f5c078' : palette.primary
  ctx.beginPath()
  ctx.ellipse(anchor.x - 12 * scale, anchor.y + 4 * scale, 5 * scale, 9 * scale, -0.7, 0, Math.PI * 2)
  ctx.fill()
  ctx.fillStyle = bellyColor
  ctx.beginPath()
  ctx.arc(anchor.x - 15 * scale, anchor.y - 1 * scale, 2.6 * scale, 0, Math.PI * 2)
  ctx.fill()

  ctx.fillStyle = '#101817'
  ctx.fillRect(anchor.x - 4 * scale, anchor.y + 1 * scale, 2.4 * scale, 2.4 * scale)
  ctx.fillRect(anchor.x + 5 * scale, anchor.y + 1 * scale, 2.4 * scale, 2.4 * scale)
  ctx.fillStyle = '#f5ecd6'
  ctx.fillRect(anchor.x - 3.6 * scale, anchor.y + 1 * scale, 0.9 * scale, 0.9 * scale)
  ctx.fillRect(anchor.x + 5.4 * scale, anchor.y + 1 * scale, 0.9 * scale, 0.9 * scale)

  ctx.strokeStyle = '#1b211f'
  ctx.lineWidth = 1.4
  ctx.beginPath()
  ctx.arc(anchor.x + 1, anchor.y + 4 * scale, 3 * scale, 0.1, Math.PI - 0.1)
  ctx.stroke()

  if (['purple', 'gold', 'red', 'rainbow'].includes(rarity)) {
    drawPetSparkles(anchor, palette, rarity, pulse)
  }
  ctx.restore()
}

function roundPetEar(x, y, width, height, rotation) {
  ctx.save()
  ctx.translate(x, y)
  ctx.rotate(rotation)
  ctx.beginPath()
  ctx.ellipse(0, 0, width, height, 0, 0, Math.PI * 2)
  ctx.fill()
  ctx.restore()
}

function drawPetSparkles(anchor, palette, rarity, pulse) {
  const count = rarity === 'rainbow' ? 8 : rarity === 'red' ? 6 : rarity === 'gold' ? 5 : 4
  const now = state.lastRenderAt || 0
  for (let i = 0; i < count; i += 1) {
    const angle = now / (420 + i * 24) + i * 1.8
    ctx.globalAlpha = 0.26 + pulse * 0.32
    ctx.fillStyle = i % 2 === 0 ? palette.glow : palette.primary
    ctx.beginPath()
    ctx.arc(anchor.x + Math.cos(angle) * (14 + i), anchor.y + Math.sin(angle * 1.4) * 9, 1.7, 0, Math.PI * 2)
    ctx.fill()
  }
  ctx.globalAlpha = 1
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
    helmet: skeleton.halo || skeleton.head,
    armor: skeleton.back || skeleton.torso,
    boots: skeleton.feetCenter || {
      x: (skeleton.leftFoot.x + skeleton.rightFoot.x) / 2,
      y: (skeleton.leftFoot.y + skeleton.rightFoot.y) / 2
    },
    ring: ringPetAnchor(skeleton.ringHand || skeleton.offHand)
  }
  Object.keys(equipped).forEach((slot) => {
    const item = equipped[slot]
    if (!item) {
      return
    }
    const appearance = equipmentAppearance(item)
    if (!appearance.aura && !['purple', 'gold', 'red', 'rainbow'].includes(item.rarity)) {
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
  const weaponProfile = heroWeaponProfile(entity)
  if (weaponProfile.type === 'bow' && weaponProfile.main) {
    drawBowOnHands(skeleton.offHand, skeleton.mainHand, weaponProfile.main)
    return
  }
  if (entity.offhand_weapon) {
    drawWeaponOnHand(skeleton.offHand, entity.offhand_weapon, true)
  } else if (weaponProfile.dual && weaponProfile.main) {
    drawWeaponOnHand(skeleton.offHand, weaponProfile.main, true)
  }
  if (equipped.weapon) {
    drawWeaponOnHand(skeleton.mainHand, equipped.weapon)
  } else if (entity.weapon) {
    drawWeaponOnHand(skeleton.mainHand, entity.weapon)
  }
}

function drawBowOnHands(frontHand, drawHand, weapon) {
  const appearance = equipmentAppearance(weapon)
  const palette = appearance.palette || FALLBACK_GEAR_PALETTES.white
  const dx = drawHand.x - frontHand.x
  const dy = drawHand.y - frontHand.y
  const angle = Math.atan2(dy, dx)
  const pull = Math.max(12, Math.min(38, Math.hypot(dx, dy)))
  ctx.save()
  ctx.translate(frontHand.x, frontHand.y)
  ctx.rotate(angle)
  ctx.strokeStyle = appearance.aura ? palette.glow : palette.primary
  ctx.lineWidth = 4
  ctx.lineCap = 'round'
  ctx.beginPath()
  ctx.arc(0, 0, 31, -1.15, 1.15)
  ctx.stroke()
  ctx.strokeStyle = '#d9d1c3'
  ctx.lineWidth = 1.5
  ctx.beginPath()
  ctx.moveTo(12, -28)
  ctx.lineTo(-pull, 0)
  ctx.lineTo(12, 28)
  ctx.stroke()
  ctx.strokeStyle = palette.accent
  ctx.lineWidth = 2
  ctx.beginPath()
  ctx.moveTo(-pull + 3, 0)
  ctx.lineTo(39, 0)
  ctx.stroke()
  ctx.fillStyle = palette.glow
  triangle(43, -4, 9, 8)
  ctx.restore()
}

function drawWeaponOnHand(hand, weapon, offhand = false) {
  const rawType = String(weapon.weapon_type || 'blade').toLowerCase()
  const type = rawType.includes('spear') || rawType.includes('pole') || rawType.includes('staff')
    ? 'spear'
    : rawType.includes('axe') || rawType.includes('hammer') || rawType.includes('heavy') || rawType.includes('great')
      ? 'heavy'
      : rawType.includes('dagger')
        ? 'dagger'
        : 'blade'
  const appearance = equipmentAppearance(weapon)
  const palette = appearance.palette || FALLBACK_GEAR_PALETTES.white
  const reach = type === 'spear' ? 62 : type === 'heavy' ? 48 : type === 'dagger' ? 27 : 37
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
  const spriteWidth = type === 'spear' ? 76 : type === 'heavy' ? 60 : type === 'dagger' ? 42 : appearance.model === 'wooden_blade' ? 50 : 54
  const spriteHeight = type === 'spear' ? 34 : type === 'heavy' ? 52 : 38
  if (drawEquipmentSprite(appearance, 0, 0, spriteWidth, spriteHeight, {
    anchorX: spriteWidth * 0.16,
    anchorY: spriteHeight / 2
  })) {
    ctx.restore()
    return
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
  if (type === 'heavy') {
    ctx.fillStyle = palette.primary
    ctx.beginPath()
    ctx.ellipse(reach + 2, -5, 16, 11, -0.28, 0, Math.PI * 2)
    ctx.fill()
    ctx.fillStyle = palette.accent
    ctx.fillRect(reach - 4, -15, 8, 28)
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

function pixelMonsterRecord(entity) {
  const name = entity.name || ''
  if (entity.role === 'boss') {
    return PIXEL_SPRITES.monsters.forest_boss
  }
  if (name.includes('thorn') || name.includes('bramble') || name.includes('ancient') || name.includes('bark')) {
    return PIXEL_SPRITES.monsters.thorn
  }
  if (name.includes('imp') || name.includes('guard') || name.includes('knight') || name.includes('squire')) {
    return PIXEL_SPRITES.monsters.imp
  }
  return PIXEL_SPRITES.monsters.slime
}

function pixelMonsterAction(entity) {
  if (!entity) return 'idle'
  if (Number(entity.hp || 0) <= 0) return 'death'
  if (entity.role === 'boss') return 'attack'
  return 'walk'
}

function drawPixelMonster(x, y, entity) {
  const sprite = pixelMonsterRecord(entity)
  if (!sprite) {
    return false
  }
  const threat = Math.max(1, Number(entity.threat || 1))
  const scaled = {
    ...sprite,
    drawWidth: Number(sprite.drawWidth || sprite.frameWidth) * Math.min(1.22, 1 + (threat - 1) * 0.08),
    drawHeight: Number(sprite.drawHeight || sprite.frameHeight) * Math.min(1.22, 1 + (threat - 1) * 0.08)
  }
  return drawSpriteSheetFrameBottom(
    scaled,
    pixelMonsterAction(entity),
    x,
    y,
    monsterFacingFlip(entity),
    entity
  )
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
  const drewPixelMonster = drawPixelMonster(x, y - flightLift + 5, entity)
  if (drewPixelMonster) {
    drawMonsterThreatOverlay(x, y - flightLift + 5, boss ? 126 : 72, boss ? 126 : 72, threatStyle)
    if (boss) {
      ctx.strokeStyle = 'rgba(255, 202, 85, 0.72)'
      ctx.lineWidth = 3
      ctx.beginPath()
      ctx.ellipse(x, y - 56, 54, 42, 0, 0, Math.PI * 2)
      ctx.stroke()
    }
    return
  }
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
    return
  }
  if (action === 'list') {
    const item = ((state.snapshot && state.snapshot.hero && state.snapshot.hero.inventory) || [])
      .find((candidate) => candidate.id === itemId)
    openListingPanel(item)
    return
  }
  if (action === 'recycle') {
    if (state.inventoryActionInFlightIds.has(itemId)) {
      return
    }
    state.inventoryActionInFlightIds.add(itemId)
    if (state.snapshot && state.snapshot.hero) {
      renderInventory(state.snapshot.hero.inventory || [], true)
    }
    postAction('/inventory/recycle', { item_id: itemId }, t('recycle'))
      .finally(() => {
        state.inventoryActionInFlightIds.delete(itemId)
        if (state.snapshot && state.snapshot.hero) {
          renderInventory(state.snapshot.hero.inventory || [], true)
        }
      })
  }
})

if (els.recycleAllButton) {
  els.recycleAllButton.addEventListener('click', () => {
    if (state.recycleAllInFlight) {
      return
    }
    state.recycleAllInFlight = true
    if (state.snapshot && state.snapshot.hero) {
      renderInventory(state.snapshot.hero.inventory || [], true)
    }
    postAction('/inventory/recycle-all', {}, t('recycleAll'))
      .finally(() => {
        state.recycleAllInFlight = false
        if (state.snapshot && state.snapshot.hero) {
          renderInventory(state.snapshot.hero.inventory || [], true)
        }
      })
  })
}

els.listingCancelButton.addEventListener('click', () => {
  closeListingPanel()
  setStatus(statusForSnapshot(state.snapshot))
})

els.listingPanel.addEventListener('click', (event) => {
  if (event.target === els.listingPanel) {
    closeListingPanel()
    setStatus(statusForSnapshot(state.snapshot))
  }
})

els.listingConfirmButton.addEventListener('click', submitListingDraft)
els.listingPriceInput.addEventListener('keydown', (event) => {
  if (event.key === 'Enter') {
    submitListingDraft()
  }
  if (event.key === 'Escape') {
    closeListingPanel()
    setStatus(statusForSnapshot(state.snapshot))
  }
})

els.talentList.addEventListener('click', (event) => {
  const button = event.target.closest('button[data-action]')
  if (!button || button.disabled || state.talentEvolutionInFlight) {
    return
  }
  if (button.dataset.action === 'evolve-talent') {
    evolveTalent(button)
  }
  if (button.dataset.action === 'expand-talent') {
    expandTalentWithDonations(button)
  }
})

if (els.systemShopList) {
  els.systemShopList.addEventListener('click', (event) => {
    const button = event.target.closest('button[data-action="system-shop-buy"]')
    if (!button || button.disabled) {
      return
    }
    const sku = button.dataset.sku
    if (state.systemShopActionInFlightSkus.has(sku)) {
      return
    }
    state.systemShopActionInFlightSkus.add(sku)
    if (state.snapshot) {
      const heroGold = state.snapshot.hero ? state.snapshot.hero.gold || 0 : 0
      renderSystemShop((state.snapshot.system_shop && state.snapshot.system_shop.items) || [], heroGold, true)
    }
    postAction('/system-shop/buy', { sku }, t('shopBuy'))
      .finally(() => {
        state.systemShopActionInFlightSkus.delete(sku)
        if (state.snapshot) {
          const heroGold = state.snapshot.hero ? state.snapshot.hero.gold || 0 : 0
          renderSystemShop((state.snapshot.system_shop && state.snapshot.system_shop.items) || [], heroGold, true)
        }
      })
  })
}

els.marketList.addEventListener('click', (event) => {
  const button = event.target.closest('button[data-action]')
  if (!button || button.disabled) {
    return
  }
  const action = button.dataset.action
  if (!['buy', 'cancel-listing', 'sell-to-system'].includes(action)) {
    return
  }
  const listingId = button.dataset.id
  if (state.marketActionInFlightIds.has(listingId)) {
    return
  }
  state.marketActionInFlightIds.add(listingId)
  if (state.snapshot && state.snapshot.market && state.snapshot.hero) {
    renderMarket(state.snapshot.market.active || [], state.snapshot.hero.id, true)
  }
  const path = action === 'cancel-listing'
    ? '/market/cancel'
    : action === 'sell-to-system'
      ? '/market/sell-to-system'
      : '/market/buy'
  const busyText = action === 'cancel-listing'
    ? t('cancelingListing')
    : action === 'sell-to-system'
      ? t('sellingSystem')
      : t('buying')
  const doneText = action === 'cancel-listing'
    ? t('cancelListing')
    : action === 'sell-to-system'
      ? t('sellSystem')
      : t('buy')
  setStatus(busyText)
  postAction(path, { listing_id: listingId }, doneText)
    .finally(() => {
      state.marketActionInFlightIds.delete(listingId)
      if (state.snapshot && state.snapshot.market && state.snapshot.hero) {
        renderMarket(state.snapshot.market.active || [], state.snapshot.hero.id, true)
      }
    })
})

els.genderMaleButton.addEventListener('click', () => setGender('male'))
els.genderFemaleButton.addEventListener('click', () => setGender('female'))
els.rollTalentButton.addEventListener('click', rollCreationTalents)
els.confirmCharacterButton.addEventListener('click', confirmCharacter)
els.loginButton.addEventListener('click', () => submitAccount('/account/login'))
els.registerButton.addEventListener('click', () => submitAccount('/account/register'))
els.accountPasswordInput.addEventListener('keydown', (event) => {
  if (event.key === 'Enter') {
    submitAccount('/account/login')
  }
})
els.logoutButton.addEventListener('click', logoutAccount)
els.cancelCreationButton.addEventListener('click', () => {
  els.creationPanel.classList.add('hidden')
  state.creationDraft = null
  setProfileStatus('')
})
els.characterSlotList.addEventListener('click', (event) => {
  const button = event.target.closest('button[data-action]')
  if (!button || button.disabled) {
    return
  }
  if (button.dataset.action === 'create-character') {
    showCreationPanel()
  }
  if (button.dataset.action === 'select-character') {
    selectCharacter(button.dataset.id)
  }
  if (button.dataset.action === 'delete-character') {
    deleteCharacter(button.dataset.id)
  }
})

els.newCharacterButton.addEventListener('click', () => {
  if (!loadSessionToken()) {
    showAccountPanel()
    return
  }
  stopGameLoop()
  state.snapshot = null
  state.previousSnapshot = null
  refreshAccount().then((accountState) => {
    if (accountState.authenticated) {
      showCharacterPanel()
    }
  })
})

window.addEventListener('resize', resizeCanvas)
resizeCanvas()
state.settings = loadStoredSettings()
applySettings()
setGender('male')
loadEquipmentTranslations()
bootstrapProfile()
window.requestAnimationFrame(draw)
