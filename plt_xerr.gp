set term postscript enhanced

set output 'test.ps'


set size square

set arrow from 1,-0.5 to 1,5 nohead lt -1
set bars small

set ytics ("NSC" 0.2, "LAI" 1.2, "VEGC" 2.2, "NPP" 3.2, "GPP" 4.2)

set yrange [-0.5:5]


set xlabel 'CO_2 effect size' offset 0,-1 font ",24"

set tics font ", 20"

set ytics format "{/:Bold %.0s}"

plot 't.txt' using 3:1:4 every 3::0 noti w xerr lt -1 lw 3 lc rgb 'dark-green' ps 2 pt 9, \
     ''      using 3:1:4 every 3::1 noti w xerr lt -1 lw 3 lc rgb 'brown' ps 2 pt 7, \
     ''      using 3:1:4 every 3::2 noti w xerr lt -1 lw 3 lc rgb 'blue' ps 2 pt 5, \
     'o.txt' using 3:1:4:5 noti w xerr lt -1 lw 3 ps 2 pt 6
