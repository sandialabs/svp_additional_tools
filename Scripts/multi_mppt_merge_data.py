# -*- coding: utf-8 -*-
"""

@author: cwhanse

Reads and processes raw data files from Test 1 and Test 2, cleans up outliers
and computes total AC and DC power, and writes a csv file containing results
from both Test sequences.

"""
import numpy as np
import pandas as pd
import os
import re
import glob
import matplotlib.pyplot as plt


plt.rcParams.update({'font.size': 16})


# translate data file column headings to internal column names
PDICT = {'p1': ' PV_P_1', 'p2': ' PV_P_2', 'p3': ' PV_P_3',
         'p4': ' PV_P_4', 'p5': ' PV_P_5', 'p6': ' PV_P_6'}


def parse_test2_str(txt):
    # parses file names from Test 2 to extract voltage, number derated, and derate levels
    v = re.search("mppt_v=(.*?)_", txt).group(1)
    d = re.search("derate=(.*?)_", txt).group(1)
    p = re.search("\((.*?)\)", txt).group(1).split(' ')
    voltage = int(v)
    n_derated = float(d)
    derate_levels = [int(k) for k in p]
    return voltage, n_derated, derate_levels


def parse_test1_str(txt):
    # parses file names from Test 1 to extract voltages and number derated inputs
    vs = re.search("\[(.*?)\]", txt).group(0).strip('[]').split(' ')
    d = re.search("n_derated=(.*?)_", txt).group(1)
    voltages = [int(v) for v in vs]
    n_derated = int(d)
    return voltages, n_derated


def flag_outliers(r):
    # flag values outside of 1.5 x (75th - 25th)
    q3 = np.percentile(r, 75)
    q1 = np.percentile(r, 25)
    iqr = 1.5 * (q3 - q1)
    return (r > q3 + iqr) | (r < q1 - iqr)


def get_ac_dc_pdc(data):
    # removes outliers and returns total AC (sum over 3 phases) and
    # total DC power (sum over 6 inputs)
    ac = data[' AC_P_1'] + data[' AC_P_2'] + data[' AC_P_3']
    dc = data[' PV_P_1'] + data[' PV_P_2'] + data[' PV_P_3'] + \
         data[' PV_P_4'] + data[' PV_P_5'] + data[' PV_P_6']
    ac_out = flag_outliers(ac)
    dc_out = flag_outliers(dc)
    u = ac_out | dc_out
    for p in PDICT:
        u = u | flag_outliers(data[PDICT[p]])
    pdc = {}
    for p in PDICT:
        pdc[p] = data[PDICT[p]][~u].mean()
    # print('  keeping ' + str(sum(~u)))
    return ac[~u], dc[~u], pdc


def check_dc_stable(data, fname, derate_level, derated):
    # checks if DC power on each input is close to target value, and if
    # the sample of DC power values indicates stable measurements
    #
    # Parameters
    # ----------
    # data : input dataframe containing sample of DC power using data file headings
    # fname : input file name, for messsages
    # derate_level : fraction of maximum DC power supplied to the input. Maximum 
    #   assumed to be 5500 here
    # derated : indicator of derated input, 0 is not derated, any other value indicates derating
    stable = True
    for k , p in enumerate(PDICT):
        dc = data[PDICT[p]]
        u = flag_outliers(dc)
        target = derate_level*5500 if derated[k] else 5500
        bias = np.abs(dc[~u].mean() - target)
        cv = dc[~u].std() / dc[~u].mean()
        if (bias > 0.02 * target):
            print(' Outside bias limit: ' + fname)
            stable = False
        if (cv > 0.05):
            print(' Outside variance limit: ' + fname)
            stable = False
    return stable


# voltage level labels
voltage_levels = {600: 'Vmin', 720: 'Vnom', 800: 'Vmax'}

# Process Test 1 files
dirn1 = 'D:\\PVmodeling\\Multi-input inverter\\svp_additional_tools\\Results\\Multi-MPPT Test 1 Data'
test1_files = glob.glob(os.path.join(dirn1, "*].csv"))

data1 = pd.DataFrame(
    index=np.arange(len(test1_files)),
    columns=['n_derated', 'p_max', 'p_ac', 'p_dc', 'eff',
              'p1', 'p2', 'p3', 'p4', 'p5', 'p6',
              'v1', 'v2', 'v3', 'v4', 'v5', 'v6'])
base_input_power = 5500

for i, fname in enumerate(test1_files):
    with open(os.path.join(dirn1, fname), 'r') as infile:
        data = pd.read_csv(infile)
        ac, dc, pdc = get_ac_dc_pdc(data)
        data1.loc[i, ('p_ac')] = ac.mean()
        data1.loc[i, ('p_dc')] = dc.mean()
        # dc power on each input
        for p in PDICT:
            data1.loc[i, (p)] = pdc[p]

        vs, nd = parse_test1_str(fname)
        data1.loc[i, ('n_derated')] = nd

        # voltage setpoints on each input, from filename
        for voltage, v in zip(['v1', 'v2', 'v3', 'v4', 'v5', 'v6'], vs):
            data1.loc[i, (voltage)] = v

        # setpoint for total power
        data1.loc[i, ('p_max')] = 5500 * (6 - nd) + 5500 * nd / 2

data1['eff'] = data1['p_ac'] / data1['p_dc']
data1['p_max'] = data1['n_derated'] * 5500 / 2 + (6 - data1['n_derated']) * 5500



# Process Test 2 files
dirn2 = 'D:\\PVmodeling\\Multi-input inverter\\svp_additional_tools\\Results\\Multi-MPPT Test 2 Data'
test2_files = glob.glob(os.path.join(dirn2, "*).csv"))

data2 = pd.DataFrame(
    index=np.arange(len(test2_files)),
    columns=['n_derated', 'p_max', 'p_ac', 'p_dc', 'eff',
              'p1', 'p2', 'p3', 'p4', 'p5', 'p6',
              'v1', 'v2', 'v3', 'v4', 'v5', 'v6'])

# for a chart of st. dev. of efficiency vs. DC power
std_e = np.zeros((len(test2_files),))

for i, fname in enumerate(test2_files):
    with open(os.path.join(dirn2, fname), 'r') as infile:
        data = pd.read_csv(infile)
    v, d, dr = parse_test2_str(fname)
    if check_dc_stable(data, fname, d, dr):
        ac, dc, pdc = get_ac_dc_pdc(data)
        data2.loc[i, ('p_ac')] = ac.mean()
        data2.loc[i, ('p_dc')] = dc.mean()
        std_e[i] = (ac / dc).std()
        # dc power on each input
        for p in PDICT:
            data2.loc[i, (p)] = pdc[p]
        # v is voltage common to all inputs
        # d is the derate level for limited inputs, fraction of full power
        # dr is a series of 0, 1: 1 if input is derated
        n_derated = sum(dr)
        data2.loc[i, ('n_derated')] = n_derated
        data2.loc[i, ('p_max')] = n_derated * d * 5500 + (6 - n_derated) * 5500
        # DC voltage by input
        data2.loc[i, ('v1', 'v2', 'v3', 'v4', 'v5', 'v6')] = v

# chart of st. dev. of efficiency vs. mean DC power
labels = []
plt.figure()
plt.rcParams.update({'font.size' : 14})
for v in voltage_levels:
    labels.append(str(int(v)) + 'V')
    u = data2['v1']==v
    plt.scatter(data2['p_dc'][u], std_e[u] * 100)
plt.ylabel('St. deviation of efficiency (%)')
plt.xlabel('DC power (W)')
plt.legend(labels, loc='upper right')
plt.tight_layout()
plt.savefig('meas_error_effic_Test2')

data2['eff'] = data2['p_ac'] / data2['p_dc']

# set up to combine
data2.index = np.arange(len(data1.index), len(data1.index)+len(test2_files))

combined = pd.concat((data1, data2))

with open('multi_inverter_combined.csv', 'w') as outfile:
    combined.to_csv(outfile)
