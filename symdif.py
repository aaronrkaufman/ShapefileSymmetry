# Name: ObserverPoints_Ex_02.py
# Description: Identifies exactly which observer points are visible 
#              from each raster surface location.
# Requirements: Spatial Analyst Extension

# Import system modules
import arcpy
from arcpy import env
import arcgisscripting
import sys, os
import numpy
import time

#from arcpy.sa import *

# Set environment settings
#path = sys.argv[1] + os.sep
path = "D:\\Dropbox\\Compactness Shared\\Data\\State Leg Shapefiles" + os.sep
env.workspace = path

#create geoprocessor
gp = arcgisscripting.create()
gp.overwriteoutput = 1

# Set local variables
#inRaster = path + sys.argv[3]
orig = r"D:\\Dropbox\\Compactness Shared\\Data\\State Leg Shapefiles\\both_orig.shp"
newx = r"D:\\Dropbox\\Compactness Shared\\Data\\State Leg Shapefiles\\both_flipped_x.shp"
newy = r"D:\\Dropbox\\Compactness Shared\\Data\\State Leg Shapefiles\\both_flipped_y.shp"

dif_x = r"D:\\Dropbox\\Compactness Shared\\Data\\State Leg Shapefiles\\temp\\temp_x.shp"
dif_y = r"D:\\Dropbox\\Compactness Shared\\Data\\State Leg Shapefiles\\temp\\temp_y.shp"
dif_x2 = r"D:\\Dropbox\\Compactness Shared\\Data\\State Leg Shapefiles\\temp\\temp_x2.shp"
dif_y2 = r"D:\\Dropbox\\Compactness Shared\\Data\\State Leg Shapefiles\\temp\\temp_y2.shp"
t_orig = r"D:\\Dropbox\\Compactness Shared\\Data\\State Leg Shapefiles\\temp\\temp_orig.shp"

outfile = r"D:\\Dropbox\\Compactness Shared\\Data\\State Leg Shapefiles\\symmetry.txt"


x_score = []
y_score = []

#myCursor = gp.SearchCursor(orig)
#row = myCursor.Next()
#csidDict = {}
#rowcount = 1
#while row:
#    ID = row.GetValue("SP_ID")
#    csidDict[rowcount]= ID
#
#    rowcount = rowcount +1
#    row = myCursor.Next()

#iter = range(1, len(csidDict.keys()))
#iter = range(1, 6800)
iter = range(6180, 6800)

for i in iter:
	try:
		arcpy.Select_analysis(newx, dif_x, ''' "SP_ID" = ''' + "'" + str(i) + "'")
		arcpy.Select_analysis(newy, dif_y,''' "SP_ID" = ''' + "'" + str(i) + "'")
		arcpy.Select_analysis(orig, t_orig, ''' "SP_ID" = ''' + "'" + str(i) + "'")

		# Here I do the symmetric difference
		arcpy.SymDiff_analysis(dif_x, t_orig, dif_x2, "ALL", 0.001)
		arcpy.SymDiff_analysis(dif_y, t_orig, dif_y2, "ALL", 0.001)

		# Calculate the area of the symmetric difference shape
		arcpy.AddField_management(dif_x2,"area2","DOUBLE","30","30","30","#","NULLABLE","NON_REQUIRED","#")
		arcpy.CalculateField_management(dif_x2,"area2","!shape.area@squarekilometers!","PYTHON_9.3","#")
		arcpy.AddField_management(dif_y2,"area2","DOUBLE","30","30","30","#","NULLABLE","NON_REQUIRED","#")
		arcpy.CalculateField_management(dif_y2,"area2","!shape.area@squarekilometers!","PYTHON_9.3","#")

		myCursor = gp.SearchCursor(t_orig)
		row = myCursor.Next()
		area_orig = row.GetValue("area")

		myCursor = gp.SearchCursor(dif_x2)
		row = myCursor.Next()
		x_ratio = row.GetValue("area2") / area_orig

		myCursor = gp.SearchCursor(dif_y2)
		row = myCursor.Next()
		y_ratio = row.GetValue("area2") / area_orig

		x_score.append(x_ratio)
		y_score.append(y_ratio)

		print(str(x_ratio), str(y_ratio), str(i))

	except AttributeError:
		x_score.append("NA")
		y_score.append("NA")
		print("NA", "NA", str(i))
	except:
		time.sleep(5)
		arcpy.Select_analysis(newx, dif_x, ''' "SP_ID" = ''' + "'" + str(i) + "'")
		arcpy.Select_analysis(newy, dif_y,''' "SP_ID" = ''' + "'" + str(i) + "'")
		arcpy.Select_analysis(orig, t_orig, ''' "SP_ID" = ''' + "'" + str(i) + "'")

		# Here I do the symmetric difference
		arcpy.SymDiff_analysis(dif_x, t_orig, dif_x2, "ALL", 0.001)
		arcpy.SymDiff_analysis(dif_y, t_orig, dif_y2, "ALL", 0.001)

		# Calculate the area of the symmetric difference shape
		arcpy.AddField_management(dif_x2,"area2","DOUBLE","30","30","30","#","NULLABLE","NON_REQUIRED","#")
		arcpy.CalculateField_management(dif_x2,"area2","!shape.area@squarekilometers!","PYTHON_9.3","#")
		arcpy.AddField_management(dif_y2,"area2","DOUBLE","30","30","30","#","NULLABLE","NON_REQUIRED","#")
		arcpy.CalculateField_management(dif_y2,"area2","!shape.area@squarekilometers!","PYTHON_9.3","#")

		myCursor = gp.SearchCursor(t_orig)
		row = myCursor.Next()
		area_orig = row.GetValue("area")

		myCursor = gp.SearchCursor(dif_x2)
		row = myCursor.Next()
		x_ratio = row.GetValue("area2") / area_orig

		myCursor = gp.SearchCursor(dif_y2)
		row = myCursor.Next()
		y_ratio = row.GetValue("area2") / area_orig

		x_score.append(x_ratio)
		y_score.append(y_ratio)

		print(str(x_ratio), str(y_ratio), str(i))


del gp
out = numpy.column_stack((x_score, y_score, iter))
numpy.savetxt(outfile, out, delimiter=',', fmt="%s")

    
   
