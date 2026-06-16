#!/usr/bin/env python3
import os, sys
import pandas as pd
import numpy as np

# -----------------------------
# INPUT CHECK
# -----------------------------
assert len(sys.argv) > 2, "You must enter filename and output"
filepath = sys.argv[1]
assert os.path.isfile(filepath), "The file must be valid"

# -----------------------------
# LOAD DATA
# -----------------------------
data = pd.read_csv(filepath, sep=",", comment=";")
data.columns = ["t", "V"]

t = data["t"].to_numpy()
v = data["V"].to_numpy()

# -----------------------------
# DAC PARAMETERS
# -----------------------------
t0 = 5e-6
dt = 10e-6
N = 2**6

targets = t0 + np.arange(N) * dt

# -----------------------------
# SAMPLE (interpolation = ważne!)
# -----------------------------
points_table = np.interp(targets, t, v)

# -----------------------------
# NORMALIZACJA KIERUNKU DAC
# -----------------------------
# jeśli DAC maleje → odwracamy OŚ ANALIZY
if points_table[-1] < points_table[0]:
    points_table = points_table[::-1]

# -----------------------------
# LSB (LEPIEJ Z FITU NIŻ RANGE!)
# -----------------------------
k = np.arange(N)
a, b = np.polyfit(k, points_table, 1)
v_fit = a * k + b

Vlsb = a  # slope = ideal step

# -----------------------------
# DNL / INL (datasheet style)
# -----------------------------
DNL = np.diff(points_table) / Vlsb - 1
INL = (points_table - v_fit) / Vlsb

# -----------------------------
# OUTPUT
# -----------------------------
np.savetxt(
    sys.argv[2],
    np.column_stack([np.arange(N-1), DNL, INL[:-1]]),
    delimiter=",",
    header="code,DNL_LSB,INL_LSB",
    comments=""
)

print(f"INL peak / LSB: {np.max(np.abs(INL))}")
print(f"DNL peak / LSB: {np.max(np.abs(DNL))}")
print(f"Monotonic: {np.all(np.diff(points_table) > 0)}")
