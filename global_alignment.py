# -*- coding: utf-8 -*-
#......................................................................
#	
# Description: 
#	This program is used to implement the global alignment based on 
#	dynamic programing algorithm 
#
#......................................................................


def usage():
	usage = '''
Usage: 
	python alignment.py <para_file> <target_seq_file> <out_file>
---------------------------------------------------------------------------
Description of the command line arguments:

	para_file: parameter file
	target_seq_file: input fasta file as reference
	out_file: output file to deposit the alignment and record the score

'''
	return usage


def parseFasta(ffasta):	
	'''
	Parsing the input fasta file
	'''

	sequences = {}
	with open(ffasta,"r") as hfasta:
		fasta = hfasta.read()
	seqlist = fasta.split(">")[1:]
	for hseq in seqlist:
		lines = hseq.split("\n")[:-1]
		header = lines[0].strip()
		seq = "".join([line.strip() for line in lines[1:] if line.strip() != ""])
		sequences[header] = seq.upper()

	return sequences




def parsePara(fpara):
	''' 
	Parsing the parameter file to retrieve the parameters

	'''
	para = []
	with open(fpara, "r") as hpara:
		for line in hpara:
			line = line.strip()
			if line and line[0] != ";":
				para.append(line.split(";")[0].strip())
	parameters = [map(int,para[:2]),[base.strip().upper() for base in para[2].split()],[map(int,penalty.split()) for penalty in para[3:]]]
	return parameters

def align(target, query, paramter):

	'''
	initiating gap: gapo
	diagonal scoring : match
	gap extending: gape
	the alphabet of given sequences: bases
	'''
	mat = []	# scoring matrix
	path = []	# matrix to record the paths of alignments

	# "$" is used to mark the start of the sequence and for starting the scoring matrix

	target = "$" + target.upper()
	query = "$" + query.upper()
	gapo = paramter[0][0]
	gape = paramter[0][1]
	
	
	bases = paramter[1]
	match = paramter[2]
	
	m = len(query)
	n = len(target)
	for j in range(m):


		f = []	# each line of scoring matrix
		align = []	# each line of path matrix
		for i in range(n):

			# defining the mat[0][0] and path[0][0]
			if i == 0 and j == 0:
				score = 0
				f.append(score)
				align.append(("",""))


			# defining the mat[j][0] and path[j][0]
			elif i == 0 and j != 0:
			
				score = gapo if j == 1 else gape * (j - 1)
				f.append(score)
				align.append(("_"*j, query[1:j+1]))

			# defining the mat[0][i] and path[0][i]
			elif j == 0 and i != 0:
				score = gapo if i == 1 else gape * (i - 1)
				
				f.append(score)
				align.append((target[1:i+1], "_"*i))

			# calculating the rest of the elements of mat and path
			else:
				'''
				h: horizontal move
				v: vertical move
				d: diagonal move
				mscore: the corresponding penalty in given parameter matrix
				score: the scoring value
				'''
				
				h = f[i-1] + gape if align[i-1][1][-1] == "_" or align[i-1][0][-1] == "_" else f[i-1] + gapo
				
				v = mat[j-1][i] + gape if path[j-1][i][0][-1] == "_" or path[j-1][i][1][-1] == "_" else mat[j-1][i] + gapo
				
				t = target[i]
				q = query[j]
				mscore = match[bases.index(t)][bases.index(q)]
				d = mat[j-1][i-1] + mscore
			
				# Obtaining the best score 
				score = max(h,v,d)

				f.append(score)
				if d == score:
					align.append((path[j-1][i-1][0]+target[i],path[j-1][i-1][1]+query[j]))
				elif h == score:
					align.append((align[i-1][0]+target[i],align[i-1][1]+"_"))
				elif v == score:
					align.append((path[j-1][i][0]+"_",path[j-1][i][1]+query[j]))
				


		mat.append(f)
		path.append(align)


	return (mat[m-1][n-1],path[m-1][n-1])
	# return (mat,path)


if __name__ == '__main__':

	import sys
	num_arguments = len(sys.argv)

	if num_arguments != 4:
		print usage()
		sys.exit("sorry, please input valid arguments!")

	
	# Receiving the input files and outout file name from command line.

	para_file = sys.argv[1]
	target_seq_file = sys.argv[2]
	out_file = sys.argv[3]
	

	query = "ACAATCG"

	seqs = parseFasta(target_seq_file)

	outfile = open(out_file,"w")
	parameter = parsePara(para_file)
	print "Processing ......"
	for seq in seqs:

		result = align(seqs[seq],query,parameter)
		
		header = ">" + seq + "\tscore: " + str(result[0]) +"\n"
		alignment = result[1][0] + "\n" + result[1][1] +"\n"
		outfile.write(header + alignment)

	print "Done!"

	outfile.close()
