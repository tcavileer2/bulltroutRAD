for f in 04-Mapped/*.bam
do echo $f `samtools flagstat $f | head -n 5 | tail -n 1` >>pctmapped.txt
done

for f in 04-Mapped/*.bam
do
samtools index $f &
done

