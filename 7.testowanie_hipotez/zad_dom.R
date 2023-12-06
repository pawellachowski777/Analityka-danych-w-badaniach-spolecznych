library(ggplot2)
library(MASS)

dane <- read.table("C:/Users/RafalMista/Desktop/UKSW/7_Dopasowanie/diagnoza/DS_2000-2009_IND_SAV.tab", sep = "\t", header = T)

# indeks wskaźników zadowolenia
# indeks wskaźników zadowolenia
zadowolenie<-dane[,c("ep64_1","ep64_2","ep64_3","ep64_4","ep64_5","ep64_6","ep64_7","ep64_8","ep64_9","ep64_10","ep64_11","ep64_12","ep64_13","ep64_14","ep64_15","ep64_16","ep64_17","ep64_18","ep64_19","ep64_20")]
zadowolenie<-na.omit(zadowolenie)
indeks<-rowSums(zadowolenie)

fit <- fitdistr(indeks, "normal")

# indeks
hist(indeks, freq = F, ylim = c(0,max(hist(indeks,freq=F)$density)))
curve(dnorm(x, fit$estimate[1], fit$estimate[2]), col="red", lwd=2, add=T)


# 1) Policzyć przedziały ufności (ze wzoru) [kwantyl rzęd p w R: qnorm(p, średnia, odch. st.)]
# 2) Oszacować przedziały dla 95% środkowych obserwacji na bazie losowania w oparciu o dopasowany rozkład

# Odpowiedzi:
# 1)
# wzór: https://pl.wikipedia.org/wiki/Przedzia%C5%82_ufno%C5%9Bci#Nieznane_odchylenie_standardowe_%E2%80%93_du%C5%BCa_pr%C3%B3ba_(n_%3E_30)
# błąd standardowy średniej = oszacowanie odchylenia standardowego średniej (odch. standardowe zmiennej/wielkość próby)
se <- sd(indeks)/sqrt(length(indeks))
c(mean(indeks) + qnorm(0.025)*se, mean(indeks) + qnorm(0.975)*se)

# 2) # losujemy, potem stosujemy wzór na przedział ufności dla średniej
symdane<-rnorm(length(indeks),fit$estimate[1], fit$estimate[2])
c(mean(symdane) - qnorm(0.975)*sd(symdane)/sqrt(length(symdane)), mean(symdane) + qnorm(0.975)*sd(symdane)/sqrt(length(symdane)))

# 3) # nie znamy wzoru na błąd standardowy, losujemy 10 000 średnich i szacujemy ich rozkład z symulacji
symdane2<-rep(NA,10000)
for (i in 1:10000) {
  symdane2[i]<-mean(rnorm(length(indeks),fit$estimate[1], fit$estimate[2]))
}
quantile(symdane2,c(0.025,0.975))




