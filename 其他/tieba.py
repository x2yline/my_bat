# -*- coding: utf-8 -*-
"""
Created on Sun Aug 21 11:01:09 2016

@author: Administrator
"""
from bs4 import BeautifulSoup
import urllib
import urllib2
import cookielib
import re
import hashlib
import json
import threading
import platform
import os


def _setup_cookie(my_cookie):
    cookie = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    urllib2.install_opener(opener)
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (SymbianOS/9.3; Series60/3.2 NokiaE72-1/021.021; Profile/MIDP-2.1 Configuration/CLDC-1.1 ) AppleWebKit/525 (KHTML, like Gecko) Version/3.0 BrowserNG/7.1.16352'),
                         ('Cookie', my_cookie), ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')]


def _fetch_like_tieba_list():
    print u'获取喜欢的贴吧ing...' if system_env else '获取喜欢的贴吧ing...'
    page_count = 1
    find_like_tieba = []
    while True:
        like_tieba_url = 'http://tieba.baidu.com/f/like/mylike?&pn=%d' % page_count
        req = urllib2.Request(like_tieba_url)
        resp = urllib2.urlopen(req).read()
        resp = resp.decode('gbk').encode('utf8')
        re_like_tieba = '<a href="\/f\?kw=.*?" title="(.*?)">.+?<\/a>'
        temp_like_tieba = re.findall(re_like_tieba, resp)
        if not temp_like_tieba:
            break
        if not find_like_tieba:
            find_like_tieba = temp_like_tieba
        else:
            find_like_tieba += temp_like_tieba
        page_count += 1

    return find_like_tieba


def _fetch_tieba_info(tieba):
    tieba_wap_url = "http://tieba.baidu.com/mo/m?kw=" + tieba
    wap_resp = urllib2.urlopen(tieba_wap_url).read()

    if not wap_resp:
        return
    re_already_sign = '<td style="text-align:right;"><span[ ]>(.*?)<\/span><\/td><\/tr>'
    already_sign = re.findall(re_already_sign, wap_resp)

    re_fid = '<input type="hidden" name="fid" value="(.+?)"\/>'
    _fid = re.findall(re_fid, wap_resp)
    fid = _fid and _fid[0] or None

    re_tbs = '<input type="hidden" name="tbs" value="(.+?)"\/>'
    _tbs = re.findall(re_tbs, wap_resp)

    tbs = _tbs and _tbs[0] or None
    return already_sign, fid, tbs


def _decode_uri_post(postData):
    SIGN_KEY = "tiebaclient!!!"
    s = ""
    keys = postData.keys()
    keys.sort()
    for i in keys:
        s += i + '=' + postData[i]
    sign = hashlib.md5(s + SIGN_KEY).hexdigest().upper()
    postData.update({'sign': str(sign)})
    return postData


def _make_sign_request(tieba, fid, tbs, BDUSS):
    sign_url = 'http://c.tieba.baidu.com/c/c/forum/sign'
    sign_request = {"BDUSS": BDUSS, "_client_id": "03-00-DA-59-05-00-72-96-06-00-01-00-04-00-4C-43-01-00-34-F4-02-00-BC-25-09-00-4E-36", "_client_type":
                    "4", "_client_version": "1.2.1.17", "_phone_imei": "540b43b59d21b7a4824e1fd31b08e9a6", "fid": fid, "kw": tieba, "net_type": "3", 'tbs': tbs}

    sign_request = _decode_uri_post(sign_request)
    sign_request = urllib.urlencode(sign_request)

    sign_request = urllib2.Request(sign_url, sign_request)
    sign_request.add_header(
        "Content-Type", "application/x-www-form-urlencoded")
    return sign_request


def _handle_response(sign_resp):
    sign_resp = json.load(sign_resp)
    error_code = sign_resp['error_code']
    sign_bonus_point = 0
    try:
        # Don't know why but sometimes this will trigger key error.
        sign_bonus_point = int(sign_resp['user_info']['sign_bonus_point'])
    except KeyError:
        pass
    if error_code == '0':
        print u"签到成功,经验+%d" % sign_bonus_point if system_env else "签到成功,经验+%d" % sign_bonus_point
    else:
        error_msg = sign_resp['error_msg']
        if error_msg == u'亲，你之前已经签过了':
            print u'之前已签到' if system_env else '之前已签到'
        else:
            print u'签到失败' if system_env else '签到失败'
            print "Error:" + unicode(error_code) + " " + unicode(error_msg)


def _sign_tieba(tieba, BDUSS):
    already_sign, fid, tbs = _fetch_tieba_info(tieba)
    if not already_sign:
        print tieba.decode('utf-8') + u'......正在尝试签到' if system_env else tieba + '......正在尝试签到'
    else:
        if already_sign[0] == "已签到":
            print tieba.decode('utf-8') + u"......之前已签到" if system_env else tieba + "......之前已签到"
            return

    if not fid or not tbs:
        print u"签到失败，原因未知" if system_env else "签到失败，原因未知"
        return

    sign_request = _make_sign_request(tieba, fid, tbs, BDUSS)
    sign_resp = urllib2.urlopen(sign_request, timeout=5)
    _handle_response(sign_resp)


def sign(my_cookie, BDUSS):
    _setup_cookie(my_cookie)
    _like_tieba_list = _fetch_like_tieba_list()
    if len(_like_tieba_list) == 0:
        print u"获取喜欢的贴吧失败，请检查Cookie和BDUSS是否正确" if system_env else "获取喜欢的贴吧失败，请检查Cookie和BDUSS是否正确"
        return
    thread_list = []
    for tieba in _like_tieba_list:
        t = threading.Thread(target=_sign_tieba, args=(tieba, BDUSS))
        thread_list.append(t)
        t.start()
        
    for t in thread_list:
        t.join(2)


def cookie1(my_cookie):
    cookie = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    urllib2.install_opener(opener)
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (SymbianOS/9.3; Series60/3.2 NokiaE72-1/021.021; Profile/MIDP-2.1 Configuration/CLDC-1.1 ) AppleWebKit/525 (KHTML, like Gecko) Version/3.0 BrowserNG/7.1.16352'),
                         ('Cookie', my_cookie), ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')]

def main():
    my_cookie = "PSTM=1467080418; BIDUPSID=D34CFCD567CC05F6914EF00875652CB9; bdshare_firstime=1471330584690; H_PS_PSSID=1425_19034_13550_17948_19861_12203_20856_20837; wise_device=0; showCardBeforeSign=1; rpln_guide=1; LONGID=1512725159; IS_NEW_USER=8d7ee1d488a55e4222ee3887; BAIDU_WISE_UID=wapp_1471748588210_624; H_WISE_SIDS=108263_102570_108268_100043_102479_100103_103550_104340_106322_109036_107515_108374_108459_108412_108332_107694_108454_108116_108085_107960_109506_108074_108120_108341_107806_107787_108295_107671_108076_107316_107242_107616; plus_cv=1::m:691fc2a7; BDUSS=EE3aVBaUm54dlVrOUJYQUVaMlFRWlI5LTk1S2RBdW95MkMwTmFnNTUxMUFwLUJYQVFBQUFBJCQAAAAAAAAAAAEAAACnWipaZDFsaW5lAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAauVdAGrlXd; BAIDUID=F2297C7C49B594B5F251EF2BF12DE804:FG=1; TIEBAUID=e69cb2e1501516811907644a; TIEBA_USERTYPE=7d1745759f20b1e7af100d7d"
    BDUSS = "EE3aVBaUm54dlVrOUJYQUVaMlFRWlI5LTk1S2RBdW95MkMwTmFnNTUxMUFwLUJYQVFBQUFBJCQAAAAAAAAAAAEAAACnWipaZDFsaW5lAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAauVdAGrlXd"
    sign(my_cookie, BDUSS)

if __name__ == "__main__":

    system_env = True if platform.system()=='Windows' else False
    main()
    #os.system("date /T >> tieba_log.log") if system_env else os.system("date >> tieba_log.log")

    my_cookie = "D43n_4dbf_saltkey=thvbCXg8; D43n_4dbf_lastvisit=1471316187; D43n_4dbf_ulastactivity=b46aFHUyajpqNIjyqUpln1Y1rRE55plk0YoDVIkXxHFtLBhMfBdL; D43n_4dbf_auth=33bcVxk6W6Xt1pLPOXJSrEbLberu%2BPMUCJA14wDMJrPB4eL5Zer152Xw4jAjxbA0fFzfDFH3iVjqsq6Q2LPyu8aN; D43n_4dbf_lastcheckfeed=3106%7C1471750772; D43n_4dbf_lip=175.5.131.149%2C1470808121; D43n_4dbf_security_cookiereport=109auuvjnoH1RSVynOErutjIO269fKhKfsNNC5ZeBtme%2FKbLjOvY; D43n_4dbf_nofavfid=1; D43n_4dbf_study_nge_extstyle=auto; D43n_4dbf_study_nge_extstyle_default=auto; tjpctrl=1471752549731; D43n_4dbf_st_p=3106%7C1471751046%7Cb4885551f91d0fef4ad10e6c77ffa6f4; D43n_4dbf_visitedfid=47; D43n_4dbf_viewid=tid_1845; D43n_4dbf_sid=oFYKk7; D43n_4dbf_sendmail=1; D43n_4dbf_checkpm=1; CNZZDATA1253022179=2084137577-1471319327-%7C1471748153; D43n_4dbf_smile=1D1; D43n_4dbf_lastact=1471751049%09misc.php%09patch"
    cookie1(my_cookie)
    req = urllib2.Request('http://bbs.chongbuluo.com/')
    resp = urllib2.urlopen(req).read()
    resp = resp.decode('utf-8').encode('utf8')

    recomp = re.compile('''<p class="xg2">(.*?)</p></td>''')
    infos = re.findall(recomp,resp)
    print infos[1].decode('utf-8')
    
    raw_input("\n\n\npress any key to exit:\n")

