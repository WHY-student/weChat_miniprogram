// pages/chooseBook/chooseBook.js
var app = getApp();

Page({
  /**
   * 页面的初始数据
   */
  data: {
    showBook:"",
    navList:[
      {
        level:"少儿",
        category:['剑桥少儿']
      },
      {
        level:"小学",
        category:['人教版']
      },    
      {
        level:"初中",
        category:['外研版','译林版','中考必备']
      },   
      {
        level:"高中",
        category:['人教版']
      },   
      {
        level:"大学",
        category:['四级','六级','考研']
      },              
    ],
    selectComfirm:false,
    books:[],
    currentBookList:[],
    choosed:0,//当前选中的导航栏
    nextBarChoosed:0,//当前选中的副导航栏
    url:app.globalData.baseUrl
  },
  onLoad: function () {
    wx.showLoading({
      title: '加载中',
      mask:true
    })
    wx.setNavigationBarTitle({ title:'添加词书'})
    var that=this
    console.log("navList",this.data.navList)
    wx.request({
      url: app.globalData.baseUrl+'/selectBook/getBooks', 
      method:"POST",
      header: {
        "Content-Type": "application/x-www-form-urlencoded"// 默认值
      },
      success (res) { 
        console.log('books',that.data.books)
        var books=res.data
        for(var i=0;i<books.length;i++){
          books[i].book_cover=app.globalData.baseUrl+books[i].book_cover
        }
        that.setData({
          books:books
        })
        that.getBookList()
        wx.hideLoading()
      }
    })    
  },
  chooseLevel(e){
    this.setData({
      choosed:e.currentTarget.dataset.level,
      nextBarChoosed:0
    })
    this.getBookList()
  },
  chooseCategory(e){
    this.setData({
      nextBarChoosed:e.currentTarget.dataset.category
    })
    this.getBookList()
  },
  getBookList(){
    var currentBookList=[]
    for(var i=0;i<this.data.books.length;i++){
      if(this.data.books[i].category==this.data.navList[this.data.choosed].category[this.data.nextBarChoosed]&&this.data.books[i].level==this.data.navList[this.data.choosed].level){
        currentBookList.push(this.data.books[i])
      }
    }
    this.setData({
      currentBookList:currentBookList
    })
    console.log('this.currentBookList',this.data.currentBookList)
  },
  chooseBook(e){
    for(var i=0;i<this.data.currentBookList.length;i++){
      if(this.data.currentBookList[i].book_id==e.currentTarget.dataset.book_id){
        this.setData({
          showBook:this.data.currentBookList[i]
        })
      }
    }
    this.setData({
      selectComfirm:true
    })
  },
  close(){
    this.setData({
      selectComfirm:false
    })
  },
  addToBook(e){ 
    var that=this
    wx.request({
      url: app.globalData.baseUrl+'/selectBook/select', 
      method:"POST",
      data: {
        user_id:app.globalData.userInfo.user_id,
        book_id:e.currentTarget.dataset.book_id
      },      
      header: {
        "Content-Type": "application/x-www-form-urlencoded"// 默认值
      },
      success (res) {
        if(res.data.msg=="不要重复操作"){
          wx.showToast({
            title: '不能重复添加',
            icon: 'error',
            duration: 1500,
            complete:that.close
          })
        }
        else{
          wx.showToast({
            title: '添加成功',
            icon: 'error',
            duration: 1500,
            complete:that.close
          }) 
          wx.reLaunch({
            url: '../homepage/homepage'
          })
        }
      }
    }) 
  }
})