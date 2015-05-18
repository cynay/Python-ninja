#!/usr/bin/env python
"""
SYNOPSIS

    TODO 4_Schneider_Yannic [-h,--help] [-v,--verbose] [--version]

DESCRIPTION

    TODO This describes how to use this script. This docstring
    will be printed by the script if there is an error or
    if the user requests help (-h or --help).

EXAMPLES

    TODO: Show some examples of how to use this script.

EXIT STATUS

    TODO: List exit codes

AUTHOR

    Yannic Schneider <cynays@gmail.com>

LICENSE

    This script is in the public domain, free from copyrights or restrictions.

VERSION

    $Id$
"""

import sys, os, traceback, optparse
import time
import re
import networkx as nx
import matplotlib.pyplot as plt
import scipy as sp
import numpy as np
import community
#from pexpect import run, spawn

def average_degree(g):
    """ Generate the average degree of a graph """
    num_nodes = g.number_of_nodes()
    degrees = g.degree()
    average_degree = 0.0

    for node in degrees:
        average_degree += degrees[node]
    print("average degree: "), average_degree / num_nodes
    print("-----\nINFO:\n"), nx.info(g), "\n-----"


def export_histogram():
    """ Export a Histogram out of the graph degree values """
    plt.hist(nw.degree().values(), bins=10)
    plt.savefig('/home/cyn/FFHS/NA-15-ZH/PVA3/graph.png')
    plt.close()


def find_nodes_with_degree(graph, degree):
    """ Find nodes with degree N in a graph and return a list """
    degrees = graph.degree()
    nodes = list()
    
    for node in degrees:
        if degrees[node] == degree:
            nodes.append(node)

    return nodes


def find_highest_degree(graph):
    """ Find the highest degree in a graph """
    degrees = graph.degree()
    max_degree = 0
    
    for node in degrees:
        if degrees[node] > max_degree:
            max_degree = degrees[node]

    return max_degree


def find_lowest_degree(graph):
    """ Find the lowest degree in a graph """
    degrees = graph.degree()
    min_degree = degrees[0]
    
    for node in degrees:
        if degrees[node] < min_degree:
            min_degree = degrees[node]
    
    return min_degree


def make_largest_diameter_graph(N): 
    """ Create a graph with the largest possible diameter for N """
    lg = nx.path_graph(N)
    
    return lg


def make_smallest_diameter_graph(N):
    """ Create a graph with the smallest possible diameter for N """
    sdg = nx.complete_graph(N)
    
    return sdg


def draw_all(graph):
    """ Draw all different layout types for graph """
    nx.draw(graph)
    plt.savefig(path + 'draw.png')
    plt.close()
    nx.draw_circular(graph)
    plt.savefig(path + 'draw_circular.png')
    plt.close()
    nx.draw_random(graph)
    plt.savefig(path + 'draw_random.png')
    plt.close()
    nx.draw_spectral(graph)
    plt.savefig(path + 'draw_spectral.png')
    plt.close()
    nx.draw_spring(graph)
    plt.savefig(path + 'draw_spring.png')
    plt.close()
    nx.draw_shell(graph)
    plt.savefig(path + 'draw_shell.png')
    plt.close()

def main ():
    """ main """
    global options, args, nw, path
    # TODO: Do something more interesting here...
    path = "/home/cyn/FFHS/NA-15-ZH/PVA4/"
    nw = nx.read_gml(path + 'dolphins.gml')

    print("Exercise 3:\n---------------------------------------------------")
    print("Nodes: "), nw.number_of_nodes()
    print("Edges: "), nw.number_of_edges()
    print("Degree of Nodes: "), nw.degree()

    max_degree = find_highest_degree(nw)
    print("Highest degree: "), max_degree
    print("Node/s with highest degree: "), \
        find_nodes_with_degree(nw,max_degree)
   
    min_degree = find_lowest_degree(nw)
    print("Lowest degree: "), min_degree
    print("Node/s with lowest degree: "), \
        find_nodes_with_degree(nw,min_degree)
    
    nx.draw(nw)
    plt.savefig(path + 'schneider-yannic-dolphin.png')
    plt.close()
    #draw_all(nw)

    
    print("\nExercise 4:\n---------------------------------------------------")
    am = nx.to_numpy_matrix(nw)
    np.savetxt(path + "Schneider_Yannic_adjacency.txt", am, \
        delimiter=' ', newline="\n", fmt='%d')
    print 'Adjacency matrix exported to textfile!'

    print("\nExercise 5:\n---------------------------------------------------")
    partition = community.best_partition(nw)
    size = float(len(set(partition.values())))
    pos = nx.spring_layout(nw)
    count = 0
    #   colors = ['#82c38d','#51a35f','#2b823a','#10621e','#00410b']    
    colors = ['#cc3333','#ffcc00','#009900','#0033ff','#663399']

    for com in set(partition.values()):
        count = count + 1
        list_nodes = [nodes for nodes in partition.keys() \
            if partition[nodes] == com]
        nx.draw_networkx_nodes(nw, pos, list_nodes, node_size = 80, \
            node_color = colors[count-1] ) #str(count / size))
    nx.draw_networkx_edges(nw, pos, alpha = 0.5)
    plt.savefig(path + '4_Schneider_Yannic_Dolphin.png')
    plt.close()
    
    print 'Graph exported to image!'

 

if __name__ == '__main__':
    try:
        start_time = time.time()
        parser = optparse.OptionParser(formatter=optparse.TitledHelpFormatter(),
            usage=globals()['__doc__'], version='$Id$')
        parser.add_option ('-v', '--verbose', action='store_true', 
            default=False, help='verbose output')
        (options, args) = parser.parse_args()

        #if len(args) < 1:
        #    parser.error ('missing argument')
        if options.verbose: print time.asctime()
        main()
        if options.verbose: print time.asctime()
        if options.verbose: print 'TOTAL TIME IN MINUTES:',
        if options.verbose: print (time.time() - start_time) / 60.0
        sys.exit(0)
    except KeyboardInterrupt, e: # Ctrl-C
        raise e
    except SystemExit, e: # sys.exit()
        raise e
    except Exception, e:
        print 'ERROR, UNEXPECTED EXCEPTION'
        print str(e)
        traceback.print_exc()
        os._exit(1)

