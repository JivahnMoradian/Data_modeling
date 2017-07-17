import os
import sys
import lib
import h5py
import datetime
import numpy as np
import netCDF4 as nc
import geospatialtools.gdal_tools as gst

# Variables that will be needed by this program
json_file = sys.argv[1] 
output_file = "test.tif"
last_output = "new.tif"
start_date = datetime.datetime(2002,1,1)
end_date = datetime.datetime(2014,12,31)

# Uses the library to read in the concerned files and retrieve the necessary
# information
jfile = lib.read_json_file(json_file)
cluster,image = lib.get_files(jfile)
res = lib.get_resolution(jfile)
var = lib.get_vars(jfile)
start,end = lib.get_dates(jfile)
dates,trim,index = lib.get_date_array(start_date,end_date,start,end)
sp = lib.get_spatial_limits(jfile)
tile = nc.Dataset(cluster)
geo = gst.retrieve_metadata(image)
nx,ny = geo['nx'],geo['ny']

# Performs warping on the template image; creates a new h5 file
lib.warp("tr",res,res,sp[0],sp[1],sp[2],sp[3],image,output_file)
template = gst.read_raster(output_file)
template[:] = np.arange(template.size).reshape(template.shape)
md = gst.retrieve_metadata(output_file)
md['nodata'] = -9999
gst.write_raster(output_file,md,template)
lib.warp("ts",nx,ny,sp[0],sp[1],sp[2],sp[3],output_file,last_output)
tiles = gst.read_raster(image)
upscaled = gst.read_raster(last_output)
f = h5py.File("Try.h5","w")

# Iterates through the variables specified by the input json file
for v in var:
    tile_var = tile['%s_tile'%v][index,:,0,0]
    list_var = []

    for up in np.unique(upscaled):
        tiles_upscaled = tiles[up == upscaled]
        lis = []
        unique_tiles = np.unique(tiles_upscaled).astype(int)
        unique_tiles = unique_tiles[unique_tiles != -9999]
        for un in unique_tiles: lis.append(np.sum(tiles_upscaled == 
            un)/float(tiles_upscaled[tiles_upscaled != -9999].size))
        lis = np.array(lis)
        out = np.sum(tile_var[:,unique_tiles]*lis,axis=1)
        list_var.append(out)
    
    # Creates a new group for this variable in the h5 file, and fills it with
    # the data acquired (both spatially and for the different time steps)
    list_var = np.array(list_var)
    group = f.create_group(v)
    data = group.create_dataset("init",data=list_var)





