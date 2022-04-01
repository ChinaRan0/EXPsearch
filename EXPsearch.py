from base64 import encode
from lxml import etree
import requests
import re
import time
import os
import warnings 
warnings.filterwarnings("ignore")               #处理错误

headerss = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
}


def CVE() :
    CVE_number = input('请输入要查询的CVE编号,如:CVE-2019-0708:')
    url = 'http://cve.scap.org.cn/'
    url1 = f'http://cve.scap.org.cn/vulns?keyword={CVE_number}'     #这里仅供调试用，后期要改成{CVE_number}
    url1_re = requests.get(url=url1,headers=headerss)
    url1_re.encoding = ('utf-8')
    # print(url1_re.text)                                              #调试
    url1_etree = etree.HTML(url1_re.text)
    url1_etree_resule_name = url1_etree.xpath('/html/body/div/div[3]/div[1]/div/table/tbody/tr/td[1]/a/text()')
    url1_etree_resule_content = url1_etree.xpath('/html/body/div/div[3]/div[1]/div/table/tbody/tr/td[4]/text()')
    url1_etree_resule_link = url1_etree.xpath('/html/body/div/div[3]/div[1]/div/table/tbody/tr/td[1]/a/@href')
    url1_etree_resule_name_handle = url1_etree_resule_name[0]
    url1_etree_resule_content_handle = url1_etree_resule_content[0]
    url1_etree_resule_link_handle = url1_etree_resule_link[0]
    print(url1_etree_resule_name_handle.strip() +  '    '  + url1_etree_resule_content_handle.strip() +'\n文章链接:' + url  + url1_etree_resule_link_handle.strip() )
    url1_re.close

def KeyWord():
    content = input('请输入查询的关键字信息:')

    #调用绿盟科技的漏洞库
    print('以下是调用的绿盟数据库：')
    url = 'http://www.nsfocus.net'
    url1 = f'http://www.nsfocus.net/index.php?act=sec_bug&type_id=&os=&keyword={content}&page=1' 
    url1_re = requests.get(url=url1,headers=headerss)
    url1_re.encoding = ('utf-8')
    obj = re.compile(r'.*?共(?P<shuliang>.*?)条记录',re.S)
    url1_re_quantity = obj.findall(url1_re.text)
    url1_re.close
    yeshu = url1_re_quantity[0]
    yeshu = int(yeshu)
    yeshu = yeshu/15
    if yeshu % 15 != 0 :
        yeshu =yeshu +1
    
    print('查询中····')
    time.sleep(2)
    print('过程可能会暂停一会来绕过服务器策略，请耐心等待脚本跑完')
    time.sleep(5)
    i = 1
    while i <= yeshu :
        url11 = f'http://www.nsfocus.net/index.php?act=sec_bug&type_id=&os=&keyword={content}&page={i}'     #调试用，后期ThinkPHP改掉
        url11_re = requests.get(url=url11,headers=headerss)
        url11_re.encoding = ('utf-8')
        url11_re_etree = etree.HTML(url11_re.text)
        url11_re_etree_title = url11_re_etree.xpath('/html/body/div[1]/section/div/section/div[1]/div[2]/div[2]/div[4]/ul/li[*]/a/text()')
        url11_re_etree_link = url11_re_etree.xpath('/html/body/div[1]/section/div/section/div[1]/div[2]/div[2]/div[4]/ul/li[*]/a/@href')
        
        j = 0
        while j < len(url11_re_etree_title) :
            print(url11_re_etree_title[j])
            print(url + url11_re_etree_link[j]) 
            j = j+1
        
        i = i+1
    Expku(content)
def Expku(content) :
    #调用expku.com的数据库
    print("\n以下是expku.com的相关数据:")
    url = 'http://www.expku.com/search.php'
    postdata = {
        "keyword": f"{content}",
        "tag": "0"
    }
    url_re = requests.post(url=url,headers=headerss,data=postdata)
    url_re.encoding = ('gb2312')

    ojb = re.compile(r'.*?\'_blank\'.*?title=\'(?P<name>.*?)\'>',re.S)
    ojb2 = re.compile(r'.*?list_explot_description"><a href=\'(?P<link>.*?)\' target=',re.S)
    
    chuli = ojb.findall(url_re.text)
    chuli2 = ojb2.findall(url_re.text)
    url_re.close
    i=0
    while i < len(chuli) :
        print(chuli[i] + '    ' + 'http://www.expku.com' +chuli2[i])
        i = i+1
    Exploit(content)

def Exploit(content) :   
    #粗略的看了一下反爬机制，太难了，而且数据也不好过滤，就直接用kali自带的了
    # 调用exploit-db库
    if os.system("searchsploit 1 > tmp") ==1 :
        print('您的电脑未正确安装searchsploit')
    else :
        print('以下的搜索结果的path皆在/usr/share/exploitdb/exploits/的相对目录下')
        os.system(f'searchsploit -t {content}')
    AliEXP(content)

def AliEXP(content) :
    # 调用 阿里云漏洞库
    print('\n以下是阿里云漏洞库的内容:')
    url = f"https://avd.aliyun.com/search?q={content}"
    yeshu = requests.get(url=url,headers=headerss,verify=False)
    yeshu.encoding = ('utf-8')
    obj1 = re.compile(r'.*?总计(?P<ysNM>.*?)条记录',re.S)
    yeshu_re = obj1.findall(yeshu.text)
    yeshu_number = yeshu_re[0].strip()
    print(yeshu_number)
    yeshu.close
    
    tmp1 = int(int(yeshu_number)/25)
    tmp2 = int(yeshu_number)%25
    if tmp2 != 0 :
        tmp1=tmp1+1
    print(tmp1)
     
    j=1
    while j<=tmp1 :
        url = f"https://avd.aliyun.com/search?q={content}&page={j}"
        url_re = requests.get(url=url,headers=headerss,verify=False)
        url_re_etree = etree.HTML(url_re.text)
        url_re_etree_title = url_re_etree.xpath('/html/body/main/div[2]/div/div[2]/table/tbody/tr[*]/td[2]/text()')
        url_re_etree_link = url_re_etree.xpath('/html/body/main/div[2]/div/div[2]/table/tbody/tr[*]/td[1]/a/@href')
        i = 0 
        while i < len(url_re_etree_link):
            print(url_re_etree_title[i] + '     ' + 'https://avd.aliyun.com' + url_re_etree_link[i])
            i = i+1
        j = j+1
    Vulhub(content)
def Vulhub(content) :
    print('\n以下是Vulhub漏洞库的内容:')
    url = f'http://android.scap.org.cn/vulns?view=global&keyword={content}'
    url_re = requests.get(url=url,headers=headerss)
    url_re.encoding = ('utf-8')
    url_re_etree = etree.HTML(url_re.text)
    url_re_etree_name = url_re_etree.xpath('/html/body/div/div[3]/div[1]/div/table/tbody/tr[*]/td[4]/text()')
    url_re_etree_link = url_re_etree.xpath('/html/body/div/div[3]/div[1]/div/table/tbody/tr[*]/td[1]/a/@href')
    j = 0
    while j < len(url_re_etree_name) :
        print(url_re_etree_name[j])
        print(url + url_re_etree_link[j]) 
        j = j+1

print('请输入搜索模式:')
print('1.CVE漏洞查询')
print('2.关键字漏洞查询')
mode = input()
if mode == "1" :
    CVE()
if mode == "2" :
    KeyWord()