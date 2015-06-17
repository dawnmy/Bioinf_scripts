# clip the reads to a particular length
paste - - - - < in.fastq | gawk -F"\t" '{print $1"\t"substr($2,1,50)"\t"$3"\t"substr($4,1,50)}'|tr "\t" "\n" > out_len50.fastq
# extarct specific reads in terms of the identifier list file
paste - - - - < in.fastq|fgrep --file read_identifier_list.txt|tr "\t" "\n" > out.fastq
# convert fastq to fasta
cat test.fq | paste - - - - | sed 's/^@/>/g'| cut -f1-2 | tr '\t' '\n'
