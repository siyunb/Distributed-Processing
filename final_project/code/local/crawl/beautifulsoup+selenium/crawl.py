#-*-coding:utf-8-*-

from selenium import webdriver      #动态操作库
from bs4 import BeautifulSoup       #网页解析库
import xlwt
from multiprocessing import Pool    #进程库

def Crawl(urls,label):
    results={}
    for url in urls:
        driver = webdriver.PhantomJS()   #无浏览器自动化过程，节省内存使用，简化操作，提高速度
        driver.get(url)
        driver.switch_to_frame('g_iframe')
        page = driver.page_source
        soup = BeautifulSoup(page, 'html.parser')
        body = soup.find('tbody')        #find其实是字符串
        lists = body.find_all('tr')      #findall生成的其实是列表
        for l in lists:
            span = l.find('span', class_='txt')
            title = span.find('b')['title']    #找到歌曲title并储存
            url = 'http://music.163.com/#' + span.find('a')['href']  #拼接歌曲的url
            print (title,url)            #输出title以及歌曲链接
            results.setdefault(title,url+'\t'+label)
    return results

def Crawl_lyrics(url):
    driver = webdriver.PhantomJS()
    driver.get(url)
    driver.switch_to_frame('g_iframe')
    page = driver.page_source
    soup = BeautifulSoup(page, 'lxml')
    content=soup.find('div', id='lyric-content').get_text() #获得歌词信息
    print ('success')
    return content                       #抛出文本内容

def write_to_excel(results,path):
    workbook = xlwt.Workbook(encoding='utf-8')       #打开一个工作簿，编码为utf-8
    worksheet = workbook.add_sheet(u'网易云')
    worksheet.write(0, 0, 'name')
    worksheet.write(0, 1, 'lyrics')
    worksheet.write(0, 2, 'label')
    flag = 1
    for key, value in results.items():
        worksheet.write(flag, 0, key)
        url = value.strip().split('\t')[0]
        lyrics = Crawl_lyrics(url).split(':')[-1]
        label = value.strip().split('\t')[1]
        worksheet.write(flag, 1, lyrics)
        worksheet.write(flag, 2, label)
        flag += 1
    workbook.save(path)


if __name__=='__main__':                            #作为主程序接口
    shanggan_urls=['http://music.163.com/#/playlist?id=2076225716']
                 'http://music.163.com/#/playlist?id=2076277368',
                  'http://music.163.com/#/playlist?id=2076294506',
               'http://music.163.com/#/playlist?id=2076311073',
                'http://music.163.com/#/playlist?id=2076270042',
                  'http://music.163.com/#/playlist?id=2076290107',
                  'http://music.163.com/#/playlist?id=2076210751']
    yuyue_urls=['http://music.163.com/#/playlist?id=2076252746',
                 'http://music.163.com/#/playlist?id=2075908456',
                 'http://music.163.com/#/playlist?id=2076083125',
                 'http://music.163.com/#/playlist?id=2075831186',
                 'http://music.163.com/#/playlist?id=2075532617',
                 'http://music.163.com/#/playlist?id=2075700493',
                 'http://music.163.com/#/playlist?id=2075622352',
                 'http://music.163.com/#/playlist?id=2073689723']

    res_shanggan = Crawl(shanggan_urls,u'伤感')
    res_yuyue =Crawl(yuyue_urls,u'愉悦')
    write_to_excel(res_shanggan,'C:/Users/Bokkin Wang/data/shanggan.xls')
    write_to_excel(res_gufeng, 'C:/Users/Bokkin Wang/data/yuyue.xls')
