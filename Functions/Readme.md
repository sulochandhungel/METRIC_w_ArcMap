Functions:

### Common_Functions.py
    get_MtDtFname - Get Metadata filename from directory
    get_MtDt - Extract metadata for a field from MTL file
    scene_center - Get scene center from MTL file
    make_PtSHP_from_LatLong - Create a point shapefile from Latitude and Longitude
   
   
### csv_functions.py
    These functions were built to extract data from csv without using base python functions. This was used for weather data extraction.
    
    extractLatLongfromCSV - Extract SiteID, Longitude, Latitude, Installation Date.
    make_ptSHP_from_CSV - Create an unprojected lat-long shapefile from csvfile.
    
    From a csv file,
        getrow - Extract a row based on row number
        getrow_from_rowName - Extract a row based on row name
        getcol - Extract a column based on column number
        getcol_from_colName - Extract a column based on column name
        getval_rowcol - Extract data based on row and column number
        getval_rowName_colName - Extract data based on row and column name
    

### shapefile.py
    Functions to help working on shapefiles.
    Provides read and write support for ESRI Shapefiles.
    author: jlawhead<at>geospatialpython.com
