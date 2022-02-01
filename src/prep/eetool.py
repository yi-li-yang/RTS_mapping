import ee
import numpy as ee


def gen_roi_geometry(long, lat):
    '''
    Generate GEE roi geometry polygon using centroid
    '''
    long1, lat1, long2, lat2 = utils.gen_roi(long, lat)
    geometry = ee.Geometry.Polygon(coords=[[[long1, lat1], [long1, lat2], [long2, lat2], [long2, lat1], ]],
                                   proj='EPSG:4326',
                                   geodesic=None,
                                   maxError=1.,
                                   evenOdd=False)
    return geometry


def band_to_arr(basemap, band: string, roi):
    '''
    basemap:ee.Image
    roi:ee.Geometry

    Convert selected band to np.array (2d)
    '''
    band_roi = basemap.sampleRectangle(region=roi)
    band_arr = band_roi.get(band)
    return np.array(band_arr.getInfo())