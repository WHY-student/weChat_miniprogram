// pages/share/share.js
var app = getApp();
Page({

  data: {
    head:"",//头像地址
    sentence:"除了tks，如何花式说“谢谢”",
    example:{eng:"i own you big time",chi:"我欠你一个人情"},
    week:["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],
    month:["January","February","March","April","May","June","July","August","September","October","November","December"],
    date:{week:3,month:7,day:7},
    wxSym:"pic/wx.png", 
    openSettingBtnHidden: false,//是否授权
    imgUrl: '',
    today_learn:0,
    clockin_amount:1,
    url:app.globalData.baseUrl
  },
  onLoad(){
    wx.setNavigationBarTitle({ title:'分享'})    
    const date=new Date();
    const week=date.getDay();
    const month=date.getMonth();
    const day=date.getDate();
    console.log(date);
    this.setData({
      "date.week":week,
      "date.month":month,
      "date.day":day,
    })
    var that=this
    wx.request({
      url: app.globalData.baseUrl+'/personal/share', 
      method:"POST",
      data: {
        user_id:app.globalData.userInfo.user_id,
      },      
      header: {
        "Content-Type": "application/x-www-form-urlencoded"// 默认值
      },
      success (res) {
        var data=res.data
        console.log("share",data)
        that.setData({
          head:app.globalData.userInfo.avatar,
          today_learn:data.today_learn,
          clockin_amount:data.clockin_amount
        })
      }
    })
  },

  onShareAppMessage: function( options ){
  　　var that = this;
  　　// 设置菜单中的转发按钮触发转发事件时的转发内容
  　　var shareObj = {
  　　　　title: "转发的标题",        // 默认是小程序的名称(可以写slogan等)
  　　　　path: '/pages/share/share',        // 默认是当前页面，必须是以‘/’开头的完整路径
  　　　　imgUrl: '',     //自定义图片路径，可以是本地文件路径、代码包文件路径或者网络图片路径，支持PNG及JPG，不传入 imageUrl 则使用默认截图。显示图片长宽比是 5:4
  　　　　success: function(res){
  　　　　　　// 转发成功之后的回调
  　　　　　　if(res.errMsg == 'shareAppMessage:ok'){
  　　　　　　}
  　　　　},
  　　　　fail: function(){
  　　　　　　// 转发失败之后的回调
  　　　　　　if(res.errMsg == 'shareAppMessage:fail cancel'){
  　　　　　　　　// 用户取消转发
  　　　　　　}else if(res.errMsg == 'shareAppMessage:fail'){
  　　　　　　　　// 转发失败，其中 detail message 为详细失败信息
  　　　　　　}
  　　　　}
    }
  　　// 来自页面内的按钮的转发
  　　if( options.from == 'button' ){
  　　　　var eData = options.target.dataset;
  　　　　console.log( eData.name );     // shareBtn
  　　　　// 此处可以修改 shareObj 中的内容
  　　　　shareObj.path = '/pages/btnname/btnname?btn_name='+eData.name;
  　　}
  　　// 返回shareObj
  　　return shareObj;
  },
    
  // 保存图片
  saveImg:function(e){
    let that = this;
    console.log("saveIng",e)
    //获取相册授权
    wx.getSetting({
      success(res) {
        if (!res.authSetting['scope.writePhotosAlbum']) {
          wx.authorize({
            scope: 'scope.writePhotosAlbum',
            success() {
              //这里是用户同意授权后的回调
              that.saveImgToLocal();
            },
            fail() {//这里是用户拒绝授权后的回调
              that.setData({
                openSettingBtnHidden: false
              })
            }
          })
        } else {//用户已经授权过了
          console.log("用户已经授权过了")
          that.saveImgToLocal();
        }
      }
    })

  },
  saveImgToLocal: function (e) {
    console.log('saveImgToLocal',e)
    let that = this;
    let imgSrc = that.data.imgUrl;
    wx.downloadFile({
      url: app.globalData.baseUrl+'/pic/bac.png',
      success: function (res) {
        console.log(res);
        //图片保存到本地
        wx.saveImageToPhotosAlbum({
          filePath: res.tempFilePath,
          success: function (data) {
            wx.showToast({
              title: '保存成功',
              icon: 'success',
              duration: 2000
            })
          },
        })
      }
    })

  },

  // 授权
  handleSetting: function (e) {
    let that = this;
    // 对用户的设置进行判断，如果没有授权，即使用户返回到保存页面，显示的也是“去授权”按钮；同意授权之后才显示保存按钮

    if (!e.detail.authSetting['scope.writePhotosAlbum']) {
      // wx.showModal({
      //   title: '警告',
      //   content: '若不打开授权，则无法将图片保存在相册中！',
      //   showCancel: false
      // })
      that.setData({
        openSettingBtnHidden: false
      })
    } else {
      // wx.showModal({
      //   title: '提示',
      //   content: '您已授权，赶紧将图片保存在相册中吧！',
      //   showCancel: false
      // })
      that.setData({
        openSettingBtnHidden: true
      })
    }
  },    
})