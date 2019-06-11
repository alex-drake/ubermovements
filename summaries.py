# -*- coding: utf-8 -*-
"""
Created on Wed May 15 09:34:59 2019

@author: Admin-dev
"""

import pandas as pd
import numpy as np
import os
import osmnx as ox
import geopandas as gpd

file_list = set(os.listdir('./data/'))

# check to see if the uberspeeds.graphml has already been created, if not, make it
if 'uberspeeds.graphml' in file_list:
    london_graph = ox.save_load.load_graphml('uberspeeds.graphml',folder='data')
    
else:
    # import segments look-up, available from Uber Movements
    segments = pd.read_csv('./data/segments_lookup.csv')

    # import output from sql query (could have queried direct into Python, but cba)
    uber_df = pd.read_csv('./data/outputs.csv')

    uber_df = uber_df.merge(segments, how='left', on='segment_id')

    uber_summary = uber_df[['osm_way_id','sum_mn_spd','sum_std_spd']].groupby(['osm_way_id'], as_index=False).sum()
    uber_summary['speed'] = uber_summary['sum_mn_spd'] / uber_summary['sum_std_spd']
    
    # check to see if London outline exists, if not import shapefile and use (not in repo, and use your own city!)
    if 'london.graphml' in file_list:
        london_graph = ox.save_load.load_graphml('london.graphml',folder='data')
    else:
        london_outline = gpd.read_file('../gis/london.shp')
        london_graph = ox.graph_from_polygon(london_outline.geometry.to_dict()[0], network_type='drive')
        ox.save_load.save_graphml(london_graph, filename='london.graphml', folder='data')
    
    for from_node, to_node, edge in london_graph.edges(data=True):
        
        # first we'll iterate through the edge id's to determine the associated ubers speed
        osm_id = edge['osmid']
        
        if type(osm_id) == list:
            
            uber_speed = list()
            
            # extract each element of the array (each id match) and add to the speed list
            for element in osm_id:            
                uber_speed.append(uber_summary['speed'][uber_summary['osm_way_id'] == element].mean())
            
            # calculate average speed from the speed array, dropping any NaN values
            uber_speed = np.nanmean(np.array(uber_speed))
    
        else:
            uber_speed = uber_summary['speed'][uber_summary['osm_way_id'] == osm_id].mean()
        
        # now let's iterate through the posted speed limit(s)
        try:    
            speeds = edge['maxspeed']
        except KeyError:
            speeds = str('unknown')
        
        if type(speeds) == list:
            speed_lim = list()
            
            for speed in speeds:
                speed_lim.append(pd.to_numeric(speed.split(' ')[0], errors=np.nan, downcast='float'))
            
            speed_lim = np.nanmax(np.array(speed_lim))
        else:
            speed_lim = pd.to_numeric(speeds.split(' ')[0], errors=np.nan, downcast='float')
        
        # add to edge data
        # calculate speed-to-limit ratio
        diff = uber_speed / speed_lim
        # assign linewidth for different ratios
        lw = 2 if 1 <= diff < 1.25 else 3 if diff >= 1.25 else 1
        # assign different line colour for different ratios
        colour = '#ffbf00' if 1 <= diff < 1.25 else '#99cc99' if diff < 1 else '#f60404' if diff >= 1.25 else '#c6c7be'
        
        # add back into graph
        london_graph[from_node][to_node][0]['uberspeedmph'] = uber_speed
        london_graph[from_node][to_node][0]['speedint'] = speed_lim
        london_graph[from_node][to_node][0]['diff'] = uber_speed / speed_lim
        london_graph[from_node][to_node][0]['colours'] = colour
        london_graph[from_node][to_node][0]['lw'] = lw
    
    # save this for use later
    ox.save_load.save_graphml(london_graph, filename='uberspeeds.graphml', folder='data')

# copy and run this in the console to get a pop-up window:- %matplotlib qt5
# you can then save specific plots from there. If you know where to look, you could just set plot limits instead (again, cba)
# set edge colors
nodes, edges = ox.graph_to_gdfs(london_graph)
edges.oneway = edges.oneway.apply(lambda x: int(x == 'true'))
edges_lite = edges[['colours','diff','geometry','speedint','u','v','uberspeedmph']]
edges_lite.to_file('./data/uberspeeds.geojson', driver='GeoJSON') # save for later

ec = pd.DataFrame([data for u, v, data in london_graph.edges(data=True)])
ec['colours'][ec.colours.isna()] = '#c6c7be'
ec['lw'][ec.lw.isna()] = 1

fig, ax = ox.plot_graph(london_graph, edge_color=ec['colours'], edge_linewidth=ec['lw'], 
                        node_size=1, node_zorder=1, fig_height=16, dpi=420)