// pages/homepage/homepage.js
var app = getApp();
import Dialog from '../../miniprogram_npm/@vant/weapp/dialog/dialog';
Page({

  /**
   * 页面的初始数据
   */
  data: {
    avatar:"",
    user_name:"",
    book_cover:"",
    book_name:"",
    days:"",
    left_days:"",
    to_learn: "",
    words: "" ,
    total:"",
    learned:"",
    // start_show:false
    url:app.globalData.baseUrl,
    vip_img:'./img/not_VIP.png'
  },
  vip(){
    if(this.data.vip_img=="./img/not_VIP.png")
    {
      wx.showModal({
        title: '',
        content: '只要88.88成会会员获得更好体验',
        confirmText:'立即加入',
        cancelText:'残忍离开',
        success (res) {
          if (res.confirm) {
            wx.request({
              url: app.globalData.baseUrl+'/pay/',
              method:"POST",
              data: {
                user_id:app.globalData.userInfo.user_id,
                total_amount:88.88,
                subject:"vip"
              },
              header: {
                "Content-Type": "application/x-www-form-urlencoded"// 默认值
              }
            })
            wx.showModal({
              title: '',
              content: '支付遇到什么问题了吗？',
              confirmText:'支付成功',
              cancelText:'遇到问题',
              success (res) {
                if (res.confirm) {
                  wx.request({
                    url: app.globalData.baseUrl+'/pay/query',
                    method:"POST",
                    data: {
                      user_id:app.globalData.userInfo.user_id,
                      total_amount:"88.88",
                      subject:"VIP"
                    },
                    header: {
                      "Content-Type": "application/x-www-form-urlencoded"// 默认值
                    }
                  })
                  console.log('确认支付结果')
                  wx.navigateTo({
                    url: '../homepage/homepage'
                  }) 
                } else if (res.cancel) {
                  console.log('遇到问题')
                }
              }
            })
          } else if (res.cancel) {
            console.log('用户点击取消')
          }
        }
      })
    }
    else
    {
      wx.request({
        url: app.globalData.baseUrl+'/pay/refund',
        method:"POST",
        data: {
          user_id:app.globalData.userInfo.user_id
        },
        header: {
          "Content-Type": "application/x-www-form-urlencoded"// 默认值
        },
        success(res)
        {
          wx.showModal({
            title: '',
            content: res.data.msg,
            confirmText:'确定',
            cancelText:'返回',
            success (res) {
              wx.navigateTo({
                url: '../homepage/homepage'
              }) 
            }
          })
        }
      }
      )
      console.log('退款')
      wx.navigateTo({
        url: '../homepage/homepage'
      })
    }
  },
  toWrongCollection(){
    wx.navigateTo({
      url: '../wrongSet/wrongSet',
    })
  },
  toCollection(){
    wx.navigateTo({
      url: '../collection/collection',
    })    
  },
  toSetPlan(){
    wx.navigateTo({
      url: '../myPlan/myPlan'
    })    
  },
  toStart(e){
    var type=e.currentTarget.dataset.type
    var path=e.currentTarget.dataset.path
    wx.navigateTo({
      url: '../doHomework/doHomework?type=' + type+'&path='+path,
    })    
  },
  toPersonal(){
    wx.navigateTo({
      url: '../personal/personal'
    })    
  },
  toChooseBook(){
    wx.navigateTo({
      url: '../myBook/myBook'
    })
  },
  toWordsList(){
    wx.navigateTo({
      url: '../wordsList/wordsList'
    })    
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    var that=this
    wx.login({
      success: res => {
        console.log("res",res) 
        var code=res.code  
        wx.getSetting({
          success (res){
            if (res.authSetting['scope.userInfo']) {
              console.log("已授权")
              wx.getUserInfo({
                success: function (res) {
                  var userInfo=JSON.parse(res.rawData)
                  console.log("userInfo",userInfo)
                  app.globalData.userInfo= {
                    user_name:userInfo.nickName,
                    user_id:code,
                    avatar:userInfo.avatarUrl
                  }
                  wx.request({
                    url: app.globalData.baseUrl+'/login/', 
                    method:"POST",
                    data: app.globalData.userInfo,
                    header: {
                      "Content-Type": "application/x-www-form-urlencoded"// 默认值
                    },
                    success (res) {     
                      var data=res.data             
                      console.log(data)
                      app.globalData.userInfo.user_id=data.user_id
                      console.log("app.globalData.userInfo",app.globalData.userInfo) 
                      that.getData()                                      
                    },
                    fail(err) {
                      console.log(err)
                    }
                  }) 
                },
              })                
            }else{
              console.log("未授权")
            }
          }
        })         
      }
    })        
  },
  getData(){
    var that=this
    wx.request({
      url: app.globalData.baseUrl+'/homepage/',
      method:"POST",
      data: {
        user_id:app.globalData.userInfo.user_id,
      },
      header: {
        "Content-Type": "application/x-www-form-urlencoded"// 默认值
      },
      success (res) {
        var data=res.data
        console.log("homepage",data)
        var img=""
        if(data.is_vip)
        {
          img = "./img/VIP.png"
        }
        else
        {
          img = "./img/not_VIP.png"
        }
        that.setData({
          book_cover:app.globalData.baseUrl+data.book_cover,
          book_name:data.book_name,
          days:data.days,
          left_days:data.left_days,
          to_learn: data.to_learn,
          words: data.words,
          total:data.total,
          learned:data.learned,
          avatar:app.globalData.userInfo.avatar,
          user_name:app.globalData.userInfo.user_name,
          vip_img:img                           
        })
        wx.hideLoading()
        if(res.data.days==null){
          wx.navigateTo({
            url: '../chooseBook/chooseBook',
          })                         
        }
      }
    })       
  },
  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {
    // wx.showLoading({
    //   title: '加载中',
    //   mask:true
    // })
    if(this.data.avatar!==''){
      this.getData()
    }
  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {

  },
 
})
