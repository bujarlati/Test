function normalizeBase(base) {
  return base.replace(/\/$/, '')
}

function requestJson(path, options) {
  const app = getApp()
  const opts = options || {}
  const method = opts.method || 'GET'
  const data = opts.data || {}
  const apiBase = normalizeBase(app.globalData.apiBase)

  return new Promise((resolve, reject) => {
    wx.request({
      url: apiBase + path,
      method,
      data,
      header: {
        'content-type': 'application/json'
      },
      timeout: 5000,
      success(res) {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(res.data)
          return
        }
        reject(new Error((res.data && res.data.error) || ('HTTP ' + res.statusCode)))
      },
      fail(err) {
        reject(new Error(err.errMsg || 'request failed'))
      }
    })
  })
}

module.exports = {
  requestJson
}
