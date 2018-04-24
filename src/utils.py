def dataCleaning():
    
    '''
    This is the data cleaning function for the CE264 final project: Marriage Analysis
    Return a pandas data frame and a numpy array:
    The first one is the data (X), the second one is the observation (y) 
    The name of each column refers to the JGSS data codebook
    For some combined categories in a particular data feature, please refer to the source code
    '''
    
    # import libraries and raw data
    import numpy as np
    import pandas as pd
    rawData = pd.read_stata('34623-0001-Data.dta')
    
    # data selected primarily by genetic algorithm
    selectedCol = ['SIZE', 'SEXA', 'TP5UNEMP', 'AGESTPWK', 'SZSJBHWK', 'TPJOBP', 'TPJBDP', 'SZCMTHR', 'XXJOB',
                   'XJOBDWK', 'SZTTLSTA', 'ST5JOB', 'SSJB1WK', 'SSTPUNEM', 'SSSJBHWK', 'SSTPJOB','SSTPJBDP', 
                   'SSTPJBSE', 'SSXJBSCH', 'SSSZWKYR', 'SSSZSTFA', 'SPAGEX', 'SPLVTG', 'PPLVTG', 'MMLVTG', 'PPAGE', 
                   'MMAGE', 'MMJOB', 'CCNUMTTL', 'CC01SEX', 'CC01AGE', 'CC02LVTG', 'CC02AGE', 'CC02MG', 'CC03MG', 
                   'CC03JOB', 'CC04LVTG', 'CC04MG', 'CC05SEX', 'CC05JOB', 'CC06SEX', 'CC06AGE', 'CC07SEX', 
                   'CC07LVTG', 'CC07AGE', 'CC07JOB', 'CC08MG', 'CC08JOB', 'SZFFOTHR', 'FFH01REL', 'FFH03SEX', 
                   'FFH04REL', 'FFH04SEX', 'FFH05REL', 'FFH05SEX', 'FFH07REL', 'FFH07SEX', 'FFH07AGE', 'SZFFONLY',
                   'SZFFTTL', 'FFHEAD', 'SZFFOUT', 'FFO01REL', 'FFO01WHY', 'FFO02REL', 'FFO02WHY', 'FFO03REL',
                   'FFO03WHY', 'FFO05REL', 'FFO05WHY', 'FFO06REL', 'FFO06WHY', 'INCSELF', 'INCSP', 'INCPEN',
                   'INCUEB', 'INCIRR', 'INCRENT', 'INCMAIN', 'SZINCOMA', 'XNUMSISE', 'XNUMBROY', 'XSSNBROY', 
                   'XSSNSISY', 'PREF15', 'TP5LOC15', 'PPJBXX15', 'PPJBSZ15', 'MMJBTP15', 'XXLSTSCH','SSLSTSCH', 
                   'PPLSTSCH', 'DOLSTSCH', 'XGRADE', 'XSPSCH']
    selectedData = rawData[selectedCol]
    
    # filter data with more than 1500 'NA' values
    NAfilter = []
    for i in selectedCol:
        if len(selectedData[selectedData[i] == 'Not applicable']) < 1500:
            NAfilter += [i]
    selectedData = selectedData[NAfilter]
    
    # data cleaning...
    selectedData['SIZE'].replace('Largest cities', 1, inplace=True)
    selectedData['SIZE'].replace('Cities with population of 200000 or more', 2, inplace=True)
    selectedData['SIZE'].replace('Cities with population of less than 200000', 3, inplace=True)
    selectedData['SIZE'].replace('Town/village', 4, inplace=True)
    selectedData['SEXA'].replace('Male', 1, inplace=True)
    selectedData['SEXA'].replace('Female', 2, inplace=True)
    selectedData['SSJB1WK'].replace('He/she worked last week.', 1, inplace=True)
    selectedData['SSJB1WK'].replace('He/she was going to work last week, but did not work.', 2, inplace=True)
    selectedData['SSJB1WK'].replace('He/she did not work.', 3, inplace=True)
    selectedData['SPLVTG'].replace('Living together', 1, inplace=True)
    selectedData['SPLVTG'].replace('Not living together (because of work circumstances)', 2, inplace=True)
    selectedData['SPLVTG'].replace('Not living together (for other reasons)', 3, inplace=True)
    selectedData['PPLVTG'].replace('Living together', 1, inplace=True)
    selectedData['PPLVTG'].replace('Not living together', 2, inplace=True)
    selectedData['PPLVTG'].replace('Deceased', 3, inplace=True)
    selectedData['MMLVTG'].replace('Living together', 1, inplace=True)
    selectedData['MMLVTG'].replace('Not living together', 2, inplace=True)
    selectedData['MMLVTG'].replace('Deceased', 3, inplace=True)
    selectedData['CC01SEX'].replace('Male', 1, inplace=True)
    selectedData['CC01SEX'].replace('Female', 2, inplace=True)
    for i in np.unique(selectedData['FFHEAD']):
        if i not in ['Respondent himself/herself', 'Husband', 'Wife']:
            selectedData['FFHEAD'].replace(i, 4, inplace=True)
    selectedData['FFHEAD'].replace('Respondent himself/herself', 1, inplace=True)
    selectedData['FFHEAD'].replace('Husband', 2, inplace=True)
    selectedData['FFHEAD'].replace('Wife', 3, inplace=True)
    selectedData['INCSELF'].replace('Chosen', 0, inplace=True)
    selectedData['INCSELF'].replace('Not chosen', 1, inplace=True)
    selectedData['INCSP'].replace('Chosen', 1, inplace=True)
    selectedData['INCSP'].replace('Not chosen', 1, inplace=True)
    selectedData['INCPEN'].replace('Chosen', 0, inplace=True)
    selectedData['INCPEN'].replace('Not chosen', 1, inplace=True)
    selectedData['INCUEB'].replace('Chosen', 0, inplace=True)
    selectedData['INCUEB'].replace('Not chosen', 1, inplace=True)
    selectedData['INCIRR'].replace('Chosen', 0, inplace=True)
    selectedData['INCIRR'].replace('Not chosen', 1, inplace=True)
    selectedData['INCRENT'].replace('Chosen', 0, inplace=True)
    selectedData['INCRENT'].replace('Not chosen', 1, inplace=True)
    selectedData.drop('INCMAIN', axis=1, inplace=True)
    for i in np.unique(selectedData['SZINCOMA']):
        if i == 'None':
            selectedData['SZINCOMA'].replace(i, 1, inplace=True)
        elif i in ['Less than 700,000 yen', '700,000 yen - 1 million yen']:
            selectedData['SZINCOMA'].replace(i, 2, inplace=True)
        elif i in ['1 million yen - 1.3 million yen',
                   '1.3 million yen - 1.5 million yen',
                   '1.5 million yen - 2.5 million yen']:
            selectedData['SZINCOMA'].replace(i, 3, inplace=True)
        elif i in ['2.5 million yen - 3.5 million yen', 
                   '3.5 million yen - 4.5 million yen',
                   '4.5 million yen - 5.5 million yen',]:
            selectedData['SZINCOMA'].replace(i, 4, inplace=True)
        elif i in ['5.5 million yen - 6.5 million yen',
                   '6.5 million yen - 7.5 million yen',
                   '7.5 million yen - 8.5 million yen',
                   '8.5 million yen - 10 million yen',
                   '10 million yen - 12 million yen',
                   '12 million yen - 14 million yen',
                   '14 million yen - 16 million yen',
                   '16 million yen - 18.5 million yen',
                   '18.5 million yen - 23 million yen',]:
            selectedData['SZINCOMA'].replace(i, 5, inplace=True)
        else:
            selectedData['SZINCOMA'].replace(i, 0, inplace=True)
    selectedData.drop('PREF15', axis=1, inplace=True)
    selectedData['TP5LOC15'].replace('Large city', 1, inplace=True)
    selectedData['TP5LOC15'].replace('Small to medium sized city', 2, inplace=True)
    selectedData['TP5LOC15'].replace('Town', 3, inplace=True)
    selectedData['TP5LOC15'].replace('Village', 4, inplace=True)
    for i in np.unique(selectedData['PPJBXX15']):
        if i == 'managers in companies/organizations':
            selectedData['PPJBXX15'].replace(i, 1, inplace=True)
        elif i == 'Not applicable':
            selectedData['PPJBXX15'].replace(i, 0, inplace=True)
        else:
            selectedData['PPJBXX15'].replace(i, 2, inplace=True)
    selectedData['PPJBSZ15'].replace('1', 1, inplace=True)
    selectedData['PPJBSZ15'].replace('Small company (2-29 employees)', 2, inplace=True)
    selectedData['PPJBSZ15'].replace('Medium-sized company (30-299 employees)', 3, inplace=True)
    selectedData['PPJBSZ15'].replace('Large company (300-999 employees)', 4, inplace=True)
    selectedData['PPJBSZ15'].replace('Major company (1000 or more employees', 5, inplace=True)
    selectedData['PPJBSZ15'].replace('Government agency', 6, inplace=True)
    selectedData['PPJBSZ15'].replace("Don't know", 0, inplace=True)
    for i in np.unique(selectedData['MMJBTP15']):
        if i == 'She was not working.':
            selectedData['MMJBTP15'].replace(i, 1, inplace=True)
        elif i == 'Temporary worker, Daily worker, Part-time temporary worker':
            selectedData['MMJBTP15'].replace(i, 2, inplace=True) 
        elif i in ["Regular employee - don't know about occupation",
                   'Regular employee - managerial position',
                   'Regular employee - non-management',
                   'Regular employee - professional (nurse, teacher, etc.)']:
            selectedData['MMJBTP15'].replace(i, 3, inplace=True)
        elif i in ["Don't know", 'No answer']:
            selectedData['MMJBTP15'].replace(i, 0, inplace=True)
        else:
            selectedData['MMJBTP15'].replace(i, 4, inplace=True)
    for i in np.unique(selectedData['XXLSTSCH']):
        if i in ['Ordinary elementary school in the old system',
                 'Higher elementary school in the old system']:
            selectedData['XXLSTSCH'].replace(i, 1, inplace=True)
        elif i in ["Junior high school/Girls' high school in the old system",
                 'Vocational school/Commerce school in the old system',
                 'Normal school in the old system',
                 'Higher school or vocational school in the old system',
                 'Junior high school',
                 'High school']:
            selectedData['XXLSTSCH'].replace(i, 2, inplace=True)
        elif i in ['No answer', "Don't know"]:
            selectedData['XXLSTSCH'].replace(i, 0, inplace=True)
        else:
            selectedData['XXLSTSCH'].replace(i, 3, inplace=True)
    for i in np.unique(selectedData['SSLSTSCH']):
        if i in ['Ordinary elementary school in the old system',
                 'Higher elementary school in the old system']:
            selectedData['SSLSTSCH'].replace(i, 1, inplace=True)
        elif i in ["Junior high school/Girls' high school in the old system",
                 'Vocational school/Commerce school in the old system',
                 'Normal school in the old system',
                 'Higher school or vocational school in the old system',
                 'Junior high school',
                 'High school']:
            selectedData['SSLSTSCH'].replace(i, 2, inplace=True)
        elif i in ['No answer', "Don't know", 'Never-married/Divorced']:
            selectedData['SSLSTSCH'].replace(i, 0, inplace=True)
        else:
            selectedData['SSLSTSCH'].replace(i, 3, inplace=True)
    for i in np.unique(selectedData['PPLSTSCH']):
        if i in ['Ordinary elementary school in the old system',
                 'Higher elementary school in the old system']:
            selectedData['PPLSTSCH'].replace(i, 1, inplace=True)
        elif i in ["Junior high school/Girls' high school in the old system",
                 'Vocational school/Commerce school in the old system',
                 'Normal school in the old system',
                 'Higher school or vocational school in the old system',
                 'Junior high school',
                 'High school']:
            selectedData['PPLSTSCH'].replace(i, 2, inplace=True)
        elif i in ['No answer', "Don't know"]:
            selectedData['PPLSTSCH'].replace(i, 0, inplace=True)
        else:
            selectedData['PPLSTSCH'].replace(i, 3, inplace=True)
    selectedData['DOLSTSCH'].replace('Graduated', 1, inplace=True)
    selectedData['DOLSTSCH'].replace('Quit', 2, inplace=True)
    selectedData['DOLSTSCH'].replace('Still a student', 3, inplace=True)
    selectedData['XSPSCH'].replace('Yes', 1, inplace=True)
    selectedData['XSPSCH'].replace('No', 2, inplace=True)
    selectedData.replace('No answer', 0, inplace=True)
    selectedData.replace('Not applicable', 0, inplace=True)
    cleanedData = selectedData.copy()

    # observation cleaning
    observation = np.array(rawData['MARC'])
    cleanedObservation = np.zeros(len(observation))
    for i in range(len(observation)):
        if observation[i] == 'Currently married':
            cleanedObservation[i] = 1
        else:
            cleanedObservation[i] = 2
    cleanedObservation = cleanedObservation.astype(int)
            
    return cleanedData, cleanedObservation