"""
--------------------------------------------------------------------------------
Script Name: lst_calculation.py
Author: Dr. Azad Rasul
Year: 2025
Email: azad.rasul@soran.edu.iq
--------------------------------------------------------------------------------
"""

# lst_calculation.py (Python 2.7 compatible)
import arcpy
from arcpy.sa import *
import os

arcpy.CheckOutExtension("Spatial")

def calculate_lst(b10_path, b4_path, b5_path, study_area, 
                 ML, AL, output_path, temp_workspace="in_memory"):
    try:
        # ========== Environment Setup ========== #
        arcpy.env.overwriteOutput = True
        arcpy.env.workspace = temp_workspace
        arcpy.AddMessage("Initializing LST calculation...")

        # ========== Validate Output Path ========== #
        output_dir = os.path.dirname(output_path)
        
        # Check if output directory is valid
        if os.path.exists(output_dir):
            if not os.path.isdir(output_dir):
                arcpy.AddError("ERROR: {} is a FILE, not a directory!".format(output_dir))
                raise ValueError("Invalid output directory path")
        else:
            arcpy.AddMessage("Creating output directory: {}".format(output_dir))
            os.makedirs(output_dir)

        # ========== Input Validation ========== #
        for band in [b10_path, b4_path, b5_path]:
            if not arcpy.Exists(band):
                msg = "Input band {} not found".format(os.path.basename(band))
                raise ValueError(msg)

        # ========== Data Preparation ========== #
        arcpy.AddMessage("Clipping input bands...")
        clipped_b10 = ExtractByMask(b10_path, study_area)
        clipped_b4 = ExtractByMask(b4_path, study_area)
        clipped_b5 = ExtractByMask(b5_path, study_area)

        # ========== Thermal Processing ========== #
        arcpy.AddMessage("Calculating TOA Radiance...")
        TOA = ML * clipped_b10 + AL  # Top of Atmosphere Radiance
        arcpy.AddMessage("TOA max: {}".format(arcpy.GetRasterProperties_management(TOA, "MAXIMUM").getOutput(0)))
        arcpy.AddMessage("TOA min: {}".format(arcpy.GetRasterProperties_management(TOA, "MINIMUM").getOutput(0)))

        arcpy.AddMessage("Calculating Brightness Temperature...")
        K1 = 774.89  # Landsat 8 Band 10 constants
        K2 = 1321.08
        BT = (K2 / arcpy.sa.Ln(K1 / TOA + 1)) - 273.15
        arcpy.AddMessage("BT max: {}".format(arcpy.GetRasterProperties_management(BT, "MAXIMUM").getOutput(0)))
        arcpy.AddMessage("BT min: {}".format(arcpy.GetRasterProperties_management(BT, "MINIMUM").getOutput(0)))
       
        # ========== Vegetation Analysis ========== #
        arcpy.AddMessage("Calculating NDVI...")
        ndvi = (Float(clipped_b5) - Float(clipped_b4)) / (Float(clipped_b5) + Float(clipped_b4) + 1e-10)

        # Calculate NDVI statistics with fallback values
        ndvi_min = arcpy.GetRasterProperties_management(ndvi, "MINIMUM").getOutput(0)
        ndvi_max = arcpy.GetRasterProperties_management(ndvi, "MAXIMUM").getOutput(0)
        ndvi_min = float(ndvi_min) if ndvi_min else -0.1
        ndvi_max = float(ndvi_max) if ndvi_max else 0.5
        arcpy.AddMessage("NDVI max: {}".format(ndvi_max))
        arcpy.AddMessage("NDVI min: {}".format(ndvi_min))


        # ========== Emissivity Calculation ========== #
        arcpy.AddMessage("Calculating Proportion of Vegetation...")
        pv = Square((ndvi - ndvi_min) / (ndvi_max - ndvi_min + 1e-10))
        
        arcpy.AddMessage("Calculating Land Surface Emissivity...")
        e = 0.004 * pv + 0.986
        e_clamped = Con(e < 0.95, 0.95, Con(e > 1.0, 1.0, e))
        arcpy.AddMessage("Emissivity max: {}".format(arcpy.GetRasterProperties_management(e_clamped, "MAXIMUM").getOutput(0)))
        arcpy.AddMessage("Emissivity min: {}".format(arcpy.GetRasterProperties_management(e_clamped, "MINIMUM").getOutput(0)))


        # ========== LST Calculation ========== #
        arcpy.AddMessage("Computing Land Surface Temperature...")
        lambda_val = 10.8  # Wavelength in micrometers
        C2 = 14388         # Planck's constant
        lst = BT / (1 + (lambda_val * BT / C2) * Ln(e_clamped))
        arcpy.AddMessage("LST max: {}".format(arcpy.GetRasterProperties_management(lst, "MAXIMUM").getOutput(0)))
        arcpy.AddMessage("LST min: {}".format(arcpy.GetRasterProperties_management(lst, "MINIMUM").getOutput(0)))

        # ========== Save Output ========== #
        lst.save(output_path)
        arcpy.AddMessage("Successfully created LST raster at: {}".format(output_path))

        # Cleanup temporary data
        if temp_workspace == "in_memory":
            arcpy.Delete_management("in_memory")

    except Exception as e:
        arcpy.AddError("Processing failed: {}".format(str(e)))
        raise

# ========== Tool Interface ========== #
if __name__ == "__main__":
    # Get parameters from ArcGIS tool dialog
    params = {
        "b10_path": arcpy.GetParameterAsText(0),
        "b4_path": arcpy.GetParameterAsText(1),
        "b5_path": arcpy.GetParameterAsText(2),
        "study_area": arcpy.GetParameterAsText(3),
        "ML": float(arcpy.GetParameterAsText(4)),
        "AL": float(arcpy.GetParameterAsText(5)),
        "output_path": arcpy.GetParameterAsText(6)
    }

    # Execute the function
    calculate_lst(**params)