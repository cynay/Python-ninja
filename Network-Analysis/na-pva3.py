#!/usr/bin/env python
"""
SYNOPSIS

    TODO 3_Schneider_Yannic [-h,--help] [-v,--verbose] [--version]

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
    plt.hist(pg.degree().values(), bins=10)
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


def make_largest_diameter_graph(N): 
    """ Create a graph with the largest possible diameter for N """
    lg = nx.path_graph(N)
    
    return lg


def make_smallest_diameter_graph(N):
    """ Create a graph with the smallest possible diameter for N """
    sdg = nx.complete_graph(N)
    
    return sdg


def main ():
    """ main """
    global options, args, pg
    # TODO: Do something more interesting here...
    pg = nx.read_gml('/home/cyn/FFHS/NA-15-ZH/PVA3/power.gml')
    print("Exercise 3:\n---------------------------------------------------")
    print("Nodes: "), pg.number_of_nodes()
    print("Edges: "), pg.number_of_edges()
    graph_degree = pg.degree()
    print("Degree of Nodes: "), graph_degree
    
    print("\nExercise 4:\n---------------------------------------------------")
    average_degree(pg)
    print("Degree_histogram list: "), nx.degree_histogram(pg)
    export_histogram()
    
    print("\nExercise 5:\n---------------------------------------------------")
    max_degree = find_highest_degree(pg)
    print("Highest degree: "), max_degree
    print("Node/s with highest degree: "), \
        find_nodes_with_degree(pg,max_degree)
    cc = list(nx.connected_component_subgraphs(pg))
    print("Number of CC in the Power-Grid: "), len(cc)
    
    print("\nExercise 6:\n---------------------------------------------------")
    print("Diameter: "), nx.diameter(pg)
    print("Center: "), nx.center(pg)
    
    print("\nExercise 7:\n---------------------------------------------------")
    subnodes = list()
    
    for x in range(10, max_degree+1):
        if len(find_nodes_with_degree(pg,x)) != 0:
            subnodes.extend(find_nodes_with_degree(pg,x))            
    
    sg = pg.subgraph(subnodes)
    scc = list(nx.connected_component_subgraphs(sg))
    print("Number of CC in Subgraph: "), len(scc)   
    max_cc = 0
    largest_cc_id = 0    
    
    for x in range(0, len(scc)):
        if scc[x].number_of_nodes() > max_cc:
            max_cc = scc[x].number_of_nodes()
            largest_cc_id = x
    
    print("Largest component: "), max_cc
    nx.draw_spectral(scc[largest_cc_id])
    plt.savefig('/home/cyn/FFHS/NA-15-ZH/PVA3/largest_connected_component.png')
    plt.close()
    
    print("\nExercise 8:\n---------------------------------------------------")
    lg = make_largest_diameter_graph(10)
    average_degree(lg)
    print("Center: "), nx.center(lg)
    nx.draw_spectral(lg)
    plt.savefig('/home/cyn/FFHS/NA-15-ZH/PVA3/largest_diameter_10.png')
    plt.close()

    sdg = make_smallest_diameter_graph(10)
    average_degree(sdg)
    print("Center: "), nx.center(sdg)
    nx.draw_circular(sdg)
    plt.savefig('/home/cyn/FFHS/NA-15-ZH/PVA3/smallest_diameter_10.png')
    plt.close()
            

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

