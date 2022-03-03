// pages/myBook/myBook.js
var app = getApp();
Page({

  /**
   * 页面的初始数据
   */
  data: {
    nowBook:"",
    allBooks:[],
    url:app.globalData.baseUrl
  },
  onLoad:function(){
    wx.showLoading({
      title: '加载中',
      mask:true
    })
    wx.setNavigationBarTitle({ title:'我的词书'})
    var that = this
    wx.request({
      url: app.globalData.baseUrl+'/changeBook/getMyBooks', 
      method:"POST",
      data:{
        user_id:app.globalData.userInfo.user_id
      },
      header: {
        "Content-Type": "application/x-www-form-urlencoded"// 默认值
      },
      success (res) { 
        var data=res.data
        console.log("MyBooks",data)
        var nowBook
        var allBooks=[]
        for(let i=0;i<data.books.length;i++){
          var book = data.books[i]
          var obj={
            id:book.book_id,
            title:book.book_name,
            vocabulary:book.words,
            pic:app.globalData.baseUrl+book.book_cover,
            learned:book.learned
          }
          console.log(obj)
          if(i==0){
            nowBook=obj
          }
          else{
            allBooks.unshift(obj)
          }
        }
        that.setData({
          nowBook:nowBook,
          allBooks:allBooks
        })
        wx.hideLoading()
      }
    })    
  },
  addBook(e){
    wx:wx.navigateTo({
      url: '../chooseBook/chooseBook',
    })
  },
  //正在学习的词书清空进度
  flashN(e){
    this.setData({
      "nowBook.learned":0,
    })
    this.clearProgress(this.data.nowBook.id)
  },
  //其他词书清空进度
  flashO(e){
    console.log(e);
    const id=e.currentTarget.dataset.id;
    this.setData({
      ["allBooks["+id+"].learned"]:0,
    })
    this.clearProgress(this.data.allBooks[id].id)
  },
  //更换当前正在学习的词书
  changeBook(e){
    var book=this.data.nowBook;
    const id=e.currentTarget.dataset.id;
    this.change(this.data.allBooks[id].id)
    // this.setData({
    //   nowBook:this.data.allBooks[id],
    //   ["allBooks["+id+"]"]:book,
    // });
    this.toHomepage()
  },

  toHomepage(){
    wx.reLaunch({
      url: '../homepage/homepage'
    })
  },
  //删除当前正在学习的词书
  deleteN(e){
    var id=e.currentTarget.dataset.id;
    const that=this;
    var book=that.data.allBooks[0];
    wx.showModal({
      content: '确认删除该书？',
      success: function (res) {
        if (res.confirm) {
          that.deleteBook(that.data.nowBook.id)
          that.data.allBooks.splice(0,1);
          that.setData({
            allBooks:that.data.allBooks,
            nowBook:book,
          });
          console.log(that.data.allBooks);
        } else {//这里是点击了取消以后
          console.log(that.data.allBooks);
        }
      }
    })
  },
  //删除其他词书
  deleteO(e){
    var id=e.currentTarget.dataset.id;
    const that=this;
    wx.showModal({
      content: '确认删除该书？',
      success: function (res) {
        if (res.confirm) {
          that.deleteBook(that.data.allBooks[id].id)
          that.data.allBooks.splice(id,1);
          that.setData({
            allBooks:that.data.allBooks,
          })
          console.log(that.data.allBooks);
        } else {//这里是点击了取消以后
          console.log(that.data.allBooks);
        }
      }
    })
  },

  clearProgress(id){
    var that = this
    wx.request({
      url: app.globalData.baseUrl+'/changeBook/clearProgress', 
      method:"POST",
      data:{
        user_id:app.globalData.userInfo.user_id,
        book_id:id
      },
      header: {
        "Content-Type": "application/x-www-form-urlencoded"// 默认值
      },
      success (res) { 
        var data=res.data
        console.log("clearProgress",data)
        if(data.msg == "成功"){
          wx.showToast({
            title: "清除进度成功！",
            icon: 'success',
            duration: 2000
          })
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

  deleteBook(id){
    var that = this
    wx.request({
      url: app.globalData.baseUrl+'/changeBook/deleteBook', 
      method:"POST",
      data:{
        user_id:app.globalData.userInfo.user_id,
        book_id:id
      },
      header: {
        "Content-Type": "application/x-www-form-urlencoded"// 默认值
      },
      success (res) { 
        var data=res.data
        console.log("deleteBook",data)
        if(data.msg == "成功"){
          wx.showToast({
            title: "删除成功！",
            icon: 'success',
            duration: 2000
          })
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

  change(id){
    var that = this
    wx.request({
      url: app.globalData.baseUrl+'/changeBook/change', 
      method:"POST",
      data:{
        user_id:app.globalData.userInfo.user_id,
        book_id:id
      },
      header: {
        "Content-Type": "application/x-www-form-urlencoded"// 默认值
      },
      success (res) { 
        var data=res.data
        console.log("change",data)
        if(data.msg == "成功"){
          wx.showToast({
            title: "换书成功！",
            icon: 'success',
            duration: 2000
          })
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
})
