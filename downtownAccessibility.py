from typing import Tuple
from build_nx import gdf_to_nx, nx_to_gdf
from calcSteepnessLevel import calc_SL, sl_signage
from calcDecay import decay_func
import networkx as nx
import geopandas
import pandas
import numpy

geopandas.options.display_precision = 9
"""
code for computing the travel distance from one-to-many (a point in downtown to all the other points in the network)
considering different LTS and STEEPNESS LEVEL scenarios:

A1. Current network limited to LTS1
A2. Current network limited to LTS2
B1. Current network limited to LTS1 and SL 5.0
B2. Current network limited to LTS2 and SL 5.0
B3. Current network limited to LTS1 and SL 3.5
C1. Improved network limited to LTS1 and SL 5.0.
C2. Improved network limited to LTS2 and SL 5.0.

"""
# source = (298960.2725999993, 5040110.302200001)  point in downtown, messounive

class NetworkPath:
    def __init__(self, G: nx.MultiDiGraph, source: Tuple):
        # self.SG = None
        self.G = G
        self.source = source

    def subgraphGetter(self, attr_lts: str, cutoff_lts: int, attr_sl: str = None, cutoff_sl: int = None)->nx.MultiDiGraph:
        """
        :param attr_lts: name of the lts related field (String)
        :param cutoff_lts: the cutoff value for lts (int)
        :param attr_sl: name of the SL related field (String)
        :param cutoff_sl: the value for SL (3.5, 5)
        :return: a subgraph that satisfies the filters of LTS and SL
        """
        if attr_lts and attr_sl:
            SG = nx.MultiDiGraph([(u,v,d) for u,v,d in self.G.edges(data=True) if d[attr_lts] <= cutoff_lts and
                                d[attr_sl]==cutoff_sl])
        elif attr_lts and not attr_sl:
            SG = nx.MultiDiGraph([(u, v, d) for u, v, d in self.G.edges(data=True) if d[attr_lts] <= cutoff_lts])
        return SG

    def set_shortestPath_value_toNode(self, subG: nx.MultiDiGraph, scenario_name: str):
        """
        :param subG: input subgraph with restricted links
        :param scenario_name: scenario name i.e. "lts2_sl35_dist"
        """
        dist_dict = self.shortestPath(subG, self.source)
        nx.set_node_attributes(self.G, dist_dict, scenario_name)

    def shortestPath(self, G, target=None) -> float: # fromOneToMany
        try:
            # return nx.shortest_path_length(G, source, target, weight='length', method='dijkstra')
            return nx.single_source_dijkstra_path_length(G, self.source, cutoff=8000, weight="length")
        except nx.NetworkXNoPath:
            return -99.0

if __name__ == '__main__':
    streets = geopandas.read_file(
        'C:\\Users\\bitas\\folders\\Research\\Montreal\\codes\\accessibility\\data\\downtown_test_2950.shp')
    print("number of lines: ", len(streets))

    streets[['lts', 'lts_c', 'lts_negD', 'length', 'slope','slope_edit']] = streets[['lts', 'lts_c','lts_negD','length', 'slope', 'slope_edit']].replace(numpy.nan, 0)
    streets['slope_edit'] = streets['slope_edit'].replace(-8888, 0)
    # streets['slope_edit'] = streets['slope_edit'].replace([-8888, numpy.nan], 0)  # or

    # Getting the source point in the network (Peel st & Messounive)
    source_coords = list(streets[streets['fid']==613]['geometry'].item().coords)[0]

    print("Computing Steepness Level...")
    streets[['sl_35', 'sl_5']] = streets.apply(lambda row: pandas.Series(calc_SL(row['length'], row['slope_edit'])),
                                               axis=1)
    streets['unsigned_sl'] = streets.apply(lambda row: min(row['sl_35'], row['sl_5']), axis=1)
    streets['signed_sl'] = streets.apply(lambda row: sl_signage(row['slope'], row['unsigned_sl']), axis=1)

    G = gdf_to_nx(streets)
    net = NetworkPath(G, source_coords)

    print("Computing Shortest Path...")
    # LTS 4 : shortest allowed path to other points on the network
    subG_shortestPath = net.subgraphGetter("lts_final", 4)
    net.set_shortestPath_value_toNode(subG_shortestPath, "lts4")

    print("Computing Scenario A1...")
    # A1. Current network limited to LTS1
    subG_A1 = net.subgraphGetter("lts_final", 1)
    net.set_shortestPath_value_toNode(subG_A1, "lts1")

    print("Computing Scenario A2...")
    # A2. Current network limited to LTS2
    subG_A2 = net.subgraphGetter("lts_final", 2)
    net.set_shortestPath_value_toNode(subG_A2, "lts2")

    print("Computing Scenario B1...")
    # B1. Current network limited to LTS1 and SL 5.0
    subG_B1 = net.subgraphGetter("lts_final", 1, "signed_sl", 5)
    net.set_shortestPath_value_toNode(subG_B1, "lts1_sl5")

    print("Computing Scenario B2...")
    # B2. Current network limited to LTS2 and SL 5.0
    subG_B2 = net.subgraphGetter("lts_final", 2, "signed_sl", 5)
    net.set_shortestPath_value_toNode(subG_B2, "lts2_sl5")

    print("Computing Scenario B3...")
    # B3. Current network limited to LTS1 and SL 3.5
    subG_B3 = net.subgraphGetter("lts_final", 1, "signed_sl", 3.5)
    net.set_shortestPath_value_toNode(subG_B3, "lts1_sl3.5")

    print("Computing Scenario B4...")
    # B4. Current network limited to LTS1 and SL 3.5
    subG_B4 = net.subgraphGetter("lts_final", 2, "signed_sl", 3.5)
    net.set_shortestPath_value_toNode(subG_B4, "lts2_sl3.5")

    # C1. Improved network limited to LTS1 and SL 5.0.
    # subG_B3 = net.subgraphGetter("lts_improved", 1, "signed_sl", 5)
    #
    # C2. Improved network limited to LTS2 and SL 5.0.

    net_vertices, net_gdf = nx_to_gdf(G)
    for sc in ["lts1", "lts2", "lts1_sl5", "lts2_sl5", "lts1_sl3.5", "lts2_sl3.5"]:
        p = f"p_{sc}"
        net_gdf[p] = net_gdf.apply(lambda row : decay_func(row["lts4"], row[sc]))

    net_vertices.to_file('C:\\Users\\bitas\\folders\\Research\\Montreal\\codes\\accessibility\\data\\test_p1.shp')
    net_gdf.to_file('C:\\Users\\bitas\\folders\\Research\\Montreal\\codes\\accessibility\\data\\test_l1.shp')

