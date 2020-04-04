Functions:

### Common_Functions.py
    get_MtDtFname - Get Metadata filename from directory
    get_MtDt - Extract metadata for a field from MTL file
    scene_center - Get scene center from MTL file
    make_PtSHP_from_LatLong - Create a point shapefile from Latitude and Longitude
   
   
### csv_functions.py
    These functions were built to extract data from csv only using base python functions. 
    This was used for weather data extraction.
    
    extractLatLongfromCSV - Extract SiteID, Longitude, Latitude, Installation Date.
    make_ptSHP_from_CSV - Create an unprojected lat-long shapefile from csvfile.
    
    From a csv file,
        getrow - Extract a row based on row number
        getrow_from_rowName - Extract a row based on row name
        getcol - Extract a column based on column number
        getcol_from_colName - Extract a column based on column name
        getval_rowcol - Extract data based on row and column number
        getval_rowName_colName - Extract data based on row and column name

### METRIC_datetime_functions.py
    These functions were built to extract and manipulate datetime between image and weather stations.
    Some of these functions require a timezone shapefile ("Timezone.shp") which has information on spatial DLS and timezone data.  
    
    project_shp_to_DEMproj - Project shapefile to DEM projection
    add_TZ_and_DLS_2_shp - Spatially join a point shapefile to the Timezone.shp shapefile
    get_DateTime_from_Landsat_MtDt - Extract datetime from Landsat metadata file
    DayLightSavings - Determine datetime of daylight savings start and end
    getLocDateTime_Image - Get local datetime from landsat image
    closest_datetime - Get the closest datetime to landsat image datetime
    get_LocDT_using_GMT_DLS - Get Local datetime using GMT and DLS
    
    

### shapefile.py
    Functions to help working on shapefiles.
    Provides read and write support for ESRI Shapefiles.
    author: jlawhead<at>geospatialpython.com
