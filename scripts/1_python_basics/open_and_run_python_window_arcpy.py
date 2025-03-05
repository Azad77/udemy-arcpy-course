"""
--------------------------------------------------------------------------------
Script Name: lst_calculation.py
Author: Dr. Azad Rasul
Year: 2025
Email: azad.rasul@soran.edu.iq
--------------------------------------------------------------------------------
"""

# Print a geodatabase path (quotes and escape characters)  
print('Loading data from "C:\\GIS\\Projects\\Forestry.gdb"')  

# Output:  
# Loading data from "C:\GIS\Projects\Forestry.gdb"  

# Example 2: Calculate Area Conversion (Square Meters to Square Kilometers)
# Convert a forest area from sq. meters to sq. kilometers  
area_sq_meters = 2500000  
area_sq_kilometers = float(area_sq_meters) / 1000000  
print("Forest Area: {} km²".format(area_sq_kilometers))

# Example 3: Combine Workspace and Feature Class Paths
# Define workspace and feature class variables  
workspace = r"C:\GIS\Data"  # raw strings (r"...").
feature_class = "Rivers.shp"  
full_path = workspace + "\\" + feature_class  # Combine paths  

print("Feature Class Location:", full_path)  

# Output:  
# Feature Class Location: C:\GIS\Data\Rivers.shp  

print("Hello from the ArcGIS Python Window!")  

# Example Script (list_layers.py):
import arcpy.mapping  

# Reference a specific MXD file  
import arcpy.mapping

# Reference a specific MXD file
mxd = arcpy.mapping.MapDocument(r"C:/data/arcpy.mxd")

# Print all layer names
for layer in arcpy.mapping.ListLayers(mxd):
    print("Layer:", layer.name)  # Access the 'name' attribute directly, no parentheses

