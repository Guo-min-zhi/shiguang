

def jsonShiguang(shiguang):
	data = {}
	data['name'] = shiguang.name
	data['description'] = shiguang.description
	data['create_time'] = shiguang.create_time
	data['start_time'] = shiguang.start_time
	data['end_time'] = shiguang.end_time
	data['first_level_tag'] = shiguang.first_level_tag
	data['cover'] = shiguang.cover
	return data