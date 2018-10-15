for f in 04-Mapped_MT/*.bam
do echo $f `samtools flagstat $f | head -n 5 | tail -n 1` >>pctmapped_MT.txt
done

for f in 04-Mapped_MT/*.bam
do
samtools index $f &
done

