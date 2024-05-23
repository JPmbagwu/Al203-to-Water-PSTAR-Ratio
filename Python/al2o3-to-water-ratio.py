#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 21 11:13:17 2024

@author: johnpaulmbagwu
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Read the TXT data file containing information about Liquid Water
df_water = pd.read_csv('WATER.TXT', delimiter=' ')

# Extract the stopping power and energy columns from the dataframe
stopping_power_water = df_water['TotalStp.Pow']
energy_water = df_water['KineticEnergy']

# Read the TXT data file containing information about Al2O3
df_al2o3 = pd.read_csv('ALUMINUMO.TXT', delimiter=' ')

# Extract the stopping power and energy columns from the dataframe
stopping_power_al2o3 = df_al2o3['TotalStp.Pow']
energy_al2o3 = df_al2o3['KineticEnergy']

# Normalize the stopping power to 150 MeV
normalization_energy = 150  # MeV
normalization_index_water = np.where(energy_water == normalization_energy)[0]
normalization_index_al2o3 = np.where(energy_al2o3 == normalization_energy)[0]

if normalization_index_water.size == 0 or normalization_index_al2o3.size == 0:
    raise ValueError("Normalization energy not found in the data.")

normalized_stopping_power_water = stopping_power_water / stopping_power_water[normalization_index_water].values[0]
normalized_stopping_power_al2o3 = stopping_power_al2o3 / stopping_power_al2o3[normalization_index_al2o3].values[0]

# Interpolate stopping power data for Al2O3 to match the energy values of Water
interpolated_stopping_power_al2o3 = np.interp(energy_water, energy_al2o3, normalized_stopping_power_al2o3)

# Calculate the Al2O3-to-Water stopping power ratio
stopping_power_ratio = interpolated_stopping_power_al2o3 / normalized_stopping_power_water

# Plotting
plt.figure(figsize=(10, 6))

# Plotting the Al2O3-to-Water stopping power ratio
plt.plot(energy_water, stopping_power_ratio, label='Al2O3-to-Water Stopping Power Ratio')

plt.title('Al2O3-to-Water Stopping Power Ratio')
plt.xlabel('Energy (MeV)')
plt.ylabel('Stopping Power Ratio')

# Set the x-axis limits to 0 MeV and 250 MeV
plt.xlim(0, 2500)

# Set the y-axis limits for better visibility
plt.ylim(0, max(stopping_power_ratio) * 1.1)

plt.grid(True)
plt.legend()

plt.show()
