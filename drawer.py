import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.signal import find_peaks
import json

with open('result.json', 'r') as file:
    data = json.load(file)

df = pd.DataFrame(data)
df['Timestamp'] = pd.to_datetime(df['Timestamp'])

frequency_df = df['Timestamp'].dt.floor('S').value_counts().sort_index()
peaks, _ = find_peaks(frequency_df.values, distance=1)
peak_seconds = frequency_df.index[peaks]

plt.figure(figsize=(12, 6))
plt.scatter(frequency_df.index, frequency_df.values)
plt.plot(frequency_df.index, frequency_df.values)
plt.title("API Request Frequency with cluster peaks")
plt.xlabel("Time(per second)")
plt.ylabel("Number of Request")
plt.grid(True)

clusters = {}
i = 0
for peak_second in peak_seconds:
    # 画图
    i += 1
    plt.plot(peak_second, frequency_df.loc[peak_second], "ro")
    plt.text(peak_second, frequency_df.loc[peak_second], f'Cluster{i}', color='red')
    plt.axvspan(peak_second, peak_second + pd.Timedelta(seconds=1), color='red', alpha=0.3)
    plt.axvspan(peak_second - pd.Timedelta(seconds=1), peak_second, color='red', alpha=0.3)
    # 聚类
    start_second = peak_second - pd.Timedelta(seconds=1)
    end_second = peak_second
    mask = (df['Timestamp']>= start_second) & (df['Timestamp'] <= end_second)
    clusters[f'Cluster{i}'] = df[mask].to_dict('records')

print(clusters)

for cluster, data in clusters.items():
    for entry in data:
        entry['Timestamp'] = entry['Timestamp'].strftime('%Y-%m-%d %H:%M:%S')

with open('cluster_result.json', 'w') as f:
    json.dump(clusters, f, indent=1)

plt.show()