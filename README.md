# EXPsearch
## 设计初衷
nm一个个找漏洞信息太jb慢了，自己写个小脚本一键查询。
## 原理
python的requests,etree,re
kali的searchsploit（因为searchsploit的数据exploit-db的库，而exploit-db太难爬了，所以就省略了，直接调用searchsploit）
## 环境安装
pip3 install requests



pip3 install lxlm


apt install searchsploit（如果你是kali则不需要运行）
## 调用的数据来源:
绿盟，expku.com，exploit-db，阿里云漏洞库，Vulhub
后期继续加
