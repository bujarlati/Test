const { requestJson } = require('../../utils/api')
const { createRenderer } = require('../../utils/renderer')

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

function decorateItem(item) {
  if (!item) {
    return null
  }
  return Object.assign({}, item, {
    slotLabel: SLOT_LABELS[item.slot] || item.slot,
    rarityLabel: RARITY_LABELS[item.rarity] || item.rarity,
    priceHint: Math.max(20, item.score * 2)
  })
}

function decorateListing(listing, heroId) {
  const item = decorateItem(listing.item)
  return Object.assign({}, listing, {
    item,
    isOwn: listing.seller_id === heroId,
    sellerLabel: listing.seller_id === heroId ? '我的挂单' : listing.seller_id
  })
}

Page({
  data: {
    hero: {},
    inventory: [],
    equippedList: [],
    marketListings: [],
    recentEvents: [],
    eventScrollTop: 0,
    statusText: '连接中',
    isOnline: false,
    isLoading: false,
    isTicking: false,
    isEquipping: false,
    isListing: false,
    isBuying: false,
    detailVisible: false,
    detailMode: '',
    detailIsInventoryItem: false,
    detailIsListingMode: false,
    detailIsEquippedMode: false,
    detailItem: null,
    detailListing: null,
    detailIsOwnListing: false,
    listingPrice: ''
  },

  onLoad() {
    this.snapshot = null
    this.renderer = null
    this.renderTimer = null
    this.tickTimer = null
    this.tickInFlight = false
    this.initCanvas()
  },

  onUnload() {
    this.stopLoops()
  },

  onHide() {
    this.stopLoops()
  },

  onShow() {
    if (this.renderer && !this.tickTimer) {
      this.startLoops()
    }
  },

  initCanvas() {
    const query = wx.createSelectorQuery()
    query
      .select('#gameCanvas')
      .fields({ node: true, size: true })
      .exec((res) => {
        const result = res && res[0]
        if (!result || !result.node) {
          this.setData({ statusText: '画布不可用', isOnline: false })
          return
        }
        const canvas = result.node
        const ctx = canvas.getContext('2d')
        const dpr = wx.getSystemInfoSync().pixelRatio || 1
        canvas.width = Math.round(result.width * dpr)
        canvas.height = Math.round(result.height * dpr)
        ctx.scale(dpr, dpr)

        this.renderer = createRenderer(canvas, ctx, {
          width: result.width,
          height: result.height
        })
        this.refreshSnapshot()
        this.startLoops()
      })
  },

  startLoops() {
    this.stopLoops()
    this.renderTimer = setInterval(() => {
      this.draw()
    }, 1000 / 30)
    this.tickTimer = setInterval(() => {
      this.tickNow({ silent: true })
    }, 1000)
  },

  stopLoops() {
    if (this.renderTimer) {
      clearInterval(this.renderTimer)
      this.renderTimer = null
    }
    if (this.tickTimer) {
      clearInterval(this.tickTimer)
      this.tickTimer = null
    }
  },

  refreshSnapshot() {
    if (this.data.isLoading) {
      return
    }
    this.setData({ isLoading: true })
    requestJson('/snapshot')
      .then((snapshot) => {
        this.applySnapshot(snapshot, '已连接')
      })
      .catch((err) => {
        this.setData({
          statusText: err.message || '连接失败',
          isOnline: false
        })
      })
      .finally(() => {
        this.setData({ isLoading: false })
        this.draw()
      })
  },

  tickNow(event) {
    if (this.tickInFlight) {
      return
    }
    const silent = event && event.silent
    this.tickInFlight = true
    this.setData({ isTicking: !silent })
    requestJson('/tick', {
      method: 'POST',
      data: { seconds: 1 }
    })
      .then((snapshot) => {
        this.applySnapshot(snapshot, '挂机中')
      })
      .catch((err) => {
        this.setData({
          statusText: err.message || '推进失败',
          isOnline: false
        })
      })
      .finally(() => {
        this.tickInFlight = false
        this.setData({ isTicking: false })
        this.draw()
      })
  },

  equipBest() {
    if (this.data.isEquipping) {
      return
    }
    this.setData({ isEquipping: true })
    requestJson('/equip-best', {
      method: 'POST'
    })
      .then((result) => {
        this.closeDetail()
        this.applySnapshot(result.snapshot, '已整理装备')
      })
      .catch((err) => {
        this.showToast(err.message || '装备失败')
      })
      .finally(() => {
        this.setData({ isEquipping: false })
        this.draw()
      })
  },

  openItemDetail(event) {
    const itemId = event.currentTarget.dataset.id
    const item = this.data.inventory.find((candidate) => candidate.id === itemId)
    if (!item) {
      return
    }
    this.setData({
      detailVisible: true,
      detailMode: 'item',
      detailIsInventoryItem: true,
      detailIsListingMode: false,
      detailIsEquippedMode: false,
      detailItem: item,
      detailListing: null,
      detailIsOwnListing: false,
      listingPrice: String(item.priceHint)
    })
  },

  openEquippedDetail(event) {
    const itemId = event.currentTarget.dataset.id
    const item = this.data.equippedList.find((candidate) => candidate.id === itemId)
    if (!item) {
      return
    }
    this.setData({
      detailVisible: true,
      detailMode: 'equipped',
      detailIsInventoryItem: false,
      detailIsListingMode: false,
      detailIsEquippedMode: true,
      detailItem: item,
      detailListing: null,
      detailIsOwnListing: false,
      listingPrice: ''
    })
  },

  openListingDetail(event) {
    const listingId = event.currentTarget.dataset.id
    const listing = this.data.marketListings.find((candidate) => candidate.id === listingId)
    if (!listing) {
      return
    }
    this.setData({
      detailVisible: true,
      detailMode: 'listing',
      detailIsInventoryItem: false,
      detailIsListingMode: true,
      detailIsEquippedMode: false,
      detailItem: listing.item,
      detailListing: listing,
      detailIsOwnListing: listing.isOwn,
      listingPrice: ''
    })
  },

  closeDetail() {
    this.setData({
      detailVisible: false,
      detailMode: '',
      detailIsInventoryItem: false,
      detailIsListingMode: false,
      detailIsEquippedMode: false,
      detailItem: null,
      detailListing: null,
      detailIsOwnListing: false,
      listingPrice: ''
    })
  },

  onPriceInput(event) {
    this.setData({
      listingPrice: event.detail.value
    })
  },

  equipSelected() {
    const item = this.data.detailItem
    if (!item || this.data.isEquipping) {
      return
    }
    this.setData({ isEquipping: true })
    requestJson('/equip-item', {
      method: 'POST',
      data: { item_id: item.id }
    })
      .then((result) => {
        this.closeDetail()
        this.applySnapshot(result.snapshot, '已穿戴')
      })
      .catch((err) => {
        this.showToast(err.message || '穿戴失败')
      })
      .finally(() => {
        this.setData({ isEquipping: false })
        this.draw()
      })
  },

  listSelected() {
    const item = this.data.detailItem
    const price = parseInt(this.data.listingPrice, 10)
    if (!item || this.data.isListing) {
      return
    }
    if (!price || price <= 0) {
      this.showToast('请输入有效价格')
      return
    }
    this.setData({ isListing: true })
    requestJson('/market/list', {
      method: 'POST',
      data: {
        item_id: item.id,
        price
      }
    })
      .then((result) => {
        this.closeDetail()
        this.applySnapshot(result.snapshot, '已挂售')
      })
      .catch((err) => {
        this.showToast(err.message || '挂售失败')
      })
      .finally(() => {
        this.setData({ isListing: false })
        this.draw()
      })
  },

  buySelectedListing() {
    const listing = this.data.detailListing
    if (!listing || listing.isOwn || this.data.isBuying) {
      return
    }
    this.setData({ isBuying: true })
    requestJson('/market/buy', {
      method: 'POST',
      data: {
        listing_id: listing.id,
        buyer_id: this.data.hero.id
      }
    })
      .then((result) => {
        this.closeDetail()
        this.applySnapshot(result.snapshot, '购买成功')
      })
      .catch((err) => {
        this.showToast(err.message || '购买失败')
      })
      .finally(() => {
        this.setData({ isBuying: false })
        this.draw()
      })
  },

  applySnapshot(snapshot, statusText) {
    const hero = snapshot.hero || {}
    const inventory = (hero.inventory || []).map(decorateItem)
    const equipped = hero.equipped || {}
    const equippedList = Object.keys(equipped).map((slot) => decorateItem(equipped[slot]))
    const market = snapshot.market || {}
    const marketListings = (market.active || []).map((listing) => decorateListing(listing, hero.id))
    const events = (snapshot.events || []).slice(-12).reverse()
    this.snapshot = snapshot
    this.setData({
      hero,
      inventory,
      equippedList,
      marketListings,
      recentEvents: events,
      eventScrollTop: 99999,
      statusText,
      isOnline: true
    })
  },

  showToast(title) {
    wx.showToast({
      title,
      icon: 'none',
      duration: 1600
    })
  },

  noop() {},

  draw() {
    if (!this.renderer) {
      return
    }
    this.renderer.render(this.snapshot, this.data.statusText)
  }
})
