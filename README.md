# Ubed2reads
Extracts number of reads in regions defined by a bed file from bam files

Given a input BED file, this tool will extract the number of reads in each region seperatelly from one or multiple bam files.


bams: BAM files to extract reads from

bam_names: Names to be used in the output can be specified here. Order the same as input bams.

output_format: if set to "violin", output csv will be correctly formatted to be used as an input to generate a violin plot with R and ggplot2.

normalize: numbers of reads in each regions will be normalized (divided) by the values specified here. Order the same as input bams.

