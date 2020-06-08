options(width=10000)

### Question 1 ###
rm(list=ls())
setwd("D:/Documents/Schoolfiles/advancedstats")
tab <- read.table('cancerdata.txt',header=TRUE,row.names=1)
tab <- apply(tab,2,log10)

plot(tab[,"CumulativeCellDivisions"],tab[,"Lifetime_cancer_risk"])

linmod <- lm(tab[,"Lifetime_cancer_risk"]~tab[,"CumulativeCellDivisions"])

abline(linmod)

plot(linmod)

summary(linmod)

### Question 2 ###
rm(list=ls())
setwd("D:/Documents/Schoolfiles/advancedstats")
casecontrol <- read.table('caseControlData.txt',header=TRUE,row.names=1)

case <- casecontrol[grep("case$",rownames(casecontrol)),]
control <- casecontrol[grep("control$",rownames(casecontrol)),]

key <- sub("case", "", row.names(casecontrol))
key <- sub("control", "", key)
newkey <- vector(length=length(key))
keysplit <-  strsplit(key, "_")
for (i in 1:length(key)){
  newkey[i] <- keysplit[[i]][1]
}


row.names(casecontrol) <- newkey

BMI <- read.table('BMI_Data.txt',fill=TRUE,header=TRUE,row.names=1)
BMI <- na.omit(BMI)

bigdf <- merge(casecontrol,BMI,by="row.names")
pvals <- vector(length=length(casecontrol))

for (i in 1:length(casecontrol)){
  x <- bigdf[[i]]
  y <- bigdf[['bmi']]
  myLm <- lm(y~x)
  pvals[i] <- anova(myLm)$"Pr(>F)"
}

hist(pvals)
pvalsBH <- p.adjust(pvals,method='BH')
print(pvalsBH)
paste("Number of hits if using threshold of FDR 10%:", sum(pvalsBH <= 0.10))