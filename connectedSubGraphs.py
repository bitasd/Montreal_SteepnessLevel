from graph_to_nx import gdf_to_nx, nx_to_gdf
import networkx as nx
import geopandas

geopandas.options.display_precision = 9
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    streets = geopandas.read_file(
        'C:\\Users\\bitas\\folders\\Research\\Montreal\\mojde\\Accessibility\\summer\\summer_12.shp')

    # streets['fid'] = streets['fid2'].astype('int')
    # scenario I : current Summer low-stress network
    streets['lts'].fillna(1, inplace=True)
    sc_1 = streets.loc[streets['lts'].isin([1])]
    # converting GeoDataframe to networkX
    G_1 = gdf_to_nx(sc_1)
    # finding connected subgraphs
    connected_subgraphs = [G_1.subgraph(cc) for cc in nx.connected_components(G_1)]
    # sorting subgraphs based on their size
    connected_subgraphs_dict = {cc.number_of_nodes(): cc for cc in connected_subgraphs}
    connected_subgraphs_dict_sorted = {k: connected_subgraphs_dict[k] for k in sorted(connected_subgraphs_dict)}

    # for size, subG in enumerate(connected_subgraphs):
    i = len(connected_subgraphs_dict_sorted)
    while i > 10:
        nx1 = nx_to_gdf(list(connected_subgraphs_dict_sorted.values())[i - 1])
        nx1[1].to_file(f"C:\\Users\\bitas\\folders\\Research\\Montreal\\Analysis\\Accessibility\\_scenario_I\\"
                       f"sub_{i}.gpkg",
                       driver="GPKG")
        i -= 1

    # scenario II : improved Summer low-stress network
    streets['lts'].fillna(1, inplace=True)
    # sc_1 = streets.loc[streets['lts_w'].isin([1])]
    # converting GeoDataframe to networkX
    G_1 = gdf_to_nx(streets)
    # finding connected subgraphs
    connected_subgraphs = [G_1.subgraph(cc) for cc in nx.connected_components(G_1)]
    # sorting subgraphs based on their size
    connected_subgraphs_dict = {cc.number_of_nodes(): cc for cc in connected_subgraphs}
    connected_subgraphs_dict_sorted = {k: connected_subgraphs_dict[k] for k in sorted(connected_subgraphs_dict)}

    # for size, subG in enumerate(connected_subgraphs):
    i = len(connected_subgraphs_dict_sorted)
    while i > 10:
        nx1 = nx_to_gdf(list(connected_subgraphs_dict_sorted.values())[i - 1])
        nx1[1].to_file(f"C:\\Users\\bitas\\folders\\Research\\Montreal\\Analysis\\Accessibility\\_scenario_II\\"
                       f"sub_{i}.gpkg",
                       driver="GPKG")
        i -= 1

    # scenario III : Winter low-stress network
    streets['lts_w'].fillna(1, inplace=True)
    sc_2 = streets.loc[streets['lts_w'].isin([1])]
    # converting GeoDataframe to networkX
    G_1 = gdf_to_nx(sc_2)
    # finding connected subgraphs
    connected_subgraphs = [G_1.subgraph(cc) for cc in nx.connected_components(G_1)]
    # sorting subgraphs based on their size
    connected_subgraphs_dict = {cc.number_of_nodes(): cc for cc in connected_subgraphs}
    connected_subgraphs_dict_sorted = {k: connected_subgraphs_dict[k] for k in sorted(connected_subgraphs_dict)}

    # for size, subG in enumerate(connected_subgraphs):
    i = len(connected_subgraphs_dict_sorted)
    while i > 10:
        nx1 = nx_to_gdf(list(connected_subgraphs_dict_sorted.values())[i - 1])
        nx1[1].to_file(f"C:\\Users\\bitas\\folders\\Research\\Montreal\\Analysis\\Accessibility\\_scenario_III\\"
                       f"sub_{i}.gpkg",
                       driver="GPKG")
        i -= 1

# len(c) for c in sorted(nx.connected_components(G), key=len, reverse=True)]
