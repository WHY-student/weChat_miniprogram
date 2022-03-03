// pages/wordExplanation/wordExplanation.js
var app = getApp();
Page({

  /**
   * 页面的初始数据
   */
  data: {
    pronunciation:"[ˌɑːftəˈnuːn]",//音标
    wordText:"afternoon",//单词
    type:"n",//词性
    meaning:"下午",//单词释义
    sentence:[{eng:"He had stay……",chi:"他整个……"},{eng:"He  is arriv……",chi:"他下午……"}],
    wordState:0,//0-已加入错词本，1-未加入错词本
    displayState:"已加入错题本",//两种显示状态：0.已加入错题本，1-加入错题本
    url:app.globalData.baseUrl
  },
  nextWord(e){
    wx:wx.navigateTo({
      url: '../doHomework/doHomework',
    })
  },
  changeTo(e){
    var that=this;
    console.log("调用TO1");
    if(that.data.wordState==0){
    wx.showModal({
      content: '是否移出错题本？',
      success: function (e) {
        if (e.confirm) {
          that.setData({
            displayState:"加入错题本",
            wordState:1,
          }),
          console.log('用户点击确定')
        } else {
          console.log('用户点击取消')
        }
      }
    })
  } else{
    wx.showModal({
      content: '是否加入错题本？',
      success: function (e) {
        if (e.confirm) {
          that.setData({
            displayState:"已加入错题本",
            wordState:0,
          })
          console.log('用户点击确定')
        } else {
          console.log('用户点击取消')
        }
      }
    })    
  }
  },  
})