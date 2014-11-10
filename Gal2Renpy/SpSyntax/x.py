import shutil
Keywords=[
	"sc",
	"sw",	#a part
	"bg",
	"bgm",
	"sound",
	"date",
	"cg",	#a part
	"vd",	#not
	"ef",	#a part
	"gf",
	"key",
	"mode",
	"view",
	"chc",
	"hpc",
	"renpy",
	"test"
]

for k in Keywords:
	k=k[0].upper()+k[1:]
	shutil.copyfile('ChSp.py',k+'Sp.py')