import csv
import json
import time
import json
import os
import datetime
import random
import bs4
import requests
import re
import sys
import getopt
import os
import datetime
import shutil
from urllib import request


USER_AGENTS = [
	"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",    
	"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",    
	"Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",    
	"Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",   
	"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",    
	"Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",    
	"Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",    
	"Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",    
	"Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",    
	"Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",    
	"Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",    
	"Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",    
	"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",    
	"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",    
	"Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
	]
IP_LIST = []


	
def get_ip():

	"""获取代理IP"""
	url = "http://www.xicidaili.com/nn"
	headers = { "Accept":"text/html,application/xhtml+xml,application/xml;",
				"Accept-Encoding":"gzip, deflate, sdch",
				"Accept-Language":"zh-CN,zh;q=0.8,en;q=0.6",
				"Referer":"http://www.xicidaili.com",
				"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"
				}

	r = requests.get(url,headers=headers)
	soup = bs4.BeautifulSoup(r.text, 'html.parser')
	data = soup.table.find_all("td")
	ip_compile= re.compile(r'<td>(\d+\.\d+\.\d+\.\d+)</td>')    # 匹配IP
	port_compile = re.compile(r'<td>(\d+)</td>')                # 匹配端口
	ip = re.findall(ip_compile,str(data))       # 获取所有IP
	port = re.findall(port_compile,str(data))   # 获取所有端口
	return [":".join(i) for i in zip(ip,port)]  # 组合IP+端口，如：115.112.88.23:8080


def _open_url(url, max_try = 3,use_post = False, data = None):
	
	while max_try > 0:
		try:
			proxy = random.choice(IP_LIST)
			# 使用选择的代理构建代理处理器对象
			httpproxy_handler = request.ProxyHandler({'http': proxy})
			opener = request.build_opener(httpproxy_handler)
			if use_post:
				req = request.Request(url, data = json.dumps(data).encode(encoding='utf-8'), headers={ 'User-Agent': random.choice(USER_AGENTS), "Content-Type": "application/json"})
			else:
				req = request.Request(url, headers={ 'User-Agent': random.choice(USER_AGENTS), "Content-Type": "application/json"})
			res = opener.open(req)
			res = res.read()
			#print ('proxy', proxy)
			return res
		except:
			max_try -= 1
			time.sleep(0)
			print ('waiting...')
	# 不换ip
	httpproxy_handler = request.ProxyHandler({})
	opener = request.build_opener(httpproxy_handler)
	if use_post:
		req = request.Request(url, data = json.dumps(data).encode(encoding='utf-8'), headers={ 'User-Agent': random.choice(USER_AGENTS), "Content-Type": "application/json"})
	else:
		req = request.Request(url, headers={ 'User-Agent': random.choice(USER_AGENTS), "Content-Type": "application/json"})
	res = opener.open(req)
	res = res.read()
	return res

def _get_dict(root_dir):
	
	cnt = 0
	ret = {}
	for root, dirs, files in os.walk(root_dir):
		for name in files:
			tmp = {}
			with open(os.path.join(root, name), 'r', encoding = 'utf-8') as f:
				tmp = json.load(f)
			cnt += len(tmp)
			ret.update(tmp)
	print ('function get_dict : ',cnt, len(ret))
	return ret



def toCsv(in_path, out_path, syList):

	out = open('baseInfo_'+out_path,'w', newline='', encoding='utf-8-sig')
	info_write = csv.writer(out,dialect='excel')
	out = open('news_'+out_path,'w', newline='', encoding='utf-8-sig')
	news_write = csv.writer(out,dialect='excel')
	out = open('support_'+out_path,'w', newline='', encoding='utf-8-sig')
	support_write = csv.writer(out,dialect='excel')
	out = open('prove_'+out_path,'w', newline='', encoding='utf-8-sig')
	prove_write = csv.writer(out,dialect='excel')
	
	# 基本信息
	firstLine = [
		'是否在首页',
		'链接',
		'筹款ID',
		'患者姓名',
		'患者身份证明是否审核',
		'所患疾病',
		'医院',
		'诊断关系是否审核',
		'收款人姓名',
		'收款人关系',
		'标题',
		'筹款说明',
		'照片数量',
		'项目发起时间',
		'项目拟筹款天数',
		'项目截至时间',
		'已筹金额(元)',
		'目标金额(元)',
		'帮助次数',
		'转发次数',
		'资金公示',
		'时间',
		'公示文字',
		'保险状况',
		'是否有商业保险',
		'是否有医保',
		'是否有低保',
		'是否有政府补助',
		'金融资产（万）',
		'年收入（万）',
		'家庭车辆财产状况',
		'数量',
		'价值（万）',
		'家庭房屋财产状况',
		'数量',
		'价值（万）'
	]
	info_write.writerow(firstLine)
	
	# 证实人列表
	firstLine = [
		'筹款ID',
		'姓名',
		'是否实名',
		'内容',
		'时间',
		'关系',
		'爱心值'
	]
	prove_write.writerow(firstLine)
	
	# 捐助列表
	firstLine = [
		'筹款ID',
		'姓名',
		'内容',
		'时间',
		'金额',
		'爱心值'
	]
	support_write.writerow(firstLine)
	
	# 筹款动态
	firstLine = [
		'筹款ID',
		'更新人',
		'内容',
		'时间'
	]
	news_write.writerow(firstLine)
	
	
	need_out = _get_dict(in_path)
	for uuid in need_out:
		# print (uuid)
		intro = need_out[uuid]['intro']
		prove = need_out[uuid]['prove']
		support = need_out[uuid]['support']
		feed = need_out[uuid]['feed']
		
		
		# 保险状况
		no_insurance, insurance, social_security, low_security, gov_assistance = '无','无','无','无','无'
		try:
			no_insurance = '无' if intro['property']['no_insurance'] else '有'
		except:
			pass
		try:
			insurance = '有' if intro['property']['insurance'] else '无'
		except:
			pass
		try:
			social_security = '有' if intro['property']['social_security'] else '无'
		except:
			pass
		try:
			low_security = '有' if intro['property']['low_security'] else '无'
		except:
			pass
		try:
			gov_assistance = '有' if intro['property']['gov_assistance'] else '无'
		except:
			pass
		if insurance == '无' and social_security == '无' and low_security == '无' and gov_assistance == '无':
			if no_insurance == '有':
				print ('error, no_insurance state!')
		else:
			if no_insurance == '无':
				print ('error, no_insurance state!')
			
			
		
		# 资金公示
		gs_text, gs, gs_time = '', '未提款', ''
		if len(feed['funds']) != 0:
			if len(feed['funds']) != 1:
				print ('warning  资金公示')
			for ss in feed['funds'][0]['content']:
				for s in ss:
					gs_text += s['text']
			gs_time = time.strftime("%Y-%m-%d (%H:%M:%S)", time.localtime(int(feed['funds'][0]['created'])))
			if feed['funds'][0]['title'][0]['text'].strip() == '提现成功':
				gs = '提现成功'
			
		#########################
		# 增信说明
		#  总资产
		total_assets = 'unknown'
		try:
			intro['property']['household_income']['total_assets']
		except:
			pass
		#  年收入
		annual_income = 'unknown'
		try:
			annual_income = intro['property']['household_income']['annual_income']
		except:
			pass
		#   车辆信息
		car_numb, car_worth, car_status = '0', '', ''
		try:
			car_numb = intro['property']['car']['numb']
		except:
			pass
		try:
			if car_numb != '0':
				car_worth = intro['property']['car']['worth']
		except:
			pass
		try:
			if car_numb != '0':
				if intro['property']['car']['status'] == '0':
					car_status = '未变卖'
				elif intro['property']['car']['status'] == '1':
					car_status = '变卖中'
				else:
					car_status = '已变卖'
		except:
			pass
		#  房屋信息
		houses_numb, houses_worth, houses_status = '0', '',''
		try:
			houses_numb = intro['property']['houses']['numb']
		except:
			pass
		try:
			if houses_numb != '0':
				houses_worth = intro['property']['houses']['worth']
		except:
			pass
		try:
			if houses_numb != '0':
				if intro['property']['houses']['status'] == '0':
					houses_status = '未变卖'
				elif intro['property']['houses']['status'] == '1':
					houses_status = '变卖中'
				else:
					houses_status = '已变卖'
		except:
			pass
		
		
		line = [
			0 if uuid not in syList else 1,
			'https://m2.qschou.com/project/love/love_v7.html?projuuid=' + uuid,
			uuid,
			prove['patient'],
			prove['patient_icons'],
			prove['disease'],
			prove['hospital'],
			prove['disease_icons'],
			prove['recipient'],
			prove['recipient_icon'],
			intro['title'],
			"“" + intro['text']  + '”',
			intro['cover_num'],
			intro['created'],
			intro['raise_days'],
			intro['stopped_time'],
			intro['raised_amount'],
			intro['target_amount'],
			intro['support_number'],
			intro['share_number'],
			gs,
			gs_time,
			gs_text,
			no_insurance,
			insurance,
			social_security,
			low_security,
			gov_assistance,
			total_assets,
			annual_income,
			car_status,
			car_numb,
			car_worth,
			houses_status,
			houses_numb,
			houses_worth
		]
		info_write.writerow(line)
		
		
		for single in prove['prove_list']:
			line = [
				uuid, 
				single['real_name'],
				'已实名' if len(single['real_name']) > 0 else '未实名',
				"“" + single['content']  + '”',
				time.strftime("%Y-%m-%d (%H:%M:%S)", time.localtime(int(single['created']))),
				single['relation'],
				single['love_point']
			]
			prove_write.writerow(line)
	
		for single in support:
			line = [
				uuid,
				single['user']['nickname'],
				"“" + single['message'] + '”',
				time.strftime("%Y-%m-%d (%H:%M:%S)", time.localtime(int(single['created']))),
				single['title'][1]['text'],
				single['love_point']
			]
			support_write.writerow(line)
			
	
		for single in feed['news']:
			text = ''
			for ss in single['content']:
				for s in ss:
					text += s['text']
			line = [
				uuid,
				single['user']['nickname'],
				"“" + text + '”',
				time.strftime("%Y-%m-%d (%H:%M:%S)", time.localtime(int(single['created']))),
			]
			news_write.writerow(line)
	print ("write over")
	
def getList():

	url = 'https://gateway.qschou.com/v3.0.0/index/homepage'
	res = _open_url(url)
	res = res.decode(encoding='utf-8')
	res = json.loads(res)
	
	return res['data']['recommend'] + res['data']['project']
	
	
if __name__ == "__main__":

	IP_LIST = get_ip()

	project_list = getList()
	syList = []
	for project in project_list:
		uuid = project['uuid']
		syList.append(uuid)

	print (len(syList))

	print('ccc')


	in_path = 'spider/2019-06-05(06-30-25)'
	out_path = '.csv'
	toCsv(in_path, out_path, syList)
