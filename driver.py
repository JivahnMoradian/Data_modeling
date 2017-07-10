import lib
import sys
import h5py
import datetime
import numpy as np
import netCDF4 as nc
import geospatialtools.gdal_tools as gst

# Variables that will be needed by this program
file_name = sys.argv[1]
ifile = "image1.tif"
ofile = "image2.tif"
h5file = "image.h5"
start_of_time = datetime.datetime(2002,1,1)
end_of_time = datetime.datetime(2014,12,31)

# Uses the library to read in the concerned files; gets the necessary
# information from the json file; creates an empty h5 file
data = lib.read_json_file(file_name)
map_name,image_name = lib.get_files(data)
start_date, end_date = lib.get_dates(data)
res = lib.get_resolution(data)
spatial = lib.get_spatial_limits(data)
variables = lib.get_vars(data)
dates,trim_dates = lib.get_date_array(start_of_time,end_of_time,start_date,end_date)
tile = nc.Dataset(map_name)
geo = gst.read_raster(image_name)
md = gst.retrieve_metadata(image_name)
md['nodata'] = -9999
f = h5py.File(h5file,"w")

# Iterates through the variables of interest
for var in variables:
    tile_var = tile['%s_tile' % var][:,:,0,0]
    new = np.copy(geo)
    x = np.unique(new).astype(np.int32)
    x = x[x != -9999]
    lis = []
    
    # Iterates through all relevant dates; creates an image for each date and
    # warps if using gdal; append each date's data to the list
    for date in trim_dates:
        for i in x: new[geo == i] = tile_var[(dates == date),i]    
        gst.write_raster(ifile,md,new)
        lib.warp(res,res,spatial[0],spatial[1],spatial[2],spatial[3],ifile,ofile)
        im = np.asarray(gst.read_raster(ofile))
        lis.append(im)

    # Creates a new group for this variable in the h5 file; fills it with the
    # data obtained for all the time steps
    array = np.array(lis)
    group = f.create_group(var)
    data = group.create_dataset("init",data=array)



