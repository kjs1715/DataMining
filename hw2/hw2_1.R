Sys.setenv(LANG="en_US.UTF-8")
Needed <- c("XML", "methods", "tm", "SnowballC", "dplyr", "classInt")
# install.packages(Needed, repos="http://cloud.r-project.org")

library(XML)
library(methods)
fileName <- file.path("/Users/kim/Desktop/HW2/nyt_corpus/samples_500")

# corpus loop
corpus_list <- dir(fileName)
dataMatrix <- data.frame()
for (j in 1:length(dir(fileName)))
{
  # read file
  cfile <- file.path(paste("/Users/kim/Desktop/HW2/nyt_corpus/samples_500/", corpus_list[[j]], sep = ''))
  result <- xmlParse(file = cfile)
  
  # nodes for needed parts
  rootNode <- xmlRoot(result)
  attrNode <- xmlSApply(rootNode[["head"]], xmlAttrs)
  classifierNode <- xmlSApply(rootNode[["head"]][["docdata"]][["identified-content"]], xmlAttrs)
  bodyNode <- xmlSApply(rootNode[["body"]][["body.content"]], xmlAttrs)
  
  # init variables 
  data_year <- NULL
  data_month <- NULL
  data_day <- NULL
  data_content <- NULL
  data_category <- NULL
  for(i in 2:(length(attrNode)-2))
  {
    if(attrNode[[i]][[2]] == c("publication_year"))
    {  
      data_year <- attrNode[[i]][[1]]
    }
    if(attrNode[[i]][[2]] == c("publication_month"))
    {
      data_month <- attrNode[[i]][[1]]
    }
    if(attrNode[[i]][[2]] == c("publication_day_of_month"))
    {
      data_day <- attrNode[[i]][[1]]
    }
  }
  cateStr <- ""
  for(i in 1:length(classifierNode))
  {
    tmp <- rootNode[["head"]][["docdata"]][["identified-content"]][[i]]
    jud1 <- startsWith(xmlValue(tmp), "Top/Features/")
    jud2 <- startsWith(xmlValue(tmp), "Top/News/")
    if(!is.na(jud1))
    {
      if(jud1) 
      {
        cateStr <- paste(cateStr, strsplit(xmlValue(tmp), '/')[[1]][3], sep='/')
        next
      }
    }
    if(!is.na(jud2))
    {
      if(jud2)
      {
        cateStr <- paste(cateStr, strsplit(xmlValue(tmp), '/')[[1]][3], sep='/')
        next
      }
    }
  }
  cateStr <- substring(cateStr, 2, nchar(cateStr))
  data_category <- cateStr
  
  if(length(bodyNode) > 0)  # could be null
  {
    for(i in 1:length(bodyNode)) {
      if(bodyNode[[i]] == "full_text")
      {
        data_content <- xmlValue(rootNode[["body"]][["body.content"]][[i]])
      }
    }
  }
  
  # expand with NA if no data there
  if(is.null(data_year)) data_year <- NA
  if(is.null(data_month)) data_month <- NA
  if(is.null(data_day)) data_day <- NA
  if(is.null(data_category)) data_category <- NA
  if(is.null(data_content)) data_content <- NA
  dataTmp <- data.frame(data_year, data_month, data_day, data_category, data_content)
  dataMatrix <- rbind(dataMatrix, dataTmp)

}
# write.csv(dataMatrix, "/Users/kim/Desktop/data.csv", row.names = FALSE)

library(tm)
dataContent <- Corpus(VectorSource(dataMatrix$data_content))
dataContent <- tm_map(dataContent, removePunctuation)
dataContent <- tm_map(dataContent, removeNumbers)
dataContent <- tm_map(dataContent, tolower)
dataContent <- tm_map(dataContent, removeWords, stopwords("english"))
library(SnowballC)
dataContent <- tm_map(dataContent, stemDocument)
dataContent <- tm_map(dataContent, stripWhitespace)

dtm <- DocumentTermMatrix(dataContent)
inspect(dtm)

library(wordcloud)
freq <- colSums(as.matrix(dtm)) # Find word frequencies 
dark2 <- brewer.pal(6, "Dark2")
wordcloud(names(freq), freq, max.words=100, rot.per=0.2, colors=dark2)

library(ggplot2)
lenFreq <- vector()
for(i in 1:dtm[[5]]) 
{
  # print(length(dtm[[6]][[2]][i]))
  lenFreq[i] <- as.character(factor(nchar(dtm[[6]][[2]][i])))
}
newFreq <- numeric(30)
for(i in 1:length(lenFreq))
{
  n <- as.numeric(lenFreq[i])
  newFreq[n] <- newFreq[n] + 1
}

namesNewFreq <- NULL
for(i in 1:33)
{
  namesNewFreq[i] <- i
}

wf <- data.frame(Counts=namesNewFreq, Frequency=newFreq)
p <- ggplot(subset(wf), aes(Counts, Frequency))
p <- p + geom_bar(stat="identity")   
p <- p + theme(axis.text.x=element_text(angle=45, hjust=1))   
p

# width bining
wordCounts <- NULL
for(i in 1:length(dataContent))
{
  dataTmp <- strsplit(dataContent[[i]][[1]][[1]], ' ')
  wordCounts[i] <- lengths(dataTmp)
}
bins <- 10
minValue <- min(wordCounts)
maxValue <- max(wordCounts)
width <- (maxValue - minValue) / bins
wordPlot <- cut(wordCounts, breaks=seq(minValue, maxValue, width))
barplot(table(wordPlot))

# depth(Equal Frequency) binning
library(Hmisc)
wordPlot2 <- table(cut2(wordCounts, m=length(wordCounts)/10))
barplot(wordPlot2)

# statistics for category

category <- as.character(dataMatrix$data_category)
categoryList <- list()
categoryList2 <- list()

for(i in 1:length(category))
{
  categoryList[i] <- strsplit(category[i], '/')
  categoryList2[[i]] <- unique(categoryList[[i]])
}


categoryDF <- data.frame(Type=NULL, Count=NULL)
for(i in 1:length(category))
{
  if(length(categoryList2[[i]]) == 0) 
    next
  for(j in 1:length(categoryList2[[i]]))
  {
    tmp <- categoryList2[[i]][j]
    w <- which(categoryDF$Type == tmp)
    print(i)
    print(j)
    if(tmp %in% categoryDF$Type)
    {
      print(categoryDF[[2]][w])
      categoryDF[[2]][w] <- categoryDF[[2]][w] + 1
    } else {
      tmpDF <- data.frame(Type=tmp, Count=1)
      categoryDF <- rbind(categoryDF, tmpDF)
      print(categoryDF)
    }
  }
}

p2 <- ggplot(subset(categoryDF), aes(Type, Count))
p2 <- p2 + geom_bar(stat="identity")   
p2 <- p2 + theme(axis.text.x=element_text(angle=45, hjust=1)) 
p2

# statistics for month

months <- dataMatrix$data_month
monthsSummary <- summary(months)
monthFreqDF <- data.frame(Month=names(monthsSummary), Freq=monthsSummary)
p3 <- ggplot(subset(monthFreqDF), aes(Month, Freq))
p3 <- p3 + geom_bar(stat="identity")   
p3 <- p3 + theme(axis.text.x=element_text(angle=45, hjust=1)) 
p3



