import os

import csv
from datetime import datetime

import arcpy
import shapefile

working_dir = os.getcwd()
reqd_dir = working_dir + "\\RequiredFiles"
csvfile = reqd_dir + "\\WeatherStn.csv"

def extractLatLongfromCSV(csvfile):
    '''
    This function extracts SiteID, Longitude, Latitude, Installation Date.
    The csvfile should have four columns with following header with four columns as:
        HeaderNames => "StationID", "Longitude", "Latitude", "InstDate"

    This function returns a list of [siteID, Latitude, Longitude and Installation Dates]

    --------------------------------------------
    Syntax:
        extractLatLongfromCSV(csvfile)

        csvfile: filename with path of csv

    e.g
        xx = extractLatLongfromCSV(csvfile)
        SiteIDs = xx[0]
        Lats = xx[1]
        Longs = xx[2]
        InstDate = xx[3]

    Output:
        SiteIDS => list of site IDs
        Lats => list of latitudes
        Longs => list of longitudes
        InstDate => list of Installation Dates
    
    '''
    longdata=[]
    latdata=[]
    siteid=[]
    instdate=[]

    with open (csvfile, 'rb') as csvf:
        contents = csv.reader(csvf,delimiter=",")
        for row in contents:
            if (row[0]!="StationID"):
                siteid.append(row[0])
                longdata.append(row[1])
                latdata.append(row[2])
                instdate.append(row[3])
                
    return [siteid, latdata, longdata, instdate]

def make_ptSHP_from_csv(csvfile, ptshpfile, stnIDlist = [], varname = "", varvalues =[]):
    '''
    This function creates an unprojected lat-long shapefile from csvfile.
    The csv file must have following 4 columns with headers as:

        HeaderNames => "StationID", "Longitude", "Latitude", "InstDate"

    ------------------------------------------------------------
    Syntax:
        make_ptSHP_from_csv(csvfile, ptshpfile, stnIDlist = [])

        csvfile: filename with path of csv
        ptshpfile: Shape filename with path of csv
        StnIDlist: <optional> list of station IDs which will be in point shapefile
                    If not specified, it converts all stations in csvfile into point shapefile

    e.g
        CSVfile = "C:\\test\\WeatherStn.csv"
        PTSfile = "C:\\test\\PTS"
        make_ptSHP_from_csv(CSVfile, PTSfile, stnIDlist = ['AGKO', 'MNTI', 'TFGI', 'CHAW'])

    Output:
        This outputs a point shapefile of name "C:\\test\\PTS_Unproj" with 4 points with stationID mentioned in stnIDlist
       
    '''
    
    w = shapefile.Writer(shapefile.POINT)
    w.field('SiteID', 'C', 40)
    w.field('Longitude')
    w.field('Latitude')
    w.field('InstallDate')
    w.field('VarSource')
    if varname != "":
        w.field(varname, 'F', 10,8  )
    ctr = 0
    with open (csvfile, 'rb') as csvf:
        contents = csv.reader(csvf,delimiter=",")
        for row in contents:
            if (row[0]!="StationID"):
                if (len(stnIDlist) != 0) and (row[0] in stnIDlist):
                    temp_index = stnIDlist.index(row[0])
                    w.point(float(row[1]), float(row[2]))
                    if type(varvalues[ctr]) == float:
                        w.record(row[0], float(row[1]), float(row[2]), row[3], row[4], float(varvalues[temp_index]))
                    else:
                        w.record(row[0], float(row[1]), float(row[2]), row[3], row[4], varvalues[ctr])
                    ctr = ctr + 1
                elif (len(stnIDlist) ==0):
                    w.point(float(row[1]), float(row[2]))
                    w.record(row[0], float(row[1]), float(row[2]), row[3], row[4])
    w.save(ptshpfile)

    return w

#ptshpfile = "C:\\Users\\Sulochan\\Desktop\\Junk\\METRIC checks\\del_this2"
#make_ptSHP_from_csv(csvfile, ptshpfile, stnIDlist = ['AGKO', 'MNTI', 'TFGI', 'CHAW'])

#print extractLatLongfromCSV(csvfile)[0]

def getrow(csvfile,rowno = 1):
    with open (csvfile, 'rb') as csvf:
        contents = csv.reader(csvf, delimiter = ",")
        ctr = 1
        for row in contents:
            if rowno == ctr:
                return row
            else:
                ctr = ctr + 1
    return None

def getrow_from_rowName(csvfile, rowname =""):
    with open (csvfile, 'rb') as csvf:
        contents = csv.reader(csvf, delimiter = ",")
        ctr = 1
        for row in contents:
            if row[0] == rowname:
                return row
            else:
                ctr = ctr +1
    return None

def getcol(csvfile, colno =1):
    cols = []
    with open (csvfile, 'rb') as csvf:
        contents = csv.reader(csvf, delimiter = ",")
        for row in contents:
            cols.append(row[colno-1])
    return cols

def getcol_from_colName(csvfile, colname = ""):
    cols = []
    with open (csvfile, 'rb') as csvf:
        contents = csv.reader(csvf, delimiter = ",")
        ctr = 1
        for row in contents:
            if ctr == 1:
                col_ind = row.index(colname)
            else:
                cols.append(row[col_ind])
            ctr = ctr + 1
    return cols


def getval_rowcol(csvfile, rowno = 1, colno=1):
    with open (csvfile, 'rb') as csvf:
        contents = csv.reader(csvf, delimiter = ",")
        ctr = 1
        for row in contents:
            if rowno == ctr:
                return row[colno-1]
            else:
                ctr = ctr + 1
    return None

def getval_rowName_colName(csvfile, rowname = "", colname =""):
    with open (csvfile, 'rb') as csvf:
        contents = csv.reader(csvf, delimiter = ",")
        ctr = 1
        for row in contents:
            if ctr == 1:
                col_ind = row.index(colname)
            else:
                if row[0] == rowname:
                    return row[col_ind]
            ctr = ctr + 1
    return None

#print getrow(csvfile, rowno=1)
#print getcol(csvfile, colno = 1)
#print getval_rowcol(csvfile, rowno = 1, colno = 3)
#print getcol_from_colName(csvfile, colname = "StationID")
#print getval_rowName_colName(csvfile,rowname = "FAFI",colname="Longitude")
