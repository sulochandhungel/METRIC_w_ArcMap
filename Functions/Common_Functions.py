import os
import arcpy
import shapefile


# FUNCTION 1: To get metadata filename from directory
def get_MtDtFname(MtDt_directory, withpath = "TRUE"):
    working_dir = os.getcwd()
    os.chdir(MtDt_directory)
    filelist = os.listdir(MtDt_directory)
    mtdata_filename = ""
    for fname in filelist:
       if ("_MTL.txt" in fname):
            mtdata_filename = fname
    os.chdir(working_dir)
    if withpath == "TRUE":
        return MtDt_directory + "\\" + mtdata_filename
    else:
        return mtdata_filename

# FUNCTION 2: To extract metadata value from MTL file
def get_MtDt(MtDt_PathFname, output = "all"):
    varbs_from_mtfile = []
    varbs_values_from_mtfile = []
    result = {}

    myfile = open(MtDt_PathFname,"r")
    line = myfile.readline()
    varbs_from_mtfile.append(str.split(line,"=")[0])
    varbs_values_from_mtfile.append(str.split(line,"=")[1])
    while ("=" in line):
        line = myfile.readline()
        if ("=" in line):
            varbs_from_mtfile.append(str.split(line,"=")[0])
            varbs_values_from_mtfile.append(str.split(line,"=")[1])
            result[str.split(line,"=")[0]] = str.split(line,"=")[1]
    if output == "all":
        print "All outputs\n"
        for xx in result.keys():
            print xx + " = " + result[xx]    
        return result
        
    result = {}
    for x in range(0,len(varbs_from_mtfile)):
        if (output in varbs_from_mtfile[x]) or (output in varbs_values_from_mtfile[x]) or output == "All":
            result[varbs_from_mtfile[x]] = varbs_values_from_mtfile[x]
            #print varbs_from_mtfile[x] + " = " + varbs_values_from_mtfile[x]
    if len(result)==1:
        #print result.keys()[0] + " = " + result[result.keys()[0]]
        return result[result.keys()[0]]
    elif len(result)>1:
        for xx in result.keys():
            if output in str.split(xx, " "):
                print xx + " = " + result[xx]
                return result[xx]
    if len(result) == 0:
        print "Variable " + output + " not found!\n"
        print "\nPlease check the variable name again\n"
        return None
    else:
        print "More than one variable value for " + output + " found!\n"
        print "Select the variable from following list\n"
        for xx in result.keys():
            print xx + " = " + result[xx]
        return None
    

# --- Example for the function ---

##MtDt_directory = "C:\\Users\\Sulochan\\Sulochan\\METRIC_Python_Model\\Landsat8\\RequiredFiles"
##output = "EARTH_SUN_DISTANCE"
##ans = display_MtDt(MtDt_directory, output)
##print ans


# FUNCTION 3: Get Scene Center from Metadata file 
def scene_center(MtDtFileName):
    '''
    This function returns the scene center based on metadata file.
    ---------------------------------------------------------------

    Syntax:
    scene_center(MtDtFileName)

        MtDtFileName: name of metadata file

    e.g.
        MtDt_directory = "C:\\Users\\Sulochan\\Sulochan\\METRIC_Python_Model\\Landsat8\\RequiredFiles"
        MtDt_Fname = display_MtDt(MtDt_directory, "FileName")
        print scene_center(MtDt_Fname)

    Output:
        
        [-120.8125575, 46.0146975]
        
    '''
    
    Bottom_Lat = (float(get_MtDt(MtDtFileName, "CORNER_LL_LAT_PRODUCT")) +\
                 float(get_MtDt(MtDtFileName, "CORNER_LR_LAT_PRODUCT")))*0.5

    Top_Lat = (float(get_MtDt(MtDtFileName, "CORNER_UL_LAT_PRODUCT")) +\
                 float(get_MtDt(MtDtFileName, "CORNER_UR_LAT_PRODUCT")))*0.5
    
    Center_Lat = (Bottom_Lat + Top_Lat)*0.5

    Left_Lon = (float(get_MtDt(MtDtFileName, "CORNER_LL_LON_PRODUCT")) +\
                 float(get_MtDt(MtDtFileName, "CORNER_UL_LON_PRODUCT")))*0.5
    
    Right_Lon = (float(get_MtDt(MtDtFileName, "CORNER_LR_LON_PRODUCT")) +\
                 float(get_MtDt(MtDtFileName, "CORNER_UR_LON_PRODUCT")))*0.5
    
    Center_Lon = (Left_Lon + Right_Lon)*0.5

    return [Center_Lon, Center_Lat]



# FUNCTION 4: Make a point shapefile using Latitude, Longitude and ID 
def make_ptSHP_from_LatLong(Longitude, Latitude, PtID, PtShpFName = ""):
    w = shapefile.Writer(shapefile.POINT)
    w.field('PtID', 'C', 40)
    w.field('Longitude')
    w.field('Latitude')

    w.point(Longitude, Latitude)
    w.record(PtID, Longitude, Latitude)

    if PtShpFName == "":
        return w
    else:
        w.save(PtShpFName)
    return
    
    

#MtDt_directory = "C:\\Users\\Sulochan\\Sulochan\\METRIC_Python_Model\\Landsat8\\RequiredFiles"
#MtDt_Fname = get_MtDtFname(MtDt_directory)
#get_MtDt(MtDt_Fname, output = "SUN_ELEVATION")
#Scene_Center = print scene_center(MtDt_Fname)

#tt = make_ptSHP_from_LatLong(Scene_Center[0], Scene_Center[1], "")
