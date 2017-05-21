import subprocess
import csv

bams = ["/projects/med/hlab/bds_Yang/ASXL1_WTtest/align/rep1/ASXL1_WT_R1.trim.PE2SE.nodup.bam", "/projects/med/hlab/bds_Yang/ASXL1_WTtest/align/rep2/Rep2_ASXL1_WT_R1.trim.PE2SE.nodup.bam", "/projects/med/hlab/bds_Yang/ASXL1_VAV/align/rep1/ASXL1_VAV_R1.trim.PE2SE.nodup.bam", "/projects/med/hlab/bds_Yang/ASXL1_VAV/align/rep2/Rep2_ASXL1_VAV_R1.trim.PE2SE.nodup.bam", "/projects/med/hlab/bds_Yang/ASXL1_SF/align/rep1/ASXL1_SF_R1.trim.PE2SE.nodup.bam", "/projects/med/hlab/bds_Yang/ASXL1_SF/align/rep2/Rep2_ASXL1_SF_R1.trim.PE2SE.nodup.bam"]
bam_names = ["WT1", "WT2", "VAV1", "VAV2", "SF1", "SF2"]
bed = "peaks_overlap_RNA_ATAC.bed"
output_format = "violinN" #violin or something else
normalize = [1, 1, 1, 1, 1, 1]

##### import bed file
bedfile = []
with open(bed, 'rb') as f:
    dialect = csv.Sniffer().sniff(f.read(1024)) #checks for delimiter
    f.seek(0)
    reader = csv.reader(f, dialect)
    for row in reader:
            temp = []
            temp.append(str(row[0]))
            temp.append(int(row[1]))
            temp.append(int(row[2]))
            bedfile.append(temp)

output = []
output_temp = ["chr","start", "stop"]
for p in bam_names:
    output_temp.append(p)
output.append(output_temp)

for i in bedfile:
    output_temp=[i[0],i[1],i[2]]
    for n, p in enumerate(bams):
        subprocess.call(["samtools", "view", str(p), i[0] + ':' + str(i[1]) + '-' + str(i[2]), "-b"], stdout=open('temp.bam','w'))
        subprocess.call(["samtools", "flagstat", "temp.bam"], stdout=open('temp_flagstat.txt','w'))
        reads = int(subprocess.check_output(["awk", "-F", " +", "NR==9 {print $1}", "temp_flagstat.txt"]))
        output_temp.append(float(reads)/normalize[n])
    output.append(output_temp)

subprocess.call(["rm", "temp.bam"])
subprocess.call(["rm", "temp_flagstat.txt"])

if output_format == "violin":
    output_violin = [["value", "sample"]]
    for x, sample in enumerate(bam_names):
        output.pop(0)
        for row in output:
            output_violin.append([row[x+3], sample])
    output = output_violin

with open(bed + "_output.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerows(output)