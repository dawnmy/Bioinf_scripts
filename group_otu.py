# -*- coding: utf-8 -*-
# @Author: ZL Deng
# @Date:   2017-11-06 13:53:57
# @Last Modified by:   ZL Deng
# @Last Modified time: 2017-11-06 14:44:10

'''
input TSV file 1: otu_otu_interaction_file
description: three columns separated with tab, the last column is the interaction type 
format: otu1	otu2	positive

######################################################################################

input TSV file 2: otu_taxa_file
description: two columns separated with tab, the last column is the taxon for grouping
format: otu1	taxon1
		otu2	taxon2

######################################################################################

output TSV file 1: taxa_interaction_count_file
description: four columns separated with tab reports the number of interaction between 
			each pair of taxa
format: taxon1	taxon2	positive	10

'''

import argparse as ap 


def group_otu(otu_otu_interaction_file, otu_taxa_file, taxa_interaction_count_file):
	otu_taxa_dic = dict()
	with open(otu_taxa_file, 'r') as otu_taxa_fh:
		for line in otu_taxa_fh:
			(otu, taxon) = line.strip().split("\t")
			otu_taxa_dic[otu] = taxon


	taxa_count_dic = dict()
	with open(otu_otu_interaction_file, 'r') as otu_otu_interaction_fh:
		for line in otu_otu_interaction_fh:
			(otu1, otu2, itype) = line.strip().split("\t")
			taxon1 = otu_taxa_dic[otu1]
			taxon2 = otu_taxa_dic[otu2]
			if (taxon1, taxon2, itype) in taxa_count_dic:
				taxa_count_dic[(taxon1, taxon2, itype)] += 1
			else:
				taxa_count_dic[(taxon1, taxon2, itype)] = 1

	out_fh = open(taxa_interaction_count_file, 'w')
	for (key, value) in taxa_count_dic.items():
		out_line = "{}\t{}\n".format("\t".join(key), str(value))
		out_fh.write(out_line)
	out_fh.close()


if __name__ == '__main__':
	parser = ap.ArgumentParser(description="group the otu interactions based on otu_taxa map file")
	parser.add_argument("otu_otu_interaction_file", help="otu otu interaction file", type=str)
	parser.add_argument("otu_taxa_file", help="otu taxa map file", type=str)
	parser.add_argument("taxa_interaction_count_file", help="resulting taxa interaction count file", type=str)

	args = parser.parse_args()
	otu_otu_interaction_file = args.otu_otu_interaction_file
	otu_taxa_file = args.otu_taxa_file
	taxa_interaction_count_file = args.taxa_interaction_count_file
	group_otu(otu_otu_interaction_file, otu_taxa_file, taxa_interaction_count_file)
