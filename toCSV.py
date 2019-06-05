import csv
import json
import time
import json
import os
import datetime
from parser import parser


def toSupport(uuid, data, fpath, isAdd = True):

	if isAdd:
		out = open(fpath,'a+', newline='', encoding='utf-8-sig')
		out = csv.writer(out,dialect='excel')
	else:
		out = open(fpath,'w', newline='', encoding='utf-8-sig')
		firstLine = ['项目uuid', '日期', '时间' , '捐款人', '捐款人uuid', '捐款文字', '捐款金额', '增加的爱心值', '总爱心值']
		out = csv.writer(out,dialect='excel')
		out.writerow(firstLine)

	line = [uuid, data['created'].split(' ')[0], data['created'].split(' ')[1][1:-1], data['user_name'], data['user_uuid'],
		data['message'], data['support_money'], data['added_love_point'], data['love_point']
	]
	out.writerow(line)	

def toProve(uuid, data, fpath, isAdd = True):

	if isAdd:
		out = open(fpath,'a+', newline='', encoding='utf-8-sig')
		out = csv.writer(out,dialect='excel')
	else:
		out = open(fpath,'w', newline='', encoding='utf-8-sig')
		firstLine = ['项目uuid', '日期', '时间' , '证实人', '关系', '证实文字', '爱心值', '是否实名']
		out = csv.writer(out,dialect='excel')
		out.writerow(firstLine)

	line = [uuid, data['created'].split(' ')[0], data['created'].split(' ')[1][1:-1],  data['name'],
		data['relation'], data['content'], data['love_point'], data['real_name']
	]
	out.writerow(line)	

def toFundsNews(uuid, data, fpath, isAdd = True):

	if isAdd:
		out = open(fpath,'a+', newline='', encoding='utf-8-sig')
		out = csv.writer(out,dialect='excel')
	else:
		out = open(fpath,'w', newline='', encoding='utf-8-sig')
		firstLine = ['项目uuid', '日期', '时间' , '发布人', '发布人uuid', '发布文字']
		out = csv.writer(out,dialect='excel')
		out.writerow(firstLine)

	line = [uuid, data['created'].split(' ')[0], data['created'].split(' ')[1][1:-1],  data['user_name'],
		data['user_uuid'], data['content']
	]
	out.writerow(line)	

def toInfo(uuid, data, fpath, isAdd = True):
	if isAdd:
		out = open(fpath,'a+', newline='', encoding='utf-8-sig')
		out = csv.writer(out,dialect='excel')
	else:
		out = open(fpath,'w', newline='', encoding='utf-8-sig')
		out = csv.writer(out,dialect='excel')
		firstLine = [
			'项目uuid', 
			'日期', 
			'时间' , 
			'项目链接', 
			'是否在首页', 
			'标题',
			'筹款说明',
			'照片数量',
			'项目发起时间',
			'项目拟筹款天数',
			'项目结束时间',
			'目标金额(元)',
			'已筹金额(元)',
			'帮助次数',
			'转发次数',
			'患者姓名',
			'患者身份证明是否审核',
			'所患疾病',
			'诊断是否审核',
			'医院',
			'收款人姓名',
			'收款人关系',
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
		out.writerow(firstLine)

	# 保险状况
	no_insurance, insurance, social_security, low_security, gov_assistance = '无','无','无','无','无'
	try:
		no_insurance = '无' if data['property']['no_insurance'] else '有'
	except:
		pass
	try:
		insurance = '有' if data['property']['insurance'] else '无'
	except:
		pass
	try:
		social_security = '有' if data['property']['social_security'] else '无'
	except:
		pass
	try:
		low_security = '有' if data['property']['low_security'] else '无'
	except:
		pass
	try:
		gov_assistance = '有' if data['property']['gov_assistance'] else '无'
	except:
		pass
	if insurance == '无' and social_security == '无' and low_security == '无' and gov_assistance == '无':
		if no_insurance == '有':
			print ('error, no_insurance state!')
			no_insurance = '无'
	else:
		if no_insurance == '无':
			print ('error, no_insurance state!')
			no_insurance = '有'
			
	#########################
	# 增信说明
	#  总资产
	total_assets = 'unknown'
	try:
		total_assets = data['property']['household_income']['total_assets']
	except:
		pass
	#  年收入
	annual_income = 'unknown'
	try:
		annual_income = data['property']['household_income']['annual_income']
	except:
		pass
	#   车辆信息
	car_numb, car_worth, car_status = '0', '', ''
	try:
		car_numb = data['property']['car']['numb']
	except:
		pass
	try:
		if car_numb != '0':
			car_worth = data['property']['car']['worth']
	except:
		pass
	try:
		if car_numb != '0':
			if data['property']['car']['status'] == '0':
				car_status = '未变卖'
			elif data['property']['car']['status'] == '1':
				car_status = '变卖中'
			else:
				car_status = '已变卖'
	except:
		pass
	#  房屋信息
	houses_numb, houses_worth, houses_status = '0', '',''
	try:
		houses_numb = data['property']['houses']['numb']
	except:
		pass
	try:
		if houses_numb != '0':
			houses_worth = data['property']['houses']['worth']
	except:
		pass
	try:
		if houses_numb != '0':
			if data['property']['houses']['status'] == '0':
				houses_status = '未变卖'
			elif data['property']['houses']['status'] == '1':
				houses_status = '变卖中'
			else:
				houses_status = '已变卖'
	except:
		pass
		
		
	line = [
		uuid,
		data['time'].split(' ')[0], 
		data['time'].split(' ')[1][1:-1].replace('-', ":"),
		'https://m2.qschou.com/project/love/love_v7.html?projuuid=' + uuid,
		data['sy'],
		data['title'],
		data['text'],
		data['cover_num'],
		data['created'],
		data['raise_days'],
		data['stopped_time'],
		data['target_amount'],
		data['raised_amount'],
		data['support_number'],
		data['share_number'],
		data['patient'],
		data['patient_icons'],
		data['disease'],
		data['disease_icons'],
		data['hospital'],
		data['recipient'],
		data['recipient_icon'],
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
	out.writerow(line)

if __name__ == "__main__":


	tmp = {}
	with open('../3.json', 'r', encoding = 'utf-8') as f:
		tmp = json.load(f)
	for uid in tmp:
		s = parser(uid, tmp[uid])
		support, prove_list, funds, news, info = s.main()

		for index, data in  enumerate(support):
			if index == 0:
				toSupport(uid, data, 'support.csv', isAdd = False)
			else:
				toSupport(uid, data, 'support.csv', isAdd = True)

		for index, data in  enumerate(prove_list):
			if index == 0:
				toProve(uid, data, 'prove.csv', isAdd = False)
			else:
				toProve(uid, data, 'prove.csv', isAdd = True)

		for index, data in  enumerate(funds):
			if index == 0:
				toFundsNews(uid, data, 'funds.csv', isAdd = False)
			else:
				toFundsNews(uid, data, 'funds.csv', isAdd = True)

		for index, data in  enumerate(news):
			if index == 0:
				toFundsNews(uid, data, 'news.csv', isAdd = False)
			else:
				toFundsNews(uid, data, 'news.csv', isAdd = True)

		for index, data in  enumerate(info):
			if index == 0:
				toInfo(uid, data, 'info.csv', isAdd = False)
			else:
				toInfo(uid, data, 'info.csv', isAdd = True)