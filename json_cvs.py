import pandas as pd

df = pd.read_json (r'data.json')
df_transposed = df.T
df_transposed["index"] += 1 
df_transposed = df_transposed.set_index(['index'])

for elem in df_transposed.local.unique():
    print(elem + " - " + str(len(df_transposed[df_transposed.local == elem])))

df = df_transposed

df.currentSpeed == df.freeFlowSpeed & df.currentTravelTime == df.freeFlowTravelTime

df["flowSpeed"] = df.currentSpeed == df.freeFlowSpeed
df["flowTravelTime"] = df.currentTravelTime == df.freeFlowTravelTime
df["transito"] = df["flowSpeed"] & df["flowTravelTime"]

df.drop('flowSpeed', inplace=True, axis=1)
df.drop('flowTravelTime', inplace=True, axis=1)

df.loc[df["transito"] == "Sem Transito", "transito"] = 0

df["transito"] = 1- (df.currentSpeed / df.freeFlowSpeed + df.freeFlowTravelTime / df.currentTravelTime  )/2

df_transposed.to_csv (r'data.csv', index=None)
