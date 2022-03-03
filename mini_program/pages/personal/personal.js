// pages/personal/personal.js
var app = getApp();
Page({
  /**
   * 页面的初始数据
   */
  data: {
    days:[],//三个属性date-当前日，isSign-是否签到，thisMonth-是否本月
    today:{year:2021,month:1,day:1,isSign:false},
    choosedDay:{year:2021,month:1,day:1,isSign:false},
    weekW:["日","一","二","三","四","五","六"],
    clockons:"",
    max_length:"",
    user_name:"",
    avatar:"",
    show: false,
    url:app.globalData.baseUrl,
    is_remind:"",
    remind_time:"",
    hourList:[],
    minList:[],
    hour:0,
    min:0,
  },
  onLoad:function(options){
    wx.setNavigationBarTitle({ title:'我的'})
    const date=new Date();
    const cur_year=date.getFullYear();
    const cur_month=date.getMonth();//0代表1月
    const cur_day=date.getDate()//1-31
    const cur_week=date.getDay();//0代表周日
    this.setData({
      "today.year":cur_year,
      "today.month":cur_month+1,
      "today.day":cur_day,
      "choosedDay":this.data.today,
    });
    this.fullDays(cur_year,cur_month);//填充days
    this.enterPage();
  },
  // 获取当月共多少天
  getThisMonthDays:function(year, month){
    return new Date(year, month+1, 0).getDate();
  },
  //获取上一月多少天
  getLastMonthDays:function(year, month){
    if(month==7)
    return new Date(year, 12, 0).getDate();
    else
    return new Date(year, month, 0).getDate();
  },
  // 获取当月第一天星期几
  getFirstDayOfWeek:function(year, month) {
    return new Date(year, month, 1).getDay();
  },
  // 获取当月最后一天星期几
  getLastDayOfWeek:function(year, month) {
    var day=this.getThisMonthDays(year,month);
    return new Date(year, month,day).getDay();
  },
  //填充days
  fullDays(year,month){
    var that=this;
    var lastMonthDays=this.getLastMonthDays(year,month);//上一月天数
    var thisMonthDays=this.getThisMonthDays(year,month);//本月天数
    that.setData({days:[]});
    const firstDayWeek=this.getFirstDayOfWeek(year,month);//第一天星期
    const lastDayWeek=this.getLastDayOfWeek(year,month);//最后一天星期

    //填充上一月天数
    for(let i=0;i<firstDayWeek;i++){
      var obj={
        date:lastMonthDays-firstDayWeek+1,
        isSign:false,
        thisMonth:false,
      }
      that.data.days.push(obj);
      lastMonthDays++;
    }
    //填充本月天数
    for(let i=1;i<=thisMonthDays;i++){
      var obj={
        date:i,
        isSign:false,
        thisMonth:true,
      }
      that.data.days.push(obj);
    }
    //填充下一月天数
    for(let i=1;i<7-lastDayWeek;i++){
      var obj={
        date:i,
        isSign:false,
        thisMonth:false,
      }
      that.data.days.push(obj);
    }
    this.setData({
      days:that.data.days
    });
  },

  toL(e){
    var NowMonth=this.data.choosedDay.month-1;
    var NowYear=this.data.choosedDay.year;
    if(NowMonth<1){
      NowMonth=12;
      NowYear--;
    }
    this.setData({
      choosedDay:{year:NowYear,month:NowMonth,day:1},
    });
    this.fullDays(this.data.choosedDay.year,this.data.choosedDay.month-1);
    this.fillClockin()
  },
  toR(e){
    var NowMonth=this.data.choosedDay.month+1;
    var NowYear=this.data.choosedDay.year;
    if(NowMonth>12){
      NowMonth=1;
      NowYear++;
    }
    this.setData({
      choosedDay:{year:NowYear,month:NowMonth,day:1},
    });
    this.fullDays(this.data.choosedDay.year,this.data.choosedDay.month-1);
    this.fillClockin()
  },

  //当前日是否打卡改为true
  signBtr(e){
    var thisMonthDays=this.getThisMonthDays(this.data.today.year,this.data.today.month);//本月天数
    for(var i=0;i<thisMonthDays;i++){
      if(this.data.today.day==this.data.days[i].date&&this.data.today.month==this.data.choosedDay.month&&this.data.today.year==this.data.choosedDay.year)
          this.setData({
            ["days["+i+"].isSign"]:"true",
            "today.isSign":true,
          });
    }
    wx.showToast({
      title: '打卡成功',
      icon: 'success',
      duration: 2000//持续的时间
    })
    setTimeout(function () {
        wx.navigateTo({
          url:'../share/share',
        })
      }, 2000)
  },
  toIndex(e){
    wx:wx.navigateTo({
      url: '',//填写首页地址
    })
  },
  // 进入页面，发送请求
  enterPage(){
    var that=this
    let f = length => Array.from({length}).map((v,k) => k);
    wx.request({
      url: app.globalData.baseUrl+'/personal/getClockons', 
      method:"POST",
      data: {
        user_id:app.globalData.userInfo.user_id,
      },      
      header: {
        "Content-Type": "application/x-www-form-urlencoded"// 默认值
      },
      success (res) {
        console.log("res",res)
        var data=res.data
        var remind_time_list=data.remind_time.split(":")
        var hour=Number(remind_time_list[0])
        var min=Number(remind_time_list[1])
        console.log("hour,min",hour,min)
        that.setData({
          max_length:data.max_length,
          clockons:data.clockons,
          user_name:app.globalData.userInfo.user_name,
          avatar:app.globalData.userInfo.avatar,
          is_remind:data.is_remind,
          remind_time:data.remind_time,
          hour:hour,
          min:min,
          hourList:f(24),
          minList:f(60)

        })
        that.fillClockin()
      }   
    })
  },

  fillClockin(){
    for(let i=0;i<this.data.clockons.length;i++){
      var clockon = this.data.clockons[i]
      var year = Number(clockon.substring(0, 4))
      var month =  Number(clockon.substring(5, 7))
      var day =  Number(clockon.substring(8, 10))
      if(year == this.data.today.year&&month == this.data.today.month&&day == this.data.today.day){
        this.setData({
          "today.isSign":true
        })
      }
      if(year == this.data.choosedDay.year&&month == this.data.choosedDay.month){
        for(let i=0;i<this.data.days.length;i++){
          if(this.data.days[i].thisMonth == true&&this.data.days[i].date == day){
            this.setData({
              ["days["+i+"].isSign"]:"true",
            });
            break;
          }
        }
      }
    }
  },

  clockin(){
    var that=this
    wx.request({
      url: app.globalData.baseUrl+'/personal/clockin', 
      method:"POST",
      data: {
        user_id:app.globalData.userInfo.user_id,
      },      
      header: {
        "Content-Type": "application/x-www-form-urlencoded"// 默认值
      },
      success (res) {
        var data=res.data
        console.log("personal/clockin",data)
        if(data.msg=='成功'){
          wx.showToast({
            title: '打卡成功！',
            icon: 'success',
            duration: 2000
          })
          //that.signBtr()
          that.enterPage();
          setTimeout(function () {
            wx.navigateTo({
              url:'../share/share',
            })
            }, 2000)
        }
        else{
          wx.showToast({
            title: data.msg,
            icon: 'error',
            duration: 2000
          })
        }
      }   
    })
  },

  share(){
    wx.navigateTo({
      url: '../share/share',
    })
  },
  onChange(e){
    var checked=e.detail
    var that=this   
    if(checked==true){
      wx.requestSubscribeMessage({
        tmplIds: ['bNEVQXRERG9H1mQxGf-ctuarD8FNPmt81eqhypD--L4'],
        success (res) {
          console.log('请求权限',res)
          if(res['bNEVQXRERG9H1mQxGf-ctuarD8FNPmt81eqhypD--L4']!="reject"){
            console.log("time",that.data.remind_time)
            wx.request({
              url: app.globalData.baseUrl+'/personal/sendMessage', 
              method:"POST",
              data: {
                user_id:app.globalData.userInfo.user_id,
                time:that.data.remind_time,
                action:checked?1:2
              },      
              header: {
                "Content-Type": "application/x-www-form-urlencoded"// 默认值
              },
              success (res) {
                console.log(res)
                that.setData({
                  is_remind:checked,
                })                    
              },            
            })                 
          }
          },        
      })     
    }
    else{
      wx.request({
        url: app.globalData.baseUrl+'/personal/sendMessage', 
        method:"POST",
        data: {
          user_id:app.globalData.userInfo.user_id,
          time:that.data.remind_time,
          action:checked?1:2
        },      
        header: {
          "Content-Type": "application/x-www-form-urlencoded"// 默认值
        },
        success (res) {
          console.log(res)
          that.setData({
            is_remind:checked,
          })                    
        },            
      })    
    }   
  },
  onInput(event) {
    this.setData({
      remind_time: event.detail,
    });
  },
//hour滚动条绑定事件
hourChange(e){
  const { picker, value, index } = e.detail;
  console.log(value);
  this.setData({
    hour:value,
  })
},
//min滚动条绑定事件
minChange(e){
  const { picker, value, index } = e.detail;
  console.log(value);
  this.setData({
    min:value,
  })
},
  confirm(event){
    var that=this;
    var hour=Number(that.data.hour)
    var min=Number(that.data.min)
    var hour_t=(hour>=10)?hour:("0"+hour)
    var min_t=(min>=10)?min:("0"+min)
    var remind_time=hour_t+":"+min_t
    console.log('hour,min,remind_time',hour,min,remind_time)
    wx.request({
      url: app.globalData.baseUrl+'/personal/sendMessage', 
      method:"POST",
      data: {
        user_id:app.globalData.userInfo.user_id,
        time:remind_time,
        action:3
      },      
      header: {
        "Content-Type": "application/x-www-form-urlencoded"// 默认值
      },
      success (res) {
        console.log(res);
        if(Number(that.data.hour)<10)
        that.setData({
          hour:hour,
          });  
        if(Number(that.data.min)<10)
        that.setData({
          min:min,
          });  
        that.setData({
        //  remind_time: event.detail,
          remind_time:remind_time,
          show:false
        });  
            
      }
    })          
 
  },
  cancel(){
    this.setData({
      show:false,
    });

  },
  changeTime(){    
    this.setData({
      show:true
    })
  }
})
