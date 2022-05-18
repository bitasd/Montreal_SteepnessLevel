from typing import Tuple
from build_nx import gdf_to_nx, nx_to_gdf
from calcSteepnessLevel import calc_SL, sl_signage
import networkx as nx
import geopandas
import pandas
import numpy

geopandas.options.display_precision = 9
"""
code for computing the travel distance from one-to-many (a point in downtown to all the other points in the network)
considering different LTS and STEEPNESS LEVEL scenarios
 
"""
# target=(278628.3641313674, 5033125.887933079),
# source = (278628.36409999843, 5033125.8878999995)  point in downtown, messounive
# source = (278529.6318000001, 5032826.068999999)  sub_22

class NetworkPath:
    def __init__(self, G, source: Tuple):
        # self.SG = None
        self.G = G
        self.source = source
#TODO: change the SL criteria
    def subgraphGetter(self, attr_lts: str, cutoff_lts: int, attr_sl: str = None, cutoff_sl: int = None)->nx.MultiGraph:
        """
        :param attr_lts: name of the lts related field (String)
        :param cutoff_lts: the cutoff value for lts (int)
        :param attr_sl: name of the SL related field (String)
        :param cutoff_sl: the boolean value for lts (int 0, 1)
        :return: a subgraph that satisfies the filters of LTS and SL
        """
        if attr_lts and attr_sl:
            SG = nx.MultiGraph([(u,v,d) for u,v,d in self.G.edges(data=True) if d[attr_lts] <= cutoff_lts and
                                d[attr_sl]==cutoff_sl])
        elif attr_lts and not attr_sl:
            SG = nx.MultiGraph([(u, v, d) for u, v, d in self.G.edges(data=True) if d[attr_lts] <= cutoff_lts])
        return SG

    def set_shortestPath_value_toNode(self, subG, scenario_name: str):
        """
        :param subG: input subgraph with restricted links
        :param scenario_name: scenario name i.e. "lts2_sl35_dist"
        """
        dist_dict = self.shortestPath(subG, self.source)
        nx.set_node_attributes(self.G, dist_dict, scenario_name)

    def shortestPath(self, G, source: Tuple, target=None) -> float: # fromToMany
        try:
            # return nx.shortest_path_length(G, source, target, weight='length', method='dijkstra')
            return nx.single_source_dijkstra_path_length(G, source, cutoff=8000, weight="length")
        except nx.NetworkXNoPath:
            return -99.0

if __name__ == '__main__':
    streets = geopandas.read_file(
        # 'C:\\Users\\bitas\\folders\\Research\\Montreal\\mojde\\Accessibility\\summer\\summer_12.shp')
        'C:\\Users\\bitas\\folders\\Research\\Montreal\\codes\\accessibility\\data\\downtown_test_2950.shp')
        # 'C:\\Users\\bitas\\folders\\Research\\Montreal\\Analysis\\Accessibility\\_scenario_III\\sub_22.gpkg')

    streets[['lts', 'lts_c', 'length', 'slope_edit']] = streets[['lts', 'lts_c','length', 'slope_edit']].replace(numpy.nan, 0)
    #TODO: change slope_edit -8888 to 0
    #TODO: replace nan with 0 for fields slope, slope_edit, lts
    streets[['sl_35', 'sl_5']] = streets.apply(lambda row: pandas.Series(calc_SL(row['length'], row['slope_edit'])),
                                               axis=1)
    streets['unsigned_sl'] = streets.apply(lambda row: min(row['sl_35'], row['sl_5']), axis=1)
    streets['signed_sl'] = streets.apply(lambda row: sl_signage(row['slope_edit'], row['unsigned_sl']), axis=1)
    G = gdf_to_nx(streets)
    net = NetworkPath(G, (298960.2725999993, 5040110.302200001))
    # LTS 4 : minimum distance to other points allowed on the network
    net.set_shortestPath_value_toNode(G, "lts4_dist")
    # LTS 2
    subG_2 = net.subgraphGetter("lts", 2)
    net.set_shortestPath_value_toNode(subG_2, "lts2_dist")
    # LTS 1 & SL 3.5
    subG_3 = net.subgraphGetter("lts", 1, "sl_35", 3.5)
    net.set_shortestPath_value_toNode(subG_3, "lts1_sl35_dist")
    # LTS 2 & SL 3.5
    subG_4 = net.subgraphGetter("lts", 2, "sl_35", 3.5)
    net.set_shortestPath_value_toNode(subG_4, "lts2_sl35_dist")

    graph = nx_to_gdf(G)
    graph[0].to_file('C:\\Users\\bitas\\folders\\Research\\Montreal\\codes\\accessibility\\data\\downtown_test_2950_access.shp')
    graph[1].to_file('C:\\Users\\bitas\\folders\\Research\\Montreal\\codes\\accessibility\\data\\downtown_test_2950_access1.shp')






