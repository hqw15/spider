import json
import os
import time
import datatime


def out_single_json(data, path):
	data = json.dumps(data, ensure_ascii=False, indent=2)
	with open(path, 'w', encoding = 'utf-8') as f:
		f.write(data)


cnt = 0
for root, dirs, files in os.walk(in_dir):
	for name in files:
		tmp = {}
		attr_out = {}
		with open(os.path.join(root, name), 'r', encoding = 'utf-8') as f:
			tmp = json.load(f)


		now_time = time.strftime("%Y-%m-%d(%H-%M-%S)", time.localtime(time.time()))


		for uid in tmp:
			if uid not in attr:
				attr_out[uid] = {}
			for attr in tmp[uid]['intro']:
				tmp[uid]['intro'][attr] = {now_time: 0}
				attr_out[uid][attr] = {0:  tmp[uid]['intro'][attr]}
				
			for attr in tmp[uid]['prove']:
				if attr != 'prove_list':
					tmp[uid]['prove'][attr] = {now_time: 0}
					attr_out[uid][attr] = {0:  tmp[uid]['prove'][attr]}

		out_single_json(tmp, os.path.join('project', name))
		out_single_json(attr_out, os.path.join('attr', name))


