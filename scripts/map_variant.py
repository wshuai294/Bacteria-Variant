#!/usr/bin/env python3

"""
Identify variants (snv, indel, sv) by mapping reads onto the reference.

Reply on: samtools, bwa, freebayes, SVABA

Jan 2, 2024

wangshuai, wshuai294@gmail.com
"""


import argparse
import os
import sys

def map_and_call(options):
    cmd = """
    ref=%s
    fq1=%s
    fq2=%s
    sample=%s
    outdir=%s
    threads=%s
    dir=$(cd `dirname $0`; pwd)
    bin_dir=$dir/../bin/

    if [ ! -d $outdir ]; then
        mkdir $outdir
    fi

    samtools faidx $ref
    bwa index $ref

    bwa mem -t $threads -R '@RG\\tID:'$sample'\\tSM:'$sample $ref $fq1 $fq2 |samtools view -bS -F 4 | samtools sort -o $outdir/$sample.sort.bam
    samtools index $outdir/$sample.sort.bam
    freebayes -f $ref -p 1 $outdir/$sample.sort.bam > $outdir/$sample.snp.indel.vcf
    svaba run -t $outdir/$sample.sort.bam -G $ref -a $outdir/$sample -p $threads

    """%(options.r, options.fq1, options.fq2, options.s, options.o, options.t)
    os.system(cmd)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Identify variants by mapping reads onto the reference.", add_help=False, \
    usage="%(prog)s -h", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    required = parser.add_argument_group("required arguments")
    optional = parser.add_argument_group("optional arguments")
    required.add_argument("-r", type=str, help="<str> reference file.", metavar="\b")
    required.add_argument("--fq1", type=str, help="<str> fastq 1 file.", metavar="\b")
    required.add_argument("--fq2", type=str, help="<str> fastq 2 file.", metavar="\b")
    required.add_argument("-s", type=str, default="sample", help="<str> Sample name.", metavar="\b")
    required.add_argument("-o", type=str, default="./", help="<str> Output folder.", metavar="\b")
    optional.add_argument("-t", type=int, default=10, help="<int> number of threads.", metavar="\b")
    optional.add_argument("-h", "--help", action="help")

    options = parser.parse_args()

    if len(sys.argv) == 1:
        print (f"see python {sys.argv[0]} -h")
    else:
        map_and_call(options)

    # samtools dict $ref >$ref.dict
# bowtie2-build -f $ref $ref 
# bowtie2 -x $ref -p $threads -1 $fq1 -2 $fq2 |grep -v "XS:i:"|samtools view -bS -F 4 | samtools sort -o $outdir/$sample.sort.bam
    # java -jar $bin_dir/picard.jar AddOrReplaceReadGroups I=$outdir/$sample.sort.bam O=$outdir/$sample.sort.header.bam LB=whatever PL=illumina PU=whatever SM=whatever
    # samtools index $outdir/$sample.sort.header.bam
    # java -Xmx5g -jar $bin_dir/GenomeAnalysisTK.jar -T HaplotypeCaller -R $ref -allowPotentiallyMisencodedQuals -I $outdir/$sample.sort.header.bam -o $outdir/$sample.snp.indel.vcf.gz