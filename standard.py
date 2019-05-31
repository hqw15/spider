import json
import os

class AttrValue:

	def __init__(self, fdir = None, fpath = None):

		self.data = self.__read_dir(fdir) if fdir != None else self.__read_dir(fdir)


	def get_attr(self, uid, attr, newest = True):

		try:
			attr = self.data[uid][attr]
			id = len(attr) - 1
			if not newest:
				id = newest
			if id == -1:
				return '*****!!!!!(((@#$^%$^$&$&%&#@$%$'
			return attr[id]
		except:
			print ('[ERROR] : no uid or attr !!!')
			return ''


	def update_attr(self, uid, attr, value):

		try:
			if uid not in self.data:
				self.data[uid] = {}
			if attr not in self.data[uid]:
				self.data[uid][attr] = {}

			new_id = len(self.data[uid][attr])

			if self.get_attr(uid, attr) == value:
				return new_id-1
			
			assert new_id not in self.data[uid][attr]
			self.data[uid][attr][new_id] = value
			return new_id
		except:
			print ('[ERROR] : update !!!')
			return -1

	def save(self, dir, end_uid, act_dir, end_dir):
		act, end = 0, 0
		act_prj, end_prj = {}, {}
		for uid in self.data:
			if uid in end_uid:
				end_prj[uid] = self.data[uid]
			else:
				act_prj[uid] = self.data[uid]

			if len(end_prj) == 100:
				self.__save_json(end_prj, os.path.join(end_dir, str(end)+'.json'))
				end_prj = {}
				end += 1
			if len(act_prj) == 100:
				self.__save_json(act_prj, os.path.join(act_dir, str(act)+'.json'))
				act_prj = {}
				act += 1
		self.__save_json(end_prj, os.path.join(end_dir, str(end)+'.json'))
		self.__save_json(act_prj, os.path.join(act_dir, str(act)+'.json'))
		print ('save over ...')

	def __save_json(self, data, path):
		data = json.dumps(data, ensure_ascii=False, indent=2)
		with open(path, 'w', encoding = 'utf-8') as f:
			f.write(data)

	def __read_dir(self, fdir):
		assert fdir != None
		all_data = {}
		for root, dirs, files in os.walk(fdir):
			for name in files:
				if name.endswith('.json'):
					tmp = {}
					with open(os.path.join(root, name), 'r', encoding = 'utf-8') as f:
						tmp = json.load(f)
					all_data.update(tmp)
		print ('read dir : tot file %d' % len(all_data))
		return all_data

	def __read_file(self, fpath):
		assert fpath != None:
		all_data = {}
		if fpath.endswith('.json'):
			with open(fpath, 'r', encoding = 'utf-8') as f:
				all_data = json.load(f)
		print ('read file : tot file %d' % len(all_data))
		return all_data
