devtools:::install_github('QinganZhao/GA')
load('JGSS')
jpY <- jp[, c('MARC')]
Yjp <- as.matrix(log(jpY))
jpX <- jp[, !(names(jp) %in% c('MARC'))]
Xjp <- as.matrix(jpX)
GA:::select(Xjp, Yjp, reg='glm')