# tieba_signin

## 获取百度贴吧COOKIE  
访问[https://tieba.baidu.com/index.html](https://tieba.baidu.com/index.html)  
打开`开发人员工具`  
在上方切换到`网络`标签  
刷新一次网页  
在左侧点击`index.html`请求，在右侧请求标头中复制`Cookie`的值（从`:`后开始复制）  
![1](https://img11.360buyimg.com/ddimg/jfs/t1/177298/16/15788/288403/60fcdce5E298c72a1/bc077c616be2ed13.png)  

## 创建secrets
`Name`为`TIEBA_COOKIE`  
`Value`为前面获取的百度贴吧COOKIE  

## 运行Actions
运行一次Actions，没有问题的话会在每天7:00自动运行  
