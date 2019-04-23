import json
import re
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from tqdm import tqdm

end_list = []
active_list = []
not_all_list = []
error_list = []


def set_up(url):
    ''' 得到连接url的webdriver
    '''

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')

    # driver = webdriver.Chrome(executable_path = '/Users/hqw/Desktop/qschou/chromedriver', chrome_options = chrome_options)
    driver = webdriver.Chrome(executable_path = 'chromedriver.exe', chrome_options = chrome_options)

    # driver.implicitly_wait(10) 
    driver.get(url)
    driver.get(url)
    # print ('get driver : %s ...' % url)
    return driver

def find_list(driver, tag):
    ''' 获取便签为tag的第一个元素，即捐助列表
    '''
    try:
        project_list = driver.find_element_by_tag_name(tag)
    except:
        print ('ERROR :  In fun:find_list, find %s error' % tag)
        exit()
    project_list = json.loads(project_list.text)['data']['project']
    driver.close()
    # print('close driver ...')
    return project_list

    # project_list = json.dumps(project_list, ensure_ascii=False, indent=2)
    # with open('/Users/hqw/Desktop/qschou/ret.json', 'w', encoding = 'utf-8') as f:
    #     f.write(project_list)
    
def simple_scroll(driver, n=10):
    ''' 简单的向下滑动n次
    '''
    time.sleep(1)
    length=600
    for i in range(0,n): 
        js="var q=document.documentElement.scrollTop="+str(length)  
        # js = 'window.scrollTo(0,document.body.scrollHeight)'
        driver.execute_script(js)  
        time.sleep(0.1) 
        length+=length 
    time.sleep(1)
    return driver

def _basic_info(driver, section, uuid):
    ''' 获取捐助项目基本信息
    '''
    ret = {'筹款ID': uuid, '标题': 'unkonwn', '筹款说明': 'unkonwn', '照片(数量)': 'unkonwn'}
    try:
        title = driver.find_element_by_class_name('fmargT').text.strip()
        ret['标题'] = title
    except:
        print ('ERROR : 获取标题错误！')

    try:
        intro = section.find_element_by_css_selector('.u-txt.J-project-intro').text
        ret['筹款说明'] = intro
    except:
        print ('ERROR : 获取筹款说明错误！')

    try:
        img = section.find_element_by_css_selector('.m-list.J-project-img-list')
        img_num = len(img.find_elements_by_tag_name('li'))
        ret['照片(数量)'] = img_num
    except:
        print ('ERROR : 获取照片(数量)错误！')

    return ret

def _zs_list(uuid, zs_num, last_num = 0):
    ''' 获取证实人列表
    '''
    ret = {'证实人列表': [], '证实人数量': zs_num}
    zs_url = 'https://m2.qschou.com/project/manage/prove_v7.html?uuid=' + uuid
    zs_driver = set_up(zs_url)
    # 向下滚动到底部
    time.sleep(3)
    length = 600
    iter_num, old_num = 0, 0
    while iter_num < 1000: 
        js = "var q=document.documentElement.scrollTop="+str(length)  
        zs_driver.execute_script(js)  
        time.sleep(0.1) 
        length += length 
        iter_num += 1
        if len(zs_driver.find_elements_by_class_name('detail')) >= int(zs_num) - last_num:
            break
        if iter_num % 100 == 0:
            if len(zs_driver.find_elements_by_class_name('detail')) == old_num:
                break
            old_num = len(zs_driver.find_elements_by_class_name('detail'))
    time.sleep(3)

    zs_list = zs_driver.find_element_by_id('cardList')
    zs_list = zs_list.find_elements_by_class_name('detail')

    for num in range(min(int(zs_num) - last_num,len(zs_list))):
        per = zs_list[num]
        love_point = per.find_element_by_class_name('love_point').text.strip()
        real_name = per.find_element_by_class_name('real_name').text.strip().split('\n')[0].strip()
        content = per.find_element_by_class_name('mycontent').text.strip()
        zs_time = per.find_element_by_class_name('myTime').text.strip()
        relation = per.find_element_by_class_name('relation').text.strip()
        verify = per.find_element_by_class_name('provIcon').text.strip()

        single_per = {'姓名': real_name, '爱心值': love_point, '内容': content, '关系': relation, '实名': verify, '时间': zs_time}
        ret['证实人列表'].append(single_per)
    zs_driver.close()
    return ret


def _money_list(driver):
    ''' 获取筹款结果
    '''

    des = ['急需筹款(元)', '已筹金额(元)', '帮助次数']
    ret = {'急需筹款(元)': 'unkonwn', '已筹金额(元)': 'unkonwn', '帮助次数': 'unkonwn'}
    try:
        moneylist = driver.find_element_by_class_name('moneylist')
    except:
        print ('ERROR : 获取筹款结果!')
        return ret
    for index, money in enumerate(moneylist.find_elements_by_tag_name('li')):
        if index > 2:
            break
        if money.text.startswith(des[index]):
            num = re.sub('\D', '', money.text)
            ret[des[index]] = num
    return ret

def _zl_list(section):
    ''' 获取资料证明
    '''
    ret = {'患者': {'姓名':'unkonwn', '审核': 'unknown'}, 
            '所患疾病': {'审核':'unknown', '疾病': 'unknown', '医院': 'unkonwn'}, 
            '收款人': {'姓名':'unknown', '关系': 'unknown'}
            }
    zl_main = section.find_elements_by_css_selector('.item.style10')
    last = None
    for zl in zl_main:
        info = zl.find_element_by_class_name('u-tit').text.strip()
        # print (info)
        if info.startswith('患者'):
            ret['患者']['姓名'] = info[3:]
            last = '患者'
        elif info.startswith('所患疾病'):
            ret['所患疾病']['疾病'] = info[5:]
            last = '所患疾病'
        elif info.startswith('收款'):
            tmp = info[4:].replace('（', '(').replace('）', ')')
            if '(' in tmp:
                ret['收款人']['姓名'] = tmp[:tmp.index('(')]
                ret['收款人']['关系'] = tmp[tmp.index('(') + 1: -1]
            else:
                ret['收款人']['姓名'] = tmp
                if tmp == ret['患者']['姓名']:
                    ret['收款人']['关系'] = '本人'
            last = '收款人'
        else:
            last = None
            
        other_info = zl.find_elements_by_class_name('u-smal-item')
        for info in other_info:
            info =  info.text.strip()
            if '审核' in info and last in ['患者', '所患疾病']:
                ret[last]['审核'] = info
            elif '医院' in info and last == '所患疾病':
                ret[last]['医院'] = info.replace('诊断医院：', '')

    zx_dict = {'家庭经济收入状况': {'年收入': 'unknown', '金融资产': 'unknown'},
                '家庭房屋财产状况': {'数量': 'unknown', '价值': 'unknown', '状态':'unknown'},
                '家庭车辆财产状况': {'数量': 'unknown', '价值': 'unknown', '状态':'unknown'},
                '保险状况': 'unknown'
                }
    zx_list = section.find_elements_by_class_name('u-memo')
    for zx in zx_list:
        title = zx.find_element_by_class_name('t1').text.strip()
        des_text = zx.find_element_by_class_name('ifont-green').text.strip()
        if title in zx_dict:
            if title == '保险状况':
                zx_dict[title] = des_text
            else:
                if des_text == '无':
                    for sx in zx_dict[title]:
                        zx_dict[title][sx] = '无'
                else:
                    des_text = des_text.split('/')
                    for single in des_text:
                        single = single.split(':')
                        if single[0].strip() in zx_dict[title]:
                            zx_dict[title][single[0].strip()] = single[1].strip()
    ret['增信补充说明'] = zx_dict

    # print (ret)

    return ret



def _fund_info(driver):
    ''' 获取筹款动态
    '''
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR,'.g-box7.news_publicity_tab.section.sectionT')) 
    )

    ret = {'筹款动态': []}
    dt_zj = driver.find_element_by_css_selector('.g-box7.news_publicity_tab.section.sectionT')
    # 筹款动态
    fund_news = dt_zj.find_element_by_id('fund_news')
    fund_news.click()
    comment_box = driver.find_element_by_class_name('comment-box')
    try:
        comment_box.find_element_by_id('all_news').click()
    except:
        pass
    comment_box = driver.find_element_by_class_name('comment-box')
    comment_list = comment_box.find_elements_by_css_selector('.citem.J-news-item')
    for comment in comment_list:
        c_name = comment.find_element_by_tag_name('h6').text.strip()
        c_text = comment.find_element_by_class_name('ctxt').text.strip()
        c_time = comment.find_element_by_class_name('citme').text.strip()
        single = {'姓名' : c_name, '文字': c_text, '时间': c_time}
        ret['筹款动态'].append(single)

    # 资金公示
    fund_public = dt_zj.find_element_by_id('fund_public')
    fund_public.click()
    time.sleep(0.1)
    dt_zj = driver.find_element_by_css_selector('.g-box7.news_publicity_tab.section.sectionT')
    comment_box = dt_zj.find_element_by_css_selector('.tab-pane.capital.active')
    text = comment_box.text.strip()
    ret['资金公示'] = text

    return ret


def _support_list(driver, num, last_num = 0):
    ''' 获取捐助者信息
    '''
    ret_list, ret = [], {}
    # 向下滑动，得到所有捐助者
    time.sleep(1)
    length=600
    iter_num, old_num = 0, 0
    while iter_num < 500: 
        js = "var q=document.documentElement.scrollTop="+str(length)  
        driver.execute_script(js)  
        time.sleep(0.1) 
        length += length 
        iter_num += 1
        if len(driver.find_elements_by_css_selector('.citem.J-support-item')) >= int(num)-last_num:
            break
        if iter_num % 25 == 0:
            if len(driver.find_elements_by_css_selector('.citem.J-support-item')) == old_num:
                break
            old_num = len(driver.find_elements_by_css_selector('.citem.J-support-item'))
    time.sleep(1)

    support_list = driver.find_elements_by_css_selector('.citem.J-support-item')
    print (num, iter_num, len(support_list))
    for index in range(min(int(num)-last_num,len(support_list))):
        support = support_list[index]
        s_love = 'unknown'
        s_text = ''
        try:
            s_love = support.find_element_by_class_name('phead').find_element_by_class_name('u-num').text.strip()
        except:  # 匿名用户 没有爱心值
            pass
        cominfo = support.find_element_by_class_name('cominfo')
        s_name = cominfo.find_element_by_class_name('first-line').find_element_by_class_name('left').text.strip()
        s_money = cominfo.find_elements_by_tag_name('small')[1].text.strip()
        try:
            s_text = cominfo.find_element_by_css_selector('.ctxt.message').text.strip()
        except:
            pass
        s_time = cominfo.find_element_by_class_name('citme').text.strip()
        single = {'爱心值' : s_love, '金额' : s_money, '姓名' : s_name, '时间': s_time, '文字': s_text}
        ret_list.append(single)

    ret['捐助者列表'] = ret_list
    ret['捐助者数量'] = num
    return ret


def get_single_info(project, zx_num, support_num):
    ''' 获取单个受捐助人的所有相关信息
    '''

    single_ret = {}

    uuid = project['uuid']
    assert project['template'] == 'love'
    # uuid = 'c3228d98-48d9-4e0b-b490-10ee956738cf'
    url = 'https://m2.qschou.com/project/love/love_v7.html?projuuid=' + uuid

    driver = set_up(url)
    driver = simple_scroll(driver)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME,'sectionT')) 
    )
   
    # 获取筹款结果
    money_list = _money_list(driver)
    single_ret['筹款结果'] = money_list

    # 筹款动态
    fund_info = _fund_info(driver)
    single_ret['筹款动态'] = fund_info
        
    section_list = driver.find_elements_by_css_selector('.section.sectionT')
    for section in section_list:
        try: 
            header = section.find_element_by_tag_name('header')
        except:
            continue
        if header.text == '筹款说明':
            # 基本信息
            basic_info = _basic_info(driver, section, uuid)
            single_ret['基本信息'] = basic_info
        elif header.text.startswith('已有'):
            # 证实人信息
            last_num = re.sub('\D', '', header.text)
            zs_list = _zs_list(uuid, last_num, zx_num)
            single_ret['证实人信息'] = zs_list
        elif header.text.startswith('资料证明'):   
            # 资料证明
            zl_list = _zl_list(section)    
            single_ret['资料证明'] = zl_list                                                                         
        elif header.text.endswith('人帮助过'):
            # 捐助人列表
            last_num = re.sub('\D', '', header.text)
            support_list = _support_list(driver, last_num, support_num)
            single_ret['捐助人信息'] = support_list  

    driver.close()
    return single_ret
    
def json_out(project_list, path):
    project_list = json.dumps(project_list, ensure_ascii=False, indent=2)
    with open(path, 'w', encoding = 'utf-8') as f:
        f.write(project_list)

def read_list(n = 2):
    project_list = []
    ret_json = 'https://gateway.qschou.com/v3.0.0/index/homepage'
    uuid_list = []
    for i in range(n):
        driver = set_up(ret_json)
        tmp_project_list = find_list(driver, 'pre')
        for project in tmp_project_list:
            if project['uuid'] not in uuid_list:
                uuid_list.append(project['uuid'])
                project_list.append(project)
    return project_list

def read_before(path = None):

    before_file = {}
    if path != None:
        with open(path, 'r', encoding='utf-8') as f:
            before_file = json.load(f)
    print ('before_file : len %d'%len(before_file))
    return before_file

def update(before_file, project_list, path_num):
    error_dict = {'error' : []}
    out = {}
    for index in tqdm(range(len(project_list))):
        project = project_list[index]
        uuid = project['uuid']
    
        zx_num, support_num = 0, 0
        if uuid in before_file:
            zx_num = int(before_file[uuid]['证实人信息']['证实人数量'])
            support_num = int(before_file[uuid]['捐助人列表']['捐助者数量'])
        
        try_cnt = 0
        for tmp_cnt in range(3):
            try:
                single_ret = get_single_info(project, zx_num, support_num)
                out[uuid] = single_ret
                try_cnt = 0
                break
            except:
                try_cnt += 1
                time.sleep(1)
        if try_cnt != 0:
            error_dict['error'].append(uuid)
            print ('fail %s' % uuid)
        
    # merge
    for uuid in out:
        if uuid in before_file:
            zs_list = before_file[uuid]['证实人信息']['证实人列表'].copy()
            support_list = before_file[uuid]['捐助者信息']['捐助人列表'].copy()
            before_file[uuid] = out[uuid]
            before_file[uuid]['证实人信息']['证实人列表'] += zs_list 
            before_file[uuid]['捐助者信息']['捐助人列表'] += support_list
        else:
            before_file[uuid] = out[uuid]
    

    json_out(before_file, os.path.join(str(path_num),'before_file.json'))
    json_out(error_dict, os.path.join(str(path_num),'error_dict.json'))




if __name__ == "__main__":


    for i in range(100):
        if not os.path.exists(str(i)):
            os.mkdir(str(i))
        project_list = read_list()
        path = None
        if i > 0:
            path = os.path.join(str(i-1), 'before_file.json')
        before_file = read_before(path)
        update(before_file, project_list, path_num = i)



    # qschou = 'https://m2.qschou.com/index_v7_3.html'
    # ret_json = 'https://gateway.qschou.com/v3.0.0/index/homepage'

    # for i in tqdm(range(100)):
    #     driver = set_up(ret_json)
    #     project_list = find_list(driver, 'pre')
    #     out = {}
    #     for index, project in enumerate(project_list):
    #         print (index, len(project_list), project['uuid'])
    #         try_cnt = 0
    #         for i in range(3):  # 每个网址最多尝试3次
    #             try:
    #                 single_ret = get_single_info(project)
    #                 out[project['uuid']] = single_ret
    #                 try_cnt = 0
    #                 break
    #             except:
    #                 try_cnt += 1
    #                 time.sleep(1)
    #         if try_cnt != 0:
    #             error_list.append(project['uuid'])
    #             print ('fail %s' % project['uuid'])


    #     json_out(out, '/Users/hqw/Desktop/qschou/test.json')
    # with open('/Users/hqw/Desktop/qschou/error.txt', 'w', encoding = 'utf-8') as f:
    #     for s in error_list:
    #         f.write(s + '\n')
