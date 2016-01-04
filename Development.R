library(dplyr)

change = function(label) {
  return (paste("a", label))
}

test = function(data){
  
  if (mean(data$TRUE.) >= 0.99)
  {
    return(data)
  }
  
  data <- group_by(data, Activity)
  summarized <- summarise(data, mean = mean(TRUE.), n = n())
  colnames(summarized) <- c("Variable", "mean", "n")
  summarized$Variable <- as.character(unlist(lapply(summarized$Variable, change)))
  
  data <- ungroup(data)
  data <- group_by(data, Country)
  summary2 <- summarise(data, mean = mean(TRUE.), n = n())
  colnames(summary2) <- c("Variable", "mean", "n")
  rbind(summarized, summary2)
  data <- ungroup(data)
  
  data <- ungroup(data)
  data <- group_by(data, Sector)
  summary2 <- summarise(data, mean = mean(TRUE.), n = n())
  colnames(summary2) <- c("Variable", "mean", "n")
  summarized <- rbind(summarized, summary2)
  
  data <- ungroup(data)
  data <- group_by(data, PartnerName)
  summary2 <- summarise(data, mean = mean(TRUE.), n = n())
  colnames(summary2) <- c("Variable", "mean", "n")
  summarized <- rbind(summarized, summary2)
  
  if ("husband" %in% colnames(data)) {
  data <- ungroup(data)
  data <- group_by(data, husband)
  summary2 <- summarise(data, mean = mean(TRUE.), n = n())
  colnames(summary2) <- c("Variable", "mean", "n")
  summarized <- rbind(summarized, summary2)
  }
  data <- ungroup(data)
  summarized$value = (1-summarized$mean)*sqrt(summarized$n) 
  #This creates a more simple model that still detects a good amount of loans
  summarized <- summarized[with(summarized, order(-value)), ]

  toremove <- as.character(summarized[1,1])
  print(toremove)
  if (substring(toremove, 1, 1) == "a") {
    data <- subset(data, Activity != substring(toremove, 3))
  }
  else {
    if (toremove == "1" | toremove == "0") 
    {
      data <- subset(data, husband != toremove)
      data$husband <- NULL
    }
    else {
    data <- subset(data, Sector != toremove & Country != toremove & PartnerName != toremove)
    }
  }
  return (test(data))
}

extract = function (id) {
  legit <- c(998356, 998232, 998956, 997331, 996748, 997022, 996082, 999124, 995455, 993810, 993764, 993757, 992994, 993970, 996544, 992516, 992370, 992527, 991868, 993052, 991940, 989604, 990094, 987764, 989302, 988753, 988792, 988407, 987774, 988634, 998356, 996748, 997022, 993764, 992994, 993970, 996544,
             100151, 100005, 998432, 999125, 994989, 995340, 994175, 994610, 991313, 988695, 99207, 1000059,
             1001490, 998506, 999002, 999137, 995920, 995844, 991521, 992822, 992920, 999207, 997118, 997211, 997125)
  if (id %in% legit){
    return ("F")
  }
  else{
    return ("T")
  }
}

data <- read.csv("/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/output.csv")
data <- test(data)
mean(data$TRUE.)
subsetted <- subset(data, TRUE. == 0)
subsetted$checked <- as.vector(unlist(lapply(subsetted$Loan.ID, extract)))
write.csv(data, "newdata.csv")
write.csv(subsetted, file = "changed.csv")