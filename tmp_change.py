import json
import os
import time
import datetime


def out_single_json(data, path):
	data = json.dumps(data, ensure_ascii=False, indent=2)
	with open(path, 'w', encoding = 'utf-8') as f:
		f.write(data)

in_dir = '2019-05-31(23-46-00)'
cnt = 0
for root, dirs, files in os.walk(in_dir):
	for name in files:
		tmp = {}
		# attr_out = {}
		with open(os.path.join(root, name), 'r', encoding = 'utf-8') as f:
			tmp = json.load(f)

		now_time = time.strftime("%Y-%m-%d(%H-%M-%S)", time.localtime(time.time()))

		for uid in tmp:
			# if uid not in attr_out:
			# 	attr_out[uid] = {}
			for attr in tmp[uid]['intro']:
				# attr_out[uid][attr] = {0:  tmp[uid]['intro'][attr]}
				tmp[uid]['intro'][attr] = {now_time: tmp[uid]['intro'][attr], 'new':tmp[uid]['intro'][attr]}
				
				
			for attr in tmp[uid]['prove']:
				if attr != 'prove_list':
					# attr_out[uid][attr] = {0:  tmp[uid]['prove'][attr]}
					tmp[uid]['prove'][attr] = {now_time: tmp[uid]['prove'][attr], 'new':tmp[uid]['prove'][attr]}
					
		out_single_json(tmp, os.path.join('project', name))
		# out_single_json(attr_out, os.path.join('attr', name))
		print ('ss')


