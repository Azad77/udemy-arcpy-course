"""
--------------------------------------------------------------------------------
Script Name: raster_analysis_arcpy.py
Author: Dr. Azad Rasul
Year: 2025
Email: azad.rasul@soran.edu.iq
--------------------------------------------------------------------------------
"""
import arcpy

# Set workspace if necessary
arcpy.env.workspace = "D:/Udemy/arcpy/data"

# Define input raster file path
raster_input = "D:/Udemy/arcpy/data/dem_subset.tif"

# Create a raster layer
output_layer = "dem_subset_layer"
arcpy.MakeRasterLayer_management(raster_input, output_layer)
print("Raster layer created successfully")

# Accessing Raster Layer Properties
if arcpy.Exists(raster_input):
    raster = arcpy.Raster(raster_input)
    extent = raster.extent
    print("Raster extent: {}, {}, {}, {}".format(extent.XMin, extent.YMin, extent.XMax, extent.YMax))
    print("Raster dimensions: {}x{}".format(raster.width, raster.height))
    print("Number of bands: {}".format(raster.bandCount))
    crs = raster.spatialReference
    print("Coordinate Reference System: {} (WKID: {})".format(crs.name, crs.factoryCode))
else:
    print("Raster file does not exist.")

# Raster Band Manipulation
if arcpy.Exists(raster_input):
    raster = arcpy.Raster(raster_input)
    print("Great, this is a valid raster layer!")
    print("Band 1 - Min: {}, Max: {}, Mean (approx): {}, Std Dev: {}".format(
        raster.minimum, raster.maximum, raster.meanCellHeight, raster.standardDeviation))
else:
    print("This is an invalid raster layer!")

# Raster Style Manipulation
arcpy.ApplySymbologyFromLayer_management("dem_subset_layer", "DEM_Layer")
print("Raster symbology applied.")

# Querying Raster Values
raster_path = "D:/Udemy/arcpy/data/clipped_Landsat_B4.tif"
point_x = 45.134042
point_y = 36.240410
wgs84_sr = arcpy.SpatialReference(4326)
point = arcpy.Point(point_x, point_y)

if arcpy.Exists(raster_path):
    raster = arcpy.Raster(raster_path)
    raster_extent = raster.extent
    print("Raster Extent: XMin: {}, XMax: {}, YMin: {}, YMax: {}".format(
        raster_extent.XMin, raster_extent.XMax, raster_extent.YMin, raster_extent.YMax))
    raster_sr = raster.spatialReference
    print("Raster Spatial Reference:", raster_sr.name)
    point_geom = arcpy.PointGeometry(point, wgs84_sr).projectAs(raster_sr)
    reprojected_x = point_geom.firstPoint.X
    reprojected_y = point_geom.firstPoint.Y
    print("Reprojected Point:", reprojected_x, reprojected_y)
    if raster_extent.contains(point_geom):
        cell_value = arcpy.GetCellValue_management(raster, "{} {}".format(reprojected_x, reprojected_y))
        print("Raster value at ({}, {}): {}".format(reprojected_x, reprojected_y, cell_value.getOutput(0)))
    else:
        print("The point is outside the raster extent.")
else:
    print("Raster layer is invalid!")

# Reproject Raster
in_raster = "D:/Udemy/arcpy/data/dem_clipped.tif"
out_raster = "D:/Udemy/arcpy/data/Reprojected_Layer_New.tif"
out_coor_system = arcpy.SpatialReference(4326)
in_coor_system = arcpy.SpatialReference(32638)

desc = arcpy.Describe(in_raster)
if not desc.spatialReference.name:
    print("Input raster does not have a defined spatial reference. Defining it now.")
    arcpy.DefineProjection_management(in_raster, in_coor_system)
else:
    print("Input raster spatial reference:", desc.spatialReference.name)

if arcpy.Exists(out_raster):
    arcpy.Delete_management(out_raster)
    print("Deleted existing output raster: " + out_raster)

try:
    arcpy.ProjectRaster_management(
        in_raster, out_raster, out_coor_system, "NEAREST",
        "3.01166281913873E-04 3.01166281913873E-04", in_coor_system
    )
    print("Raster reprojected successfully!")
except arcpy.ExecuteError:
    print("ArcPy error:", arcpy.GetMessages(2))
except Exception as e:
    print("Unexpected error:", str(e))

# Export Raster
arcpy.CopyRaster_management(
    "D:/Udemy/arcpy/data/dem_subset.tif",
    "D:/Udemy/arcpy/data/exported_raster.tif",
    format="TIFF"
)
print("Raster exported successfully.")
