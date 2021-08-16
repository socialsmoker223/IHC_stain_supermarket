import csv
import json
import math
from numpy.lib.npyio import save
import pandas as pd
import numpy as np
from datetime import datetime

from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
from mlxtend.preprocessing import TransactionEncoder

class Trainer(object):
    """docstring for Trainer."""
    def __init__(self):
        super(Trainer, self).__init__()
        

    def trimmed_item(self, item, trimIHCdict):

        if trimIHCdict.__contains__(item):
            return True
        else:
            return False

    def load_clean_csv(self, csv_fp, trimmed_mapping2):

        data = []
        IHCdict = {}
        
        with open(csv_fp, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in spamreader:
                data.append(row)

        for datum in data:
            if len(datum) >3 :

                datum.append(datum[4].replace("AND",";").replace("And",";").replace("and",";").replace("+",";").replace("urgent",";URGENT;").replace("Urgent",";URGENT;").replace("URGENT",";URGENT;").split(";"))
                for num in range(0,datum[5].count('')):
                    datum[5].remove('')
                for num in range(0,datum[5].count(' ')):
                    datum[5].remove(' ')
                for num in range(0,datum[5].count('0')):
                    datum[5].remove('0')
                for num in range(0,datum[5].count('.')):
                    datum[5].remove('.')

        for datum in data:
            if len(datum) >3 :
                for i in range(len(datum[5])):
                    datum[5][i] = datum[5][i].upper().replace(" ","").replace(".","").replace("~","").replace(":","").replace(":","")
                    if datum[5][i] in trimmed_mapping2.keys():
                        if ";" in trimmed_mapping2[datum[5][i]]:

                            datum[5].extend(trimmed_mapping2[datum[5][i]].split(";"))
                            datum[5].pop(i)
                        else:
                            datum[5][i] = trimmed_mapping2[datum[5][i]]

                datum[5]= list( filter(None, datum[5]))
                for i in range(len(datum[5])):

                    if IHCdict.__contains__(datum[5][i]):
                        IHCdict[datum[5][i]] = IHCdict[datum[5][i]] + 1
                    else:
                        IHCdict[datum[5][i]] = 1



        trimIHCdict = {}
        for key, value in IHCdict.items():
            if value > 4 :
                trimIHCdict[key] = value

        trimmed_data = []            
        item_to_delete = []            
        for i in range(len(data)):
            if len(data[i]) >3 :
                    data[i].append(list(filter(lambda x: self.trimmed_item(x, trimIHCdict),data[i][5])))

            if len(data[i]) <=3 or not data[i][6]:
                item_to_delete.append(i)
            else:
                trimmed_data.append(data[i])
                
        return data, trimmed_data, trimIHCdict, item_to_delete

    def nCr(self, n,r):
        return math.factorial(n) / (math.factorial(r) * math.factorial(n-r))

    def count_combos(self, n):
        total = 0
        for r in range(1, n+1):
            c = self.nCr(n,r)
            if r < 11:
                print(f"No. of combos for nCr: n = {n}, r = {r} : ", c)
            total +=c
        print("Total: ", total)
        return total


    def preprocess(self, fp_csv, fp_mapping, out_fp_clean_csv, **kwargs):
        
        with open(fp_mapping) as f:
            mapping_table_clean = json.load(f)

        # load and clean data
        data, trimmed_data, trimIHCdict, item_to_delete = \
            self.load_clean_csv(fp_csv, trimmed_mapping2=mapping_table_clean)

        # to generate the list , for data analysis
        # no more comment from now , this selects last element, which is the stain
        orderlist = []
        for i in range(len(trimmed_data)):
            orderlist.append(trimmed_data[i][6])

        # converts lists of basket into 1 hot encoded
        te = TransactionEncoder()
        te_ary = te.fit_transform(orderlist)
        df = pd.DataFrame(te_ary, columns = te.columns_)
        # df.to_csv(out_fp_clean_csv)
        
        print("Total number of transactions",len(df))
        print("Total number of unique stains",len(df.columns))
        print("Total number of all possible combinations", self.count_combos(len(df.columns)))
        
        return df

    def mine(self, df, min_support, metric, metric_min_threshold, fp_itemsets, fp_rules, save_csv = False, **kwargs):
        print(min_support)
        # mining
        # prune infrequent itemsets
        frequent_itemsets = apriori(df, min_support=min_support, use_colnames=True)
        print("Total number of  frequent itemsets", len(frequent_itemsets))

        # find association of item sets
        rules = association_rules(frequent_itemsets, metric=metric, min_threshold=metric_min_threshold)
        print("Total number of association rules", len(rules))

        # save
        if save_csv:
            frequent_itemsets.to_csv(fp_itemsets)
            rules.to_csv(fp_rules)
        
        return frequent_itemsets, rules

    def fit(self, csv, min_support=0.01):
        fp_csv = csv
        fp_mapping = r"./data/mapping_table_clean.json"
        out_fp_clean_csv = r"./data/clean.csv"
        metric = "confidence"
        metric_min_threshold = 0.8
        fp_itemsets = "itemsets_{}.csv".format(min_support)
        fp_rules = "rules_{}.csv".format(min_support)
        config = dict(fp_csv=fp_csv,
                 fp_mapping=fp_mapping,
                 out_fp_clean_csv=out_fp_clean_csv,
                 fp_itemsets=fp_itemsets,
                 fp_rules=fp_rules,
                  min_support=min_support,
                  metric=metric,
                  metric_min_threshold=metric_min_threshold,
                 )
        df = self.preprocess(**config)
        result = self.mine(df, 
                      min_support=min_support, 
                      metric=metric, 
                      metric_min_threshold=metric_min_threshold, 
                      fp_itemsets="items_{}.csv".format(min_support),
                     fp_rules="rules_{}.csv".format(min_support)
                     )

        return result

def main():
    csv = r"./data/ihc_record.csv"
    trainer = Trainer()
    output_csv = trainer.fit(csv)
    pass

if __name__ == "__main__":
    main()
    pass
