# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 15:25:18 2019

@author: Matthew Wolf
"""

# Data structure and methods for ANDE methodology

def validDates(dataFrame):
    
    for i in dataFrame.index:
        
        sp_boolean = pd.isnull(dataFrame['start-planned'][i])
        sa_boolean = pd.isnull(dataFrame['start-actual'][i])
        ep_boolean = pd.isnull(dataFrame['end-planned'][i])
        ea_boolean = pd.isnull(dataFrame['end-actual'][i])
        
        blank_dates = sp-boolean + sa-boolen + ep-boolean + ea-boolean
    
    # count the number of dates for the row - if there is only one, we don't have sufficient data to filter by date
    if blank_dates < 2:
        
        dataFrame.at[i, 'valid-dates'] = False
    
    # if we don't have a proper start date, we don't have sufficient data to filter by date
    elif dataFrame.at[i, 'start-planned'] + dataFrame.at[i, 'start-actual'] == 0:
    
        dataFrame.at[i, 'valid-dates'] = False
    
    # if we don't have a proper end date, we don't have sufficient data to filter by date
    elif dataFrame.at[i, 'end-planned'] + dataFrame.at[i, 'end-actual'] == 0:
        
        dataFrame.at[i, 'valid-dates'] = False
        
    else:
        dataFrame.at[i, 'valid-dates'] = True
        
def proporYearDone(datetime):
    months = datetime.month
    days = datetime.day
    return ((months * 30) + days ) / 365

def proporYearToGo(datetime):
    months = datetime.month
    days = datetime.day
    return (365 - ((months * 30) + days )) / 365
        
        
def activityInYear(dateFrame, year):
    
    for i in dataFrame.index:
        
        # if the actual start and end dates are valid, use those
        if not pd.isnull(dataFrame.at[i,'end-actual']) and not pd.isnull(dataFrame.at[i,'start-actual']):
            
            # if end is after the target year AND start is before the target year, the activity was active the whole year
            if dataFrame.at[i, 'end-actual'].year > year and dataFrame.at[i, 'start-actual'].year < year:
                dataFrame.at[i, 'date-in-year'] = 1
            
            # otherwise, if either the start date and end date were both in the target year, the total-commitment (and annual-commitment) should be kept
            elif dataFrame.at[i, 'end-actual'].year == year and dataFrame.at[i, 'start-actual'].year == year:
                dataFrame.at[i, 'date-in-year'] = 1
            
            # If the end date is in the target year, we want to know what proportion of the year has passed before the activity ended
            elif dataFrame.at[i, 'end-actual'].year == year:
                dataFrame.at[i, 'date-in-year'] = proporYearGone(dataFrame, dataFrame.at[i, 'end-actual'])
                
            # If the start date is in the target year, we want to know what proportion of the year remains over which the activity will be active 
            elif dataFrame.at[i, 'start-actual'].year == year:
                dataFrame.at[i, 'date-in-year'] = proporYearToGo(dataFrame, dataFrame.at[i, 'start-actual'])
            
            # Otherwise, the activity was not active during the target year
            else:
                dataFrame.at[i, 'date-in-year'] = 0
        
        # if the actual start and planned end dates are valid, use those
        elif not pd.isnull(dataFrame.at[i,'end-planned']) and not pd.isnull(dataFrame.at[i,'start-actual']):
            
            # if end is after the target year AND start is before the target year, the activity was active the whole year
            if dataFrame.at[i, 'end-planned'].year > year and dataFrame.at[i, 'start-actual'].year < year:
                dataFrame.at[i, 'date-in-year'] = 1
            
            # otherwise, if either the start date and end date were both in the target year, the total-commitment (and annual-commitment) should be kept
            elif dataFrame.at[i, 'end-planned'].year == year and dataFrame.at[i, 'start-actual'].year == year:
                dataFrame.at[i, 'date-in-year'] = 1
            
            # If the end date is in the target year, we want to know what proportion of the year has passed before the activity ended
            elif dataFrame.at[i, 'end-planned'].year == year:
                dataFrame.at[i, 'date-in-year'] = proporYearGone(dataFrame, dataFrame.at[i, 'end-planned'])
                
            # If the start date is in the target year, we want to know what proportion of the year remains over which the activity will be active 
            elif dataFrame.at[i, 'start-actual'].year == year:
                dataFrame.at[i, 'date-in-year'] = proporYearToGo(dataFrame, dataFrame.at[i, 'start-actual'])
            
            # Otherwise, the activity was not active during the target year
            else:
                dataFrame.at[i, 'date-in-year'] = 0
                
        # if the actual start and planned end dates are valid, use those
        elif not pd.isnull(dataFrame.at[i,'end-planned']) and not pd.isnull(dataFrame.at[i,'start-planned']):
            
            # if end is after the target year AND start is before the target year, the activity was active the whole year
            if dataFrame.at[i, 'end-planned'].year > year and dataFrame.at[i, 'start-planned'].year < year:
                dataFrame.at[i, 'date-in-year'] = 1
            
            # otherwise, if either the start date and end date were both in the target year, the total-commitment (and annual-commitment) should be kept
            elif dataFrame.at[i, 'end-planned'].year == year and dataFrame.at[i, 'start-planned'].year == year:
                dataFrame.at[i, 'date-in-year'] = 1
            
            # If the end date is in the target year, we want to know what proportion of the year has passed before the activity ended
            elif dataFrame.at[i, 'end-planned'].year == year:
                dataFrame.at[i, 'date-in-year'] = proporYearGone(dataFrame, dataFrame.at[i, 'end-planned'])
                
            # If the start date is in the target year, we want to know what proportion of the year remains over which the activity will be active 
            elif dataFrame.at[i, 'start-planned'].year == year:
                dataFrame.at[i, 'date-in-year'] = proporYearToGo(dataFrame, dataFrame.at[i, 'start-planned'])
            
            # Otherwise, the activity was not active during the target year
            else:
                dataFrame.at[i, 'date-in-year'] = 0


        