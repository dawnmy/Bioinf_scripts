#!/bin/bash
#$ -N sge_qc_bt2
#$ -l arch=linux-x64
#$ -pe multislot 20
#$ -b n
## -q all.q
#$ -i /dev/null
#$ -e /vol/cluster-data/dzhiluo/sge_logs/
#$ -o /vol/cluster-data/dzhiluo/sge_logs/
#$ -cwd

# The directives above are for the Sun Grid Engine
# -pe 20: Informs SGE that we use the predefined parallell environment with
# the name 'multislot' and that 20 slots/cores are needed for this job
# -q all.q: Job will be sumitted in queue all.q


# I M P O R T A N T:
# DO NOT write stdout and stderr logfiles (-o and -e directives) to the 
# user home partition since this would trash the fileserver and slow down
# the system for other users!!!! Use /vol/cluster-data/USERNAME/WHATEVER 
# instead!


# such a script can be submitted with: qsub sge_qc.sh


# print local hostname and PATH variable to STDOUT. This will appear in the jobs STDOUT log 

# setup pathes
export FASTQ_MCF=/home/dzhiluo/tools/ea-utils/fastq-mcf
export BOWTIE2=/vol/biotools/bin/bowtie2
export NCORE=20
export SAMTOOLS=/vol/biotools/bin/samtools
export HTSEQ_COUNT=/usr/bin/htseq-count
gff=$1
outdir=${2%/}
feature=CDS
id=ID
for file in ./*.fastq
do 
        bname=`basename ${file%.fastq}`;
        clfastq=${outdir}/${bname}_cl.fastq;
        cllog=${clfastq%.fastq}.log;
        countfile=${outdir}/${bname}_count.txt

	$FASTQ_MCF -q 20 -l 20 -x 5 ./adaptors.fa ${file} -o ${clfastq} >> ${cllog};

        bamfile=${outdir}/${bname}_sorted.bam
        bamlog=${outdir}/${bname}_bam.log

        $BOWTIE2 -p $NCORE -x $index -U ${clfastq} |$SAMTOOLS view -Shb - 2>> $bamlog|$SAMTOOLS sort -@ $NCORE -m 5G -f - $bamfile >> $bamlog 2>&1
        $SAMTOOLS index $bamfile
        ${HTSEQ_COUNT} -r pos -t $feature -f bam -i $id $file $gff  > $countfile
        echo "htseq-count -t $feature -f bam -i $id $file $gff  > $countfile"
done

cd $outdir
# extract the counted feature IDs 
for file in ./*_count.txt
do
        # if an 'annotation' file does not exist, it will be created by extracting the first column of the first input file and writing it to a temporary annotation file.
        # if an 'annotation' file exists, this step will not be performed and the script goes directly to the next step of the for-loop.
        if [ ! -f "annotation" ]; then
        grep -v -E 'SAM alignment|GFF lines processed|^__' $file  | awk '{print $1}' > annotation
        fi

# for all input files the second column containing counts per gene will be written to a temporary file '*.tmp' 
        grep -v -E 'SAM alignment|GFF lines processed|^__' $file  | awk '{print $2}' > ${file%_count.txt}.tmp
done


# the temporary 'annotation' and '*.tmp' files with counts are written to a temporary file 'counts'
paste annotation *.tmp > counts

# a temporary 'title' file is created by concatenating "ID" (for the column containing the unique identifier) and the names of the input files with file extensions removed
echo "ID" `ls *_count.txt`|tr ' ' '\t'|sed 's/_count\.txt//g' > title

# The 'title' file and the 'counts' file are concatenated and the result is written to a file with the name specified as input to the script
cat title counts > expression_table.txt

# temporary files are removed
rm annotation *.tmp counts title
