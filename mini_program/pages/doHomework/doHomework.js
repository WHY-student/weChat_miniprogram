// pages/wordtest/wordtest.js
var app = getApp();
Page({
  jumpBtn:function(options){
    wx.navigateBack()
  },
  /**
   * 页面的初始数据
   */
  data: {
    mask:false,
    learned:"",
    total:"",
    choices:[],
    right_word:"",
    words:[],
    colors:["white","#43caac","#ff4d5e"],
    imgs:["/pic/right.png","/pic/error.png"],
    src:"",
    right_or_wrong:"",
    explanation:false,
    type:"",
    path:"",
    full_url:"",
    audioAction_1: {
      method: 'pause'
    },    
    audioAction_2: {
      method: 'pause'
    },  
    audioAction_3: {
      method: 'pause'
    },
    url:app.globalData.baseUrl
  },
  onLoad(options){
    wx.showLoading({
      title: '加载中',
      mask:true
    })
    wx.setNavigationBarTitle({ title:'单词100'})
    var type = options.type
    var path=options.path
    var full_url=type==1?(app.globalData.baseUrl+'/practice'+path):app.globalData.baseUrl+'/practice/getWords'
    // console.log('url',url,type)
    this.setData({
      type:type,
      path:path,
      full_url:full_url
    })
    this.getWords()
  },
  getWords(){
    var that=this
    var aab={
      user_id:app.globalData.userInfo.user_id,
      source:that.data.type
    }
    console.log("data",aab)
    wx.request({
      url: that.data.full_url, 
      method:"POST",
      data:{
        user_id:app.globalData.userInfo.user_id,
        source:that.data.type
      },
      header: {
        "Content-Type": "application/x-www-form-urlencoded"// 默认值
      },
      success (res) {
        var data=res.data
        var i
        console.log("words",data)
        for(i=0;i<data.length;i++){
          data[i].pronunciation=app.globalData.baseUrl+data[i].pronunciation
          // data[i].examples[0]=data[i].examples[0].split(". ")
        }
        that.setData({
          words:data
        })
        var choices=that.getChoices(0)
        that.setData({
          choices:choices,
          total:data.length,
          right_word:data[0],
          src:data[0].pronunciation,
          learned:1
        })
        wx.hideLoading()
        console.log("data[0].pronunciation",data[0].pronunciation)
        that.playAudio_1()
        console.log("data",data)
      },

    })      
  },
  playAudio_1: function () {
    this.setData({
      audioAction_1: {
        method: 'play'
      }
    });
  },  
  playAudio_2: function () {
    this.setData({
      audioAction_2: {
        method: 'play'
      }
    });
  },   
  playAudio_3: function () {
    this.setData({
      audioAction_3: {
        method: 'play'
      }
    });
  },    
  collection(e){
    var word_id=e.currentTarget.dataset.word_id
    console.log("word_id",word_id)
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
        console.log("res",res)
        var right_word=that.data.right_word
        right_word.is_in_collection=!right_word.is_in_collection
        that.setData({
          right_word:right_word
        })
      }
    })
  }, 
  getChoices:function(index){
    var data=this.data.words
    var choices=[
      {
        type:true,
        afterChoose:false,
        explanation:data[index].explanation
      }
    ]
    for(var i=0;i<3;i++){
      choices.push({
        type:false,
        afterChoose:false,
        explanation:data[index].wrong_choices[i]
      })
    }
    return this.randSort(choices)
  },
  randSort:function(arr){
    for(var i = 0,len = arr.length;i < len; i++ ){
          var rand = parseInt(Math.random()*len);
          var temp = arr[rand];
          arr[rand] = arr[i];
          arr[i] = temp; 
     }
     return arr;
  },  
  choose(e){
    var index=e.currentTarget.dataset.index
    var that=this
    this.setData({
      mask:true
    })
    wx.request({
      url: app.globalData.baseUrl+'/practice/click', 
      method:"POST",
      data:{
        user_id:app.globalData.userInfo.user_id,
        word_id:that.data.right_word.word_id,
      },
      header: {
        "Content-Type": "application/x-www-form-urlencoded"// 默认值
      },
      success (res) {
        console.log("res",res.data)
        that.setData({
          mask:false
        })        
        that.updateChoices(index)
      }
    })
  },
  updateChoices(index){
  var choices=this.data.choices
  var learned=this.data.learned++
  choices[index].afterChoose=true
  if(!choices[index].type){
    learned=this.data.learned
    for(var i=0;i<4;i++){
      if(choices[i].type){
        choices[i].afterChoose=true
        break
      }
    }
    this.setData({
      choices:choices,
      right_or_wrong:this.data.url+"/music/error.mp3",      
    })  
    this.playAudio_3()
    var that=this
    setTimeout(function(){
      that.setData({
        explanation:true,      
      })
      that.playAudio_2()
    },1000)           
  }
  else{
    this.setData({
      choices:choices,
      right_or_wrong:this.data.url+"/music/correct.mp3",      
    })  
    this.playAudio_3()       
    if(learned<this.data.total){
      learned=this.data.learned++
      var that=this   
      setTimeout(function(){ 
        var new_choices=that.getChoices(learned-1)
        var right_word=that.data.words[learned-1]
        var src=right_word.pronunciation        
        that.setData({
          choices:new_choices,
          learned:learned,
          right_word:right_word,
          src:src
        })    
        that.playAudio_1()    
      }, 1000);          
    }else{
      var that=this
      if(this.data.type==1){
        wx.navigateTo({
          url:  '../clockIn/clockIn?num='+that.data.total,
        })        
      }
      else if(this.data.type==2||this.data.type==4){
        wx.navigateTo({
          url: '../wrongSet/wrongSet',
        })            
      }
      else{
        wx.showModal({
          content:"太棒了！再来一组吧",
          confirmText:"继续学习",//默认是“确定”
          cancelText:"下次一定",//默认是“取消”
          success: function (e) {
            if(e.confirm){
              that.getWords()
            }
            else{
              wx.reLaunch({
                url: '../homepage/homepage'
              })
            }
          }
        })
      }
    }   
  }
  },
  addOrRemove(){
    var that=this
    wx.showModal({
      content:this.data.right_word.is_in_wrongwords? '是否移出错题本？':"是否加入错题本",
      success: function (e) {
        if (e.confirm) {
          that.do_add_or_remove()
        } else {
          console.log('用户点击取消')
        }
      }
    })
   
  },
  do_add_or_remove(){
    var action=this.data.right_word.is_in_wrongwords?2:1
    var right_word=this.data.right_word
    right_word.is_in_wrongwords=!right_word.is_in_wrongwords
    var that=this
    wx.request({
      url: app.globalData.baseUrl+'/practice/wrongWords', 
      method:"POST",
      data:{
        user_id:app.globalData.userInfo.user_id,
        word_id:that.data.right_word.word_id,
        action:action
      },
      header: {
        "Content-Type": "application/x-www-form-urlencoded"// 默认值
      },
      success (res) {        
        that.setData({
          right_word:right_word
        })
        wx.showToast({
          title: action!=2?'加入成功':'移除成功', 
          icon: 'success', 
          duration: 1500,
        })        
      }
    })      
  },
  nextWord(){
    console.log('this.data',this.data)
    if(this.data.learned<=this.data.total){
      var learned=this.data.learned++
      var that=this   
      var new_choices=that.getChoices(learned-1)
      var right_word=that.data.words[learned-1]
      var src=right_word.pronunciation
      that.setData({
        choices:new_choices,
        learned:learned,
        right_word:right_word,
        explanation:false,
        src:src,
        audioAction_3: {
          method: 'pause'
        }        
      })   
      this.playAudio_1()           
    } 
    else{    
      if(this.data.type==1){
        var that=this
        wx.navigateTo({
          url: '../clockIn/clockIn?num='+that.data.total,
        })        
      }
      else if(this.data.type==2||this.data.type==4){
        wx.navigateTo({
          url: '../wrongSet/wrongSet',
        })            
      }
      else if(this.data.type==3){
        wx.showModal({
          content:"太棒了！再来一组吧",
          confirmText:"继续学习",//默认是“确定”
          cancelText:"下次一定",//默认是“取消”
          success: function (e) {
            if(e.confirm){
              that.getWords()
            }
            else{
              wx.reLaunch({
                url: '../homepage/homepage',
              })      
            }
          }
        }) 
      }
    } 
  }
})