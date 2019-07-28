import pandas as pd
import numpy as np
import pickle
import networkx as nx
import matplotlib.pyplot as plt
import collections
import sys

#function for forming an edge list. Each element in the edge list is a pair of authors which means they are co-author
def form_edge_list(records):
    m, n = np.shape(records)
    edgelist = []

    for index in range(m):
        authors = records[index, 2]
        num_of_authors = len(authors)

        i = 0;
        while i < num_of_authors - 1:
            j = i + 1
            while j < num_of_authors:
                if (authors[i], authors[j]) not in edgelist and (authors[j], authors[i]) not in edgelist:
                    edgelist = edgelist + [(authors[i], authors[j])]
                j += 1
            i += 1
    return edgelist

#function for plotting the graph of authorship network
def plot_graph(graph):
    pos = nx.spring_layout(graph)
    nx.draw_networkx_nodes(graph, pos, node_size = 25)
    nx.draw_networkx_edges(graph, pos, alpha=0.7)
    plt.axis('off')
    plt.show()

#function for plotting histograms
def plot_histogram(sequence, graph_title, x_label, y_label, width_value):
    count = collections.Counter(sequence)
    value, value_count = zip(*count.items())

    fig, ax = plt.subplots()
    plt.bar(value, value_count, width = width_value, color = 'b')

    plt.title(graph_title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    if graph_title == "Degree Histogram" or graph_title == "Diameter Histogram":
        ax.set_xticks(value)
        ax.set_xticklabels(value)
    else:
        diff = (max(value) - min(value))/12
        current_value = min(value)
        xticks = [current_value]
        while current_value < max(value):
            current_value += diff
            xticks.append(current_value)
        ax.set_xticks(xticks)
        ax.set_xticklabels("{:.5f}".format(d) for d in xticks)
        
    plt.show()
    

#start of main block where execution will begin
if __name__ == '__main__':

    #open the file having authorship records
    file = None
    try:
        file = open("data.pkl", 'rb')
    except FileNotFoundError:
        sys.exit("Error: First run coauthorship_scraper.py to generate data.pkl file")
        
    data_frame = pickle.load(file)
    rows = data_frame.values;


    #call function form_edge_list to generate an edge list for the network
    edge_list = form_edge_list(rows)

    #generate graph using the edge list
    graph = nx.Graph()
    graph.add_edges_from(edge_list)

    #call function plot_graph to plot the graph
    plot_graph(graph)
    

    #calculate degree of all nodes and plot histogram of degree vs no of nodes with each degree
    degree = nx.degree(graph)
    degree_sequence = sorted([d for n, d in degree])
    plot_histogram(degree_sequence, "Degree Histogram", "Degree", "Number of Nodes", 0.80)
    

    #calculate clustering coefficient of all nodes and plot histogram of clustering coefficient vs no of nodes with each clustering coefficient
    clustering_coefficient = nx.clustering(graph)
    clustering_sequence = sorted(list(clustering_coefficient.values()))
    plot_histogram(clustering_sequence, "Clustering Coefficient Histogram", "Clustering Coefficient", "Number of Nodes", 0.02)
    

    #calculate closeness centrality of all nodes and plot histogram of closeness centrality vs no of nodes with each closeness centrality
    closeness = nx.closeness_centrality(graph)
    closeness_sequence = sorted(list(closeness.values()))
    plot_histogram(closeness_sequence, "Closeness Centrality Histogram", "Closeness Centrality", "Number of Nodes", 0.001)
    

    #calculate betweenness centrality of all nodes and plot histogram of betweenness centrality vs no of nodes with each betweenness centrality
    betweenness = nx.betweenness_centrality(graph)
    betweenness_sequence = sorted(list(betweenness.values()))
    plot_histogram(betweenness_sequence, "Betweenness Centrality Histogram", "Betweenness Centrality", "Number of Nodes", 0.001)
    

    #calculate page rank of all nodes and plot histogram of page rank vs no of nodes with each page rank
    page_rank = nx.pagerank(graph, alpha=0.9)
    pr_sequence = sorted(list(page_rank.values()))
    plot_histogram(pr_sequence, "Page Rank Histogram", "Page Rank", "Number of Nodes", 0.001)
    

    #calculate diameter of all connected components and plot histogram of diameter vs no of connected components with each diameter
    connected_components = nx.connected_component_subgraphs(graph)
    diameters = []
    for component in connected_components:
        diameter = nx.diameter(component)
        diameters.append(diameter)
    diameter_sequence = sorted(diameters)
    plot_histogram(diameter_sequence, "Diameter Histogram", "Diameter", "Number of Connected Components", 0.80)
    





