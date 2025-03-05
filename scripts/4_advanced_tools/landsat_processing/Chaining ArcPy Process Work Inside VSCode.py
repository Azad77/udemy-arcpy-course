"""
--------------------------------------------------------------------------------
Script Name: Chaining_ArcPy_Process.py
Author: Dr. Azad Rasul
Year: 2025
Email: azad.rasul@soran.edu.iq
--------------------------------------------------------------------------------
"""

import arcpy
import os
import numpy as np

# Step 1: Define workspace and environment settings
raster_folder = r"D:/Udemy/arcpy/data/LC08_L2SP_168035_20170923_20200903_02_T1"
# raster_folder = os.path.join(data_folder, "LC08_L2SP_168035_20170923_20200903_02_T1")
arcpy.env.workspace = raster_folder
arcpy.env.overwriteOutput = True

# Step 2: Listing Raster Bands
# List all raster bands in the Landsat folder
raster_list = arcpy.ListRasters()

# Filter the list to include only TIFF files
raster_list = [r for r in raster_list if r.lower().endswith('.tif')]

print("Raster Bands", raster_list)


# Step 4: Craete True Color Image
# Define the output path for the true color image
true_color_image = os.path.join(raster_folder, "Landsat_TrueColor2.tif")
# Check if the true color image already exists
if arcpy.Exists(true_color_image):
    arcpy.management.Delete(true_color_image)

# Create the true color image using bands 4 (Red), 3 (Green), and 2 (Blue)
print("Creating true color image...")
arcpy.management.CompositeBands([os.path.join(raster_folder, f) for f in raster_list if 'B4' in f or 'B3' in f or 'B2' in f], true_color_image)
print("True color image created successfully at:", true_color_image)

# Step 4: Calculate NDVI from Landsat 8 Bands

import arcpy
import os

# Check out Spatial Analyst extension
arcpy.CheckOutExtension("Spatial")

# Define workspace
raster_folder = r"D:/Udemy/arcpy/data/LC08_L2SP_168035_20170923_20200903_02_T1"
arcpy.env.workspace = raster_folder
arcpy.env.overwriteOutput = True

# Define Band 5 (NIR) and Band 4 (Red)
band5_path = os.path.join(raster_folder, "LC08_L2SP_168035_20170923_20200903_02_T1_SR_B5.TIF")
band4_path = os.path.join(raster_folder, "LC08_L2SP_168035_20170923_20200903_02_T1_SR_B4.TIF")

# Ensure rasters exist
if not (arcpy.Exists(band5_path) and arcpy.Exists(band4_path)):
    raise FileNotFoundError("One or both Landsat 8 bands (B4, B5) are missing!")

# Load and scale bands properly (Landsat 8 SR scaling parameters)
scale_factor = 0.0000275
offset = -0.2
nir = arcpy.sa.Raster(band5_path) * scale_factor + offset
red = arcpy.sa.Raster(band4_path) * scale_factor + offset

# Calculate NDVI using correct formula
ndvi = (nir - red) / (nir + red)

# Save NDVI raster
ndvi_raster = os.path.join(raster_folder, "NDVI_new.tif")
ndvi.save(ndvi_raster)

print("NDVI raster created successfully at:", ndvi_raster)


# Step 6: Reprojecting the Rasters to a Different Coordinate System
import arcpy
import os

# Define workspace
raster_folder = r"D:/Udemy/arcpy/data/LC08_L2SP_168035_20170923_20200903_02_T1"
arcpy.env.workspace = raster_folder
arcpy.env.overwriteOutput = True

# Define input NDVI raster
ndvi_raster = os.path.join(raster_folder, "NDVI_new.tif")

# Ensure the NDVI raster exists
if not arcpy.Exists(ndvi_raster):
    raise IOError("NDVI raster not found at {}".format(ndvi_raster))

# Define output reprojected raster
reprojected_raster = os.path.join(raster_folder, "NDVI_Reprojected2.tif")

# Correctly define the coordinate system
spatial_ref = arcpy.SpatialReference(32638)  # WGS 1984 UTM Zone 38N

# Reproject NDVI raster
arcpy.management.ProjectRaster(ndvi_raster, reprojected_raster, spatial_ref)

print("NDVI raster reprojected successfully at:", reprojected_raster)

# Step 7: Clipping Raster to a Study Area
# Define clipping boundary
clip_shapefile = r"D:/Udemy/arcpy/data/Ranya_utm38.shp"
clipped_raster = os.path.join(raster_folder, "NDVI_Clipped2.tif")

# Clip the NDVI raster to the study area
arcpy.management.Clip(ndvi_raster, "", clipped_raster, clip_shapefile, "", "ClippingGeometry")
print("NDVI clipped to study area successfully.")

import arcpy
import os
import numpy as np
# Step 8: Classify NDVI Raster using Reclassify Based on Thresholds for Vegetation Density
# Define the reclassification scheme
reclass_scheme = arcpy.sa.RemapRange([
    [-1.0, 0.0, 1],  # Non-vegetated
    [0.0, 0.2, 2],   # Low vegetation
    [0.2, 0.4, 3],   # Moderate vegetation
    [0.4, 0.6, 4],   # High vegetation
    [0.6, 1.0, 5]    # Very high vegetation
])
   
# Reclassify the NDVI raster
reclass_ndvi = arcpy.sa.Reclassify(ndvi_raster, "VALUE", reclass_scheme)

# Save the reclassified NDVI raster
reclass_ndvi_raster = os.path.join(raster_folder, "Reclass_NDVI_new1.tif")
reclass_ndvi.save(reclass_ndvi_raster)

print("Reclassified NDVI raster created successfully at:", reclass_ndvi_raster)


# Step 9: Calculating Zonal Statistics
# Define zone feature class
zone_shapefile = r"D:/Udemy/arcpy/data/Ranya_utm38.shp"

# Define output table
output_table = os.path.join(raster_folder, "NDVI_ZonalStats1.dbf")

# Calculate zonal statistics
# Use the correct field name from the shapefile
zone_field = "FID"  # Replace "FID" with the actual field name if different
arcpy.sa.ZonalStatisticsAsTable(zone_shapefile, zone_field, ndvi_raster, output_table, "DATA", "MEAN")
print("Zonal statistics calculated successfully. Output table created at:", output_table)

