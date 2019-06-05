import csv
import json
import time
import json
import os
import datetime


class parser:

	def __init__(self, uuid, data):

		self.uuid = uuid
		self.data = data

		self.support_list = data['support']
		self.prove = data['prove']
		self.feed = data['feed']
		self.intro = data['intro']

	def __support(self):
		toCsv = []
		for support in self.support_list:
			single = {
				'support_money': support['title'][1]['text'],
				'added_love_point' : support['added_love_point'],
				'created' : time.strftime("%Y-%m-%d (%H:%M:%S)", time.localtime(int(support['created']))),
				'message' : support['message'],
				'user_uuid' : support['user']['uuid'],
				'user_name' : support['user']['nickname'],
				'love_point' : support['love_point'],
			}
			toCsv.append(single)
		return toCsv

	def __prove_list(self):
		toCsv = []
		for prover in self.prove['prove_list']:
			single = {
				'content' : prover['content'],
				'created' : time.strftime("%Y-%m-%d (%H:%M:%S)", time.localtime(int(prover['created']))),
				'relation' : prover['relation'],
				'name' : prover['real_name'],
				'love_point' : prover['love_point'],
				'real_name' : '已实名' if len(prover['real_name']) > 0 else '未实名',
			}
			toCsv.append(single)
		return toCsv

	def __funds(self):
		toCsv = []
		for fund in self.feed['funds']:
			single = {
				'title' : fund['title'][0]['text'],
				'created' : time.strftime("%Y-%m-%d (%H:%M:%S)", time.localtime(int(fund['created']))),
				'content' : fund['content'][0][0]['text'],
				'user_uuid' : fund['user']['uuid'],
				'user_name' : fund['user']['nickname'],
			}
			toCsv.append(single)
		return toCsv
	
	def __news(self):
		toCsv = []
		for news in self.feed['news']:
			single = {
				'title' : news['title'][0]['text'],
				'created' : time.strftime("%Y-%m-%d (%H:%M:%S)", time.localtime(int(news['created']))),
				'content' : news['content'][0][0]['text'],
				'user_uuid' : news['user']['uuid'],
				'user_name' : news['user']['nickname']
			}
			toCsv.append(single)
		return toCsv

	def __info(self):
		toCsv = []
		tmp = {
			'sy' : self.__tochange(self.data['sy']),
			'support_number' : self.__tochange(self.intro['support_number']),
			'stopped_time' : self.__tochange(self.intro['stopped_time']),
			'text' : self.__tochange(self.intro['text']),
			'title' : self.__tochange(self.intro['title']),
			'created' : self.__tochange(self.intro['created']),
			'raise_days' : self.__tochange(self.intro['raise_days']),
			'property' : self.__tochange(self.intro['property']),
			'share_number' : self.__tochange(self.intro['share_number']),
			'raised_amount' : self.__tochange(self.intro['raised_amount']),
			'target_amount' : self.__tochange(self.intro['target_amount']),
			'cover_num' : self.__tochange(self.intro['cover_num']),
			'hospital' : self.__tochange(self.prove['hospital']),
			'recipient' : self.__tochange(self.prove['recipient']),
			'patient' : self.__tochange(self.prove['patient']),
			'disease' : self.__tochange(self.prove['disease']),
			'patient_icons' : self.__tochange(self.prove['patient_icons']),
			'recipient_icon' : self.__tochange(self.prove['recipient_icon']),
			'disease_icons' : self.__tochange(self.prove['disease_icons']),
		}
		num_ = len(tmp['sy'])
		for sx in tmp:
			if len(tmp[sx]) != num_:
				print ('[error]  ',  sx)
		tmp_time = []
		for iter_ in range(num_):
			single = {'time' : tmp['sy'][iter_][0]}
			print (tmp['sy'][iter_][0])
			for sx in tmp:
				single[sx] = tmp[sx][iter_][1]
			toCsv.append(single)

		return toCsv

	def __tochange(self, data):
		ret = {}
		for key_time in data:
			if key_time != 'new':
				time_ = int(time.mktime(time.strptime(key_time,'%Y-%m-%d(%H-%M-%S)')))
				ret[time_] = [key_time, data[key_time]]
		ret = sorted(ret.items(), key=lambda ret:ret[0],reverse = False)
		newData = []
		value = ret[0][1][1]
		for single in ret:
			time_, value_ = single[1][0], single[1][1]
			if value_ == '':
				value_ = value
			else:
				value = value_
			newData.append([time_.replace('(', " ("), value_])
		return newData

	def main(self):

		support = self.__support()
		prove_list = self.__prove_list()
		funds = self.__funds()
		news = self.__news()
		info = self.__info()
		
		return support, prove_list, funds, news, info


	
if __name__ == "__main__":

	tmp = {}
	with open('../3.json', 'r', encoding = 'utf-8') as f:
		tmp = json.load(f)
	for uid in tmp:
		s = parser(uid, tmp[uid])
		s.main()

		# break



# def _get_dict(root_dir):
	
# 	cnt = 0
# 	ret = {}
# 	for root, dirs, files in os.walk(root_dir):
# 		for name in files:
# 			tmp = {}
# 			with open(os.path.join(root, name), 'r', encoding = 'utf-8') as f:
# 				tmp = json.load(f)
# 			cnt += len(tmp)
# 			ret.update(tmp)
# 	print ('function get_dict : ',cnt, len(ret))
# 	return ret



# def toCsv(in_path, out_path):

# 	out = open('baseInfo_'+out_path,'w', newline='', encoding='utf-8-sig')
# 	info_write = csv.writer(out,dialect='excel')
# 	out = open('news_'+out_path,'w', newline='', encoding='utf-8-sig')
# 	news_write = csv.writer(out,dialect='excel')
# 	out = open('support_'+out_path,'w', newline='', encoding='utf-8-sig')
# 	support_write = csv.writer(out,dialect='excel')
# 	out = open('prove_'+out_path,'w', newline='', encoding='utf-8-sig')
# 	prove_write = csv.writer(out,dialect='excel')
	
# 	# 基本信息
# 	firstLine = [
# 		'是否在首页',
# 		'链接',
# 		'筹款ID',
# 		'患者姓名',
# 		'患者身份证明是否审核',
# 		'所患疾病',
# 		'医院',
# 		'诊断关系是否审核',
# 		'收款人姓名',
# 		'收款人关系',
# 		'标题',
# 		'筹款说明',
# 		'照片数量',
# 		'项目发起时间',
# 		'项目拟筹款天数',
# 		'已筹金额(元)',
# 		'目标金额(元)',
# 		'帮助次数',
# 		'转发次数',
# 		'资金公示',
# 		'时间',
# 		'公示文字',
# 		'保险状况',
# 		'是否有商业保险',
# 		'是否有医保',
# 		'是否有低保',
# 		'是否有政府补助',
# 		'金融资产（万）',
# 		'年收入（万）',
# 		'家庭车辆财产状况',
# 		'数量',
# 		'价值（万）',
# 		'家庭房屋财产状况',
# 		'数量',
# 		'价值（万）'
# 	]
# 	info_write.writerow(firstLine)
	
# 	# 证实人列表
# 	firstLine = [
# 		'筹款ID',
# 		'姓名',
# 		'是否实名',
# 		'内容',
# 		'时间',
# 		'关系',
# 		'爱心值'
# 	]
# 	prove_write.writerow(firstLine)
	
# 	# 捐助列表
# 	firstLine = [
# 		'筹款ID',
# 		'姓名',
# 		'内容',
# 		'时间',
# 		'金额',
# 		'爱心值'
# 	]
# 	support_write.writerow(firstLine)
	
# 	# 筹款动态
# 	firstLine = [
# 		'筹款ID',
# 		'更新人',
# 		'内容',
# 		'时间'
# 	]
# 	news_write.writerow(firstLine)
	
	
# 	need_out = _get_dict(in_path)
# 	for uuid in need_out:
# 		print (uuid)
# 		intro = need_out[uuid]['intro']
# 		prove = need_out[uuid]['prove']
# 		support = need_out[uuid]['support']
# 		feed = need_out[uuid]['feed']
		
		
# 		# 保险状况
# 		no_insurance, insurance, social_security, low_security, gov_assistance = '无','无','无','无','无'
# 		try:
# 			no_insurance = '无' if intro['property']['no_insurance'] else '有'
# 		except:
# 			pass
# 		try:
# 			insurance = '有' if intro['property']['insurance'] else '无'
# 		except:
# 			pass
# 		try:
# 			social_security = '有' if intro['property']['social_security'] else '无'
# 		except:
# 			pass
# 		try:
# 			low_security = '有' if intro['property']['low_security'] else '无'
# 		except:
# 			pass
# 		try:
# 			gov_assistance = '有' if intro['property']['gov_assistance'] else '无'
# 		except:
# 			pass
# 		if insurance == '无' and social_security == '无' and low_security == '无' and gov_assistance == '无':
# 			if no_insurance == '有':
# 				print ('error, no_insurance state!')
# 		else:
# 			if no_insurance == '无':
# 				print ('error, no_insurance state!')
			
			
		
# 		# 资金公示
# 		gs_text, gs, gs_time = '', '未提款', ''
# 		if len(feed['funds']) != 0:
# 			if len(feed['funds']) != 1:
# 				print ('warning  资金公示')
# 			for ss in feed['funds'][0]['content']:
# 				for s in ss:
# 					gs_text += s['text']
# 			gs_time = time.strftime("%Y-%m-%d (%H:%M:%S)", time.localtime(int(feed['funds'][0]['created'])))
# 			if feed['funds'][0]['title'][0]['text'].strip() == '提现成功':
# 				gs = '提现成功'
			
# 		#########################
# 		# 增信说明
# 		#  总资产
# 		total_assets = 'unknown'
# 		try:
# 			intro['property']['household_income']['total_assets']
# 		except:
# 			pass
# 		#  年收入
# 		annual_income = 'unknown'
# 		try:
# 			annual_income = intro['property']['household_income']['annual_income']
# 		except:
# 			pass
# 		#   车辆信息
# 		car_numb, car_worth, car_status = '0', '', ''
# 		try:
# 			car_numb = intro['property']['car']['numb']
# 		except:
# 			pass
# 		try:
# 			if car_numb != '0':
# 				car_worth = intro['property']['car']['worth']
# 		except:
# 			pass
# 		try:
# 			if car_numb != '0':
# 				if intro['property']['car']['status'] == '0':
# 					car_status = '未变卖'
# 				elif intro['property']['car']['status'] == '1':
# 					car_status = '变卖中'
# 				else:
# 					car_status = '已变卖'
# 		except:
# 			pass
# 		#  房屋信息
# 		houses_numb, houses_worth, houses_status = '0', '',''
# 		try:
# 			car_numb = intro['property']['houses']['numb']
# 		except:
# 			pass
# 		try:
# 			if car_numb != '0':
# 				car_worth = intro['property']['houses']['worth']
# 		except:
# 			pass
# 		try:
# 			if car_numb != '0':
# 				if intro['property']['houses']['status'] == '0':
# 					car_status = '未变卖'
# 				elif intro['property']['houses']['status'] == '1':
# 					car_status = '变卖中'
# 				else:
# 					car_status = '已变卖'
# 		except:
# 			pass
		
		
# 		line = [
# 			0,
# 			'https://m2.qschou.com/project/love/love_v7.html?projuuid=' + uuid,
# 			uuid,
# 			prove['patient'],
# 			prove['patient_icons'],
# 			prove['disease'],
# 			prove['hospital'],
# 			prove['disease_icons'],
# 			prove['recipient'],
# 			prove['recipient_icon'],
# 			intro['title'],
# 			"“" + intro['text']  + '”',
# 			intro['cover_num'],
# 			intro['created'],
# 			intro['raise_days'],
# 			intro['raised_amount'],
# 			intro['target_amount'],
# 			intro['support_number'],
# 			intro['share_number'],
# 			gs,
# 			gs_time,
# 			gs_text,
# 			no_insurance,
# 			insurance,
# 			social_security,
# 			low_security,
# 			gov_assistance,
# 			total_assets,
# 			annual_income,
# 			car_status,
# 			car_numb,
# 			car_worth,
# 			houses_status,
# 			houses_numb,
# 			houses_worth
# 		]
# 		info_write.writerow(line)
		
		
# 		for single in prove['prove_list']:
# 			line = [
# 				uuid, 
# 				single['real_name'],
# 				'已实名' if len(single['real_name']) > 0 else '未实名',
# 				"“" + single['content']  + '”',
# 				time.strftime("%Y-%m-%d (%H:%M:%S)", time.localtime(int(single['created']))),
# 				single['relation'],
# 				single['love_point']
# 			]
# 			prove_write.writerow(line)
	
# 		for single in support:
# 			line = [
# 				uuid,
# 				single['user']['nickname'],
# 				"“" + single['message'] + '”',
# 				time.strftime("%Y-%m-%d (%H:%M:%S)", time.localtime(int(single['created']))),
# 				single['title'][1]['text'],
# 				single['love_point']
# 			]
# 			support_write.writerow(line)
			
	
# 		for single in feed['news']:
# 			text = ''
# 			for ss in single['content']:
# 				for s in ss:
# 					text += s['text']
# 			line = [
# 				uuid,
# 				single['user']['nickname'],
# 				"“" + text + '”',
# 				time.strftime("%Y-%m-%d (%H:%M:%S)", time.localtime(int(single['created']))),
# 			]
# 			news_write.writerow(line)
# 	print ("write over")
	
	
	

