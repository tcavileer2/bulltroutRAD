from glob import glob

outf = open("00-cleaning.sh", 'w')

for r1 in glob("./00-RawData/*R1*.fastq"):
    r2 = r1.replace("_R1_", "_R2_")
    s = r1.split("/")[2].split("_")[0]
    cmd = "hts_AdapterTrimmer -m 50 -O -L ./01-hts_AdapterTrimmed/trim.log -1 " + r1 + " -2 " + r2 + " | "
    cmd += "hts_SeqScreener -S -O -A -L ./01-hts_AdapterTrimmed/trim.log | "
    cmd += "hts_SeqScreener -k 15 -x .01 -S -s adapters.fa -A -L ./01-hts_AdapterTrimmed/trim.log -p ./01-hts_AdapterTrimmed/" + s
    outf.write(cmd + '\n')

outf.close()

