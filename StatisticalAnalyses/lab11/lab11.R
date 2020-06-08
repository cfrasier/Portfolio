options(width=10000)
options(digits = 4)
rm(list=ls())
setwd("D:/Documents/Schoolfiles/advancedstats/lab11/")

tab <- read.table("prePostPhylum.txt",header=TRUE,sep='\t')
numCols <- ncol(tab)
myColClasses <- c(rep("character",4), rep("numeric", numCols-4))
tab <-read.table("prePostPhylum.txt",header=TRUE,sep="\t",colClasses=myColClasses)

tabNums<-tab[,5:10]

colGenotype <- vector(length=nrow(tab))
colCage <- vector(length=nrow(tab))
colTimepoint <- vector(length=nrow(tab))

for (i in 1:nrow(tab)){
  
  ## Color by genotype ##
  if (tab$genotype[i] == "WT"){
    colGenotype[i] <- "red"
    if (grepl("1",tab$cage[i]) == TRUE)
      colCage[i] <- "violetred2"
    else if (grepl("2",tab$cage[i]) == TRUE)
      colCage[i] <- "skyblue"
    else if (grepl("3",tab$cage[i]) == TRUE)
      colCage[i] <- "sienna"
    else if (grepl("4",tab$cage[i]) == TRUE)
      colCage[i] <- "slategray1"
    else if (grepl("5",tab$cage[i]) == TRUE)
      colCage[i] <- "yellow"
    else if (grepl("6",tab$cage[i]) == TRUE)
      colCage[i] <- "tan1"
}  else if (tab$genotype[i] == "10-/-"){
    colGenotype[i] <- "blue"
    if (grepl("1",strsplit(tab$cage[i],"_")[[1]][1]) == TRUE)
      colCage[i] <- "chartreuse"
    else if (grepl("2",strsplit(tab$cage[i],"_")[[1]][1]) == TRUE)
      colCage[i] <- "brown1"
    else if (grepl("3",strsplit(tab$cage[i],"_")[[1]][1]) == TRUE)
      colCage[i] <- "forestgreen"
    else if (grepl("4",strsplit(tab$cage[i],"_")[[1]][1]) == TRUE)
      colCage[i] <- "darkviolet"
    else if (grepl("5",strsplit(tab$cage[i],"_")[[1]][1]) == TRUE)
      colCage[i] <- "darkslategrey"
}
  if (tab$time[i] == "PRE"){
    colTimepoint[i] <- "green"
  }
  else {
    colTimepoint[i] <- "purple"
  }
}

tab$colGenotype <- colGenotype
tab$colCage <- colCage
tab$colTimepoint <- colTimepoint

print(tab)
myPCOA <- princomp(tabNums)

plot(myPCOA$scores[,1],myPCOA$scores[,2],pch=15,col=colGenotype,main="PCA1 vs. PCA2 (by genotype)")
legend("topleft",legend=c("WT","10-/-"),pch=15,col=c("red","blue"))
plot(myPCOA$scores[,1],myPCOA$scores[,2],pch=15,col=tab$colCage,main="PCA1 vs. PCA2 (by cage)")
plot(myPCOA$scores[,1],myPCOA$scores[,2],pch=15,col=tab$colTimepoint,main="PCA1 vs. PCA2 (by Time)")
legend("topleft",legend=c("PRE","POST"),pch=15,col=c("green","purple"))
plot(myPCOA$scores[,1],myPCOA$scores[,2],pch=15,main="All points, no color")

PCA1WT <- c()
PCA1Mut <- c()
PCA2WT <- c()
PCA2Mut <- c()

PCA1Pre <- c()
PCA1Post <- c()
PCA2Pre <- c()
PCA2Post <- c()


for (i in 1:nrow(tab)){
  
  ## Color by genotype ##
  if (tab$genotype[i] == "WT"){
    PCA1WT <- c(PCA1WT,myPCOA$scores[i,1])
    PCA2WT <- c(PCA2WT,myPCOA$scores[i,2])
  } 
  else if (tab$genotype[i] == "10-/-"){
    PCA1Mut <- c(PCA1Mut,myPCOA$scores[i,1])
    PCA2Mut <- c(PCA2Mut,myPCOA$scores[i,2])
  }    
    
  if (tab$time[i] == "PRE"){
    PCA1Pre <- c(PCA1Pre,myPCOA$scores[i,1])
    PCA2Pre <- c(PCA2Pre,myPCOA$scores[i,2])
  }
  else {
    PCA1Post <- c(PCA1Post,myPCOA$scores[i,1])
    PCA2Post <- c(PCA2Post,myPCOA$scores[i,2])
  }
}

paste("P-value for t-test for Genotype Effect on PCA1:", t.test(PCA1WT,PCA1Mut)$p.value)
paste("P-value for t-test for Genotype Effect on PCA2:", t.test(PCA2WT,PCA2Mut)$p.value)
paste("P-value for t-test for Time Effect on PCA1:", t.test(PCA1Pre,PCA1Post)$p.value)
paste("P-value for t-test for Time Effect on PCA2:", t.test(PCA2Pre,PCA2Post)$p.value)

myLm <- lm(myPCOA$scores[,1] ~ colCage , x=TRUE)
paste("P-value for ANOVA for Cage Effect on PCA1:", anova(myLm)$ "Pr(>F)"[1])

myLm <- lm(myPCOA$scores[,2] ~ colCage , x=TRUE)
paste("P-value for ANOVA for Cage Effect on PCA2:", anova(myLm)$ "Pr(>F)"[1])