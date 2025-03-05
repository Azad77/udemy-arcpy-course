"""
--------------------------------------------------------------------------------
Script Name: mastering_vector_layer_arcpy.py
Author: Dr. Azad Rasul
Year: 2025
Email: azad.rasul@soran.edu.iq
--------------------------------------------------------------------------------
"""

# 1- Add Layers in Python Console
import arcpy

# Reference the currently open ArcMap document
mxd = arcpy.mapping.MapDocument("CURRENT")

# Get the first data frame (map) in the document
df = arcpy.mapping.ListDataFrames(mxd)[0]

# List of shapefiles in the "data" folder to be added to the map
shapefiles = [
    "D:/Udemy/arcpy/data/country.shp",
    "D:/Udemy/arcpy/data/lakes.shp",
    "D:/Udemy/arcpy/data/one_point.shp",
    "D:/Udemy/arcpy/data/places.shp"
]

# Loop through each shapefile and add it to the map
for shp in shapefiles:
    layer = arcpy.mapping.Layer(shp)  # Convert shapefile to layer
    arcpy.mapping.AddLayer(df, layer, "AUTO_ARRANGE")  # Add the layer to the map automatically

print("Layers added successfully!")

# 2- Remove Layers in Python Console ArcMap
import arcpy

# Reference the currently open ArcMap document
mxd = arcpy.mapping.MapDocument("CURRENT")

# Get the first data frame (map) in the document
df = arcpy.mapping.ListDataFrames(mxd)[0]

# Remove all layers from the data frame
for lyr in arcpy.mapping.ListLayers(mxd, "", df):
    arcpy.mapping.RemoveLayer(df, lyr)

print("All layers removed.")

# 3- Remove Layers from an MXD in Python Script
import arcpy

# Provide the full path to your ArcMap document (.mxd)
mxd_path = r"C:/data/arcpy.mxd"  # Change this to your actual MXD file path

# Load the MXD file
mxd = arcpy.mapping.MapDocument(mxd_path)

# Get the first data frame in the MXD
df = arcpy.mapping.ListDataFrames(mxd)[0]

# Remove all layers
for lyr in arcpy.mapping.ListLayers(mxd, "", df):
    arcpy.mapping.RemoveLayer(df, lyr)

# Save changes to the MXD file
mxd.save()

print("All layers were removed successfully.")

# 4- Add Layers to MXD in VSCode
import arcpy

# Load the MXD file (ensure the file path is correct)
mxd = arcpy.mapping.MapDocument(r"C:/data/arcpy.mxd")

# Get the first data frame in the MXD
df = arcpy.mapping.ListDataFrames(mxd)[0]

# List of shapefiles in the "data" folder
shapefiles = [
    r"D:/Udemy/arcpy/data/country.shp",
    r"D:/Udemy/arcpy/data/lakes.shp",
    r"D:/Udemy/arcpy/data/one_point.shp",
    r"D:/Udemy/arcpy/data/places.shp"
]

# Add each shapefile to the map
for shp in shapefiles:
    layer = arcpy.mapping.Layer(shp)  # Convert shapefile to layer
    arcpy.mapping.AddLayer(df, layer, "AUTO_ARRANGE")  # Add the layer to the map automatically

# Save changes to the MXD file
mxd.save()

print("Layers added successfully!")

# 5- Export to Shapefile
# Reference the currently open ArcMap document
mxd = arcpy.mapping.MapDocument("CURRENT")

# Get the first data frame (map) in the document
df = arcpy.mapping.ListDataFrames(mxd)[0]

# Find the layer to export
cities_lyr = arcpy.mapping.ListLayers(mxd, "cities", df)[0]

# Export the cities layer to a new shapefile
arcpy.FeatureClassToFeatureClass_conversion(cities_lyr, "C:/output", "Cities_Export.shp")

# 6- Set Workspace:
arcpy.env.workspace = "D:/Udemy/arcpy/data"


# 7- List All Shapefiles in the Folder

shapefiles = arcpy.ListFeatureClasses()
print(shapefiles)

# Selecting Features
# 8- Select by Attribute
# Reference the currently open ArcMap document
mxd = arcpy.mapping.MapDocument("CURRENT")

# Get the first data frame (map) in the document
df = arcpy.mapping.ListDataFrames(mxd)[0]

# Find the layer to export
cities = arcpy.mapping.ListLayers(mxd, "cities", df)[0]

arcpy.Select_analysis("cities.shp", "selected_places_new.shp", '"population" > 1000000')

# 9- Select by Location
# Create feature layers for the rivers and states shapefiles
arcpy.MakeFeatureLayer_management("rivers.shp", "rivers_layer")
arcpy.MakeFeatureLayer_management("states.shp", "states_layer")

# Select rivers that intersect with states
arcpy.SelectLayerByLocation_management("rivers_layer", "INTERSECT", "states_layer")

# Copy the selected features to a new shapefile
arcpy.CopyFeatures_management("rivers_layer", "intersecting_rivers_new.shp")

# 10- Add Field and Update Attributes
# Add a new text field to the 'country' shapefile
arcpy.AddField_management(r"D:\Udemy\arcpy\data\country.shp", "new_field", "TEXT", field_length=50)

# Update the new field with formatted population data
import arcpy

shp_path = r"D:\Udemy\arcpy\data\country.shp"
fields = [f.name for f in arcpy.ListFields(shp_path)]

# Check if required fields exist
if "new_field" in fields and "POP_CNTRY" in fields:
    with arcpy.da.UpdateCursor(shp_path, ["POP_CNTRY", "new_field"]) as cursor:
        for row in cursor:
            if row[0] is not None:
                population_in_millions = row[0] / 1000000  # Convert to millions
                formatted_population = "{:.0f} million".format(population_in_millions)
                row[1] = "Population: {}".format(formatted_population)
                cursor.updateRow(row)
    print("Values updated successfully based on POP_CNTRY.")
else:
    print("Error: 'POP_CNTRY' or 'new_field' does not exist.")

# 11- Spatial Analysis: Union
import arcpy

# Paths to the shapefiles
shp_path_country = r"D:\Udemy\arcpy\data\country.shp"
shp_path_lakes = r"D:\Udemy\arcpy\data\lakes.shp"
output_shp = r"D:\Udemy\arcpy\data\union_countries_lakes_new.shp"

# Check if input shapefiles exist
if arcpy.Exists(shp_path_country) and arcpy.Exists(shp_path_lakes):
    try:
        print("Unioning {} and {} into {}...".format(shp_path_country, shp_path_lakes, output_shp))
        arcpy.Union_analysis([shp_path_country, shp_path_lakes], output_shp)
        print("Union completed successfully.")
    except Exception as e:
        print("Error occurred during Union: {}".format(e))
else:
    print("Error: One or more input shapefiles do not exist.")

# 12- Clip Operation
import arcpy
import datetime

# Define paths for the input and output shapefiles
country_shp = r"D:/Udemy/arcpy/data/country.shp"
clip_area_shp = r"D:/Udemy/arcpy/data/Ranya_utm38.shp"

# Generate a unique filename with the current timestamp
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
output_shp = r"D:/Udemy/arcpy/data/clipped_country_{}.shp".format(timestamp)

# Perform the Clip operation
arcpy.Clip_analysis(country_shp, clip_area_shp, output_shp)
print(f"Clip analysis completed successfully. Output saved to {output_shp}")


# 13- Spatial Join
arcpy.SpatialJoin_analysis("D:/Udemy/arcpy/data/states.shp", 
                           "D:/Udemy/arcpy/data/lakes.shp", 
                           "D:/Udemy/arcpy/data/joined_states_lakes_new.shp", 
                           "JOIN_ONE_TO_MANY") ________________________________________
# 14- Debugging and Error Handling
try:
    arcpy.CreateFeatureclass_management("D:/Udemy/arcpy/data", "new_shapefile.shp", "POINT")
    print("Feature class created successfully.")
except arcpy.ExecuteError:
    print("An error occurred while creating the feature class:", arcpy.GetMessages())
except Exception as e:
    print("A non-ArcPy error occurred:", str(e))


