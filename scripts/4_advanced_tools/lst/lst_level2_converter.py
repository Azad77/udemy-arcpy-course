"""
--------------------------------------------------------------------------------
Script Name: lst_level2_converter.py
Author: Dr. Azad Rasul
Year: 2025
Email: azad.rasul@soran.edu.iq
--------------------------------------------------------------------------------
"""

# lst_level2_converter.py (Python 2.7 compatible)
import arcpy
from arcpy.sa import *
import os

arcpy.CheckOutExtension("Spatial")

def convert_level2_lst(b10_path, study_area, scale_factor, offset, output_path):
    try:
        # ========== Environment Setup ========== #
        arcpy.env.overwriteOutput = True
        arcpy.AddMessage("Initializing Level 2 LST conversion...")

        # ========== Input Validation ========== #
        if not arcpy.Exists(b10_path):
            raise ValueError("ST_B10 file not found")

        # ========== Clip Band 10 ========== #
        arcpy.AddMessage("Clipping ST_B10 to study area...")
        clipped_b10 = ExtractByMask(b10_path, study_area)

        # ========== Apply Scaling ========== #
        arcpy.AddMessage("Applying scale and offset...")
        scaled = clipped_b10 * scale_factor + offset

        # ========== Convert to Celsius ========== #
        arcpy.AddMessage("Converting to Celsius...")
        lst_celsius = scaled - 273.15

        # ========== Save Output ========== #
        lst_celsius.save(output_path)
        arcpy.AddMessage("LST saved to: {}".format(output_path))

        arcpy.AddMessage("LST max: {}".format(arcpy.GetRasterProperties_management(lst_celsius, "MAXIMUM").getOutput(0)))
        arcpy.AddMessage("LST min: {}".format(arcpy.GetRasterProperties_management(lst_celsius, "MINIMUM").getOutput(0)))


    except Exception as e:
        arcpy.AddError("Error: {}".format(str(e)))
        raise

# ========== Tool Interface ========== #
if __name__ == "__main__":
    params = {
        "b10_path": arcpy.GetParameterAsText(0),
        "study_area": arcpy.GetParameterAsText(1),
        "scale_factor": float(arcpy.GetParameterAsText(2)),
        "offset": float(arcpy.GetParameterAsText(3)),
        "output_path": arcpy.GetParameterAsText(4)
    }
    convert_level2_lst(**params)