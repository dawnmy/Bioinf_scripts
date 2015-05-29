import numpy as np
import pylab as plt
import seaborn as sns
import pandas as pd


df = pd.read_csv("similarity_matrix.txt", sep="\t",header=0,index_col=0)
# print df.index.is_unique

# df = np.matrix(df)
# print df["NAG"]

# df["NAG"]
province = list(df.index)

l1 = []
for i in province:

	for j in df.columns.values:
		for k in df[j][i]:
			if k !=0:
				 l1.append([(j.split(".")[0],i),k])


pro = set(province)

comp = {}
for p in pro:
	for q in pro:
		l2 = []
		for r in l1:
			if r[0][0] == p and r[0][1] == q:


				l2.append(r[1])
		comp[(p,q)] = l2





l3 = []
# l4 = []
for com in comp:
	if comp[com]:
		l3.append([com,comp[com]])
	elif (not comp[com]) and (com[0] != com[1]):
		l3.append([com,comp[(com[1],com[0])]])


		# l4.append(comp[com])

for pr in list(pro):
	data = []
	labels = []
	o = ['FKLD','BRAZ','SATL','WTRA','NAG','NADR']
	order = [pr+" ~ "+od for od in o]
	
	for l in l3:
		if l[0][0] == pr:

			# dt[]
			# data.append(("~".join(l[0]),l[1]))
			label = [" ~ ".join(l[0])] * len(l[1])
			labels.extend(label)
			data.extend(l[1])

	print len(data), len(labels)


		
	df = pd.DataFrame(dict(score=data, group=labels))
	# print data



	sns.boxplot(df.score, df.group, order=order)
	plt.savefig(pr + "_comparison.pdf")
	plt.show()


		# li = []
		# li.append(df[j][i])
		
	

# print df["FKLD.1"]["FKLD"]
# print df["FKLD"]["FKLD"]

# gp = df.groupby('FKLD').groups
# print gp
# gp = df[df.groupby(level=0).transform(len)['FKLD'] > 1]
# gp.to_csv("matrix.txt",sep="\t")

# print df[df.groupby(level=0).transform(len)['FKLD'] > 1]
# print len(data["FKLD"])
# data = [randn(100), randn(50)]
# sns.boxplot(data)

# g = sns.factorplot("day", "total_bill", "sex", tips, kind="box",
# sns.heatmap(data)
