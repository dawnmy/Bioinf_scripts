#!/usr/bin/env python
# coding=utf-8
# @author: Deng

from Bio import SeqIO

def parseGB(gb):
	header_seq = {}
	record = SeqIO.read(gb, "genbank")
	for feature in record.features:
	    if feature.type == "gene":
	    	if "gene" in feature.qualifiers:
		        feature_name = feature.qualifiers["gene"][0] 
		        sequence = feature.extract(record.seq)
		    	header_seq[feature_name] = str(sequence)
	return header_seq


def countCodon(nseq):							# define a function for counting codons
	codon_seq = []								# a list to store the codons of the given sequence
	codon_count = {}							# a list of tuple to store the count for every 64 codon
	for i in range(0,len(nseq),3):
		codon = nseq[i:i+3]						# splice sequence into codon
		codon_seq.append(codon)
	for j in codon_table:
		codon_count[j] = (codon_seq.count(j), codon_table[j])	# count each codon
	return codon_count

def main():
	logfile = open("Dshi_condon_log.txt","w")
	dict_seq = parseGB("NC_009952.gbk")
	
	total_count = {}
	for seq in dict_seq:
		logfile.write("> " + seq + "\n")
		codon_counts = countCodon(dict_seq[seq])
		for record in codon_counts:
			logfile.write("\t".join((record, str(codon_counts[record][0]),codon_counts[record][1])) + "\n")
			if total_count.has_key(record):
				total_count[record] += codon_counts[record][0]
			else:
				total_count[record] = codon_counts[record][0]			
		logfile.write("\n")
	logfile.write("> The accumulative total usage of codons\n")
	for (key,value) in total_count.items():
		logfile.write("\t".join((key,str(value),codon_table.get(key,'*'))) + "\n")
	logfile.close()

if __name__ == '__main__':
	bases = ["T","C","A","G"]                               
	codons = [a+b+c for a in bases for b in bases for c in bases]		# a list of 64 codons
	amino_acids = 'FFLLSSSSYY**CC*WLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG'
	# generate a codon table
	codon_table = dict(zip(codons, amino_acids))
	main()
