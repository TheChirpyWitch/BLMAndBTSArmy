library(tidyverse)
library(tidytext)
library(igraph)
library(ggraph)
library(ggplot2)

dat <- read_csv("followers_powerlaw.csv")

x <- dat$degree
y <- dat$count

#plot(x, y, main="Degree distribution from followers network", ylab='Count of users', xlab='Degree', log="x")
ggplot(dat, aes(x=x, y=y)) + geom_point() + geom_smooth() + scale_x_log10(breaks=c(10,100,1000,5000,10000), limits=c(20,250000))
