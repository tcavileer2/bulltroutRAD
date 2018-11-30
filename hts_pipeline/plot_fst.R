fs = c("populations.fst_fc-fl.tsv", "populations.fst_fc-pl.tsv", "populations.fst_fl-pl.tsv")

pdf(file="all_fst_plot.pdf", w=300, h=15)
par(mfrow=c(3,1))
for(f in fs){
    d = read.table(f, header=F, sep='\t', as.is=T)
    colnames(d) = c('Locus.ID', 'Pop.1.ID',  'Pop.2.ID',  'Chr',  'BP',  'Column',  'Overall.Pi',  'AMOVA.Fst',  "Fishers.P",  'Odds.Ratio',  'CI.Low',  'CI.High',  'LOD', 'Corrected.AMOVA.Fst', 'Smoothed.AMOVA.Fst', 'Smoothed.AMOVA.Fst.P-value', 'Window.SNP.Count')

    maxes = tapply(X=d$BP, INDEX=d$Chr, FUN=max)
    cmaxes = cumsum(maxes)
    cmaxes2 = c(0, cmaxes)
    cmaxes2 = cmaxes2[1:length(cmaxes)]
    names(cmaxes2) = names(cmaxes)
    xcoord = as.numeric(d$BP) + cmaxes2[d$Chr]
    par(las=2)
    plot(d$Smoothed.AMOVA.Fst, type='o', x=xcoord, xaxt='none', ylab='Smoothed.AMOVA.Fst', main=paste(f, 'Smoothed.AMOVA.Fst'))
    text(d$Chr[!duplicated(d$Chr)], y=1, x=xcoord[!duplicated(d$Chr)])
    abline(v=xcoord[!duplicated(d$Chr)], col='red')
    axis(side=1, at=xcoord, labels=d$BP, cex.axis=.5)
}
dev.off()




f = "populations.fst_Hermiston.OR.USA-Rexburg.ID.USA.tsv"

f = "populations.fst_Garfield City.WA.USA-Claresholm.Alberta.Canada.tsv"

f = "populations.fst_Arbon.ID.USA-Kimberly.ID.USA.tsv"

x11()
d = read.table(f, header=F, sep='\t', as.is=T)
colnames(d) = c('Locus.ID', 'Pop.1.ID',  'Pop.2.ID',  'Chr',  'BP',  'Column',  'Overall.Pi',  'AMOVA.Fst',  "Fisher's.P",  'Odds.Ratio',  'CI.Low',  'CI.High',  'LOD', 'Corrected.AMOVA.Fst', 'Smoothed.AMOVA.Fst', 'Smoothed.AMOVA.Fst.P-value', 'Window.SNP.Count')

maxes = tapply(X=d$BP, INDEX=d$Chr, FUN=max)
cmaxes = cumsum(maxes)
cmaxes2 = c(0, cmaxes)
cmaxes2 = cmaxes2[1:length(cmaxes)]
names(cmaxes2) = names(cmaxes)
xcoord = as.numeric(d$BP) + cmaxes2[d$Chr]
plot(d$Smoothed.AMOVA.Fst, type='o', x=xcoord, xaxt='none', ylab='Smoothed.AMOVA.Fst', main=paste(f, 'Smoothed.AMOVA.Fst'))







d = read.table("populations.fst_fc-pl.tsv", header=F, sep='\t', as.is=T)
colnames(d) = c('Locus.ID', 'Pop.1.ID',  'Pop.2.ID',  'Chr',  'BP',  'Column',  'Overall.Pi',  'AMOVA.Fst',  "Fisher's.P",  'Odds.Ratio',  'CI.Low',  'CI.High',  'LOD', 'Corrected.AMOVA.Fst', 'Smoothed.AMOVA.Fst', 'Smoothed.AMOVA.Fst.P-value', 'Window.SNP.Count')
maxes = tapply(X=d$BP, INDEX=d$Chr, FUN=max)
cmaxes = cumsum(maxes)
cmaxes2 = c(0, cmaxes)
cmaxes2 = cmaxes2[1:length(cmaxes)]
names(cmaxes2) = names(cmaxes)
xcoord = as.numeric(d$BP) + cmaxes2[d$Chr]

data.frame(d$Bp, cmaxes[d$Chr], as.numeric(d$BP) + cmaxes[d$Chr])

xcoord = cumsum(as.numeric(d$BP))


pdf(file="populations.fst_fc-pl.pdf", w=300, h=5)
par(las=2)
plot(d$Smoothed.AMOVA.Fst, type='o', x=xcoord, xaxt='none')
axis(side=1, )
text(d$Chr[!duplicated(d$Chr)], y=1, x=xcoord[!duplicated(d$Chr)])
abline(v=xcoord[!duplicated(d$Chr)])
dev.off()

