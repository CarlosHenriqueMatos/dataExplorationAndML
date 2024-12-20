(first.vector <- c(1, 3, 5, 9, 10) )

(second.vector <- c(0 , 1, 2, 3, 4, 5, 6, 7, 8, 9))

(length(first.vector))
(length(second.vector))

(first.vector1 <- c(first.vector, second.vector))

firstMATRIX <- matrix(c(2, 4, 3, 1, 5, 7, 6, 15, 9, 99), nrow = 2, ncol = 5, byrow = TRUE)

secondMATRIX <- matrix(c(4, 3, 1, 2, 3, 9, 10, 11, 5, 15), nrow = 2, ncol = 5, byrow = TRUE)

matrix.mean <- mean(firstMATRIX)

#A print, but not necessary when using RStudio
print(matrix.mean)

median.result <- median(firstMATRIX)
print(median.result)
