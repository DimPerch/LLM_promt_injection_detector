import pandas as pd
from InjectionDetector import *
from sklearn.metrics import f1_score

detector = HeuristicDetector()

df = pd.read_csv('dataset/final_prompts.csv')
results = []

for i in range(len(df)):
    results.append(HeuristicDetector.check(df.iloc[i, 0]))

print(f1_score(df['jailbreak'], results))