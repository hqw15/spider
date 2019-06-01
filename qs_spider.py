import json
import time
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
# from standard import AttrValue



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


def get_para():
	
	in_dir = ''
	space = 3600
	try:
		opts, args = getopt.getopt(sys.argv[1:],"i:s:",["in_dir=","space="])
	except getopt.GetoptError:
		print ('*.py -i <in_dir> -s <space>(optional)')
		sys.exit(2)
	for opt, arg in opts:
		if opt in ("-i", "--in_dir"):
			in_dir = arg
		elif opt in ("-s", "--space"):
			space = int(arg)
	return in_dir, space

	
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
	'''	打开一个网页
	'''
	
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
			time.sleep(60)
			#print ('waiting...')
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
	
def getList():
	'''	获取首页项目
	'''

	url = 'https://gateway.qschou.com/v3.0.0/index/homepage'
	res = _open_url(url)
	res = res.decode(encoding='utf-8')
	res = json.loads(res)
	
	return res['data']['recommend'] + res['data']['project']
	

def getIntro(uuid, is_new = True, old_dict = None):

	# 筹款说明
	text_url = 'https://text.qschou.com/'+uuid+'.html'
	res = _open_url(text_url)
	intro = res.decode(encoding='utf-8')
	
	# 项目筹款 + 照片 + 标题 + 分享 + 时间 + 征信说明
	url = 'https://gateway.qschou.com/v3.0.0/project/index/text/' + uuid
	res = _open_url(url)
	res = res.decode(encoding='utf-8')
	res = json.loads(res)['data']
	
	ret = {'text': intro, 
			'target_amount': res['project']['target_amount'],
			'raised_amount': res['project']['raised_amount'],
			'cover_num': len(res['project']['cover']),
			'title': res['project']['name'],
			'support_number': res['project']['support_number'],
			'share_number': res['project']['share_number'],
			'created' : time.strftime("%Y-%m-%d (%H:%M:%S)", time.localtime(int(res['project']['created']))),
			'server_time': time.strftime("%Y-%m-%d (%H:%M:%S)", time.localtime(int(res['project']['server_time']))),
			'stopped' : res['project']['stopped'], 
			'raise_days': res['project']['raise_days'], 
			'property' : res['property']
	}

	url = 'https://gateway.qschou.com/v3.0.0/project/index/auth2/' + uuid
	res = _open_url(url)
	res = res.decode(encoding='utf-8')
	res = json.loads(res)['data']

	over_timestamp = int(res['over_timestamp'])
	if over_timestamp > 0:
		ret['stopped_time']  = time.strftime("%Y-%m-%d (%H:%M:%S)", time.localtime(over_timestamp))
	else:
		ret['stopped_time']  = ''
			
	return ret
	
def getProve(uuid, is_new = True, old_dict = None):
	
	# 证实人数量 + 患者 + 疾病 + 医院 + 。。。
	
	url = 'https://gateway.qschou.com/v3.0.0/project/index/newverify/' + uuid
	res = _open_url(url)
	res = res.decode(encoding='utf-8')
	res = json.loads(res)['data']
	
	patient, patient_icons, disease, disease_icons, hospital, recipient, recipient_icon = '','','','','','',''
	
	for item in res['verify_item']:
		if item['title'].startswith('患者'):
			patient = item['title'].replace(':', '：').split('：')[1].strip()
			if 'icons' in item:
				for single in item['icons']:
					patient_icons += (single + "/")
				patient_icons = patient_icons[:-1]
		elif item['title'].startswith('所患疾病'):
			disease = item['title'].replace(':', '：').split('：')[1].strip()
			if 'icons' in item:
				for single in item['icons']:
					single = single.replace(':', '：').strip()
					if '诊断证明已审核' == single:
						disease_icons = single
					elif single.startswith('诊断医院：'):
						hospital = single.replace('诊断医院：', '').strip()
		elif item['title'].startswith('收款'):
			recipient = item['title'].replace(':', '：').split('：')[1].strip()
			if '(' in recipient and ')' in recipient:
				recipient_icon = recipient[recipient.index('(') + 1 : -1]
				recipient = recipient[: recipient.index('(')]
	
	ret = {'patient' : patient,
			'patient_icons' : patient_icons,
			'disease' : disease,
			'disease_icons' : disease_icons,
			'hospital' : hospital,
			'recipient' : recipient,
			'recipient_icon' : recipient_icon,
	}
	
	next = ''
	prove_list = []
	last_id = ''
	if not is_new and len(old_dict['prove']['prove_list']) > 0:
		last_id = old_dict['prove']['prove_list'][0]['id']
	
	max_try, total = 1000, 1000000
	while max_try > 0:
		max_try -= 1
		url = 'https://gateway.qschou.com/v3.0.0/project/prove/'+ uuid + '?next=' + next
		res = _open_url(url)
		res = res.decode(encoding='utf-8')
		res = json.loads(res)
		
		next = res['next']
		if max_try == 999:
			total = int(res['data']['total'])
		data = res['data']['list']
		is_end, end_index = False, 0
		for s in data:
			if s['id'] == last_id:
				is_end = True
				break
			end_index += 1
		prove_list += data[:end_index]
		if is_end or len(prove_list) >= total or next == '':
			break
	if not is_new:
		ret['prove_list'] = prove_list + old_dict['prove']['prove_list']
	else:
		ret['prove_list'] = prove_list 
	return ret


	
def feed(uuid, is_new = True, old_dict = None):
	'''	动态 资金公示
	'''
	
	ret = {'news': [], 'funds': []}
	url = 'https://gateway.qschou.com/v3.0.0/feed/project?uuid=' + uuid 
	res = _open_url(url)
	res = res.decode(encoding='utf-8')
	res = json.loads(res)
	ret['news'] = res['data']
	
	url = 'https://gateway.qschou.com/v3.0.0/feed/publicity/funds/' + uuid 
	res = _open_url(url)
	res = res.decode(encoding='utf-8')
	res = json.loads(res)
	ret['funds'] = res['data']

	return ret
	
	
def getSupport(uuid, is_new = True, old_dict = None):
	'''	捐助信息
	'''

	last_id = ''
	if not is_new and len(old_dict['support']) > 0:
		last_id = old_dict['support'][0]['id']

	next = {'next': ''}
	support_list = []
	max_try = 10000
	while max_try > 0:
		max_try -= 1
		url = 'https://gateway.qschou.com/v3.0.0/support/support/' + uuid
		res = _open_url(url,use_post = True, data = next)
		res = res.decode(encoding='utf-8')
		res = json.loads(res)
		next['next'] = res['next']
		data = res['data']
		is_end, end_index = False, 0
		for s in data:
			if s['id'] == last_id:
				is_end = True
				break
			end_index += 1
		support_list += data[:end_index]
		if next['next'] == '' or is_end:
			break
	if not is_new:
		return support_list + old_dict['support']
	else:
		return support_list
	
def update(uuid, is_new = True, old_dict = None, max_try = 3):
	
	while max_try > 0:
		max_try -= 1
		try:
			ret = {}
			ret['intro'] = getIntro(uuid, is_new, old_dict)
			ret['prove'] = getProve(uuid, is_new, old_dict)
			ret['support'] = getSupport(uuid, is_new, old_dict)
			ret['feed'] = feed(uuid, is_new, old_dict)
			return True, ret
		except:
			time.sleep(60)
	return False, None
	
	
def out_single_json(data, path):

	data = json.dumps(data, ensure_ascii=False, indent=2)
	with open(path, 'w', encoding = 'utf-8') as f:
		f.write(data)
	
def get_before_list(root_dir):
	
	befor_list = []
	for root, dirs, files in os.walk(root_dir):
		for name in files:
			tmp = {}
			with open(os.path.join(root, name), 'r', encoding = 'utf-8') as f:
				tmp = json.load(f)
			for uuid in tmp:
				befor_list.append(uuid)
	return befor_list
		
if __name__ == "__main__":


	s = time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime(time.time()))
	
	in_dir, space = get_para()
	iter_cnt = 0
	while True:
		print ('============<<<' + str(iter_cnt) + '>>>============')
		# attrValue = AttrValue(fdir = 'project')
		iter_cnt += 1
		new_list = []
		old_list = []
		befor_list = get_before_list(in_dir)
		start_time = time.time()
		IP_LIST = get_ip()
		print (len(befor_list))
		print (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' : collect new project ...')
		while True:
			end_time = time.time()
			if end_time - start_time > space or len(new_list) > 50:
				break
			project_list = getList()
			for project in project_list:
				uuid = project['uuid']
				if project['template'] == 'love' and uuid not in befor_list and uuid not in new_list:
					new_list.append(uuid)
				if project['template'] == 'love' and uuid in befor_list :
					old_list.append(uuid)
			time.sleep(0)
		print (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' : add new project ...(' + str(len(new_list)) + ')')


		output = time.strftime("%Y-%m-%d(%H-%M-%S)", time.localtime(time.time()))
		if not os.path.exists(output):
			os.mkdir(output)
		# 添加新的project
		out, out_index = {}, 0
		for index, uuid in  enumerate(new_list):
			succ, tmp = update(uuid)
			if succ:
				now_time = time.strftime("%Y-%m-%d(%H-%M-%S)", time.localtime(time.time()))
				for attr in tmp['intro']:
					tmp['intro'][attr] = {now_time: tmp['intro'][attr], 'new': tmp['intro'][attr]}
				for attr in tmp['prove']:
					if attr != 'prove_list':
						tmp['prove'][attr] = {now_time: tmp['prove'][attr], 'new' : tmp['prove'][attr]}
				out[uuid] = tmp 
				out[uuid]['sy'] = {now_time : 1 }
			else:
				print ('fail : add new project  %s' % uuid)
			if index != 0 and index % 10 == 0:
				out_single_json(out, os.path.join(output, 'add_' + str(out_index) + '.json'))
				out = {}
				out_index += 1
		if len(out) > 0:
			out_single_json(out, os.path.join(output, 'add_' + str(out_index) + '.json'))
		out_index = 0
		out = {}
		
		# 更新已有project
		print (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' : update old project ...')
		for root, dirs, files in os.walk(in_dir):
			for name in files:
				tmp = {}
				out = {}
				#print (name)
				with open(os.path.join(root, name), 'r', encoding = 'utf-8') as f:
					tmp = json.load(f)
				for uuid in tmp:
					now_time = time.strftime("%Y-%m-%d(%H-%M-%S)", time.localtime(time.time()))
					succ, tmp_dict = update(uuid, is_new = False, old_dict = tmp[uuid])
					if succ:
						out[uuid] = tmp_dict
						out[uuid]['sy'] = tmp[uuid]['sy'].copy()
						for attr in tmp_dict['intro']:
							if tmp_dict['intro'][attr] == tmp[uuid]['intro'][attr]['new']:
								tmp_dict['intro'][attr] = tmp[uuid]['intro'][attr].copy()
								tmp_dict['intro'][attr][now_time] = ''
							else:
								value = tmp_dict['intro'][attr].copy()
								tmp_dict['intro'][attr] = tmp[uuid]['intro'][attr].copy()
								tmp_dict['intro'][attr][now_time] = value
								tmp_dict['intro'][attr]['new'] = value

						for attr in tmp_dict['prove']:
							if attr != 'prove_list':
								is_same = False
								if (type(tmp_dict['prove'][attr]).__name__=='dict'):
									if (type(tmp[uuid]['prove'][attr]['new']).__name__=='dict'):
										if cmp(tmp_dict['prove'][attr], tmp[uuid]['prove'][attr]['new']) == 0:
											tmp_dict['prove'][attr] = tmp[uuid]['prove'][attr].copy()
											tmp_dict['prove'][attr][now_time] = ''
											is_same = True
								else:
									if tmp_dict['prove'][attr] == tmp[uuid]['prove'][attr]['new']:
										tmp_dict['prove'][attr] = tmp[uuid]['prove'][attr].copy()
											tmp_dict['prove'][attr][now_time] = ''
											is_same = True
								if not same:
									value = tmp_dict['prove'][attr].copy()
									tmp_dict['prove'][attr] = tmp[uuid]['prove'][attr].copy()
									tmp_dict['prove'][attr][now_time] = value
									tmp_dict['prove'][attr]['new'] = value
								
					else:
						out[uuid] = tmp[uuid]
						print ('update fail... %s' % uuid)
					
					if uuid in old_list:
						out[uuid]['sy'][now_time] = 1
					else:
						out[uuid]['sy'][now_time] = 0

				out_single_json(out, os.path.join(output, str(out_index) + '.json'))
				out_index += 1
		
		shutil.rmtree(in_dir)

		in_dir = output
				
		break
				
				
				
		
			
	