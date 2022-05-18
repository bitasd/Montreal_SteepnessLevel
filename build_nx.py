import networkx as nx
import geopandas
from shapely.geometry import Point


def gdf_to_nx(gdf_network):
    # generate graph from GeoDataFrame of LineStrings
    net = nx.MultiDiGraph()
    net.graph['crs'] = gdf_network.crs
    # fields = list(gdf_network.columns)
    fields = ['ID_TRC_int', 'CLASSE', 'SENS_CIR', 'slope', 'slope_edit', 'length', 'lts', 'lts_negD', 'lts_c', 'umbrell_id', 'geometry', 'signed_sl', 'fid'] #

    for index, row in gdf_network.iterrows():

        first = row.geometry.coords[0]
        last = row.geometry.coords[-1]

        data = [row[f] for f in fields]
        attributes = dict(zip(fields, data))
        attr_rev = attributes.copy()

        if attributes['SENS_CIR'] == -1:
            # add a REVERSED edge w with-flow lane


            attr_rev['slope_edit'] = attributes['slope_edit'] * (-1)
            attr_rev['signed_sl'] = attributes['signed_sl'] * (-1)
            attr_rev['lts_final'] = attributes['lts']
            net.add_edge(last, first, **attr_rev)

            if attributes['lts_c'] != -9999:
                # add an edge w contraflow lane
                attributes['lts_final'] = attributes['lts_c']
                net.add_edge(first, last, **attributes)

        elif attributes['SENS_CIR'] == 1:
            attributes['lts_final'] = attributes['lts']
            net.add_edge(first, last, **attributes)

            if attributes['lts_c'] != -9999:
                # add a REVERSED edge with contraflow lane
                attr_rev['slope_edit'] = attributes['slope_edit'] * (-1)
                attr_rev['signed_sl'] = attributes['signed_sl'] * (-1)
                attr_rev['lts_final'] = attributes['lts_c']
                net.add_edge(last, first, **attr_rev)

        elif attributes['SENS_CIR'] == 0:
            # add edge
            attributes['lts_final'] = attributes['lts']
            net.add_edge(first, last, **attributes)

            # add reversed edge
            attr_rev['slope_edit'] = attributes['slope_edit'] * (-1)
            attr_rev['signed_sl'] = attributes['signed_sl'] * (-1)

            if attributes['lts_negD']!= -9999:  # asymmetric situation
                attr_rev['lts_final'] = attributes['lts_negD']

            else:  # symmetric situation
                attr_rev['lts_final'] = attributes['lts']

            net.add_edge(last, first, **attr_rev)

        else:
            print('elsed out')

    return net


def nx_to_gdf(net, nodes=True, edges=True):
    # generate nodes and edges geodataframes from graph
    if nodes is True:
        print('nodes')
        node_xy, node_data = zip(*net.nodes(data=True))

        gdf_nodes = geopandas.GeoDataFrame(list(node_data), geometry=[Point(i, j) for i, j in node_xy])
        print("gdf_nodes: ", len(gdf_nodes))
        gdf_nodes.crs = net.graph['crs']

    if edges is True:
        print('edges')
        starts, ends, edge_data = zip(*net.edges(data=True))
        gdf_edges = geopandas.GeoDataFrame(list(edge_data))
        print("gdf_edges: ", len(gdf_edges))
        gdf_edges.crs = net.graph['crs']

    if nodes is True and edges is True:
        print('1')
        return gdf_nodes, gdf_edges
    elif nodes is True and edges is False:
        print('2')
        return gdf_nodes
    else:
        print('3')
        return gdf_edges



