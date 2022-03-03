// pages/wrongSet/wrongSet.js
var app = getApp();
Page({
  /**
   * 页面的初始数据
   */
  data: {
    words:[],
    total:"",
    audioAction: {
      method: 'pause'
    },  
    music:"", 
    url:app.globalData.baseUrl
  },
  playAudio: function () {
    this.setData({
      audioAction: {
        method: 'play'
      }
    });
  },   
  onLoad:function(){
    wx.showLoading({
      title: '加载中',
      mask:true
    })
    wx.setNavigationBarTitle({ title:'收藏夹'})
    var that=this
    wx.request({
      url: app.globalData.baseUrl+'/words/getWords', 
      method:"POST",
      data: {
        user_id:app.globalData.userInfo.user_id,
        source:2
      },      
      header: {
        "Content-Type": "application/x-www-form-urlencoded"// 默认值
      },
      success (res) {
        console.log("res",res)
        var words=res.data['words']
        var total=words.length
        for(var i=0;i<words.length;i++){
          words[i].status=true
          words[i].pronunciation=app.globalData.baseUrl+words[i].pronunciation
        }
        that.setData({
          words:words,
          total:total
        })
        wx.hideLoading()
      }    
    })
  },
  play(e){
    const id=e.currentTarget.dataset.id
    var music=this.data.words[id].pronunciation
    this.setData({
      music:music
    })
    this.playAudio()
  },
  practice(){
    wx.navigateTo({
      url: '../doHomework/doHomework?type=2' + '&path=getWords',
    })      
  },
  interpretationCli(e){
    const id=e.currentTarget.dataset.id;
    var words=this.data.words
    words[id].status=!words[id].status
    this.setData({
      words:words
    })
  },
  collection(e){
    var word_id=e.currentTarget.dataset.word_id
    var index=e.currentTarget.dataset.index
    console.log("index",index)
    var that=this
    wx.request({
      url: app.globalData.baseUrl+'/words/collection', 
      method:"POST",
      data:{
        user_id:app.globalData.userInfo.user_id,
        word_id:word_id,
      },
      header: {
        "Content-Type": "application/x-www-form-urlencoded"// 默认值
      },
      success (res) {
        var words=that.data.words
        console.log("words",words,index)
        words[index].is_in_collection=!words[index].is_in_collection
        that.setData({
          words:words
        })
      }
    })
  },   
  switchCli(e){
    var checked=e.detail.value
    var words=this.data.words
    for(var i=0;i<words.length;i++){
      words[i].status=!checked
    }
    this.setData({
      words:words
    })
  }
})