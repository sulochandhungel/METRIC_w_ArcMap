"""
METRIC_datetime_functions.py
Provides support for METRIC datetime functions.
author: sulochandhungel<at>gmail.com
date: 20160527
"""

from Common_Functions import *
from ArcGIS_functions_4_METRIC import *
import datetime
from datetime import datetime
import os
import shapefile

# For Testing:

#MtDtFileName = 'c:\\users\\sulochan\\sulochan\\metric_python_model\\landsat8_wshed_automated\\RequiredFiles\\LC80440282015128LGN00_MTL.txt'
#print get_DateTime_from_Landsat_MtDt(MtDtFileName)
#j=1
#if j==1:


def project_shp_to_DEMproj(shp_FName, DEM_fname, output_FName):
	'''
	Function to project shapefile to DEM projection
	'''
	
    RasterObj = arcpy.Raster (DEM_fname)
    sptref = RasterObj.spatialReference.GCS  
    
    # Process: Project
    arcpy.DefineProjection_management(shp_FName, sptref)
    
    sptref = RasterObj.spatialReference
    arcpy.Project_management(shp_FName, output_FName, sptref)

    return


def add_TZ_and_DLS_2_shp(shp_FName, TZ_DLS_shpfile, output_Fname):
	'''
	Function to spatially join a point shpfile to a shapefile with Time Zone and Daylight savings. 
	'''
	
    arcpy.SpatialJoin_analysis(shp_FName, TZ_DLS_shpfile, output_Fname)


def get_DateTime_from_Landsat_MtDt(MtDtFileName):
	'''
	Extract datetime from Landsat Metadata file
	'''
	
    mydate = str.split(get_MtDt(MtDtFileName, "DATE_ACQUIRED"),"-")
    yr = str(int(mydate[0]))
    mo = str(int(mydate[1]))
    da = str(int(mydate[1][0:2]))
    mydate_ = yr + "-" + mo + "-" + da
    
    mytime = str.split(get_MtDt(MtDtFileName, "SCENE_CENTER_TIME"),":")
    hr_ = ""
    for i in mytime[0]:
        if i.isdigit():
            hr_ = hr_ +str(i)
    n_ = len(hr_)
    n = min(2,n_)
    hr = str(int(hr_[0:n]))
	
    mi_ = ""
    for i in mytime[1]:
        if i.isdigit():
           mi_ = mi_ +str(i)
    n_ = len(mi_)
    n = min(2,n_)
    mi = str(int(mi_[0:n]))
	
    sec_ = ""
    for i in mytime[2]:
        if i.isdigit():
           sec_ = sec_ +str(i)
    n_ = len(sec_)
    n = min(2,n_)
    sec = str(int(sec_[0:n]))
    mytime_ = hr + ":" + mi + ":" + sec
    return(mydate_ +" "+ mytime_)

#print mydate_
#print mytime_


def DayLightSavings(yearN):
	'''
	Determine date and time of DLS start and end.
	'''
	
    from datetime import datetime
    mon = 3
    for i in range(8,16):
        strdate = str(i) + "/" + str(mon) + "/" + str(yearN) + " 02:00:00"
        #print strdate
        myweekday = datetime.strptime(strdate, '%d/%m/%Y %H:%M:%S').strftime('%A')
        #print myweekday
        if myweekday == "Sunday":
            Start_Daylight_Sav = strdate

    mon = 11
    for i in range(1,8):
        strdate = str(i) + "/" + str(mon) + "/" + str(yearN) + " 02:00:00"
        #print strdate
        myweekday = datetime.strptime(strdate, '%d/%m/%Y %H:%M:%S').strftime('%A')
        #print myweekday
        if myweekday == "Sunday":
            End_Daylight_Sav = strdate
    
    startDLS = datetime.strptime(Start_Daylight_Sav,"%d/%m/%Y %H:%M:%S")
    endDLS = datetime.strptime(End_Daylight_Sav,"%d/%m/%Y %H:%M:%S")

    return [startDLS,endDLS]



#GMTtime = datetime(2014, 12, 31, 18, 43, 42)
#longitude = -119.26630999999999
#latitude = 46.015185
#DEM_file = 'C:\\Users\\Sulochan\\Sulochan\\METRIC_Python_Model\\Landsat8_Wshed\\DEMFiles\\DEM.tif'
#TZ_DLS_shpfile = 'C:\\Users\\Sulochan\\Sulochan\\METRIC_Python_Model\\Landsat8_Wshed\\RequiredFiles\\Time_Zone.shp'
#temp_dir = 'C:\\Users\\Sulochan\\Sulochan\\METRIC_Python_Model\\Landsat8_Wshed\\TempFiles'
#j=1
#if j==1:
def getLocDateTime_Image(GMTtime, longitude, latitude, DEM_file, TZ_DLS_shpfile, temp_dir):
	''' 
	Get Local datetime from Landsat image
	'''

    from arcpy import env
    import datetime
    
    if os.path.exists(temp_dir + "\\Scn_Cen.shp"):
        arcpy.Delete_management(temp_dir + "\\Scn_Cen.shp")
        arcpy.Delete_management(temp_dir + "\\Scn_Cen_Proj.shp")
        arcpy.Delete_management(temp_dir + "\\Scn_Cen_TZ_DLS.shp")
    make_ptSHP_from_LatLong(longitude, latitude, temp_dir + "\\Scene_Center", temp_dir + "\\Scn_Cen.shp")
    project_shp_to_DEMproj(temp_dir + "\\Scn_Cen.shp", DEM_file, temp_dir + "\\Scn_Cen_Proj.shp")
    add_TZ_and_DLS_2_shp(temp_dir + "\\Scn_Cen_Proj.shp", TZ_DLS_shpfile, temp_dir + "\\Scn_Cen_TZ_DLS.shp")

    sf = shapefile.Reader(temp_dir + "\\Scn_Cen_TZ_DLS.shp")
    
    ## The following part is added because pyshp or shapefile module (downloaded)
    ## adds a 'deletionflag' field as tuple when creating a shapefile
    ## This 'deletionflag' field is added in the field list but
    ## did not have values in record list
    ## ---- Added because of 'deletionflag' --- START
    if (type(sf.fields[0])==tuple):
        sf_fields_selected = sf.fields[1:len(sf.fields)]
    else:
        sf_fields_selected=sf.fields
    ## --- Added because of 'deletionflag' --- END
    
    for i in range(0,len(sf_fields_selected)):
        sf_field = sf_fields_selected[i][0]
        if (sf_field=="GMTOffset"):
            GMTOffind = i
        if (sf_field=="DayLghtSav"):
            DayLSavInd = i

    for i in range(0,sf.numRecords):
        GMTOffset = float(sf.records()[i][GMTOffind])
        DLS = float(sf.records()[i][DayLSavInd])
        GMT_delta = datetime.timedelta(hours = GMTOffset)
        Loc_Scene_Center = GMTtime + GMT_delta
    
        DLS_Year = Loc_Scene_Center.year
        DLS_Start = DayLightSavings(DLS_Year)[0]
        DLS_End = DayLightSavings(DLS_Year)[1]
    
        DayLightSav = (GMTtime>DLS_Start and
                       GMTtime<DLS_End) ## If true, apply Day light savings
        
        # GMT TO STANDARD Mountain (-7) [ Between DLS_Start and DLS_End ] 
        # GMT TO DAYLIGHT SAVINGS Mountain (-7) + Daylightsavings (1) = (-6)
        # e.g. 00 GMT Mountain Standard = 17:00 earlier day
        # e.g. 00 GMT Mountain Daylight savings = 18:00 earlier day
        
        if DayLightSav == True:
            DLS_delta = datetime.timedelta(hours = DLS)
        else:
            DLS_delta = datetime.timedelta(hours = 0)
    
        Loc_Scene_center_DLS = GMTtime + GMT_delta + DLS_delta
        print "\n ImageDateTime (GMT): " + str(GMTtime)
        print "\n ImageDateTime (Local with Daylight Savings): " + str(Loc_Scene_center_DLS)

    arcpy.Delete_management(temp_dir + "\\Scn_Cen.shp")
    arcpy.Delete_management(temp_dir + "\\Scn_Cen_Proj.shp")
    sf.shp.close()
    sf.shx.close()
    sf.dbf.close()
    arcpy.Delete_management(temp_dir + "\\Scn_Cen_TZ_DLS.shp")

    Loc_DT_str = str(Loc_Scene_center_DLS)

    return Loc_Scene_center_DLS
    #print Loc_Scene_center_DLS
##GMTtime = datetime.strptime("2016-03-31 09:30:08", "%Y-%m-%d %H:%M:%S")
##longitude = -111.876183
##latitude = 40.758701
##getLocDateTime_Image(GMTtime, longitude, latitude)

def getLocDateTime(GMTtime="", longitude=0.0, latitude=0.0, DEM_file = "", TZ_DLS_shpfile = "", temp_dir = ""):
	'''
	Get Local datetime at a specific latitude and longitude
	'''

    if temp_dir == "":
        temp_dir = os.getcwd() + "\\TempFiles"
        f = open(temp_dir + '\\Temp_outputs.txt', 'r')
        line = f.readline()
        while ("Local_Date_Time" in line):
            line = f.readline()
            return str.split(str(line),"\n")[0]
        return "Temp_outputs.txt not found!"
    else:
        return getLocDateTime_Image(GMTtime, longitude, latitude, DEM_file, TZ_DLS_shpfile, temp_dir)

def closest_datetime(ReqDateTime, mi, closeto = "Closest", msg = "hide"):
	'''
	Get the closest datetime (e.g. within 15 min, 30 min, 1 hour) of a given datetime.
	closeto can be - "Closest", "After" or "Before"
	'''

    from datetime import datetime
    from datetime import timedelta

    ### THIS PART IS TO SUPRESS PRINT STATEMENTS IN MIDDLE ##
    ### BASED ON msg = "hide" or "show" ###
    ###
    ### START ###

    import os
    import sys
    old_stdout = sys.stdout

    if msg == "hide":
        f = open(os.devnull, 'w')
        sys.stdout = f

    ###
    ### END ###

    ## WHAT IS THE FUNCTION TRYING TO DO?
    ##
    ## Assume required datetime is "2016-03-01 13:45:45"
    ## Assume we need to find closest 10th minute of hour 
    ## Build a sequence of series of time steps  +(10+1)th and -(10+1)th
    ## minutes from required datetime
    ##
    ## So in this example it would create a time list of
    ## named "datetime_generated"
    ## 2016-03-01 13:34:45
    ## 2016-03-01 13:35:45
    ## ....
    ## ....
    ## 2016-03-01 13:54:45
    ## 2016-03-01 13:55:45
    ##

    DT = datetime.strptime(ReqDateTime, "%Y-%m-%d %H:%M:%S")
    print "Date Time of Image: " + str(DT)

    b = timedelta(seconds = 60 * (mi+1))

    DT_plus = DT + b
    DT_minus = DT - b

    if DT_plus > datetime.now() and closeto == "After":
        print " Cannot find data values for future with \n closeto = '"'After'"'"
        print " Forcing \n closeto = '"'Before'"'"
        closeto = "Before"

    datetime_generated = [DT_minus + timedelta(minutes=x)\
                      for x in range(0, ((DT_plus-DT_minus).seconds)/60)]

    ##
    ## The closest time required to acquire data would be 13:50:00
    ## Assuming that data is collected every 10 minutes of the hour
    ##
    ## If data is collected every hour, a list of minutes is created as
    ## sel_times = [0, 10, 20, 30, 40, 50, 60]
    ##
    ## So anything between 13:34:45 to 13:55:45 is selected such that it
    ## falls between 13:00:00, 13:10:00, 13:20:00, .... , 13:60:00
    ##

    time_ = []
    sel_times = range(0,61,mi) # for every 15th minute in the hour if mi = 15

    for i in range(0,len(datetime_generated)):
        DT_gen = datetime_generated[i]
        if DT_gen.minute in sel_times:
            time_str = str(DT_gen.year) + "-" +\
                           str(DT_gen.month) + "-" +\
                           str(DT_gen.day) + " " +\
                           str(DT_gen.hour) + ":" +\
                           str(DT_gen.minute) + ":" +\
                           "00"
            DT_time_str = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
            
            if closeto == "Closest":
                time_.append(DT_time_str)
            elif closeto == "Before":
                if DT_time_str <= DT:
                    time_.append(DT_time_str)
            elif closeto == "After":
                if DT_time_str > DT:
                    time_.append(DT_time_str)


    ## There will be two selections in "time_"
    ## 13:40:00 and 13:50:00
    ##
    ## Now the one value in "time_" where difference with required datetime is minimum is
    ## chosen as the output date_time.
    ##
                    
    minute_diff = []
    for i in range(0, len(time_)):
        if DT > time_[i]:
            minute_diff.append((DT - time_[i]).seconds)
        else:
            minute_diff.append((time_[i]-DT).seconds)
        if min(minute_diff) == minute_diff[i]:
            output_time = time_[i]
            
    
    print "Closest " + str(mi) + "th minute of hour is: "  + str(output_time)

    sys.stdout = old_stdout # FOR REMOVING SUPPRESSED PRINT STATEMENTS
    return output_time

##j=1
#import datetime
##GMTtime = datetime.datetime(2015, 7, 18, 18, 49, 26)
##GMToff = -8
##DLS = 1
##if j == 1:
def get_LocDT_using_GMT_DLS(GMTtime, GMToff, DLS = 1):
	'''
	Get Local Datetime using GMT and DLS.
	'''

    import datetime
    GMT_delta = datetime.timedelta(hours = GMToff)
    Loc_DT_without_DLS = GMTtime + GMT_delta

    DLS_Year = Loc_DT_without_DLS.year
    DLS_Start = DayLightSavings(DLS_Year)[0]
    DLS_End = DayLightSavings(DLS_Year)[1]

    DayLightSav = (GMTtime>DLS_Start and
                   GMTtime<DLS_End) ## If true, apply Day light savings

##        # GMT TO STANDARD Mountain (-7) [ Between DLS_Start and DLS_End ] 
##        # GMT TO DAYLIGHT SAVINGS Mountain (-7) + Daylightsavings (1) = (-6)
##        # e.g. 00 GMT Mountain Standard = 17:00 earlier day
##        # e.g. 00 GMT Mountain Daylight savings = 18:00 earlier day

    if DayLightSav == True:
        DLS_delta = datetime.timedelta(hours = DLS)
    else:
        DLS_delta = datetime.timedelta(hours = 0)

    #print "DayLIght"
    #print DLS_delta
    return (GMTtime + GMT_delta + DLS_delta)


##GMTtime = datetime.datetime(2015, 4, 16, 16, 30, 26)
##GMToff = -8
##print get_LocDT_using_GMT_DLS(GMTtime, GMToff, DLS = 1)
