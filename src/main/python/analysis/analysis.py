#!/usr/bin/env python
# coding: utf-8

# In[]:

import pandas as pd
import matplotlib.pyplot as pyplot
import numpy as np
from cycler import cycler
import scipy as sp
import matsim as ms

# todo: https??
hh = pd.read_csv('../covid-sim/src/assets/' + 'berlin-hospital.csv', sep=",").fillna(value=0.)
# hh = pd.read_csv('/Users/kainagel/public-svn/matsim/scenarios/countries/de/episim/original-data/Fallzahlen/Berlin/10052020_TaSpi.csv', sep=";").fillna(value=0.)
hh.index = pd.date_range(start='2020-03-01', periods=hh.index.size)

cc = pd.read_csv('/Users/kainagel/public-svn/matsim/scenarios/countries/de/episim/original-data/Fallzahlen/RKI/berlin-cases.csv', sep=",").fillna(value=0.)
cc.index = pd.date_range(start='2020-02-21', periods=cc.index.size)

# In[]:

# base = '2020-05-28-21:45:02_triang_theta6.9E-7__infectedBNC3.0_3.0__contag1.5_1.5_exclHome_startDate2020-02-15_ciCorrA0.55@2020-03-08_triangStrt2020-03-08_alpha1.2_ciCorrB0.15@2020-04-15over14days/'

# base = '2020-05-28-22:19:14_triang_theta1.4E-6__infectedBNC3.0_3.0__contag1.5_1.5_exclHome_startDate2020-02-15_ciCorrA0.55@2020-03-08_triangStrt2020-03-08_alpha1.2_ciCorrB0.15@2020-04-15over14days/'

# base = '2020-05-28-22:30:30_triang_theta5.0E-7__infectedBNC3.0_3.0__contag1.5_1.5_exclHome_startDate2020-02-15_ciCorrA0.55@2020-03-08_triangStrt2020-03-08_alpha1.2_ciCorrB0.15@2020-04-15over14days/'

# base = '2020-05-28-22:36:20_triang_theta5.0E-8__infectedBNC3.0_3.0__contag1.5_1.5_exclHome_startDate2020-02-15_ciCorrA0.55@2020-03-08_triangStrt2020-03-08_alpha1.2_ciCorrB0.15@2020-04-15over14days/'
# base = '2020-05-28-22:43:51_triang_theta5.0E-9__infectedBNC3.0_3.0__contag1.5_1.5_exclHome_startDate2020-02-15_ciCorrA0.55@2020-03-08_triangStrt2020-03-08_alpha1.2_ciCorrB0.15@2020-04-15over14days/'
# base = '2020-05-28-23:10:32_triang_theta2.0E-8__infectedBNC3.0_3.0__contag1.5_1.5_exclHome_startDate2020-02-15_ciCorrA0.55@2020-03-08_triangStrt2020-03-08_alpha1.2_ciCorrB0.15@2020-04-15over14days/'
# base = '2020-05-29-08:18:49_triang_theta4.0E-8__infectedBNC3.0_3.0__contag1.5_1.5_exclHome_startDate2020-02-15_ciCorrA0.55@2020-03-08_triangStrt2020-03-08_alpha1.2_ciCorrB0.15@2020-04-15over14days/'
# base = '2020-05-29-08:18:55_triang_theta3.0E-8__infectedBNC3.0_3.0__contag1.5_1.5_exclHome_startDate2020-02-15_ciCorrA0.55@2020-03-08_triangStrt2020-03-08_alpha1.2_ciCorrB0.15@2020-04-15over14days/'
# base = '2020-05-29-08:40:58_triang_theta3.5E-8__infectedBNC3.0_3.0__contag1.5_1.5_exclHome_startDate2020-02-15_ciCorrA0.55@2020-03-08_triangStrt2020-03-08_alpha1.2_ciCorrB0.15@2020-04-15over14days/'
# base = '2020-05-29-10:36:41_triang_theta3.2E-8__infectedBNC3.0_3.0__contag1.5_1.5_exclHome_startDate2020-02-15_ciCorrA0.55@2020-03-08_triangStrt2020-03-08_alpha1.2_ciCorrB0.15@2020-04-15over14days/'
# base = '2020-05-29-15:17:43_triang_theta3.2E-8__infectedBNC3.0_3.0__contag1.5_1.5_exclHome_startDate2020-02-15_ciCorrA0.55@2020-03-08_triangStrt2020-03-08_alpha1.2_ciCorrB0.15@2020-04-15over14days/'

# base = '2020-05-29-23:05:17_triang_theta8.0E-10__infectedBNC3.0_3.0__contag1.5_1.5_exclHome_startDate2020-02-15_ciCorrA0.55@2020-03-08_triangStrt2020-03-08_alpha1.2_ciCorrB0.15@2020-04-15over14days/'
# base = '2020-05-29-23:14:00_triang_theta2.0E-9__infectedBNC3.0_3.0__contag1.5_1.5_exclHome_startDate2020-02-15_ciCorrA0.55@2020-03-08_triangStrt2020-03-08_alpha1.2_ciCorrB0.15@2020-04-15over14days/'
# base = '2020-05-30-00:00:50_triang_theta3.0E-9__infectedBNC3.0_3.0__contag1.5_1.5_exclHome_startDate2020-02-15_ciCorrA0.55@2020-03-08_triangStrt2020-03-08_alpha1.2_ciCorrB0.15@2020-04-15over14days/'
# base = '2020-05-30-00:35:40_triang_theta4.0E-9__infectedBNC3.0_3.0__contag1.5_1.5_exclHome_startDate2020-02-15_ciCorrA0.55@2020-03-08_triangStrt2020-03-08_alpha1.2_ciCorrB0.15@2020-04-15over14days/'

# base = '2020-05-30-08:18:11_triang_theta4.5E-9__infectedBNC3.0_3.0__contag1.5_1.5_exclHome_startDate2020-02-15_ciCorrA0.55@2020-03-08_triangStrt2020-03-08_alpha1.2_ciCorrB0.15@2020-04-15over14days/'
# base = '2020-05-30-15:01:38_triang_theta4.5E-9__infectedBNC3.0_3.0__contag1.5_1.5_exclHome_startDate2020-02-15_ciCorrA0.55@2020-03-08_triangStrt2020-03-08_alpha1.2_ciCorrB0.15@2020-04-15over14days/'
# base = '2020-05-30-21:31:26_triang_theta4.5E-9__infectedBNC3.0_3.0__contag1.5_1.5_exclHome_startDate2020-02-15_ciCorrA0.55@2020-03-08_triangStrt2020-03-08_alpha1.2_ciCorrB0.15@2020-04-15over14days/'

# base = '2020-05-30-00:01:03_triang_theta5.0E-9__infectedBNC3.0_3.0__contag1.5_1.5_exclHome_startDate2020-02-15_ciCorrA0.55@2020-03-08_triangStrt2020-03-08_alpha1.2_ciCorrB0.15@2020-04-15over14days/'
# base = '2020-05-30-00:01:11_triang_theta6.0E-9__infectedBNC3.0_3.0__contag1.5_1.5_exclHome_startDate2020-02-15_ciCorrA0.55@2020-03-08_triangStrt2020-03-08_alpha1.2_ciCorrB0.15@2020-04-15over14days/'

# base = '2020-05-31-16:31:45_unrestr_theta1.4E-6__infectedBNC3.0_3.0__contag1.5_1.5_exclHome_startDate2020-02-15/'
# base = '2020-05-31-16:43:43_unrestr_theta6.9E-7__infectedBNC3.0_3.0__contag1.5_1.5_exclHome_startDate2020-02-15/'
# base = '2020-05-31-16:50:07_unrestr_theta6.9E-7__infectedBNC3.0_3.0__contag1.5_1.5__sShed1.0__sSusc0.0_exclHome_startDate2020-02-15/'
# base = '2020-05-31-16:51:16_unrestr_theta6.9E-7__infectedBNC3.0_3.0__contag1.5_1.5__sShed2.0__sSusc0.0_exclHome_startDate2020-02-15/'
# base = '2020-05-31-16:51:03_unrestr_theta6.9E-7__infectedBNC3.0_3.0__contag1.5_1.5__sShed3.0__sSusc0.0_exclHome_startDate2020-02-15/'

# base = '2020-05-31-16:51:16_unrestr_theta6.9E-7__infectedBNC3.0_3.0__contag1.5_1.5__sShed2.0__sSusc0.0_exclHome_startDate2020-02-15/'
# base = '2020-05-31-17:07:42_unrestr_theta2.0E-6__infectedBNC3.0_3.0__contag1.5_1.5__sShed2.0__sSusc0.0_exclHome_startDate2020-02-15/'

# base = '2020-05-31-17:52:22_unrestr_theta2.0E-6__pWSymp0.0__infectedBNC3.0_3.0__contag1.5_1.5__sShed0.0__sSusc0.0_exclHome_startDate2020-02-15/'
# base = '2020-05-31-18:13:30_unrestr_theta1.0E-5__pWSymp0.0__infectedBNC3.0_3.0__contag1.5_1.5__sShed0.0__sSusc0.0_exclHome_startDate2020-02-15/'
# base = '2020-05-31-18:24:23_unrestr_theta1.0E-6__pWSymp0.0__infectedBNC3.0_3.0__contag1.5_1.5__sShed0.0__sSusc0.0_exclHome_startDate2020-02-15/'

# base = '2020-05-31-19:02:27_unrestr_theta8.0E-7__pWSymp0.0__infectedBNC3.0_3.0__contag1.5_1.5__sShed0.0__sSusc0.0_exclHome_startDate2020-02-15/'
# base = '2020-05-31-19:02:46_unrestr_theta7.0E-7__pWSymp0.0__infectedBNC3.0_3.0__contag1.5_1.5__sShed0.0__sSusc0.0_exclHome_startDate2020-02-15/'

# base = '2020-06-01-14:34:27_unrestr_theta3.0E-7__pWSymp0.0__infectedBNC3.0_3.0__contag1.5_1.5__sShed0.0__sSusc0.0_startDate2020-02-15/'
# base = '2020-06-01-14:34:34_unrestr_theta1.0E-7__pWSymp0.0__infectedBNC3.0_3.0__contag1.5_1.5__sShed0.0__sSusc0.0_startDate2020-02-15/'

# base = '2020-06-01-18:38:53__unrestr__theta2.3E-6@3__pWSymp0.0__infectedBNC3.0_3.0__contag1.5_1.5__sShed0.0__sSusc0.0_startDate2020-02-15/'

# base = '2020-06-01_21-02-43__unrestr__theta6.9E-7@10__pWSymp0.0__infectedBNC3.0_3.0__contag1.5_1.5__sShed0.0__sSusc0.0_startDate2020-02-15/'


# base = '2020-06-01_22-08-20__unrestr__theta2.3E-6@3__pWSymp0.0__infectedBNC3.0_3.0__contag1.5_1.5__sShed2.0__sSusc0.0_startDate2020-02-15/'
# base = '2020-06-01_22-08-32__unrestr__theta6.9E-7@10__pWSymp0.0__infectedBNC3.0_3.0__contag1.5_1.5__sShed2.0__sSusc0.0_startDate2020-02-15/'
# base = '2020-06-01_22-08-44__unrestr__theta1.0E-7@100__pWSymp0.0__infectedBNC3.0_3.0__contag1.5_1.5__sShed2.0__sSusc0.0_startDate2020-02-15/'

# base = '2020-06-01_23-40-52__unrestr__theta1.0E-6@10__pWSymp0.0__infectedBNC3.0_3.0__contag1.5_1.5__sInfct1.0__sSusc0.0_startDate2020-02-15/'

# base = '2020-06-02_20-49-43__unrestr__theta6.9E-7@10__pWSymp0.0__sInfct0.0__sSusc0.0_startDate2020-02-15/'
# base = '2020-06-02_21-30-45__unrestr__theta8.0E-7@10__pWSymp0.0__sInfct0.0__sSusc0.0_startDate2020-02-15/'
# base = '2020-06-02_21-30-53__unrestr__theta9.0E-7@10__pWSymp0.0__sInfct0.0__sSusc0.0_startDate2020-02-15/'
# base = '2020-06-02_21-31-01__unrestr__theta1.0E-6@10__pWSymp0.0__sInfct0.0__sSusc0.0_startDate2020-02-15/'
base = '2020-06-03_08-08-35__frmSnz__theta1.0E-6@10__pWSymp0.0__sInfct0.0__sSusc0.0_ciCorr0.3_@2020-03-08_alpha1.4_startDate2020-02-15_startDate2020-02-15/'

rr = pd.read_csv(base + 'infections.txt', sep='\t')
rr['date'] = pd.to_datetime(rr['date'])
rr.set_index('date',inplace=True)

infectedCumulative = rr.loc[rr['district'] == 'Berlin', ['nInfectedCumulative']]
nContagious = rr.loc[rr['district'] == 'Berlin', ['nContagiousCumulative']]
nShowingSymptoms = rr.loc[rr['district'] == 'Berlin', ['nShowingSymptomsCumulative']]

# rr2b = pd.concat([hh['Gemeldete Fälle'], infectedCumulative.rolling('3D').mean()], axis=1).fillna(value=0.)

fit = pd.Series(1 * np.exp(np.arange(0, 30, 1) * np.log(2.) / 2.8))
fit.index = pd.date_range(start="2020-02-20", periods=fit.size)

fit2 = pd.Series(60 * np.exp(np.arange(0, 30, 1) * np.log(2.) / 8))
fit2.index = pd.date_range(start="2020-03-01", periods=30)

fit3 = pd.Series(400 * np.exp(np.arange(0, 80, 1) * np.log(2.) / (-17)))
fit3.index = pd.date_range(start="2020-03-01", periods=80)

rr3 = pd.concat([cc['cases'], infectedCumulative.diff(),nContagious.diff(), nShowingSymptoms.diff(),fit,fit2,fit3], axis=1)

pyplot.close('all')
pyplot.rcParams['figure.figsize']=[12, 5]
default_cycler = (cycler(color=['r', 'g', 'b', 'y','red','purple','orange']) +
                  cycler(linestyle=['', '', '', '','-','-','-']) +
                  cycler(marker=['.','','.','','','','']))
pyplot.rc('axes', prop_cycle=default_cycler)
axes = rr3.plot(logy=True,grid=True)
# axes.set_ylim(0,250)
axes.set_xlim(pd.to_datetime('2020-02-15'),pd.to_datetime('2020-08-15'))
pyplot.axvline(pd.to_datetime('2020-03-11'), color='red', linestyle='-', lw=1)
pyplot.axvline(pd.to_datetime('2020-03-16'), color='red', linestyle='-', lw=1)
# pyplot.axvline(pd.to_datetime('2020-03-21'), color='red', linestyle='-', lw=1)
pyplot.show()

# In[]:

# --

infected = rr.loc[rr['district'] == 'Berlin' , ['nSeriouslySick','nCritical']]


infected['shouldBeInHospital'] = infected['nSeriouslySick'] + infected['nCritical']

rr3 = pd.concat([hh['Stationäre Behandlung'], hh['Intensivmedizin'], infected['shouldBeInHospital'], infected['nCritical']], axis=1).fillna(value=0.)

pyplot.close('all')
pyplot.rcParams['figure.figsize']=[12, 5]
default_cycler = (cycler(color=['r', 'g', 'b', 'y','pink','purple']) +
                  cycler(linestyle=['', '', '', '','-','']) +
                  cycler(marker=['.','.','.','.',",",'']))
pyplot.rc('axes', prop_cycle=default_cycler)
rr3.plot(logy=True,grid=True)
pyplot.show()

# In[]:

# infectedCumulative = rr.loc[rr['district'] == 'Berlin' , ['day', 'nInfectedCumulative']]
# infectedCumulative.index = pd.date_range(start=simStartDate, periods=infectedCumulative.size / 2)
rr2b = infectedCumulative['nInfectedCumulative']

fit = pd.Series(2 * np.exp(np.arange(0, 60, 1) * np.log(2.) / 2.8))
fit.index = pd.date_range(start="2020-02-15", periods=60)

rr3 = pd.concat([rr2b, fit], axis=1)

pyplot.close('all')
pyplot.rcParams['figure.figsize']=[12, 5]
default_cycler = (cycler(color=['r', 'g', 'b', 'y','pink','purple']) +
                  cycler(linestyle=['-', '-', '-', '-','-','']) +
                  cycler(marker=['','','','',",",'']))
pyplot.rc('axes', prop_cycle=default_cycler)
rr3.plot(logy=True,grid=True)
pyplot.axvline(23, color='y', linestyle='-', lw=1)
pyplot.show()

# ln[]:

# ss = pd.read_csv(base + 'timeUse.txt', sep='\t' )
#
# ss.drop(columns=['day','Unnamed: 1','home'],inplace=True)
#
# plt.close('all')
# plt.rcParams['figure.figsize']=[12,7]
# # default_cycler = (cycler(color=['r', 'g', 'b', 'y','pink','purple']) +
# #                   cycler(linestyle=['', '-', '-', '','-','']) +
# #                   cycler(marker=['o','','','',",",'']))
# # plt.rc('lines', linewidth=1)
# # plt.rc('axes', prop_cycle=default_cycler)
# ss.plot(kind='line',logy=False,grid=True,xlim=[1,60])
# # plt.axvline(17, color='y', linestyle='-', lw=1)
# plt.axvline(23, color='y', linestyle='-', lw=1)
# plt.show()

# # ln[]:
#
# tt = pd.read_csv(base +'restrictions.txt', sep='\t' )
#
# tt.drop(columns=['day','pt','tr','Unnamed: 1','home'],inplace=True)
#
# plt.close('all')
# plt.rcParams['figure.figsize']=[12,7]
# # default_cycler = (cycler(color=['r', 'g', 'b', 'y','pink','purple']) +
# #                   cycler(linestyle=['', '-', '-', '','-','']) +
# #                   cycler(marker=['o','','','',",",'']))
# # plt.rc('lines', linewidth=1)
# # plt.rc('axes', prop_cycle=default_cycler)
# tt.plot(kind='line',logy=False,grid=True,xlim=[1,60])
# # plt.axvline(17, color='y', linestyle='-', lw=1)
# plt.axvline(23, color='y', linestyle='-', lw=1)
# plt.show()


# In[]:
infectionEvents = pd.read_csv(base + "infectionEvents.txt", sep="\t")

# In[]:
plans = ms.plan_reader( "../shared-svn/projects/episim/matsim-files/snz/BerlinV2/episim-input/be_v2_snz_entirePopulation_emptyPlans_withDistricts.xml.gz", selectedPlansOnly = True )
# plans = ms.plan_reader( "../shared-svn/projects/episim/matsim-files/snz/BerlinV2/episim-input/testPlans_withDistricts.xml.gz", selectedPlansOnly = True )
# plans = ms.plan_reader( "../shared-svn/projects/episim/matsim-files/snz/BerlinV2/episim-input/test2.xml", selectedPlansOnly = True )

personAge = dict()
cnt = 0
for person, plan in plans:
    cnt += 1
    personId = person.attrib['id']
    matsimAttributes = person.find('attributes')
    for matsimAttribute in matsimAttributes:
        if matsimAttribute.attrib['name'] == 'age':
            personAge[personId] = int(matsimAttribute.text)
    # if cnt >= 30:
    #     break

print(personAge)

# In[]:

personsByAge = dict.fromkeys(range(100),0)
for abc in personAge:
    personsByAge[personAge.get(abc)] += 0.02

infectionsByAge = dict.fromkeys(range(100),0)
for abc in infectionEvents.loc[:,"infected"]:
    infectionsByAge[personAge.get(abc)] += 1


print(infectionsByAge)

pyplot.bar(*zip(*personsByAge.items()))
pyplot.bar(*zip(*infectionsByAge.items()))
pyplot.show()
