#coding:utf-8
#################################
#Copyright(c) 2014 dtysky
#################################

#Return hash for a dict which may contain a dict as its value or others
def DHash(Dict):
	dh=0
	if isinstance(Dict,dict):
		for tmp in Dict:
			if isinstance(Dict[tmp],dict):
				dh+=hash(tmp)
				for sub in Dict[tmp]:
					dh+=hash(sub+str(Dict[tmp][sub]))
			else:
				dh+=hash(tmp)+hash(str(Dict[tmp]))
	else:
		dh+=hash(str(Dict))
	return dh