
import re
import pandas as pd
import requests
import bs4 as bs

main_data = pd.read_csv('health_risk_data.csv')
main_data = main_data.drop_duplicates()

def enter_age():
    x = input('enter age')
    x = int(x)
    if 1 <= x <= 99:
        x = str(x)
        pass
    else:
        enter_age()
    return x
    


races =  {'all':'*All*','n':'1002-5','a':'A-PI','b':'2054-5','w':'2106-3','l':'2135-2'}

races2 = {'*All*': 'All','1002-5':'American Indian or Alaska Native','A-PI':'Asian or Pacific Islander',
'2054-5':'Black or African American','2106-3':'White','2135-2':'Hispanic or Latino'}


def race(race, races2):
    x = input('enter latino or hispanic? : [y or n]')
    if x == 'y':
        latino = '2135-2'
        race = '*All*'
        race_df = 'Hispanic or Latino'
        pass
    elif x == 'n':
        x = input('enter race : w for white, b for black, a for asian, n for native american: ')
        if x in races.keys():
            latino = '*All*'
            race = races[x]
            race_df = races2[race]
            pass
    else:
        race(race, races2)
    return latino, race, race_df


def enter_gender():
    x = input('enter gender -- enter m or f :')
    if x == 'm':
        sex = 'M'
        pass
    elif x == 'f':
        sex = 'F'
        pass
    else:
        enter_gender()
    return sex

A = enter_age()
G = enter_gender()
R = race(race, races2)


def createParameterList(parameterList):
    """Helper function to create a parameter list from a dictionary object"""
    
    parameterString = ""
    
    for key in parameterList:
        parameterString += "<parameter>\n"
        parameterString += "<name>" + key + "</name>\n"
        
        if isinstance(parameterList[key], list):
            for value in parameterList[key]:
                parameterString += "<value>" + value + "</value>\n"
        else:
            parameterString += "<value>" + parameterList[key] + "</value>\n"
        
        parameterString += "</parameter>\n"
        
    return parameterString

def get_data(A, G, R):
    b_parameters = {
        "B_1": "D76.V28", #15 Leading Causes of Death
        "B_2": "*None*", 
        "B_3": "*None*",
        "B_4": "*None*", 
        "B_5": "*None*"
    }
    m_parameters = {
        "M_1": "D76.M1",   # Deaths, must be included
        "M_2": "D76.M2",   # Population, must be included
        "M_3": "D76.M3",   # Crude rate, must be included
        #"M_31": "D76.M31",        # Standard error (crude rate)
        #"M_32": "D76.M32"         # 95% confidence interval (crude rate)
    }
    
    # values highlighted in a "Finder" control for hierarchical lists, 
    # such as the "Regions/Divisions/States/Counties hierarchical" list.
    
    # For this example, include all years, months, census regions, hhs regions, states. Only include ICD-10 K00-K92
    # for disease of the digestive system
    
    f_parameters = {
        "F_D76.V1": ["*All*"], # year/month
        "F_D76.V10": ["*All*"], # Census Regions - dont change
        "F_D76.V2": ["*All*"], 
            # ICD-10 Codes - Drug overdose deaths are identified using ICD–10 underlying cause-of-death codes: 
            # X40–X44, X60–X64, X85, and Y10–Y14.
        "F_D76.V27": ["*All*"], # HHS Regions - dont change
        "F_D76.V9": ["*All*"] # State County - dont change
    }
    
    # contents of the "Currently selected" information areas next to "Finder" controls in the "Request Form."
    
    # For this example, include all dates, census regions, hhs regions, and states.
    # Only include ICD-10 code K00-K92 for disease of the digestive system
    
    
    i_parameters = {
        "I_D76.V1": "*All* (All Dates)",  # year/month
        "I_D76.V10": "*All* (The United States)", # Census Regions - dont change
        "I_D76.V2": "*All* (The United States)", # ICD-10 Codes
        "I_D76.V27": "*All* (The United States)", # HHS Regions - dont change
        "I_D76.V9": "*All* (The United States)" # State County - dont change
    }
    
    # variable values to limit in the "where" clause of the query, found in multiple select 
    # list boxes and advanced finder text entry boxes in the "Request Form."
    
    # For this example, we want to include ten-year age groups for ages 15-44.
    # For all other categories, include all values
    v_parameters = {
        "V_D76.V1": "",         # Year/Month
        "V_D76.V10": "",        # Census Regions
        "V_D76.V11": "*All*",   # 2006 Urbanization
        "V_D76.V12": "*All*",   # ICD-10 130 Cause List (Infants)
        "V_D76.V17": R[0],   # Hispanic Origin
        "V_D76.V19": "*All*",   # 2013 Urbanization
        "V_D76.V2": "",         # ICD-10 Codes
        "V_D76.V20": "*All*",   # Autopsy
        "V_D76.V21": "*All*",   # Place of Death
        "V_D76.V22": "*All*",   # Injury Intent
        "V_D76.V23": "*All*",   # Injury Mechanism and All Other Leading Causes
        "V_D76.V24": "*All*",   # Weekday
        "V_D76.V25": "*All*",   # Drug/Alcohol Induced Causes
        "V_D76.V27": "",        # HHS Regions
        "V_D76.V4": "*All*",    # ICD-10 113 Cause List
        "V_D76.V5": "*All*", # Ten-Year Age Groups
        "V_D76.V51": "*All*",   # Five-Year Age Groups
        "V_D76.V52": [A, A],   # Single-Year Ages
        "V_D76.V6": "00",       # Infant Age Groups
        "V_D76.V7": G,    # Gender
        "V_D76.V8": R[1],    # Race
        "V_D76.V9": ""          # State/County
    }
    
    
    
    # other parameters, such as radio buttons, checkboxes, and lists that are not data categories
    
    # For this example, include age-adjusted rates, use ten-year age groups (D76.V5), use state location by default, 
    # show rates per 100,000, use 2013 urbanization and use ICD-10 Codes (D76.V2) for cause of death category
    
    o_parameters = {
        "O_V10_fmode": "freg",    # Use regular finder and ignore v parameter value
        "O_V1_fmode": "freg",     # Use regular finder and ignore v parameter value
        "O_V27_fmode": "freg",    # Use regular finder and ignore v parameter value
        "O_V2_fmode": "freg",     # Use regular finder and ignore v parameter value
        "O_V9_fmode": "freg",     # Use regular finder and ignore v parameter value
        "O_aar": "aar_all",       # age-adjusted rates
        "O_aar_pop": "0000",      # population selection for age-adjusted rates
        "O_age": "D76.V52",        # select age-group (e.g. ten-year, five-year, single-year, infant groups)
        "O_javascript": "on",     # Set to on by default
        "O_location": "D76.V9",   # select location variable to use (e.g. state/county, census, hhs regions)
        "O_precision": "1",       # decimal places
        "O_rate_per": "100000",   # rates calculated per X persons
        "O_show_totals": "false",  # Show totals for 
        "O_timeout": "300",
        "O_title": "Digestive Disease Deaths, by Age Group",    # title for data run
        "O_ucd": "D76.V2",        # select underlying cause of death category
        "O_urban": "D76.V19"      # select urbanization category
    }
    
    
    # values for non-standard age adjusted rates (see mortality online databases).
    
    # For this example, these parameters are ignored as standard age adjusted rates are used
    
    vm_parameters = {
        "VM_D76.M6_D76.V10": "*All*",        # Location
        "VM_D76.M6_D76.V17": "*All*",   # Hispanic-Origin
        "VM_D76.M6_D76.V1_S": "*All*",  # Year
        "VM_D76.M6_D76.V7": "*All*",    # Gender
        "VM_D76.M6_D76.V8": "*All*"     # Race
    }
    
    # Miscellaneous hidden inputs/parameters usually passed by web form. These do not change.
    misc_parameters = {
        "action-Send": "Send",
        "finder-stage-D76.V1": "codeset",
        "finder-stage-D76.V1": "codeset",
        "finder-stage-D76.V2": "codeset",
        "finder-stage-D76.V27": "codeset",
        "finder-stage-D76.V9": "codeset",
        "stage": "request"
    }
    

    
    xml_request = "<request-parameters>\n"
    xml_request += createParameterList(b_parameters)
    xml_request += createParameterList(m_parameters)
    xml_request += createParameterList(f_parameters)
    xml_request += createParameterList(i_parameters)
    xml_request += createParameterList(o_parameters)
    xml_request += createParameterList(vm_parameters)
    xml_request += createParameterList(v_parameters)
    xml_request += createParameterList(misc_parameters)
    xml_request += "</request-parameters>"
    
      
    url = "https://wonder.cdc.gov/controller/datarequest/D76"
    response = requests.post(url, data={"request_xml": xml_request, "accept_datause_restrictions": "true"})
    print(response.status_code)
    if response.status_code == 200:
        data2 = response.text
    else:
        print("something went wrong")
    return data2


xml_data = get_data(A, G, R)


def xml2df(xml_data):
    """ This function grabs the root of the XML document and iterates over
        the 'r' (row) and 'c' (column) tags of the data-table
        Rows with a 'v' attribute contain a numerical value
        Rows with a 'l attribute contain a text label and may contain an
        additional 'r' (rowspan) tag which identifies how many rows the value
        should be added. If present, that label will be added to the following
        rows of the data table.
    
        Function returns a two-dimensional array or data frame that may be 
        used by the pandas library."""
    
    root = bs.BeautifulSoup(xml_data,"lxml")
    all_records = []
    row_number = 0
    rows = root.find_all("r")
    
    for row in rows:
        if row_number >= len(all_records):
            all_records.append([])
              
        for cell in row.find_all("c"):
            if 'v' in cell.attrs:
                try:
                    all_records[row_number].append(float(cell.attrs["v"].replace(',','')))
                except ValueError:
                    all_records[row_number].append(cell.attrs["v"])
            else:
                if 'r' not in cell.attrs:
                    all_records[row_number].append(cell.attrs["l"])
                else:
                
                    for row_index in range(int(cell.attrs["r"])):
                        if (row_number + row_index) >= len(all_records):
                            all_records.append([])
                            all_records[row_number + row_index].append(cell.attrs["l"])
                        else:
                            all_records[row_number + row_index].append(cell.attrs["l"])
                                           
        row_number += 1
    return all_records
 

data_frame = xml2df(xml_data)

df = pd.DataFrame(data=data_frame, columns=["Cause of Death","Deaths", "Population", "Crude Rate"])
    

df['Cause of Death'] = df['Cause of Death'].apply(lambda x: re.sub(r"\(.*\)", "", x))
df['Cause of Death'] = df['Cause of Death'].apply(lambda x: re.sub('#','',x))
df['Gender'] = G
df['Age'] = A
df['Race'] = R[2]



concat_data = pd.concat([main_data,df])
concat_data.to_csv('health_risk_data.csv', index= None)



