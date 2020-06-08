#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import subprocess

import numpy as np
import optuna
import pandas as pd
from sklearn.metrics import mean_squared_log_error


def read_data(f, district, hospital, rki, window=5):
    """   Reads in three csv files """
    # Simulation output
    df = pd.read_csv(f, sep="\t", parse_dates=[2])
    df = df[df.district == district]
    df.set_index('date', drop=False, inplace=True)
    df['cases'] = df.nShowingSymptomsCumulative.diff(1)
    df['casesSmoothed'] = df.cases.rolling(window).mean()
    df['casesNorm'] = df.casesSmoothed / df.casesSmoothed.mean()

    hospital = pd.read_csv(hospital, parse_dates=[0], dayfirst=True)
    rki = pd.read_csv(rki, parse_dates={'date': ['month', 'day', 'year']})
    rki.set_index('date', drop=False, inplace=True)
    rki['casesCumulative'] = rki.cases.cumsum()
    rki['casesSmoothed'] = rki.cases.rolling(window).mean()
    rki['casesNorm'] = rki.casesSmoothed / rki.casesSmoothed.mean()

    return df, hospital, rki


def percentage_error(actual, predicted):
    """ https://stackoverflow.com/questions/47648133/mape-calculation-in-python """
    res = np.empty(actual.shape)
    for j in range(actual.shape[0]):
        # Small values are measured with mean error
        if abs(actual[j]) >= 15:
            res[j] = (actual[j] - predicted[j]) / actual[j]
        else:
            res[j] = (actual[j] - predicted[j]) / np.mean(actual)
    return res


def mean_absolute_percentage_error(y_true, y_pred):
    return np.mean(np.abs(percentage_error(np.asarray(y_true), np.asarray(y_pred)))) * 100


def infection_rate(f, district, target_rate=2, target_interval=3):
    """  Calculates the R values between a fixed day interval and returns MSE according to target rate """

    df = pd.read_csv(f, sep="\t")
    df = df[df.district == district]

    rates = []
    for i in range(25, 40):
        prev = float(df[df.day == i - target_interval].nTotalInfected)
        today = float(df[df.day == i].nTotalInfected)

        rates.append(today / prev)

    rates = np.array(rates)

    return rates.mean(), np.square(rates - target_rate).mean()


def calc_multi_error(f, district, start, end, hospital="berlin-hospital.csv", rki="berlin-cases.csv"):
    """ Compares hospitalization rate """

    df, hospital, rki = read_data(f, district, hospital, rki)

    df = df[(df.date >= start) & (df.date <= end)]
    hospital = hospital[(hospital.Datum >= start) & (hospital.Datum <= end)]
    rki = rki[(rki.date >= start) & (rki.date <= end)]

    peak = str(df.loc[df.cases.idxmax()].date)

    error_sick = mean_squared_log_error(hospital["Stationäre Behandlung"], df.nSeriouslySick)
    error_critical = mean_squared_log_error(hospital["Intensivmedizin"], df.nCritical)

    # Assume Dunkelziffer of factor 8
    # error_cases = mean_squared_log_error(cmp["Gemeldete Fälle"].diff(1).dropna() * 8, df.nShowingSymptomsCumulative.diff(1).dropna())
    # error_cases = mean_squared_log_error(rki.drop(rki.index[0]).cases * 8, df.nShowingSymptomsCumulative.diff(1).dropna())
    error_cases = mean_squared_log_error(rki.casesNorm, df.casesNorm)

    # Dunkelziffer
    dz = float(df.nContagiousCumulative.tail(1) / rki.casesCumulative.tail(1))

    return error_cases, error_sick, error_critical, peak, dz


def objective_unconstrained(trial):
    """ Objective for constrained infection dynamic. """

    n = trial.number
    c = trial.suggest_uniform("calibrationParameter", 1e-06, 4e-06)

    scenario = trial.study.user_attrs["scenario"]
    district = trial.study.user_attrs["district"]

    cmd = "java -jar matsim-episim-1.0-SNAPSHOT.jar scenarioCreation trial %s --number %d --unconstrained --calibParameter %.12f" % (scenario, n, c)

    print("Running calibration for %s (district: %s) : %s" % (scenario, district, cmd))
    subprocess.run(cmd, shell=True)

    rate, error = infection_rate("output-calibration-unconstrained/%d/infections.txt" % n, district)
    trial.set_user_attr("mean_infection_rate", rate)

    return error


def objective_ci_correction(trial):
    """ Objective for ci correction """

    n = trial.number
    params = dict(
        number=n,
        scenario=trial.study.user_attrs["scenario"],
        district=trial.study.user_attrs["district"],
        # Parameter to calibrate
        correction=trial.suggest_uniform("ciCorrection", 0.2, 1),
        start=trial.study.user_attrs["start"],
        end=trial.study.user_attrs["end"]
    )

    cmd = "java -Xmx5G -jar matsim-episim-1.0-SNAPSHOT.jar scenarioCreation trial %(scenario)s --days 14" \
          " --number %(number)d --correction %(correction).3f" \
          "--start %(start)s" % params

    print("Running ci correction with params: %s" % params)
    print("Running calibration command: %s" % cmd)
    subprocess.run(cmd, shell=True)

    e_cases, e_sick, e_critical, peak, dz = calc_multi_error("output-calibration/%d/infections.txt" % n,
                                                             params["district"], start=params["start"], end=params["end"])

    trial.set_user_attr("error_cases", e_cases)
    trial.set_user_attr("error_sick", e_sick)
    trial.set_user_attr("error_critical", e_critical)
    trial.set_user_attr("peak", peak)
    trial.set_user_attr("dz", dz)

    return e_cases


def objective_multi(trial):
    """ Objective for multiple parameter """
    global district, scenario

    n = trial.number

    params = dict(
        scenario=scenario,
        district=district,
        number=n,
        # Parameter to calibrate
        #c=trial.suggest_uniform("calibrationParameter", 0.5e-06, 3e-06),
        # offset=trial.suggest_int('offset', -8, 4),
        # ci_homeq=trial.suggest_loguniform("home_quarantine", 0.1, 1),
        # ci_homeq=1,
        alpha=trial.suggest_uniform("alpha", 1, 2),
        correction=trial.suggest_uniform("ciCorrection", 0.2, 1),
    )

    cmd = "java -Xmx5G -jar matsim-episim-1.0-SNAPSHOT.jar scenarioCreation trial %(scenario)s --days 75" \
          " --number %(number)d --alpha %(alpha).3f" \
          " --correction %(correction).3f --start \"2020-03-08\"" % params

    print("Running multi objective with params: %s" % params)
    print("Running calibration command: %s" % cmd)
    subprocess.run(cmd, shell=True)
    e_cases, e_sick, e_critical, peak, dz = calc_multi_error("output-calibration/%d/infections.txt" % n, params["district"],
                                                             start="2020-03-08", end="2020-04-07")

    trial.set_user_attr("error_cases", e_cases)
    trial.set_user_attr("error_sick", e_sick)
    trial.set_user_attr("error_critical", e_critical)
    trial.set_user_attr("peak", peak)
    trial.set_user_attr("dz", dz)

    return e_cases, e_sick, e_critical


if __name__ == "__main__":
    # Needs to be run from top-level episim directory!

    parser = argparse.ArgumentParser(description="Run calibrations with optuna.")
    parser.add_argument("n_trials", metavar='N', type=int, nargs="?", help="Number of trials", default=10)
    parser.add_argument("--district", type=str, default="Berlin",
                        help="District to calibrate for. Should be 'unknown' if no district information is available")
    parser.add_argument("--scenario", type=str, help="Scenario module used for calibration", default="SnzBerlinScenario25pct2020")
    parser.add_argument("--start", help="Start date of comparison", type=str, default="2020-03-10")
    parser.add_argument("--end", help="End date of comparison", type=str, default="2020-05-20")
    parser.add_argument("--snapshot", type=str, default=None)
    parser.add_argument("--objective", type=str, choices=["unconstrained", "ci_correction", "multi"], default="unconstrained")

    args = parser.parse_args()

    if args.objective == "multi":
        study = optuna.multi_objective.create_study(
            study_name=args.objective, storage="sqlite:///calibration.db", load_if_exists=True,
            directions=["minimize"] * 3
        )

        district = args.district
        scenario = args.scenario

    else:
        study = optuna.create_study(
            study_name=args.objective, storage="sqlite:///calibration.db", load_if_exists=True,
            direction="minimize"
        )

    # Copy all args to study
    for k, v in args.__dict__.items():
        study.set_user_attr(k, v)

    objective = objective_multi if args.objective == "multi" else objective_unconstrained

    study.optimize(objective, n_trials=args.n_trials)
