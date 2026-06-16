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

```{figure} data/opamp_schematic.png
:name: opamp_sch

Schemat elektryczny wykorzystanego w projekcie wzmacniacza operacyjnego.
```

Dokonano analizy wzmacniacza operacyjnego w celu uzyskania jego parametrów.

```{note}
Symulacji dokonano dla wzmacniacza w konfiguracji bufora jak na poniższym schemacie

::::{figure} data/opampsim_schematic.png
:width: 50%
Schemat symulacyjny wzmacniacza operacyjnego.
::::

```

```{plot} gnuplot
:caption: Wzmocnienie oraz margines fazy wzmacniacza operacyjnego w symulacji po schemacie.

set datafile separator ","

file = "assets/data/opamp_sim_stb_schematic.csv"

# Wzmocnienie przy najniższej częstotliwości
stats file using 2 every ::1::1 nooutput
A0 = STATS_min

# Poziom -3 dB
A3 = A0 - 3.0

# Znalezienie pierwszego punktu poniżej A0-3dB
stats file using (($2 <= A3) ? $1 : 1/0) nooutput
f3db = STATS_min

# Wartość wzmocnienia w tym punkcie
stats file using (($1 == f3db) ? $2 : 1/0) nooutput
gain3db = STATS_min

set logscale x
set grid

set xlabel "Częstotliwość [Hz]" font ",24"

set ylabel "Wzmocnienie [dB]" font ",24"
set y2label "Margines fazy [deg]" font ",24"
set y2tics font ",20"
set ytics font ",20"
set xtics font ",20"

set key left bottom box font ",24"

set arrow from f3db, graph 0 to f3db, graph 1 \
    nohead dt 2 lc rgb "red"

set label sprintf("%.3g -3 dB @ %.3g Hz", A0, f3db) \
    at f3db, gain3db offset 1,1 tc rgb "red"

plot \
    file every ::1 using 1:2 with lines lw 2 title "Loop Gain", \
    file every ::1 using 3:(180+$4) axes x1y2 with lines lw 2 title "Phase Margin", \
    '+' using (f3db):(gain3db) with points pt 7 ps 1.5 lc rgb "red" notitle
```

Na poniższym wykresie przedstawiono odpowiedź wzmacniacza na skok napięcia.

```{plot} gnuplot
:caption: Odpowiedź na skok napięcia wzmacniacza operacyjnego w symulacji po schemacie.

set datafile separator ","
file = "assets/data/opamp_sim_tran_schematic.csv"

set xlabel "Czas [s]" font ",24"
set ylabel "Napięcie [V]" font ",24"
set key box font ",24"
set xtics font ",20"
set ytics font ",20"

plot file using 1:2 with lines title "Odpowiedź wzmacniacza", \
file using 1:4 with lines title "Przebieg idealny"
```

Dla schematu {numref}`opamp_sch` wykonano layout:

```{figure} data/opamp_layout.png
Layout wzmacniacz operacyjnego.
```

Następnie przeprowadzono analogiczną analize wzmacniacza dla extraktu z layoutu.

```{plot} gnuplot
:caption: Wzmocnienie oraz margines fazy wzmacniacza operacyjnego w symulacji po ekstrakcie.

set datafile separator ","

file = "assets/data/opamp_sim_stb_postext.csv"

# Wzmocnienie przy najniższej częstotliwości
stats file using 2 every ::1::1 nooutput
A0 = STATS_min

# Poziom -3 dB
A3 = A0 - 3.0

# Znalezienie pierwszego punktu poniżej A0-3dB
stats file using (($2 <= A3) ? $1 : 1/0) nooutput
f3db = STATS_min

# Wartość wzmocnienia w tym punkcie
stats file using (($1 == f3db) ? $2 : 1/0) nooutput
gain3db = STATS_min

set logscale x
set grid

set xlabel "Częstotliwość [Hz]" font ",24"

set ylabel "Wzmocnienie [dB]" font ",24"
set y2label "Margines fazy [deg]" font ",24"
set y2tics font ",20"
set ytics font ",20"
set xtics font ",20"

set key left bottom box font ",24"

set arrow from f3db, graph 0 to f3db, graph 1 \
    nohead dt 2 lc rgb "red"

set label sprintf("%.3g -3 dB @ %.3g Hz", A0, f3db) \
    at f3db, gain3db offset 1,1 tc rgb "red"

plot \
    file every ::1 using 1:2 with lines lw 2 title "Loop Gain", \
    file every ::1 using 3:(180+$4) axes x1y2 with lines lw 2 title "Phase Margin", \
    '+' using (f3db):(gain3db) with points pt 7 ps 1.5 lc rgb "red" notitle
```

Na poniższym wykresie przedstawiono odpowiedź wzmacniacza na skok napięcia.

```{plot} gnuplot
:caption: Odpowiedź na skok napięcia wzmacniacza operacyjnego w symulacji po ekstrakcie.

set datafile separator ","
file = "assets/data/opamp_sim_tran_postext.csv"

set xlabel "Czas [s]" font ",24"
set ylabel "Napięcie [V]" font ",24"
set key box font ",24"
set xtics font ",20"
set ytics font ",20"

plot file using 1:2 with lines title "Odpowiedź wzmacniacza", \
file using 1:4 with lines title "Przebieg idealny"
```

```{table} Podsumowanie statystyk wzmacniacza
| Parametr | Schemat | Layout | Jednostka |
|---|---|---|---|
| Wzmocnienie przy spadku o 3dB | 91.4 | 91.4 | dB |
| Częstotliwość, przy któ©ej wzmocnienie spadło o 3dB | 989  | 989 | Hz |
| Margines fazy | 76.3 | 74.13 | deg |

```

## Projekt klucza dwuwejściowego

```{admonition} Przełącznik dwuwejściowy
Układ elektroniczny posiadająćy dwa wejścia: normalnie-otwarrte oraz normalnie-zamknięte,
sterowany sygnałem cyfrowym.

::::{figure} data/switch2_symbol.png
:width: 50%
Symbol elektryczny przełącznika
::::

Na powyższym schemacie pin `IO1` jest wejściem normalnie-otwartym (ponieważ przy $S=0$ nie przewodzi),
natomiast pin `IO3` to wejście normalnie-zamknięte (gdyż przy $S=0$ przewodzi).

```

Ukłąd skłąda się z inwertera oraz dwuch bramek transmisyjnych (T-Gate).

```{figure} data/switch2_schematic.png
Schemat przełącznika dwuwejściowego.
```

Następnie wykonano jego layout:

```{figure} data/switch2_layout.png
Layout przełąćznika dwuwejściowego.
```

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
set y2tics font ",20"

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
set key box right bottom font ",24"
set xlabel "Stan" font ",24"
set ylabel "DNL" font ",24"
set y2label "INL" font ",24"
set xtics font ",20"
set ytics font ",20"
set xzeroaxis linetype 1 linewidth 2 linecolor rgb "black"
set xtics axis
set y2tics font ",20"

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
| $\frac{\text{INL}_{\text{peak}}}{V_{LSB}}$ | 0 | $0.289$ | $0.369$ |  |
| $\frac{\text{DNL}_{\text{peak}}}{V_{LSB}}$ | 0 | $0.25$ | $0.652$ |  |
```

# Część cyfrowa

# Podsumowanie

# Literatura

- prof. dr hab. inż. Marek Idzik - Przetworniki Cyfrowo-Analogowe DAC.
- dr. inż. Tomasz Fiutowski - Integration of Circuits in CMOS Technology.
- dr. Inż. Krzysztof Świentek - Projektowanie układów cyfrowych w środowisku Cadence.
