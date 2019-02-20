 **cdut2016** 一个简洁美观的班级辅助系统。使用flask开发，前端使用Bootstrap。    

---

#### 项目结构


├─app
│  ├─auth                                   //个人
│  │ 
│  ├─errors                                 //网络错误处理
│  │  
│  ├─main                                   //主要
│  │  
│  ├─manage                                 //管理中心
│  │        
│  ├─news_cdut                              //理工通知
│  │  
│  ├─personal                               //个人中心
│  │  
│  ├─spider                                 //爬虫
│  │  
│  ├─static                                 //静态文件
│  │  ├─css
│  │  └─img
│  ├─templates                              //html模板
│  │  ├─announces
│  │  ├─auth
│  │  ├─email
│  │  ├─errors
│  │  ├─manage
│  │  ├─news_cdut
│  │  └─personal
│  └─__pycache__
│ 
├─logs                                      //日志
│                        
├─cdut2016.py                               //启动入口
│ 
├─config.py                                 //配置
│ 
├─README.MD                                 //README
│ 
└─requirements.txt                          //包

#### 功能特性

* 当教务处有成绩更新时，会通过邮件通知
* 通过下载excel到本地简单的收集信息

#### 版本内容更新

v1.0 初始版本

v1.1 最终版本

* fix some bugs
* ~~看来只能拿来收集一些简单的东西了，如有人参加或这不参加什么了~~
* 目前访问首页时比以前慢，因为每次访问首页都要运行爬虫。
* `font-size: 1.4vw` 用电脑模拟的手机的字体大小还合适，用手机真机看确实有点小，如果用Bootstra的样式来设置理论上应该会好些;

#### todo list
- [x] 表单手机更加方便，表单字体适配

#### 部署
* 参考 [this](https://blog.csdn.net/weixin_38256474/article/details/82185100)

#### 更新
* 首先备份了数据库，但在更新时出现了问题，怎么也更新不了，于是先用`netstat -lnp|grep 8000`
查看是哪个进程占用了8000端口，然后用`ps pid`杀死了该进程;再重新启动项目，并把之前备份的数据恢复。
