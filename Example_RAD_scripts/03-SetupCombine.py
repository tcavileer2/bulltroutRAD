from glob import glob
import os

outf = open("03-concat-commands.sh", 'w')
outf2 = open("03-concatfiles_list.txt",'w')

for folder in os.listdir('./02-process_radtags_f'):
    for r1_f in glob('./02-process_radtags_f/' + folder + '/*.1.fq.gz'):
        s = r1_f.split('/')[-1].split('.')[0]
        r2_f = r1_f.replace(".1.fq.gz", '.2.fq.gz')
        r1_r = r1_f.replace("02-process_radtags_f", "02-process_radtags_r")
        r2_r = r2_f.replace("02-process_radtags_f", "02-process_radtags_r")
        outf2.write('\t'.join([s,r1_f,r2_f,r1_r,r2_r]) + '\n')
        cmd = 'zcat ' + r1_f + ' ' + r1_r + ' | gzip > ./03-combined/' + s + ".1.fq.gz\n"
        outf.write(cmd)
        cmd = 'zcat ' + r2_f + ' ' + r2_r + ' | gzip > ./03-combined/' + s + ".2.fq.gz\n"
        outf.write(cmd)
outf.close()
outf2.close()
