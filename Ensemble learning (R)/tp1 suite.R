require(ElemStatLearn)
require(class)
require(caret)

data("mixture.example")
x<-data.frame(mixture.example$x)
dim(x)
y<-as.factor(mixture.example$y)
table(y)
c1 <- makePSOCKcluster(6)
registerDoParallel(c1)

trControl<-trainControl(method="repeatedcv",number=5,repeats=10)
K=c(1,3,5,7,9,11,15,17,23,25,35,45,55,83,101,151)
fit<-train(x,y,
           method="knn",
           tuneGrid = expand.grid(k=K),
           trControl = trControl,
           metric = "Accuracy")
stopCluster(c1)
plot(fit)
print(fit)
