import requests
import bs4
import lxml


def get_check_code():
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/84.0.4147.89 Safari/537.36'}
    session = requests.session()
    page = 'http://es.bnuz.edu.cn/CheckCode.aspx'
    img = session.get(page, stream=True, headers=headers)
    with open('check.jpg', 'wb') as f:
        f.write(img.content)
    return session


def login(session, id, passwords, checkcode):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/84.0.4147.89 Safari/537.36'}
    data = {
        'TextBox1': id,
        'TextBox2': passwords,
        'TextBox3': '',
        'RadioButtonList1': "学生".encode('gb2312', 'replace'),
        'Button4_test': '',
        '__VIEWSTATE': '',
        '__EVENTVALIDATION': '',
        '_VIEWSTATEGENERATOR': '',
        '__PREVIOUSPAGE': ''
    }
    url = "http://es.bnuz.edu.cn/"
    login_page = session.get(url, headers=headers)
    soup = bs4.BeautifulSoup(login_page.content, 'lxml')
    VIEWSTATE = soup.find('input', id='__VIEWSTATE')['value']
    EVENTVALIDATION = soup.find('input', id='__EVENTVALIDATION')['value']
    VIEWSTATEGENERATOR = soup.find('input', id="__VIEWSTATEGENERATOR")['value']
    PREVIOUSPAGE = soup.find('input', id='__PREVIOUSPAGE')['value']
    data['__VIEWSTATE'] = VIEWSTATE
    data['__EVENTVALIDATION'] = EVENTVALIDATION
    data['TextBox3'] = checkcode
    data['_VIEWSTATEGENERATOR'] = VIEWSTATEGENERATOR
    data['__PREVIOUSPAGE'] = PREVIOUSPAGE
    session.post(url, data=data, headers=headers)
    return session


def into_curriculum(session):  # 获取课程表
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/84.0.4147.89 Safari/537.36',
        'Referer': 'http://es.bnuz.edu.cn/xs_main.aspx?xh=12345678',
        'Host': 'es.bnuz.edu.cn'
    }
    url = 'http://es.bnuz.edu.cn/jwgl/xskbcx.aspx?xh=123456&xm=123456&gnmkdm=N121601'
    result = session.get(url, headers=headers)
    connection = result.content.decode('utf-8')
    soup = bs4.BeautifulSoup(connection, 'lxml')
    soup = soup.find(id='table1')
    soup = soup.findAll('li')
    return soup


def get_score(session, year, semester):  # 获取成绩单
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/84.0.4147.89 Safari/537.36',
        'Referer': 'http://es.bnuz.edu.cn/xs_main.aspx?xh=12345678',
        'Host': 'es.bnuz.edu.cn'
    }
    data = {
        "ScriptManager1": "upp1|Button1",
        "ScriptManager1_HiddenField:": ";;AjaxControlToolkit, Version=1.0.20229.20821, Culture=neutral, PublicKeyToken=28f01b0e84b6d53e:zh-CN:c5c982cc-4942-4683-9b48-c2c58277700f:e2e86ef9:1df13a87:af22e781",
        "__VIEWSTATE": "",
        "__VIEWSTATEGENERATOR": "",
        "__VIEWSTATEENCRYPTED": "",
        "ddlXN": "",
        "ddlXQ": "",
        "ccd_xn_ClientState": "",
        "ccd_xq_ClientState": "",
        "hiddenInputToUpdateATBuffer_CommonToolkitScripts": 1,
        "__ASYNCPOST": "true",
        "Button1": "按学期查询".encode("gb2312", "replace"),
    }
    url = 'http://es.bnuz.edu.cn/jwgl/xscjcx.aspx?xh=123456&xm=123456&gnmkdm=N121605'
    get_html = session.get('http://es.bnuz.edu.cn/jwgl/xscjcx.aspx?xh=123456&xm=123456&gnmkdm=N121605',
                           headers=headers).content
    soup = bs4.BeautifulSoup(get_html, 'lxml')
    data['__VIEWSTATE'] = soup.find('input', id='__VIEWSTATE')['value']
    data["__VIEWSTATEGENERATOR"] = soup.find('input', id='__VIEWSTATEGENERATOR')['value']
    data["ddlXN"] = (str(year) + "-" + str(year + 1))
    data["ddlXQ"] = semester
    data["ccd_xn_ClientState"] = (str(year) + "-" + str(year + 1)) + ":::" + (str(year) + "-" + str(year + 1))
    data["ccd_xq_ClientState"] = str(semester) + ":::" + str(semester)
    result = session.post(url, data, headers=headers)
    connection = result.content.decode('utf-8')
    html = bs4.BeautifulSoup(connection, 'lxml')
    html.find('tr')
    dataList = []
    for tag in html.findAll('td'):
        words = tag.getText()
        words = words.replace("\n", "")
        words = words.replace("\xa0", "")
        words = words.replace(" ", "")
        if words is not None:
            dataList.append(words)
    return dataList
