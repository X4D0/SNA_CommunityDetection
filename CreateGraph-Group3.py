import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

#import relasi.csv
df_relation = pd.read_csv("relasi.csv")
# Read Edge List
G = nx.from_pandas_edgelist(df_relation,'Source','Target')
# Show Network Info
print(nx.info(G))
# Visualize the Graph using NetworkX
pos = nx.spring_layout(G)
plt.axis('off')
nx.draw_networkx(G, pos=pos, with_labels=False, node_size=10, node_color='r', edgecolors='black')
plt.show()
