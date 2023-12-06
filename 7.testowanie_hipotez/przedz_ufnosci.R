# Milionowa populacja 
pop<-rep(NA,1000000)
p<-0.78

for (i in 1:length(pop)) {
  pop[i]<-ifelse(runif(1,min = 0, max = 1) <= p, 1,0)
}

# Ankieta - 1000 osób
n_prob<-1000
resp<-sample.int(length(pop), size = n_prob) # bias za 1: , prob = (pop+1)/sum(pop+1)

# Wyniki ankiet
wyniki<-pop[resp]

# Szacunek p
p_szac<-sum(wyniki)/n_prob

# Błędy standardowe
se<-sqrt(p_szac*(1-p_szac)/n_prob)

# Przedział ufności dla odsetka: https://pl.wikipedia.org/wiki/Przedzia%C5%82_ufno%C5%9Bci#Przedzia%C5%82_ufno%C5%9Bci_dla_odsetka_(wska%C5%BAnik_struktury)
c(p_szac + qnorm(0.025)*se, p_szac + qnorm(0.975)*se)


# Jak to działa?
l_badan<-1000
badania<-rep(NA,l_badan)

for (b in 1:l_badan) {
  resp_b<-sample.int(length(pop), n_prob)
  wyniki_b<-pop[resp_b]
  p_b<-sum(wyniki_b)/n_prob
  dolny<-p_b - qnorm(0.975)*sqrt(p_b*(1-p_b)/n_prob)
  gorny<-p_b + qnorm(0.975)*sqrt(p_b*(1-p_b)/n_prob)
  badania[b]<-ifelse(p < dolny | p > gorny, 0, 1)
}

sum(badania)/length(badania)

# 1. Jak zmieni się przedział ufności, gdy obniży się poziom ufności? 
# przy 95% 0.7428773 0.7951227 przy 90% 0.7698511 0.8121489
# im większy poziom ufności tym szerszy zakres, orzy 100% łapie wszystko, kążdą odpowiedź

# 2. Jak zmieni się przedział ufności, gdy zmniejszy się próbę (mniej ankietowanych osób)?
# przy 1000 0.7428773 0.7951227 przy 700 0.7075061 0.7724939
# zmniejszy się, im większa próba, tym większa jakość (przedziały mniejsze)

# 3. Jak zmieni się przedział ufności, gdy zmniejszy się populacja?
# przy 1 mln 0.7428773 0.7951227 przy 0,5 mln 0.7356055 0.7883945
# nie zmieni się

# 4. Jak zmieni się przedział ufności, gdy p populacyjny będzie bardzo niski?
# przy 78 0.7428773 0.7951227 przy 0.05 0.03475088 0.06124912


# 5. Jak zmieni się przedział ufności, gdy "1" będą bardziej prawdopodobne do ankietowania?


