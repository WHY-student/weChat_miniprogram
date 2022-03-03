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
    type:0,
    not_learn:[],
    learned:[],
    switch:true,
    url:app.globalData.baseUrl
  },
  playAudio: function () {
    this.setData({
      audioAction: {
        method: 'play'
      }
    });
  },  
  onChange(e){
    console.log("e",e)
    var type=e.detail.index
    var words=type==0?this.data.learned:this.data.not_learn
    this.setData({
      type:type,
      words:words,      
    })
    this.changeStatus(this.data.switch)
  },   
  onLoad:function(){
    wx.showLoading({
      title: '加载中',
      mask:true
    })
    var that=this
    wx.request({
      url: app.globalData.baseUrl+'/words/', 
      method:"POST",
      data: {
        user_id:app.globalData.userInfo.user_id,
      },      
      header: {
        "Content-Type": "application/x-www-form-urlencoded"// 默认值
      },
      success (res) {
        console.log("words",res.data)
        var not_learn=res.data.not_learn
        var learned=res.data.learn
        for(var i=0;i<not_learn.length;i++){
          not_learn[i].status=true
          not_learn[i].pronunciation=app.globalData.baseUrl+not_learn[i].pronunciation
        }        
        for(var i=0;i<learned.length;i++){
          learned[i].status=true
          learned[i].pronunciation=app.globalData.baseUrl+learned[i].pronunciation
        }    
        that.setData({
          not_learn:not_learn,
          learned:learned,
          words:learned,
          total:learned.length,
          type:0
        })                 
        wx.hideLoading()
        // var words=res.data
        // var total=words.length
        // console.log("words",words)
        // for(var i=0;i<words.length;i++){
        //   words[i].status=true
        //   words[i].pronunciation=app.globalData.baseUrl+words[i].pronunciation
        // }
        // that.setData({
        //   words:words,
        //   total:total
        // })
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
      url: '../doHomework/doHomework?type=' + '2',
    })      
  },
  interpretationCli(e){
    const id=e.currentTarget.dataset.id;
    console.log(e);
    var words=this.data.words
    words[id].status=!words[id].status
    this.setData({
      words:words
    })
    // if(this.data.wrongWords[id].status==true){
    //   this.setData({
    //     ["wrongWords["+id+"].exSrc"]:this.data.url+"/pic/back.png",
    //     ["wrongWords["+id+"].status"]:false,
    // })}else{
    //   this.setData({
    //     ["wrongWords["+id+"].exSrc"]:this.data.url+"/pic/open.png",
    //     ["wrongWords["+id+"].status"]:true,
    //   })
    // }
  },
  switchCli(e){
    console.log("e",e)
    var switch_1=!e.currentTarget.dataset.switch
    this.setData({
      switch:switch_1
    })
    this.changeStatus(this.data.switch)
    

    // var checked=e.detail.value
    // var words=this.data.words
    // for(var i=0;i<words.length;i++){
    //   words[i].status=!checked
    // }
    // this.setData({
    //   words:words
    // })


    // const len=this.data.wrongWords.length;
    // console.log(e);
    // if(this.data.checked==false){
    // for(var i=0;i<len;i++){
    //   this.setData({
    //     ["wrongWords["+i+"].status"]:false,
    //     checked:true,
    //   })
    // }}else{
    //   for(var i=0;i<len;i++){
    //     this.setData({
    //       ["wrongWords["+i+"].status"]:true,
    //       checked:false,
    //     })
    //   }
    // }
  },
  changeStatus(checked){
    var words=this.data.words
    for(var i=0;i<words.length;i++){
      words[i].status=checked
    }
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
        console.log("words",words)
        words[index].is_in_collection=!words[index].is_in_collection
        that.setData({
          words:words
        })
      }
    })
  },     
})