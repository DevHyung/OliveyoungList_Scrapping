#_*_ coding:utf-8 _*_
import codecs
from bs4 import BeautifulSoup
import requests, json
import sys
from six.moves import urllib
reload(sys)
sys.setdefaultencoding('utf-8')
import xlsxwriter
#import lxml
#import urllib

#from urllib import quote
_data = {
    "pageIdx": "1",
    "searchType": "area",
    "rgn1": "",
    "rgn2": ""
}
_newdata = {
    "pageIdx": "1",
    "searchType": "new"
}
tmp = { 'rgn1' : ''}
rgn1 = ['강원도','경기도','경상남도','경상북도','광주광역시','대구광역시','대전광역시','부산광역시','서울특별시','세종특별자치시',
            '울산광역시','인천광역시','전라남도','전라북도','제주특별자치도','충청남도','충청북도']
rgn2_2d = []
regionclasslist = []
tmptotal = 0
class c_store():
    def __init__(self):
        self.name = "" #매장이름
        self.link = "" #매장 링크 주소
        self.addr = "" #매장 주소
        self.num = ""  # 전화번호
        self.method = "-"
        self.subway = "-" #가까운 지하철역
        self.region = ""
    def setinfo(self,_name,_link,_addr):
        self.name =_name
        self.link =_link
        self.addr =_addr

class c_region():
    def __init__(self):
        self.rgn = "" #지역 이름 ex 서울시/강남구
        self.totalcnt = 0 #지역에 해당하는 갯수
        self.storelist = [] # c_stroe 클래스를 저장할 리스트

def getRgn2():
    for rgn in rgn1:
        tmp['rgn1'] = rgn
        response = requests.post('http://www.oliveyoung.co.kr/store/store/getStoreSubAreaListJson.do', data=tmp,headers={'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'})
        txt =response.content.split(',')
        for idx in range(0,len(txt)):
            txt[idx] = txt[idx].replace('[','')
            txt[idx] = txt[idx].replace(']', '')
            txt[idx] = txt[idx].replace('"', '')
        rgn2_2d.append(txt)
def getJsonByPost(metroidx):
    #for idx in range(0,len(rgn1)):
    global tmptotal
    _data['rgn1']  = rgn1[metroidx]
    for rgn2txt in rgn2_2d[metroidx]:
        tmp = c_region()    #
        tmp.rgn = _data['rgn1'] + '/' + rgn2txt #
        print tmp.rgn+"진행중...",
        _data['rgn2'] = rgn2txt
        response = requests.post('http://www.oliveyoung.co.kr/store/store/getStoreListJson.do', data=_data,
                                 headers={'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'})
        data = json.loads(response.content)
        #,store['addr']
        try:
            print data['totalCount']
            tmptotal +=data['totalCount']
            tmp.totalcnt = data['totalCount']

            for store in data['storeList']:
                tmpstore = c_store()
                tmpstore.setinfo(store['strNm'],"http://www.oliveyoung.co.kr/store/store/getStoreDetail.do?strNo=" + store['strNo'],store['addr'])
                tmp.storelist.append(tmpstore)
                #print store['strNm'],"http://www.oliveyoung.co.kr/store/store/getStoreDetail.do?strNo=" + store['strNo']
            if data['totalCount'] > 20:
                #print "20넘음"
                _data['pageIdx'] = 2
                response = requests.post('http://www.oliveyoung.co.kr/store/store/getStoreListJson.do', data=_data,
                                         headers={
                                             'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'})
                data = json.loads(response.content)
                for store in data['storeList']:
                    tmpstore = c_store()
                    tmpstore.setinfo(store['strNm'],"http://www.oliveyoung.co.kr/store/store/getStoreDetail.do?strNo=" + store['strNo'], store['addr'])
                    tmp.storelist.append(tmpstore)
                    #print "http://www.oliveyoung.co.kr/store/store/getStoreDetail.do?strNo=" + store['strNo']
                _data['pageIdx'] = 1
            regionclasslist.append(tmp)
        except:
            tmp.totalcnt = 0
            pass
def newjson():
    # for idx in range(0,len(rgn1)):
    global tmptotal
    #_data['rgn1'] = rgn1[metroidx]
    #for rgn2txt in rgn2_2d[metroidx]:
    tmp = c_region()  #
    #tmp.rgn = _data['rgn1'] + '/' + rgn2txt  #
    #print tmp.rgn + "진행중...",
    #_data['rgn2'] = rgn2txt
    response = requests.post('http://www.oliveyoung.co.kr/store/store/getStoreListJson.do', data=_newdata,
                             headers={'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'})
    data = json.loads(response.content)
    try:
        idx = len( data['storeList'])
        print idx,"개"
        tmp.totalcnt = idx
        for store in data['storeList']:
            tmpstore = c_store()
            tmpstore.region = store['addr'].split(' ')[0]+'/'+store['addr'].split(' ')[1]
            tmpstore.setinfo(store['strNm'],
                             "http://www.oliveyoung.co.kr/store/store/getStoreDetail.do?strNo=" + store['strNo'],
                             store['addr'])
            tmp.storelist.append(tmpstore)

        if idx > 20:
            print "20넘음"
            _data['pageIdx'] = 2
            response = requests.post('http://www.oliveyoung.co.kr/store/store/getStoreListJson.do', data=_newdata,
                                     headers={
                                         'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'})
            data = json.loads(response.content)
            for store in data['storeList']:
                tmpstore = c_store()
                tmpstore.region = store['addr'].split(' ')[0] + '/' + store['addr'].split(' ')[1]
                tmpstore.setinfo(store['strNm'],
                                 "http://www.oliveyoung.co.kr/store/store/getStoreDetail.do?strNo=" + store[
                                     'strNo'], store['addr'])
                tmp.storelist.append(tmpstore)
                # print "http://www.oliveyoung.co.kr/store/store/getStoreDetail.do?strNo=" + store['strNo']
            _data['pageIdx'] = 1
        regionclasslist.append(tmp)
    except:
        tmp.totalcnt = 0
        pass
def newextractinfo(regionclass):
    # print len(regionclass.storelist) , "가진클래스넘어옴"
    for storeclass in regionclass.storelist:
        url = storeclass.link
        cnt = 0
        while (cnt < 3):
            try:
                f = urllib.request.urlopen(url)
                break;
            except urllib.error.HTTPError as e:
                print(e.reason)
                urllib.request.urlcleanup()
                print "get_bs_by_url error 1 : urlopen재시도중"
                try:
                    f = urllib.request.urlopen(url)
                    break;
                except:
                    urllib.request.urlcleanup()
                    print "리셋후재연결중"
                cnt += 1
        if cnt == 3: return None
        resultXML = f.read()
        bs = BeautifulSoup(resultXML, "lxml")
        telnum = bs.find("span", class_="tel").get_text()  # 저나번호
        try:
            map = bs.find("li", id="mapInfo")
            map = map.find_all('p')
            if telnum == map[0].get_text():
                pass
            storeclass.method = map[0].get_text()
            storeclass.subway = map[1].get_text()
            # print "추출"
        except:
            pass
        finally:
            storeclass.num = telnum
def extractinfo(regionclass):
    #print len(regionclass.storelist) , "가진클래스넘어옴"
    for storeclass in regionclass.storelist:
        url = storeclass.link
        #print url
        #url = 'http://www.oliveyoung.co.kr/store/store/getStoreDetail.do?strNo=D274'

        cnt = 0
        while (cnt < 3):
            try:
                f = urllib.request.urlopen(url)
                break;
            except urllib.error.HTTPError as e:
                print(e.reason)
                urllib.request.urlcleanup()
                print "get_bs_by_url error 1 : urlopen재시도중"
                try:
                    f = urllib.request.urlopen(url)
                    break;
                except:
                    urllib.request.urlcleanup()
                    print "리셋후재연결중"
                cnt += 1
        if cnt == 3: return None
        resultXML = f.read()
        bs = BeautifulSoup(resultXML, "lxml")
        telnum = bs.find("span", class_="tel").get_text() #저나번호
        try:
            map = bs.find("li",id="mapInfo")
            map = map.find_all('p')
            if telnum == map[0].get_text():
                pass
            storeclass.method =map[0].get_text()
            storeclass.subway =map[1].get_text()
            #print "추출"
        except:
            pass
        finally:
            storeclass.num = telnum

gogo = 16
if __name__ == '__main__':
    # http://www.oliveyoung.co.kr/store/store/getStoreDetail.do?strNo=DA9D store 상세
    #print "총" , len(rgn1), "지역존재" , "전지역은",rgn1[gogo-1]
    #getRgn2()
    #getJsonByPost(gogo) # 크게크게 경기인지 고양인지를 주고
    newjson()
    with codecs.open("new.txt", "w", encoding='utf-8-sig') as f:
        for regiondata in regionclasslist:
            extractinfo(regiondata) #큰 지역 regionclasslist만큼준다
            for store in regiondata.storelist:
                rg1 = store.region.split('/')[0]
                rg2 = store.region.split('/')[1]
                f.write(store.name+'@'+store.link+'@'+ rg1+'@'+rg2+'@'+store.addr+'@'
                        + store.subway+'@'+store.method+'@'+ store.num+'\n')
    print "총 ", tmptotal,"개"
    #print len(regionclasslist)
    """idx = 0
    print "리스트갯수::",len(regionclasslist)
    for data in  regionclasslist:
        for store in data.storelist:
            print data.rgn,store.name, store.link , store.addr
            idx +=1
    print idx"""

