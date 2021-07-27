# tieba_signin

## 功能
### 自动签到
输入`Cookie`后每天自动签到所有关注的贴吧  
### 自动水贴
`IS_AUTO_POST`设为`True`时，随机在每个关注的贴吧中选择一个帖子回复随机表情  
**此功能有可能导致封号，请谨慎使用**

## 获取百度贴吧COOKIE  
访问[https://tieba.baidu.com/index.html](https://tieba.baidu.com/index.html)  
打开`开发人员工具`  
在上方切换到`网络`标签  
刷新一次网页  
在左侧点击`index.html`请求（其他请求也可以，只要请求标头中有`Cookie`即可），在右侧请求标头中复制`Cookie`的值（从`:`后开始复制）  
>由于`Cookie`中可能有特殊字符导致脚本运行失败，所以脚本报错时可以尝试只留下`Cookie`中的`BDUSS`和`STOKEN`两项  

![1](https://img11.360buyimg.com/ddimg/jfs/t1/177298/16/15788/288403/60fcdce5E298c72a1/bc077c616be2ed13.png)  

## 创建secrets
|Name|Value|备注|是否必填|
|:---:|:---:|:---:|:---:|
|`TIEBA_COOKIE`|前面获取的百度贴吧COOKIE|只需要`BDUSS`和`STOKEN`两项|是|
|`IS_AUTO_POST`|`True`或不填|为`True`时开启自动水贴|否|

## 运行Actions
运行一次Actions，没有问题的话会在每天7:00自动运行  
