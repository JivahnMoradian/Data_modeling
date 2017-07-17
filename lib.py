import os
import json
import datetime
import numpy as np

# Reads in the relevant json file
def read_json_file(file_name): return json.load(open(file_name))

# Gets the relevant map and image files
def get_files(data): return data['map_name'],data['image_name']

# Gets the spatial limits of interest
def get_spatial_limits(data):
    minlat = data['spatial_limits'][0]['minlat']
    minlon = data['spatial_limits'][1]['minlon']
    maxlat = data['spatial_limits'][2]['maxlat']
    maxlon = data['spatial_limits'][3]['maxlon']
    return np.array([minlon,minlat,maxlon,maxlat])

# Gets the desired resolution
def get_resolution(data):
    res = data['resolution'].split("/")
    return float(res[0])/float(res[1])

# Gets the desired start and end dates
def get_dates(data):
    d1 = np.array(data['time_interval'][0]['start_date'].split(","))
    d2 = np.array(data['time_interval'][1]['end_date'].split(","))
    date1 = datetime.datetime(int(d1[0]),int(d1[1]),int(d1[2]))
    date2 = datetime.datetime(int(d2[0]),int(d2[1]),int(d2[2]))
    return [date1,date2]

# Gets the variables of interest
def get_vars(data): return data['vars']

# Creates arrays of all possible dates and of all dates of interest
def get_date_array(start,end,start_date,end_date):
    date1,date2 = start,end
    dates = []
    while (date1 <= date2):
        dates.append(date1)
        date1 = date1 + datetime.timedelta(days=1)
    trim = dates[dates.index(start_date):dates.index(end_date)+1]
    dates = np.array(dates)
    trim = np.array(trim)
    index = []
    for i in range(dates.size):
        if (dates[i] in trim): index.append(i)
    index = np.array(index)
    return [dates,trim,index]

# Performs the image warping with the command line
def warp(t,a,b,c,d,e,f,g,h):
    os.system('rm %s'%(h))
    os.system('gdalwarp -%s %f %f -te %f %f %f %f %s %s'%(t,a,b,c,d,e,f,g,h))



