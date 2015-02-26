import os
import numpy as np
import matplotlib
matplotlib.use('Agg')

from matplotlib.pyplot import *

# Make sure england-basemap-osgrid.tiff is downloaded to this directoty
DOWNLOADS_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__)))

# Firstly, define the URLs from which we'll be fetching the data. These URLs
# come from
# http://data.gov.uk/dataset/live-traffic-information-from-the-highways-agency-road-network.
PREDEFINED_LOCATIONS_DOCUMENT_URL = 'http://hatrafficinfo.dft.gov.uk/feeds/datex/England/PredefinedLocationJourneyTimeSections/content.xml'
JOURNEY_TIME_DOCUMENT_URL = 'http://hatrafficinfo.dft.gov.uk/feeds/datex/England/JourneyTimeData/content.xml'

# Fetch and parse the data
from lxml.objectify import parse
from lxml.etree import tostring
from urllib2 import urlopen

locations_root = parse(urlopen(PREDEFINED_LOCATIONS_DOCUMENT_URL)).getroot()
journey_time_root = parse(urlopen(JOURNEY_TIME_DOCUMENT_URL)).getroot()

locations = list(locations_root.payloadPublication.predefinedLocationSet.predefinedLocation)

def location_to_lnglat_pair(location):
    to = location.predefinedLocation.tpeglinearLocation.to
    from_ = location.predefinedLocation.tpeglinearLocation['from']
    to_lnglat = (float(to.pointCoordinates.longitude), float(to.pointCoordinates.latitude))
    from_lnglat = (float(from_.pointCoordinates.longitude), float(from_.pointCoordinates.latitude))
    return (to_lnglat, from_lnglat)

location_segments = dict((l.attrib['id'], location_to_lnglat_pair(l)) for l in locations)
location_ids = location_segments.keys()

from osgeo import osr

bng = osr.SpatialReference()
bng.ImportFromEPSG(27700)

wgs84 = osr.SpatialReference()
wgs84.ImportFromEPSG(4326)

wgs84_to_bng = osr.CoordinateTransformation(wgs84, bng)

# Co-ordinate transform includes height and so we need to define a little helper function
def segment_to_bng(segment):
    return list(x[:2] for x in wgs84_to_bng.TransformPoints(segment))

segment_coords = np.array(list(segment_to_bng(location_segments[loc]) for loc in location_ids))


import os
from osgeo import gdal

# DOWNLOADS_DIR is the location of your downloads folder
map_ds_file = os.path.join(DOWNLOADS_DIR, 'england-basemap-osgrid.tiff')
if not os.path.isfile(map_ds_file):
    import sys
    print('Expected to find England basemap at ' + map_ds_file)
    sys.exit(1)

base_map_ds = gdal.Open(map_ds_file)

# The geo-transform maps pixel co-ordinates to image locations
origin_x, pixel_size_x, _, origin_y, _, pixel_size_y = base_map_ds.GetGeoTransform()

# Compute minx, maxx, miny, maxy for image. Notice that, since pixel_size_y is -ve, the miny is not origin_y.
base_map_extent = (
    origin_x, origin_x + pixel_size_x * base_map_ds.RasterXSize,
    origin_y + pixel_size_y * base_map_ds.RasterYSize, origin_y,
)

base_map = np.transpose(base_map_ds.ReadAsArray(), (1,2,0))

# Putting it together

# Offsetting segments
# Compute 'left' unit vector for each segment

# Unit direction of each segment
segment_directions = segment_coords[:,1,:] - segment_coords[:,0,:]
segment_directions /= np.sqrt((segment_directions ** 2).sum(-1))[..., np.newaxis]

# 'Left' is just direction rotated 90 degrees
segment_offsets = segment_directions.dot(np.array([[0, 1], [-1, 0]]))

from matplotlib import transforms

# Parsing Journey Times

# Parse publication time
import iso8601
data_time = iso8601.parse_date(journey_time_root.payloadPublication.publicationTime.text)
data_time.strftime('%X, %x')

# Extract the data themselves
journey_time_elems = list(journey_time_root.payloadPublication.elaboratedData)

def extract_journey_times(datum):
    bdv = datum.basicDataValue
    return bdv.affectedLocation.locationContainedInGroup.predefinedLocationReference.text, (float(bdv.travelTime), float(bdv.freeFlowTravelTime), float(bdv.normallyExpectedTravelTime))

journey_times = dict(extract_journey_times(elem) for elem in journey_time_elems)
journey_time_data = np.array(list(journey_times[loc_id] if loc_id in journey_times else (np.nan, np.nan, np.nan) for loc_id in location_ids))

# Plotting the final result

# Extract the data we want to plot. In this case it is delay time.
data = (journey_time_data[:,0] - journey_time_data[:,2]) / 60

# Find where the 'good' (i.e. non-NaN and non-zero) data is
good_data = np.logical_and(np.isfinite(data), journey_time_data[:,0] > 0)

figure(figsize=(8,8))

# Plot the base map at 50% opacity over a black background
gca().set_axis_bgcolor((0,0,0))
imshow(base_map, extent=base_map_extent, alpha=0.7)

# Add the line collection which is just the links
from matplotlib.collections import LineCollection
lc = LineCollection(segment_coords, lw=6, color='white', alpha=0.2)
gca().add_collection(lc)

# Add the LineCollection showing bad data
lc = LineCollection(segment_coords[np.logical_not(good_data),...],
    lw=2, color='gray',
    offsets=3*segment_offsets[np.logical_not(good_data),...], transOffset=transforms.IdentityTransform())
gca().add_collection(lc)

# Add the LineCollection showing good data
lc = LineCollection(segment_coords[good_data,...],
    array=data[good_data], cmap=cm.RdYlGn_r, clim=(15, 45), lw=2,
    offsets=3*segment_offsets[good_data,...], transOffset=transforms.IdentityTransform())
gca().add_collection(lc)

# Add a colour bar
cb = colorbar(lc, extend='both')
cb.set_label('Delay / minutes')

# Set plot title and label axes
title('Travel delays in England on {0} at {1}'.format(data_time.strftime('%d-%B-%Y'), data_time.strftime('%H:%M')))

# Comment out if you want to have the x- and y- axes labelled
gca().get_xaxis().set_visible(False)
gca().get_yaxis().set_visible(False)

tight_layout()

output_filename = 'england-traffic-delays-{0}.jpeg'.format(data_time.strftime('%Y%m%d%H%M'))
savefig(output_filename)
print('Written output to ' + output_filename)

# vim:sw=4:sts=4:et
