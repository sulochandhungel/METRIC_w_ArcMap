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