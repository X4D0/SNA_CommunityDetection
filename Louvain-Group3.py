import community as community_louvain
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

# import csv
df = pd.read_csv('relasi.csv')

# load the karate club graph
G = nx.from_pandas_edgelist(df,'Source','Target')

# compute the best partition
partition = community_louvain.best_partition(G)

# List member from community
max_k_w = []
for com in set(partition.values()):
    list_nodes = [nodes for nodes in partition.keys()
                  if partition[nodes] == com]
    max_k_w = max_k_w + [list_nodes]
node_mapping = {}
map_v = 0
for node in G.nodes():
    node_mapping[node] = map_v
    map_v += 1
community_num_group = len(max_k_w)
print('Total Komunitas terbentuk :',community_num_group)
modularity = community_louvain.modularity(partition, G)
print('Nilai Modularity :', modularity)

#Sort Down Community
z = sorted( max_k_w, key=len, reverse=True )

# Select Top 3 Community
z = z[0:3]
#Create new graph for every Top Community
i = 0
for x in z:
    Grr = nx.Graph()
    i = i+1
    print('\nKomunitas ke-',i,' dengan jumlah anggota: ',len(x))
    print('Dengan modularity:',partition[x[0]])
    print('Dengan Anggota: ',x)
    Grr.add_nodes_from(x)
    for y in x:
        for q in G.edges([y]):
            Grr.add_edge(*q)
    
    # Get Tweet's Author
    cc = nx.degree_centrality(Grr)
    df_cc = pd.DataFrame.from_dict({
        'node': list(cc.keys()),
        'centrality': list(cc.values())
    })
    cc_result = df_cc.sort_values('centrality', ascending=False)
    print('Pembuat Tweet :', cc_result.iat[0,0])
    search = df[df['Source'] == cc_result.iat[0,0]]
    found = search['TweetID'].value_counts().idxmax()
    print('Tweet ID :', found)
    
    # Draw Graph
    pos = nx.spring_layout(Grr)
    nx.draw_networkx_nodes(Grr, pos, node_size=5)
    nx.draw_networkx_edges(Grr, pos, alpha=0.2)
    plt.show()


