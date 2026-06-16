# Abstrakt


# Cel projektu

Celem projektu było zaprojektowanie układu prostego przetwornika cyfrowo-analogowego (DAC) w technologii CMOS (ams-0.35um) oraz przeprowadzenie symulacji jego działania.
DAC miał posiadać 6-bitowe wejście cyfrowe i gnerować odpowiednie napięcie wyjściowe w zakresie od $V_{min} = 1V$ do $V_{max} = 2V$.

# Wstęp teoretyczny

Przetwornik cyfrowo-analogowy (DAC) to urządzenie elektroniczne, które przekształca sygnał cyfrowy (binarny) na napięcie analogowe w danym zakresi.

# Aparatura i metodyka wykonania

DO wykonania projektu wykorzystano oprogramowanie Cadence Virtuoso w wersji `IC6.1.8-64b.500.6`
oraz innych narzędzi z pakietu Cadence:

```console
Design kit: AMS 410 in Cadence 2019/2020
```

# Projekt układu

W trakcie realizacji projektu zaprojektowano trzy układy:
1. Wzmacniacz operacyjny
2. Klucz dwuwejściowy
3. Przetwornik cyfrowo-analogowy

Dla każdego z tych układów wykonano: schemat, layout, ekstrakt z layoutu oraz opracowano zestaw symulacji (uruchomionych zarówno dla schematu jak i dla ekstraktu).

## Projekt wzmacniacza operacyjnego

Zaprojektowano dwustopniowy wzmacniacz operacyjny.

## Projekt klucza dwuwejściowego

## Projekt przetwornika cyfrowo-analogowego

Przy pomocy wymienionych wyżej elementów, oraz dodatkowych elementów z biblioteki `PRIMLIB` stworzono schemat
6-bitowego przetwornika cyfrowo-analogowego.

Schemat składa się z części wejściowej wykorzystującej lustra prądowe oraz odpowiednie klucze.
Wartość rezystancji $R5$ dobrano tak, aby $I_{R5} = 5\mu A$.
Wartość szerokości tranzystorów $MPi$ (gdzie $i \in \left\{0,1,2,3,4,5\right\}$) dobrano tak,
aby prąd płynący przez każdy z nich był równy $I_{MPi} = 2^i * I_{R5}$, tzn. $w_{MPi} = 2^i * w_{MPi}$.

```{figure} data/dac_schematic2.png
Schemat części wejściowej przetwornika cyfrowo-analogowego.
```

Część wyjściowa wykorzystuje wzmacniacz operacyjny w celu zapewnienia odpowiedniej impedancji wyjściowej oraz wzmocnienia sygnału.

Wartości rezystancji $R1$ i $R2$ dobrano tak, aby napięcie referencyjne $V_{ref} = V_{min}$, korzystając ze wzoru na dzielnik napięcia:

$$
V_{ref} = V_{min} = \frac{R2}{R1 + R2} * V_{DD}
$$

gdzie $V_{DD} = 3.3V$ dla wykorzystywanej technologii.

Poniżej przedstawiono schemat części wyjściowej przetwornika:

```{figure} data/dac_schematic1.png
Schemat części wyjściowej przetwornika cyfrowo-analogowego.
```

### Symulacja po schemacie

Wykonano symulacje shematową typu transient dla całego układu, podając na wejście przetwornika sygnał cyfrowy
o okresie $T_{LSB} = 20 \mu s$.

```{plot} gnuplot
:name: dac_sim_sch
:caption: Zależność napięcia wyjściowego DAC od czasu dla symulacji schematowej oraz zależność napięcia wyjściowego od cyfrowego stanu wejścia.

set datafile separator ","
set datafile commentschars ";"
set xlabel "Czas [us]" font ",24"
set ylabel "Napięcie [U]" font ",24"
set grid ls 2
set grid xtics, mxtics lw 1
set key box font ",24"
set xtics font ",20"
set ytics font ",20"

t0 = 5e-6      # 5 us
dt = 10e-6     # 10 us
f(x) = a*x + b
eps = 2.51e-6 # 2us
fit f(x) 'assets/data/dac_sim_schematic.vcsv' using \
    (((($1-t0)/dt - floor(($1-t0)/dt)) < eps/dt) ? (floor(($1-t0)/dt + 0.5)) : NaN):2 \
    via a,b

set x2label "Stan" font ",24"
set x2tics font ",20"
set x2range [0:2**6]
set xtics 50
set mxtics 5

plot "assets/data/dac_sim_schematic.vcsv" using ($1*1e6):2 with lines lw 2 title "Napięcie wyjściowe przetwornika", \
'assets/data/dac_sim_schematic.vcsv' using \
(((($1-t0)/dt - floor(($1-t0)/dt)) < eps/dt) ? $1*1e6 : 1/0):2 with points title "Punkt pomiaru napięcia w czasie symulacji" pt 7 ps .5, \
f(x) axes x2y2 title "Dopasowanie zależności napięćia od nr stanu.", \
'assets/data/dac_sim_schematic.vcsv' using \
(((($1-t0)/dt - floor(($1-t0)/dt)) < eps/dt) ? (floor(($1-t0)/dt + 0.5)) : NaN):2 with points axes x2y2 title "Napięcie dla danego stanu" pt 7 ps 0.5
```

Dokonano również analizy wyjścia przetwornika w trakcie zmiany stanu wejścia ("szumy" na powyższym wykresie).

```{plot} gnuplot
:caption: Charakterystyka punktu przełączania stanów

set datafile separator ","
set datafile commentschars ";"

t0 = 20e-6
t_prev = 2e-6
dt = 0.15e-6

set xtics font ",20"
set ytics font ",20"
set xlabel "Czas w symulacji [us]" font ",24"
set ylabel "Napięcie wyjściowe [V]" font ",24"
set key box font ",24"

plot "assets/data/dac_sim_schematic.vcsv" using \
(($1 > (t0 - t_prev) && $1 < t0 + dt) ? $1*1e6 : NaN):2 \
with lines lw 2 \
title "Napięcie wyjściowe przetwornika w trakcie zmiany stanu"
```

```{note}
Oscylacje są spowodowane niestabilnością wzmacniacza operacyjnego i w trakcie projektu zostąły częściowo wyeliminowane doborem pojemności sprzężenia zwrotnego.
Obecny stan jest akceptowalny w kontekście niniejszego projektu.
```

Zbadano liniowość przetwornika wyznaczająć jego parametry DNL (Differtential Non-Linearity) oraz INL (Integral Non-Linearity) według wzorów:

$$
\text{DNL}_n = \frac{\Delta V - V_{LSB}}{V_{LSB}} \\
\text{INL} = \sum_n \text{DNL}_n
$$

Gdzie:
- $\Delta V$ to różnica napięcia miedzy schodkami
- $V_{LSB} = \frac{V_{max} - V_{min}}{N-1}$
- $n$ - numer stanu, $n \in \mathbb{N} \cup \left<0, N\right>$

Poniższy wykres przedstawia wartości DNL dla poszczegulnych schodków dla symulacji po schemacie:

```{plot} gnuplot
:caption: Badanie liniowości przetwornika dla symulacji po schemacie

set datafile separator ","
set grid
set key box font ",24"
set xlabel "Stan" font ",24"
set ylabel "DNL" font ",24"
set y2label "INL" font ",24"
set xtics font ",20"
set ytics font ",20"
set xzeroaxis linetype 1 linewidth 2 linecolor rgb "black"
set xtics axis

plot 'assets/data/dac_dnl_schematic.csv' using 1:2 with linespoints pt 3 title "Zależność DNL od stanu", \
'assets/data/dac_dnl_schematic.csv' using 1:3 with linespoints axes x1y2 pt 4 title "Zależność INL od stanu"
```

Wartość całkowego współczynnika nieliniowości wyniosła $\text{INL} = 2.64 * 10^{-15}$

### Layout

Wykonano layout przetwornika korzystając z narzędzie `Layout XL`:

```{figure} data/dac_layout.png
Layout przetwornika cyfrowo-analogowego.
```

Następnie stworzono ekstrakt z layout'u i powturzono symulacje otrzymując następujące wyniki:

```{important}
Z powodu podejrzewanego błędu w extraktorze, ekstrakcji dokonano uwzględniając **wyłącznie pojemności pasożytnicze** (tzw. "C only").
Przy prubie ekstrakcji uwzględniającej opory, układ przestawał działać poprawnie.
```

```{plot} gnuplot
:name: dac_sim_layout
:caption: Zależność napięcia wyjściowego DAC od czasu dla symulacji po ekstrakcji oraz zależność napięcia wyjściowego od cyfrowego stanu wejścia.

set datafile separator ","
set datafile commentschars ";"
set xlabel "Czas [us]" font ",24"
set ylabel "Napięcie [U]" font ",24"
set grid ls 2
set grid xtics, mxtics lw 1
set key box font ",24"
set xtics font ",20"
set ytics font ",20"

t0 = 5e-6      # 5 us
dt = 10e-6     # 10 us
f(x) = a*x + b
eps = 2.51e-6 # 2us
fit f(x) 'assets/data/dac_sim_postext.vcsv' using \
    (((($1-t0)/dt - floor(($1-t0)/dt)) < eps/dt) ? (floor(($1-t0)/dt + 0.5)) : NaN):2 \
    via a,b

set x2label "Stan" font ",24"
set x2tics font ",20"
set x2range [0:2**6]
set xtics 50
set mxtics 5

plot "assets/data/dac_sim_postext.vcsv" using ($1*1e6):2 with lines lw 2 title "Napięcie wyjściowe przetwornika", \
'assets/data/dac_sim_spostext.vcsv' using \
(((($1-t0)/dt - floor(($1-t0)/dt)) < eps/dt) ? $1*1e6 : 1/0):2 with points title "Punkt pomiaru napięcia w czasie symulacji" pt 7 ps .5, \
f(x) axes x2y2 title "Dopasowanie zależności napięćia od nr stanu.", \
'assets/data/dac_sim_postext.vcsv' using \
(((($1-t0)/dt - floor(($1-t0)/dt)) < eps/dt) ? (floor(($1-t0)/dt + 0.5)) : NaN):2 with points axes x2y2 title "Napięcie dla danego stanu" pt 7 ps 0.5
```

Poniższy wykres przedstawia analizę napięcia wyjściowego przetwornika przy zmianie stanu wejściowego:

```{plot} gnuplot
:caption: Charakterystyka punktu przełączania stanów w symulacji po ekstrakcji.

set datafile separator ","
set datafile commentschars ";"

t0 = 20e-6
t_prev = 2e-6
dt = 0.15e-6

set xtics font ",20"
set ytics font ",20"
set xlabel "Czas w symulacji [us]" font ",24"
set ylabel "Napięcie wyjściowe [V]" font ",24"
set key box font ",24"

plot "assets/data/dac_sim_postext.vcsv" using \
(($1 > (t0 - t_prev) && $1 < t0 + dt) ? $1*1e6 : NaN):2 \
with lines lw 2 \
title "Napięcie wyjściowe przetwornika w trakcie zmiany stanu"
```

Wyznaczono równiez charakterystykę liniowości DACa:


```{plot} gnuplot
:caption: Badanie liniowości przetwornika dla symulacji po ekstrakcie

set datafile separator ","
set grid
set key box font ",24"
set xlabel "Stan" font ",24"
set ylabel "DNL" font ",24"
set y2label "INL" font ",24"
set xtics font ",20"
set ytics font ",20"
set xzeroaxis linetype 1 linewidth 2 linecolor rgb "black"
set xtics axis

plot 'assets/data/dac_dnl_postextract.csv' using 1:2 with linespoints pt 3 title "Zależność DNL od stanu", \
'assets/data/dac_dnl_postextract.csv' using 1:3 with linespoints axes x1y2 pt 4 title "Zależność INL od stanu"
```

Całkowa nieliniowość wyniosłą $\text{INL} = -2.88 * 10^{-15}$.

### Porównanie wyników symulacji

```{table} Porównanie wyników symulacji z wartościami oczekiwanymi
| Parametr | Wartość oczekiwana | Wartość w symulacji po schemacie | Wartość w symulacji po ekstrakcie | Jednostka |
|---|---|---|---|---|
| $V_{min}$ | 1 | 1.04 | 1.12 | V |
| $V_{max}$ | 2 | 2.06 | 2.06 | V |
| $\text{INL}_{\text{peak}}$ | 0 | $0.251$ | $0.654$ |  |
```

# Podsumowanie

# Literatura

- prof. dr hab. inż. Marek Idzik - Przetworniki Cyfrowo-Analogowe DAC.
- dr. inż. Tomasz Fiutowski - Integration of Circuits in CMOS Technology.
- dr. Inż. Krzysztof Świentek - Projektowanie układów cyfrowych w środowisku Cadence.
