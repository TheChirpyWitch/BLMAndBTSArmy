ceb2 <- delete.edges(g, ceb$removed.edges[bridgeObject])

clusterInfo <- clusters(ceb2)

which(clusterInfo$membership == 1)

m <- (matrix('', nrow = 19800, ncol = 1))
cnt = 0

for(i in 1:length(clusters(ceb2)$csize)){
  arrayStr = strsplit(toString(which(clusterInfo$membership == i)), ",")
  #print(which(clusterInfo$membership == i))
  #print(i)
  for(j in 1:length(arrayStr[[1]])){
    cnt = cnt + 1
    #print(trimws(arrayStr[[1]][j]))
    m[cnt,1] <- trimws(arrayStr[[1]][j])
  }
  cnt = cnt + 1
  m[cnt,1] <- ""
}

which(clusterInfo$membership == length(clusters(ceb2)$csize))

which(clusterInfo$membership == 2)

write.csv(m, file = 'C:\\Users\\Anirudh\\Documents\\OneDrive\\SJSU\\CS185C Advanced Practical Computing Topics\\Project Work\\ceb_groups.csv')
