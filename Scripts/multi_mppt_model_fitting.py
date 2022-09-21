# -*- coding: utf-8 -*-
"""

@author: cwhanse

Reads a csv file containing data from both Test sequences. Fits the multi-input
inverter model, writes the fitted model to a json file, and makes plots showing quality of model.

"""
import numpy as np
import pandas as pd
import pvlib
import os
import matplotlib.pyplot as plt
import json

plt.rcParams.update({'font.size': 16})

# Read csv file with both Tests combined
path = 'D:\\PVmodeling\\Multi-input inverter'
datafile = 'multi_inverter_combined.csv'

with open(os.path.join(path, datafile), 'r') as infile:
    data = pd.read_csv(infile, index_col=0)

data = data.dropna()

# add voltage labels for model fitting
voltage_levels = {600: 'Vmin', 720: 'Vnom', 800: 'Vmax'}
data['dc_voltage_level'] = np.nan

for i in data.index:
    vs = np.unique(data.loc[i, ['v1', 'v2', 'v3', 'v4', 'v5', 'v6']])
    if len(vs)==1:
        data.loc[i, ('dc_voltage_level')] = voltage_levels[vs[0]]

# extract subset of data where DC power is equal on each input
# this subset is used for model fitting because that is the current CEC 
# practice
balanced_u = ((data['n_derated']==6) | (data['n_derated']==0)) \
                & ~data['dc_voltage_level'].isna()
balanced = data[balanced_u]

fitted = pvlib.inverter.fit_sandia(
    balanced['p_ac'], balanced['p_dc'], balanced['v1'],
    balanced['dc_voltage_level'], p_ac_0=33000, p_nt=5)

with open('inverter_model', 'w') as outfile:
    outfile.write(json.dumps(fitted))

p_dc = np.array(data[['p1', 'p2', 'p3', 'p4', 'p5', 'p6']]).T
v_dc = np.array(data[['v1', 'v2', 'v3', 'v4', 'v5', 'v6']]).T

# Predict AC power at all conditions
predict = pvlib.inverter.sandia_multi(v_dc, p_dc, fitted)
predict_err = (predict - data['p_ac']) / data['p_ac'] * 100

fig = plt.figure()
plt.scatter(data['p_ac'][~balanced_u], predict_err[~balanced_u])
plt.scatter(data['p_ac'][balanced_u], predict_err[balanced_u], marker='s')
plt.ylabel('Error in predicted AC power (%)')
plt.xlabel('Measured AC power (W)')
plt.legend(['All conditions', 'Equal inputs'])
plt.tight_layout()
plt.savefig('ac_power_pred_err.png')

efficiency = data['p_ac'] / data['p_dc'] * 100
effic_pred = predict / data['p_dc'] * 100

fig5 = plt.figure()
labels = []
equal_voltage = ~data['dc_voltage_level'].isna()
temp = data[equal_voltage]
temp_p_dc_sum = temp['p_dc']
temp_predict = predict[equal_voltage]
temp_efficiency = efficiency[equal_voltage]
temp_eff_pred = effic_pred[equal_voltage]
colors = []

for v in voltage_levels:
    labels.append(str(v) + "V")
    labels.append('')
    u = temp['dc_voltage_level'] == voltage_levels[v]
    p = plt.plot(temp_p_dc_sum[u], temp_efficiency[u], '.')
    x = np.asarray([temp_p_dc_sum[u], temp_efficiency[u]]).T
    df = pd.DataFrame(data=x)
    df = df.sort_values(0)
    colors.append(p[0].get_color())

for k, v in enumerate(voltage_levels):
    u = temp['dc_voltage_level'] == voltage_levels[v]
    x = np.asarray([temp_p_dc_sum[u], temp_eff_pred[u]]).T
    df = pd.DataFrame(data=x)
    df = df.sort_values(0)
    plt.plot(df[0], df[1], color=colors[k])

labels = labels[0:-1:2]
plt.xlabel('Total DC power (W)')
plt.ylabel('Efficiency (%)')
plt.legend(labels, loc='lower center', ncol=3)
plt.tight_layout()
plt.savefig('efficiency_vs_dc_power.png')
