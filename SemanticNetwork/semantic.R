library(tidyverse)
library(tidytext)
library(igraph)
library(ggraph)
data(stop_words)
dat <- read_csv("original_tweets.csv") %>% 
  transmute(
    id = 1:nrow(.), # headline identification number for reference
    text = gsub("[-/]", " ", tweet),
    text = tolower(gsub("[^A-Za-z ]", "", text))
  ) %>% 
  unnest_tokens(word, text) %>% 
  anti_join(stop_words, by = "word") %>% 
  filter(word != "uddudcc" & word != "tco" & word != "weure" & word != "nhttps" & word != "de") # corpus-specific stop word


dat1 <- read_csv("original_tweets.csv") %>% 
  transmute(
    id = 1:nrow(.), # headline identification number for reference
    text = gsub("[-/]", " ", tweet),
    text = tolower(gsub("[^A-Za-z ]", "", text))
  ) %>% 
  unnest_tokens(word, text, token = "ngrams", n = 2) %>% 
  anti_join(stop_words, by = "word") %>% 
  filter(word != "uddudcc" & word != "tco" & word != "weure" & word != "nhttps" & word != "de") # corpus-specific stop word


cosine_matrix <- function(tokenized_data, lower = 0, upper = 1, filt = 0) {
  
  if (!all(c("word", "id") %in% names(tokenized_data))) {
    stop("tokenized_data must contain variables named word and id")
  }
  
  if (lower < 0 | lower > 1 | upper < 0 | upper > 1 | filt < 0 | filt > 1) {
    stop("lower, upper, and filt must be 0 <= x <= 1")
  }
  
  docs <- length(unique(tokenized_data$id))
  
  out <- tokenized_data %>%
    count(id, word) %>%
    group_by(word) %>%
    mutate(n_docs = n()) %>%
    ungroup() %>%
    filter(n_docs < (docs * upper) & n_docs > (docs * lower)) %>%
    select(-n_docs) %>%
    mutate(n = 1) %>%
    spread(word, n, fill = 0) %>%
    select(-id) %>%
    as.matrix() %>%
    lsa::cosine()
  
  filt <- quantile(out[lower.tri(out)], filt)
  out[out < filt] <- diag(out) <- 0
  out <- out[rowSums(out) != 0, colSums(out) != 0]
  
  return(out)
}

walktrap_topics <- function(g, ...) {
  wt <- igraph::cluster_walktrap(g, ...)
  
  membership <- igraph::cluster_walktrap(g, ...) %>% 
    igraph::membership() %>% 
    as.matrix() %>% 
    as.data.frame() %>% 
    rownames_to_column("word") %>% 
    arrange(V1) %>% 
    rename(group = V1)
  
  dendrogram <- stats::as.dendrogram(wt)
  
  return(list(membership = membership, dendrogram = dendrogram))
}

cos_mat1 <- cosine_matrix(dat1, lower = .01, upper = .80, filt = .80)

cos_mat <- cosine_matrix(dat, lower = .01, upper = .80, filt = .80)

g <- graph_from_adjacency_matrix(cos_mat, mode = "undirected", weighted = TRUE)
set.seed(1840)
ggraph(g, layout = "nicely") +
  geom_edge_link(aes(alpha = weight), show.legend = FALSE) + 
  geom_node_label(aes(label = name)) +
  theme_void()

topics <- walktrap_topics(g)

par(cex = .6)
plot(topics$dendrogram)

topics$membership %>% 
  group_by(group) %>% 
  summarise(words = paste(word, collapse = ", "))



V(g)$cluster <- arrange(topics$membership, word)$group
set.seed(1840)
ggraph(g, layout = "nicely") +
  geom_edge_link(aes(alpha = weight), show.legend = FALSE) + 
  geom_node_label(
    aes(label = name, color = factor(cluster)), 
    show.legend = FALSE
  ) +
  theme_void()
