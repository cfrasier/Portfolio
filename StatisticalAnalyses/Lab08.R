rm(list=ls())
setwd("D:/Documents/Schoolfiles/advancedstats")
tab<-read.table("nc101_scaff_dataCounts.txt",sep="\t",header=TRUE,row.names=1)

# remove rare genes
tab <- tab[ apply(tab,1, median)> 5,]

tabNorm <- tab
for (i in 1:ncol(tab)){
  colSum = sum(tab[,i])
  tabNorm[,i] =tabNorm[,i]/colSum
}

day2tab <- tabNorm[1:3]
week12tab <- tabNorm[4:6]
week18tab <- tabNorm[7:11]

pvals <- vector(length=nrow(tabNorm))

for (i in 1:nrow(tabNorm)){
  pvals[i] <- t.test(day2tab[i,],week12tab[i,])$p.value
}
hist(pvals,breaks=50,main='Uncorrected p-vals (D2 vs W12)')

paste("Number of hits if using threshold p<0.05:", sum(pvals <= 0.05))

paste("Number of hits if using threshold p<1.66667e-5:", sum(pvals <= 0.05/nrow(tabNorm)))

pvalsBH <- p.adjust(pvals,method='BH')
paste("Number of hits if using threshold p<0.05:", sum(pvalsBH <= 0.05))





pvals <- vector(length=nrow(tabNorm))

for (i in 1:nrow(tabNorm)){
  pvals[i] <- t.test(day2tab[i,],week18tab[i,])$p.value
}
hist(pvals,breaks=50,main='Uncorrected p-vals (D2 vs W18)')

paste("Number of hits if using threshold p<0.05:", sum(pvals <= 0.05))

paste("Number of hits if using threshold p<1.66667e-5:", sum(pvals <= 0.05/nrow(tabNorm)))

pvalsBH <- p.adjust(pvals,method='BH')
paste("Number of hits if using threshold p<0.05:", sum(pvalsBH <= 0.05))





pvals <- vector(length=nrow(tabNorm))

for (i in 1:nrow(tabNorm)){
  pvals[i] <- t.test(week12tab[i,],week18tab[i,])$p.value
}
hist(pvals,breaks=50,main='Uncorrected p-vals (W12 vs W18)')

paste("Number of hits if using threshold p<0.05:", sum(pvals <= 0.05))

paste("Number of hits if using threshold p<1.66667e-5:", sum(pvals <= 0.05/nrow(tabNorm)))

pvalsBH <- p.adjust(pvals,method='BH')
paste("Number of hits if using threshold p<0.05:", sum(pvalsBH <= 0.05))


