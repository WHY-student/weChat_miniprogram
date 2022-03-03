// app.js

App({
  onLaunch() {
    // 展示本地存储能力
    const logs = wx.getStorageSync('logs') || []
    logs.unshift(Date.now())
    wx.setStorageSync('logs', logs)
  },
  globalData: {
    userInfo: null,
    // baseUrl:"http://192.168.31.68:8888"
    baseUrl:"http://10.127.154.246:8888"
    // baseUrl:"http://10.139.121.164:8888"
  },
})
