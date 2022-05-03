import pandas as pd
import datetime as dt

df = pd.read_json (r'data.json')
df_transposed = df.T
df_transposed["index"] = [a for a in range(df_transposed.confidence.count())]
df_transposed = df_transposed.set_index(['index'])

for elem in df_transposed.local.unique():
    print(elem + " - " + str(len(df_transposed[df_transposed.local == elem])))

df = df_transposed

def date_timeToRecord_date(value):
    # 2019-02-13 23:00:00
    return dt.datetime.strptime(value,'%m-%d-%Y_%H:%M:%S')
     

df["record_date"] = df["date_time"].map(lambda x: date_timeToRecord_date(x))
df.drop("date_time", axis=1, inplace=True)


df.confidence = df.confidence.map(lambda x: float(x))
df.currentSpeed = df.currentSpeed.map(lambda x: int(x))
df.freeFlowSpeed = df.freeFlowSpeed.map(lambda x: int(x))
df.currentTravelTime = df.currentTravelTime.map(lambda x: int(x))
df.freeFlowTravelTime = df.freeFlowTravelTime.map(lambda x: int(x))


df.currentSpeed == df.freeFlowSpeed & df.currentTravelTime == df.freeFlowTravelTime

df["flowSpeed"] = df.currentSpeed == df.freeFlowSpeed
df["flowTravelTime"] = df.currentTravelTime == df.freeFlowTravelTime
df["transito"] = df["flowSpeed"] & df["flowTravelTime"]

df.drop('flowSpeed', inplace=True, axis=1)
df.drop('flowTravelTime', inplace=True, axis=1)

df.loc[df["transito"] == "Sem Transito", "transito"] = 0

df["transito"] = (1 - (df.currentSpeed / df.freeFlowSpeed + df.freeFlowTravelTime / df.currentTravelTime)/2) * df.confidence

df_transposed.to_csv (r'data.csv', index=None)

