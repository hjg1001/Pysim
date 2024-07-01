import random
name=['埃', '尔', '维', '拉', '卡', '尔', '多', '尼', '亚', '赛', '伦', '斯', '普', '罗', '斯', '庇', '阿', '尔', '基', '恩', '塞', '尔', '托', '斯', '弗', '拉', '尼', '克', '斯', '泽', '拉', '夫', '科', '尔', '瓦', '多', '阿', '斯', '特', '里', '亚', '莱', '昂', '尼', '斯', '贝', '塔', '拉', '格', '洛', '瑞', '安', '德', '拉', '科', '尼', '亚', '埃', '尔', '米', '拉', '佩', '尔', '西', '亚', '塞', '勒', '尼', '斯', '瓦', '拉', '多', '尔', '卡', '斯', '泰', '利', '亚', '奥', '里', '昂', '阿', '斯', '蒂', '特', '卡', '尔', '贝', '拉', '弗', '里', '奇', '亚', '波', '尔', '瓦', '尼', '亚', '阿', '尔', '科', '尔', '塔', '拉', '米', '尔', '赫', '克', '索']
def generate_nation_name():
	NationName=''
	for _ in range(random.randint(1,4)):
		NationName+=random.choice(name)
	if len(NationName)==1:NationName+=random.choice(['朝','国'])
	else:NationName+=random.choice(['王国','公国','帝国','王朝'])
	return NationName
def generate_city_name():
	CityName=''
	for _ in range(random.randint(2,4)):
		CityName+=random.choice(name)
	return CityName