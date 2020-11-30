library(tidyverse)
library(tidytext)
library(igraph)
library(ggraph)
library(ggplot2)

dat <- read_csv("followers_powerlaw.csv")

x <- dat$degree
y <- dat$count

#plot(x, y, main="Degree distribution from followers network", ylab='Count of users', xlab='Degree', log="x")
p <- ggplot(dat, aes(x=x, y=y)) + geom_point() + geom_smooth() + scale_x_log10(breaks=c(10,100,1000,5000,10000), limits=c(20,250000)) + ggtitle("Degree distribution from followers network") + xlab("Number of followers/Degree") + ylab("Count of users")
p + + ggtitle("Degree distribution from followers network") + xlab("Number of followers/Degree") + ylab("Count of users")

dat1 <- read_csv("retweet_Degree.csv")

x1 <- dat1$degree
y1 <- dat1$count

#plot(x, y, main="Degree distribution from followers network", ylab='Count of users', xlab='Degree', log="x")
p1 <- ggplot(dat1, aes(x=x1, y=y1)) + geom_point() + geom_smooth() + scale_x_log10(breaks=c(1,10,100,1000), limits=c(1,2000)) + scale_y_log10(breaks=c(1,10,100,1000,10000), limits=c(1,10000))
p1 + ggtitle("Degree distribution from retweets network") + xlab("Number of retweets/Degree") + ylab("Count of users")
