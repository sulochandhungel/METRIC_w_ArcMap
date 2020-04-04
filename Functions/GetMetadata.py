def get_MtDt(MtDt_PathFname, output = "all"):
    '''
    This function extracts metadata value from .MTL file.    
   '''

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
