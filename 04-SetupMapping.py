from glob import glob
from os.path import join as jp

outf = open("04-mapping-commands.sh", 'w')
#bwa mem -t 4 -R '@RG\tID:bwa\tSM:ID3\tPL:ILLUMINA' ./idx/idx ./03-combined/ID3.1.fq.gz ./03-combined/ID3.2.fq.gz 

bwaIndex = './idx/idx'

for r1 in glob("./03-combined/*.1.fq.gz"):
    r2 = r1.replace('.1.fq.gz', '.2.fq.gz')
    s = r1.split('/')[-1].replace('.1.fq.gz', '')
    if s[0] == 'Z':
        print r1, s
    cmd = ' '.join(["bwa mem -t 5 -R '@RG\\tID:bwa\\tSM:"+ s +"\\tPL:ILLUMINA'", 
                    bwaIndex, r1, r2, " 2>./04-Mapped/" + s + '.log' + " | samtools view -bS - | samtools sort - > ./04-Mapped/" + s + '.bam',
                    ]) + '\n'
    outf.write(cmd)
outf.close()

