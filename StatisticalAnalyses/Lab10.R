options(width=10000)

### Question A ###
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

timepoints <- c(rep("day2",length=3),rep("day86",length=3),rep("day128",length=5))

pvals <- vector(length=nrow(tabNorm))
residualsA <- vector(length=nrow(tabNorm))

for( i in 1:nrow(tabNorm)) 
{
  myData <- as.numeric( tabNorm[i,] ) 
  myLm <- lm(myData ~ timepoints,x=TRUE)
  pvals[i] <- anova(myLm)$ "Pr(>F)"[1]
  residualsA[i] <- sum(residuals(myLm)^2)
}
pValuesOneWayAnova <- pvals
hist(pValuesOneWayAnova,breaks=20)
pvalsBH <- p.adjust(pvals,method='BH')
paste("Number of hits if using threshold of FDR 5%:", sum(pvalsBH <= 0.05))


### Question B ###

timepointsNum <- c(rep(2,length=3),rep(86,length=3),rep(128,length=5))

pvals <- vector(length=nrow(tabNorm))
residualsB <- vector(length=nrow(tabNorm))

for( i in 1:nrow(tabNorm)) 
{
  myData <- as.numeric( tabNorm[i,] ) 
  myLm <- lm(myData ~ timepointsNum,x=TRUE)
  pvals[i] <- anova(myLm)$ "Pr(>F)"[1]
  residualsB[i] <- sum(residuals(myLm)^2)
}

pValuesRegression <- pvals
hist(pValuesRegression,breaks=20)
pvalsBH <- p.adjust(pvals,method='BH')
paste("Number of hits if using threshold of FDR 5%:", sum(pvalsBH <= 0.05))

### Question C ###

pvals <- vector(length=nrow(tabNorm))

for (i in 1:length(residualsA)){
  f <- ((residualsB[i]-residualsA[i])/1)/(residualsA[i]/8)
  pvals[i] <- pf(f,1,8,lower.tail=FALSE)
}

pValueModelDiff <- pvals
hist(pValueModelDiff,breaks=20)
pvalsBH <- p.adjust(pvals,method='BH')
paste("Number of hits if using threshold of FDR 5%:", sum(pvalsBH <= 0.05))

### Question D ###

index <- 1:nrow(tabNorm)
myFrame <- data.frame( index, pValuesOneWayAnova,pValuesRegression,pValueModelDiff)

myFrame <- myFrame[ order(myFrame$pValuesOneWayAnova), ] 

boxplot( as.numeric( tabNorm[ myFrame$index[1],]) ~ timepoints,main="Top Anova 3 Param Hit") 


myFrame <- myFrame[ order(myFrame$pValuesRegression), ] 

boxplot( as.numeric( tabNorm[ myFrame$index[1],]) ~ timepointsNum,main="Top Anova 2 Param Hit") 
regressionLm <- lm(as.numeric( tabNorm[ myFrame$index[1],]) ~ timepointsNum,x=TRUE)
abline(regressionLm,col="red")


myFrame <- myFrame[ order(myFrame$pValueModelDiff), ] 

boxplot( as.numeric( tabNorm[ myFrame$index[1],]) ~ timepoints,main="Top Different Model Hit") 
