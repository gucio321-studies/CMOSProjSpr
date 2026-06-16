#!/usr/bin/env python3
import os, sys
import pandas
import numpy as np

assert len(sys.argv) > 2, "You must enter filename and output"
filepath = sys.argv[1]
assert os.path.isfile(filepath), "The file must be valid"

data = pandas.read_csv(filepath_or_buffer=filepath, sep=",", comment=";")
#data = data.rename(columns={'1.040020875811852':'V'})
data.columns = ["0", "V"]

# convert to numpy for speed
t = data["0"].to_numpy()
v = data["V"].to_numpy()

t0 = 5e-6  # 5 ps
dt = 10e-6 # 10 ps
N = 2**6

targets = t0 + np.arange(N) * dt

points_table = np.empty(N)

idx = np.abs(t[:, None] - targets).argmin(axis=0)

points_table[:] = v[idx]

Vmin = min(points_table)
Vmax = max(points_table)
Vlsb = (Vmax-Vmin)/(N-1)

DNL = [(points_table[i-1] - points_table[i]-Vlsb)/Vlsb for i in range(1,N)]
DNL.reverse()
INL = np.cumsum(DNL)
np.savetxt(sys.argv[2], np.column_stack([np.arange(N-1), DNL, INL]), delimiter=",")
print(f"INL peak: {np.max(np.abs(DNL))}")
