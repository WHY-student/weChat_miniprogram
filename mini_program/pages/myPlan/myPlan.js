// pages/myPlan/myPlan.js
var app = getApp();
import Toast from '@vant/weapp/toast/toast';
Page({
  data: {
    total:"",
    book_cover:'',
    book_name:"",
    learnNum:[5,10,15,20,25,30,35,40,45,50,55,60,65,70],
    reviewNum:[0,5,10,15,20,25,30,35,40,45,50,55,60,65,70],
    lastPlan:{learn:0,review:0},//修改后的计划,数字为对应索引
    words_number:"",//根据对象宽度设置单词数量
    minutes:"",
    days:"",
    defeat_learn_index:"",//左边初始索引
    defeat_review_index:"",//右边初始索引
  },
  onLoad:function(){
    wx.setNavigationBarTitle({ title:'我的计划'})
    var that=this
    wx.createIntersectionObserver().relativeToViewport().observe('#select', (res) => {
      res.intersectionRect.width // 相交区域的宽度
      res.intersectionRect.height // 相交区域的高度
      console.log("height",res.intersectionRect.height)
      that.number = res.intersectionRect.height/45
      console.log("number",that.number)
      wx.request({
        url: app.globalData.baseUrl+'/myPlan/getPlan', 
        method:"POST",
        data:{
          user_id:app.globalData.userInfo.user_id
        },
        header: {
          "Content-Type": "application/x-www-form-urlencoded"// 默认值
        },
        success (res) { 
          var data=res.data
          console.log("data",data)
          // var nowPlan={
          //   learn:data.daily_learn,
          //   review:data.daily_review,
          // }
          console.log("words_number", parseInt(that.number))
          var Lindex,Rindex;
          for(var i=0;i<that.data.learnNum.length;i++)
          {
            if(that.data.learnNum[i]==data.daily_learn)
            {
              Lindex=i;
              break;
            }
          }
          for(var i=0;i<that.data.reviewNum.length;i++)
          {
            if(that.data.reviewNum[i]==data.daily_review)
            {
              Rindex=i;
              break;
            }
          }
          console.log("Lindex", Lindex)
          console.log("Rindex", Rindex)
          var lastPlan={
            learn:data.daily_learn,
            review:data.daily_review
          }
          that.setData({
            daily_learn: data.daily_learn,
            daily_review: data.daily_review,
            lastPlan:lastPlan,
            book_cover:app.globalData.baseUrl+data.book_cover,
            total:data.total,
            book_name:data.book_name,          
            words_number:parseInt(that.number),
            minutes:(data.daily_learn+data.daily_review)/2,//学习花费时间
            days:Math.ceil(data.total/data.daily_learn),//学习花费天数
            defeat_learn_index:Lindex,//左边初始索引
            defeat_review_index:Rindex,//右边初始索引
          })
          // console.log("nowPlan",that.data.nowPlan)
        }
      })
      console.log('data',this.data)
    })
  },
  saveBtr(e){
    console.log("保存计划")
    var that = this
    wx.request({
      url:  app.globalData.baseUrl+'/myPlan/changePlan',
      method:"POST",
      data:{
        user_id:app.globalData.userInfo.user_id,
        daily_learn:that.data.lastPlan.learn,
        daily_review:that.data.lastPlan.review,
      },
      header: {
        "Content-Type": "application/x-www-form-urlencoded"// 默认值
      },
      success (res) { 
        wx.showToast({
          title: '保存成功！', 
          icon: 'success', 
          duration: 1500,
        })
      }
    })
    wx.reLaunch({
      url: '../homepage/homepage'
    })
  },
  LCli(e){
    const{picjer,value,index}=e.detail;
    this.setData({
      "lastPlan.learn":value,
      minutes:Math.ceil((value+this.data.lastPlan.review)/10)*5,//学习花费时间
      days:Math.ceil(this.data.total/value),//学习花费天数
    })
  },
  RCli(e){
    const{picjer,value,index}=e.detail;
    this.setData({
      "lastPlan.review":value,
      minutes:(value+this.data.lastPlan.learn)/2,
    })
    //两个赋值需要分开，不然会出bug
  }
})