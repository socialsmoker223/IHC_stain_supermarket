import streamlit as st
import csv
import json
import pandas as pd
import numpy as np
from datetime import datetime
import re

from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
from mlxtend.preprocessing import TransactionEncoder

def clean_itemsets(x):
    p = "frozenset\(\{'(.*)'\}\)"
    mo = re.compile(p)
    y = mo.match(x)[1]
    y = y.replace("'","").replace(" ","").split(",")
    y = set(y)
    return y

def clean_itemsets_to_str(x):
    p = "frozenset\(\{'(.*)'\}\)"
    mo = re.compile(p)
    y = mo.match(x)[1]
    y = y.replace("'","").replace(" ","").split(",")
    return y


# config
stain_default = ['CD10']



# main
st.title("IHC Stain Super Market")

st.markdown("## 1 ) Upload rules")
df = pd.read_json("./data/stains.json")
stains = [stain[0] for stain in df.values]

file = st.file_uploader("Upload rules.csv", type="csv")
if file is not None: 
    df = pd.read_csv(file, index_col=0)
    st.write(f"Number of rules uploaded : {len(df)}")

    df['if'] = df.antecedents.apply(clean_itemsets)
    df['then'] = df.consequents.apply(clean_itemsets)



# user input
st.markdown("## 2 ) Add a stain to your basket")
selected_raw = st.multiselect("Add stains to your basket", stains, default=stain_default, key=1)
selected = set(selected_raw)

# select top 5
df_out = df[df['if'].apply(lambda x: True if selected.issubset(x) else False)].sort_values("conviction", ascending=False)
df_out = df_out[:5]
st.write("Your current basket:")
st.write(selected_raw)

# [TODO]
recs_out = []
recs_ant = df_out.antecedents.apply(clean_itemsets_to_str).to_list()
recs_con = df_out.consequents.apply(clean_itemsets_to_str).to_list()

# breakdown suggestion as indivicual items
for rec in recs_ant:
    recs_out.extend(rec)
recs_ant = list(set(recs_out))

for rec in recs_con:
    recs_out.extend(rec)
recs_con = list(set(recs_out))

recs = list(set(recs_out))

st.markdown("## 3 ) Recommendations")
st.write("You may also be interested in :")
st.write(recs_ant)
st.write(recs_con)

for r in recs:
    if st.button(r, key=1):
        stain_default.append(r)

st.write(stain_default)

