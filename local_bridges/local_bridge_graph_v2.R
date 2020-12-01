
g1<-graph.empty(n=12061, directed=TRUE)

for(e in E(g)){
  v<-ends(g,E(g)[e])
  grpV1 = -1
  grpV2 = -1
  
  connection <- file("C:\\Users\\Anirudh\\Documents\\OneDrive\\SJSU\\CS185C Advanced Practical Computing Topics\\Project Work\\cebs_groups_v2.csv")
  
  open(connection)
  
  line <- readLines(connection, n=1)
  
  cnt = 1
  while(length(line) > 0) {
    if(cnt > 1){
      line1_elements <- strsplit(line, ",")
      
      if(line1_elements[[1]][2] == v[1]){
        grpV1 = strtoi(line1_elements[[1]][3])  
      }else if(line1_elements[[1]][2] == v[2]){
        grpV2 = strtoi(line1_elements[[1]][3])
      }
      edgeFlag <- (grpV1 != -1 && grpV2 != -1 && grpV1 != grpV2)
      if(edgeFlag){
        edges <- c(grpV1, grpV2)
        
        nwedges <- gsub(",","",edges)
        
        if(!are.connected(g1, grpV1, grpV2)){
          g1 <- add.edges(g1,nwedges)
        }
        
        close(connection)
        
        break
      }
      
    }
    line <- readLines(connection, n=1)
    
    cnt = cnt + 1
  }
}

E(g1)

m <- (matrix('', nrow = 5909, ncol = 2))

for(e in 1:5909){
  v<-ends(g1,E(g1)[e])
  m[e,1] <- v[1]
  m[e,2] <- v[2]
}

write.csv(m, file = 'C:\\Users\\Anirudh\\Documents\\OneDrive\\SJSU\\CS185C Advanced Practical Computing Topics\\Project Work\\grouped_clusters.csv')

deg<-degree(g1, mode="in")

deg

V(g1)$defaultSize = ifelse((deg>1),ifelse((deg>3),10*2,10*1.3),3)

E(g1)$defaultSize = 5

plot(g1, vertex.size =  V(g1)$defaultSize, vertex.label = NA, edge.width = E(g1)$defaultSize)

save.image()
