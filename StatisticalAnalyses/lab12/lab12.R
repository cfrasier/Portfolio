options(width=10000)
options(digits=5)
rm(list=ls())
library("nlme")
setwd("D:/Documents/Schoolfiles/advancedstats/lab11/")

tab <- read.table("prePostPhylum.txt",header=TRUE,sep='\t')
numCols <- ncol(tab)
myColClasses <- c(rep("character",4), rep("numeric", numCols-4))
tab <-read.table("prePostPhylum.txt",header=TRUE,sep="\t",colClasses=myColClasses)


colGenotype <- vector(length=nrow(tab))
colCage <- vector(length=nrow(tab))
colTimepoint <- vector(length=nrow(tab))

for (i in 1:nrow(tab)){
  
  ## Color by genotype ##
  if (tab$genotype[i] == "WT"){
    colGenotype[i] <- "wildtype"
    if (grepl("1",tab$cage[i]) == TRUE)
      colCage[i] <- paste("WT", 1 , sep="")
    else if (grepl("2",tab$cage[i]) == TRUE)
      colCage[i] <- paste("WT", 2 , sep="")
    else if (grepl("3",tab$cage[i]) == TRUE)
      colCage[i] <- paste("WT", 3 , sep="")
    else if (grepl("4",tab$cage[i]) == TRUE)
      colCage[i] <- paste("WT", 4 , sep="")
    else if (grepl("5",tab$cage[i]) == TRUE)
      colCage[i] <- paste("WT", 5 , sep="")
    else if (grepl("6",tab$cage[i]) == TRUE)
      colCage[i] <- paste("WT", 6 , sep="")
  }  else if (tab$genotype[i] == "10-/-"){
    colGenotype[i] <- "IL"
    if (grepl("1",strsplit(tab$cage[i],"_")[[1]][1]) == TRUE)
      colCage[i] <-  paste("IL", 1 , sep="")
    else if (grepl("2",strsplit(tab$cage[i],"_")[[1]][1]) == TRUE)
      colCage[i] <- paste("IL", 2 , sep="")
    else if (grepl("3",strsplit(tab$cage[i],"_")[[1]][1]) == TRUE)
      colCage[i] <- paste("IL", 3 , sep="")
    else if (grepl("4",strsplit(tab$cage[i],"_")[[1]][1]) == TRUE)
      colCage[i] <- paste("IL", 4 , sep="")
    else if (grepl("5",strsplit(tab$cage[i],"_")[[1]][1]) == TRUE)
      colCage[i] <- paste("IL", 5 , sep="")
  }
}

tab$colCage <- factor(colCage)  
tab$genotype <- colGenotype

tab <- tab[tab$time == "POST",]
tabNums<-tab[,4:11]

par(mfrow=c(3,2))

pvalindex <- 1
pvalsall <- c()

for (i in 2:7){
  data <- tabNums[,i]
  cage <- tabNums$colCage
  genotype <- tabNums$genotype
  M.gls <- gls(data~genotype,method="REML",correlation = corCompSymm( form = ~1 | cage),data=tabNums)
  mixed <- lme(data~genotype,method="REML",random=~1|cage,data=tabNums)
  pval <- anova(mixed)$"p-value"[2]
  pvalsall[pvalindex] <- pval
  plot(tabNums[,i]~tabNums$colCage,main=paste(names(tabNums)[i],";mixed lm pval =",signif(pval,4),"; intraclass rho",signif(coef(M.gls$modelStruct[1]$corStruct,unconstrained=FALSE)[[1]],4)))
  pvalindex <- pvalindex + 1
}

pvalsBH <- p.adjust(pvalsall,method='BH')
for (i in 1:length(pvalsBH)){
  if(pvalsBH[i] <= 0.1){
    print(paste("Significant Hit for Genotype Difference at 10% BH FDR:",names(tabNums)[i+1]))
  }
}


