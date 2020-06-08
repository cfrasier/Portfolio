library("nlme")
rm(list=ls())

numHospitalsPerGroup <- 3
sampleSize <- 5

getSimData <- function()
{
  index <- 1
  hospitalIndex <-1
  drugIndex <-1
  data <- vector()
  hospital <- vector()
  drug <- vector()
  
  for( i in 1:(numHospitalsPerGroup*2))
  {
    hospitalEffect <- rnorm( 1,mean=0, sd=50)
    
    for( j in 1:sampleSize)
    {
      data[index] <- rnorm(1,mean=hospitalEffect , sd=50)
      hospital[index] <- paste("H", hospitalIndex , sep="")
      drug[index] <- paste("D", drugIndex,sep="")
      index <- index + 1
    }
    
    hospitalIndex <- hospitalIndex + 1
    drugIndex <- drugIndex + 1
    
    if( drugIndex > 2 ) 
      drugIndex = 1
  }
  
  myT <- data.frame(data,hospital,drug)
  
}

print(myT <- getSimData())
print(myT$hospital)
print(c(myT$data,myT$hospital))
plot(myT$data~myT$hospital)