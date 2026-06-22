# Abstrakt

Zaprojektowano przetwornik DAC w architekturze I-Steering z 6-bitowym wejściem.
Uzyskano napięcie wyjściowe przetwornika w zakresie od $V_{min}=1.04 V$ do $V_{max} = 2.06V$.
Błąd nieliniowości całkowej otrzymano na poziomie $INL=0.289 V_\text{LSB}$ oraz różniczkowej $DNL=0.25 V_\text{LSB}$.

# Cel projektu

Celem projektu było zaprojektowanie układu prostego przetwornika cyfrowo-analogowego (DAC) w technologii CMOS (ams-0.35um) oraz przeprowadzenie symulacji jego działania.

DAC wykonany w architekturze I-Steering miał posiadać 6-bitowe wejście cyfrowe i generować odpowiednie napięcie wyjściowe w zakresie od $V_{min} = 1V$ do $V_{max} = 2V$.

Należało również opracować układ cyfrowy generujący na wyjściu odpowiedni przebieg do sterowania przetwornikiem.

# Aparatura i metodyka wykonania

Do wykonania projektu wykorzystano oprogramowanie Cadence Virtuoso w wersji `IC6.1.8-64b.500.6`
oraz innych narzędzi z pakietu Cadence:

```console
Design kit: AMS 410 in Cadence 2019/2020
```

# Projekt układu

W trakcie realizacji projektu zaprojektowano następujące układy:

1. Wzmacniacz operacyjny
2. Klucz dwuwejściowy
3. Przetwornik cyfrowo-analogowy
4. Cyfrowy generator przebiegów

Dla każdego z układów wykonano schemat elektryczny oraz przeprowadzono odpowiednie symulacje funkcjonalne.

## Projekt wzmacniacza operacyjnego

Zaprojektowano dwustopniowy wzmacniacz operacyjny.

```{figure} data/opamp_schematic.png
:name: opamp_sch

Schemat elektryczny wykorzystanego w projekcie wzmacniacza operacyjnego.
```

Dokonano analizy wzmacniacza operacyjnego w celu wyznaczenia jego podstawowych parametrów.

```{note}
Symulacji dokonano dla wzmacniacza w konfiguracji bufora jak na poniższym schemacie

::::{figure} data/opampsim_schematic.png
:width: 75%

Schemat symulacyjny wzmacniacza operacyjnego.
:::
```

```{plot} gnuplot
:caption: Wzmocnienie oraz margines fazy wzmacniacza operacyjnego.

set datafile separator ","

file = "assets/data/opamp_sim_stb_schematic.csv"

stats file using 2 every ::1::1 nooutput
A0 = STATS_min

A3 = A0 - 3.0

stats file using (($2 <= A3) ? $1 : 1/0) nooutput
f3db = STATS_min

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
:caption: Odpowiedź na skok napięcia wzmacniacza operacyjnego.

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

W poniższej tabeli zestawiono najważniejsze parametry wzmacniacza:

```{table} Podsumowanie statystyk wzmacniacza
:name: opamp_stats

| Parametr | Wartość | Jednostka |
|---|---|---|
| Wzmocnienie przy spadku o 3 dB | 91.4 | dB |
| Częstotliwość graniczna (-3 dB) | 989 | Hz |
| Margines fazy | 76.3 | deg |

```

```{important}
Uzyskane parametry potwierdzają poprawną pracę wzmacniacza oraz jego przydatność jako bufora wyjściowego w projektowanym przetworniku DAC.
```

## Projekt klucza dwuwejściowego

```{admonition} Przełącznik dwuwejściowy

Układ elektroniczny posiadający dwa wejścia: normalnie-otwarte oraz normalnie-zamknięte,
sterowany sygnałem cyfrowym.

::::{figure} data/switch2_symbol.png
:width: 50%

Symbol elektryczny przełącznika.
:::

Na powyższym schemacie pin `IO1` jest wejściem normalnie-otwartym,
natomiast pin `IO3` jest wejściem normalnie-zamkniętym.
```

Układ składa się z inwertera oraz dwóch bramek transmisyjnych (T-Gate).

```{figure} data/switch2_schematic.png
Schemat przełącznika dwuwejściowego.
```

## Projekt przetwornika cyfrowo-analogowego

Przy pomocy wymienionych wyżej elementów oraz dodatkowych elementów z biblioteki `PRIMLIB`
stworzono schemat 6-bitowego przetwornika cyfrowo-analogowego.

Schemat składa się z dwóch części: wejściowej i wyjściowej.

Część wejściowa wykorzystuje lustra prądowe oraz odpowiednie klucze.
Wartość rezystancji $R5$ dobrano tak, aby:

$$
I_{R5}=5\mu A
$$

Szerokości tranzystorów dobrano zgodnie z binarnym ważeniem źródeł prądowych:

$$
I_{MPi}=2^i \cdot I_{R5}
$$

```{figure} data/dac_schematic2.png
Schemat części wejściowej przetwornika cyfrowo-analogowego.
```

Część wyjściowa wykorzystuje wzmacniacz operacyjny.

Wartości rezystancji $R1$ i $R2$ dobrano tak, aby:

$$
V_{ref}=V_{max}
=
\frac{R2}{R1+R2}V_{DD}
$$

gdzie:

$$
V_{DD}=3.3V
$$

```{figure} data/dac_schematic1.png
Schemat części wyjściowej przetwornika cyfrowo-analogowego.
```

### Symulacja przetwornika

Wykonano symulację typu transient dla całego układu, podając na wejście sygnał cyfrowy
o okresie:

$$
T_{LSB}=20\mu s
$$

```{plot} gnuplot
:name: dac_sim_sch
:caption: Zależność napięcia wyjściowego DAC od czasu oraz zależność napięcia wyjściowego od cyfrowego stanu wejścia.

set datafile separator ","
set datafile commentschars ";"
set xlabel "Czas [us]" font ",24"
set ylabel "Napięcie [U]" font ",24"
set grid ls 2
set grid xtics, mxtics lw 1
set key box font ",24"
set xtics font ",20"
set ytics font ",20"

t0 = 5e-6
dt = 10e-6
f(x) = a*x + b
eps = 2.51e-6

fit f(x) 'assets/data/dac_sim_schematic.vcsv' using \
    (((($1-t0)/dt - floor(($1-t0)/dt)) < eps/dt) ? (floor(($1-t0)/dt + 0.5)) : NaN):2 \
    via a,b

set x2label "Stan" font ",24"
set x2tics font ",20"
set x2range [0:2**6]

plot "assets/data/dac_sim_schematic.vcsv" using ($1*1e6):2 with lines lw 2 title "Napięcie wyjściowe przetwornika"
```

Przeanalizowano również zachowanie wyjścia podczas przełączania kolejnych stanów.

```{plot} gnuplot
:caption: Charakterystyka punktu przełączania stanów.

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
Zaobserwowane oscylacje wynikają z dynamiki układu sprzężenia zwrotnego wzmacniacza operacyjnego i pozostają na akceptowalnym poziomie.
```

Zbadano liniowość przetwornika wyznaczając parametry DNL i INL:

$$
\text{DNL}_n = \frac{\Delta V - V_{LSB}}{V_{LSB}}
$$

$$
\text{INL}_m = \sum_{n=0}^{m}\text{DNL}_n
$$

gdzie:

- $\Delta V$ — różnica napięć pomiędzy sąsiednimi stanami,
- $V_{LSB}$ — idealny krok przetwornika,
- $n,m$ — numer stanu.

```{plot} gnuplot
:caption: Badanie liniowości przetwornika.

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

plot 'assets/data/dac_dnl_schematic.csv' using 1:2 with linespoints pt 3 title "DNL", \
'assets/data/dac_dnl_schematic.csv' using 1:3 with linespoints axes x1y2 pt 4 title "INL"
```

### Podsumowanie parametrów DAC

```{table} Porównanie wyników symulacji z wartościami oczekiwanymi

| Parametr | Wartość oczekiwana | Wartość uzyskana | Jednostka |
|---|---|---|---|
| $V_{min}$ | 1 | 1.04 | V |
| $V_{max}$ | 2 | 2.06 | V |
| $\text{INL}_{peak}$ | 0 | 0.289 | $V_{LSB}$ |
| $\text{DNL}_{peak}$ | 0 | 0.25 | $V_{LSB}$ |

```

# Część cyfrowa

Zaprojektowano generator sygnału cyfrowego w języku Verilog pozwalający generować:

- przebieg prostokątny,
- przebieg trójkątny.

Przygotowano odpowiedni testbench i wykonano symulację funkcjonalną.

```{plot} gnuplot
:caption: Wynik symulacji modułu cyfrowego.

set datafile separator ","
set xlabel "Czas [ps]" font ",24"
file = "assets/data/wave_gen_sim_code.csv"
set key box font ",24"

set xtics font ",20"
set ytics font ",20"

set arrow from graph 0, first 63 to graph 1, first 63 \
    nohead dt 2 lc rgb "red"

plot file using 1:4 with lines title "sygnał wyjściowy"
```

```{tip}
Zweryfikowano poprawne działanie generatora dla różnych parametrów amplitudy, okresu oraz kroku przebiegu.
```

## Integracja części analogowej i cyfrowej

Połączono cyfrowy generator przebiegów z projektowanym przetwornikiem DAC.

```{figure} data/daccyfr_schematic.png
Schemat połączenia części cyfrowej i analogowej.
```

Wykonano symulację kompletnego układu.

```{figure} data/daccyfrsim_schematic.png
Układ symulacyjny dla całości układu.
```

Otrzymano następujący przebieg napięcia wyjściowego:

```{plot} gnuplot
:caption: Zależność napięcia od czasu dla kompletnego układu DAC.

set datafile separator ","
file = "assets/data/daccyfr_sim_schematic.csv"

set xtics font ",20"
set ytics font ",20"
set grid
set xlabel "Czas [s]" font ",24"
set ylabel "Napięcie [V]" font ",24"
set key box font ",24"

plot file using 1:2 with lines title "Wyjście przetwornika cyfrowo-analogowego"
```

# Podsumowanie

Celem projektu było zaprojektowanie i zweryfikowanie działania 6-bitowego przetwornika cyfrowo-analogowego w architekturze I-Steering wraz z cyfrowym generatorem sygnałów sterujących.

W ramach projektu wykonano schematy poszczególnych bloków funkcjonalnych oraz przeprowadzono symulacje pozwalające na ocenę parametrów układu.

Przeprowadzone analizy potwierdziły poprawne działanie przetwornika oraz możliwość generowania napięcia wyjściowego w zakładanym zakresie od około $1V$ do $2V$.

Uzyskane wartości nieliniowości różniczkowej i całkowej pozostają na akceptowalnym poziomie dla założeń projektu.

Dodatkowo zaprojektowano wzmacniacz operacyjny pełniący funkcję bufora wyjściowego oraz cyfrowy generator przebiegów umożliwiający automatyczne sterowanie przetwornikiem.

Symulacja kompletnego systemu potwierdziła poprawną współpracę części analogowej i cyfrowej.

Uzyskane wyniki pokazują, że zaprojektowany układ spełnia założenia funkcjonalne projektu i może stanowić podstawę do dalszej optymalizacji pod kątem dokładności i liniowości przetwarzania.

# Literatura

- prof. dr hab. inż. Marek Idzik — Przetworniki Cyfrowo-Analogowe DAC.
- dr inż. Tomasz Fiutowski — Integration of Circuits in CMOS Technology.
- dr inż. Krzysztof Świentek — Projektowanie układów cyfrowych w środowisku Cadence.
