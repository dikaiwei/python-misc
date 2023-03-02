# -*-coding:utf-8-*-

import pandas as pd
import numpy as np
import re


if __name__ == "__main__":
    print("hello world")

    df = pd.read_excel("C:/Users/weidikkai01/Downloads/accountMessage.xlsx")
    df.drop("\t", axis=1, inplace=True)

    df[df == "-"] = np.nan
    df.dropna(axis=0, how="all", inplace=True)
    df.columns = ["index", "name", "age", "weight", "m_breast", "m_waist", "m_hip", "f_breast", "f_waist", "f_hip"]
    df[["first_name", "last_name"]] = df["name"].str.split(expand=True)
    df.drop_duplicates("name", inplace=True)
    df.drop("name", axis=1, inplace=True)

    rows_with_pound = df["weight"].str.contains("lbs").fillna(False)
    df.loc[rows_with_pound, "weight"] = df.loc[rows_with_pound, "weight"].apply(lambda x: round(float(x[:-3])/2.2, 0))
    df.loc[(~rows_with_pound) & (df["weight"].notnull()), "weight"] = df.loc[(~rows_with_pound) & (df["weight"].notnull()), "weight"].\
        apply(lambda x: float(re.sub("kgs", "", str(x))))

    df.loc[df["m_breast"].notnull(), "sex"] = "male"
    df.loc[df["f_breast"].notnull(), "sex"] = "female"

    df["age"].fillna(round(df["age"].mean(),0), inplace=True)
    for col in ("weight", "f_waist"):
        df.loc[(df["sex"] == "female") & (df[col].isnull()), col] = round(df.loc[(df["sex"] == "female"), col].mean(), 0)

    df = df.\
        loc[df["sex"] == "male", [i for i in df.columns if i not in ("f_breast", "f_waist", "f_hip")]].\
        rename(columns={"m_breast": "breast", "m_waist": "waist", "m_hip": "hip"}).\
        append(df.loc[df["sex"] == "female", [i for i in df.columns if i not in ("m_breast", "m_waist", "m_hip")]].
               rename(columns={"f_breast": "breast", "f_waist": "waist", "f_hip": "hip"}))

    print(df)
