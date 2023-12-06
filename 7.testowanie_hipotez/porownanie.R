# Różne poparcia w różnych miastach
pm1<-0.7
pm2<-0.68

miasto1<-ifelse(runif(100000,min = 0, max = 1) <= pm1, 1,0) # Każdy mieszkaniec 100 tys. miasta ma przypisane poparcie
miasto2<-ifelse(runif(100000,min = 0, max = 1) <= pm2, 1,0)

n_prob<-1000 # Ankieta dla 1000 osób
resp1<-sample.int(length(miasto1), size = n_prob) # Losowanie w mieście 1
resp2<-sample.int(length(miasto2), size = n_prob) # Losowanie w mieścid 2

wyniki1<-miasto1[resp1] # Wyniki ankiet
wyniki2<-miasto2[resp2]

c(sum(wyniki1)/n_prob, sum(wyniki2)/n_prob) # Oszacowane poparcia w mieście 1 i mieście 2

# Ważne parametry
# średnie
p1_sz<-sum(wyniki1)/n_prob # = mean(wyniki1)
p2_sz<-sum(wyniki2)/n_prob # = mean(wyniki2)
# bł. standardowe (czyli oszacowania odch. standardowych średnich)
se1<-sqrt(p1_sz*(1-p1_sz)/n_prob)
se2<-sqrt(p2_sz*(1-p2_sz)/n_prob)

# Czy te dwie wartości są "statystycznie różne"?

# Przedział ufności
# Symulacja
n_sim<-100000
p.miasto1<-rnorm(n_sim, p1_sz, se1) # 100 000 losowych średnich/odsetków poparcia z parametrów dla miasta 1
p.miasto2<-rnorm(n_sim, p2_sz, se2) # 100 000 losowych średnich/odsetków poparcia z parametrów dla miasta 2
roznica <- p.miasto1 - p.miasto2
quantile(roznica,c(0.025,0.975))

# Bezmyślna symulacja
n_sim<-100000
p.miasto1<-rep(NA,n_sim)
p.miasto2<-rep(NA,n_sim)
for (s in 1:n_sim) {
  p.miasto1[s]<-mean(rbinom(1000,1,p1_sz)) # 100 000 losowych średnich/odsetków poparcia z parametrów dla miasta 1
  p.miasto2[s]<-mean(rbinom(1000,1,p2_sz)) # 100 000 losowych średnich/odsetków poparcia z parametrów dla miasta 2
}

roznica <- p.miasto1 - p.miasto2
quantile(roznica,c(0.025,0.975))

# https://pl.wikipedia.org/wiki/Test_dla_proporcji#Testy_dla_dw%C3%B3ch_proporcji

# Testowanie hipotez
# Hipoteza zerowa: pm1 == pm2
# Hipoteza alternatywna: pm1 != pm2

# Sprawdzamy, jak zachowa się statystyka testowa przy założeniu H0
# Założenie H0: pm1 == pm2

# Bezmyślna symulacja (można bezpośrednio ze wzoru: https://online.stat.psu.edu/stat415/lesson/9/9.4)
# Skoro pm1 == pm2, to poparcie z obu miast można sumować
pm12<-(sum(wyniki1)+sum(wyniki2))/(length(wyniki1)+length(wyniki2))
n_sim2<-1000000
# Rozkład statystyki testowej
r_stat_test<-rnorm(n_sim2, pm12, se1)-rnorm(n_sim, pm12, se2) # zakładamy, że średnie te same, ale bł. standardowe różne
# Statystyka testowa
stat_test<-p1_sz-p2_sz
quantile(stat_test,c(0.025,0.975))

# Czy mieści się w środku, czy na krańcach rozkładu?
sum(r_stat_test > stat_test)/n_sim2 # Jeżeli powyżej 0,025 i poniżej 0,975 to w środku na poziomie istotnosci 5%
plot(density(r_stat_test),xlim = c(-stat_test,stat_test))
abline(v = stat_test)


# 1. Jak zmienia się ocena istotności statystycznej przy różnych różnicach między pm1 i pm2?
# Przy wyższych różnicach, istotność statystyczna rośnie.

# 2. Jak zmienia się ocena istotności statystycznej przy różnych wielkościach próby?
# Wielkość próby zwiększa precyzję oszacowań. Im większa próba, tym mniejszy błąd standardowy

# 3. Jak zmienia się ocena istotności statystycznej przy różnych wielkościach populacji?
# Wielkość populacji może pośrednio wpłynąć na ocenę instotności statystycznej. Przy bardzo małej próbie
# badanie może objąć dużą część populacji, i nie będzie potrzeby uogólniać rzeczywistości, skoro zbadaliśmy 
# większość populacji

