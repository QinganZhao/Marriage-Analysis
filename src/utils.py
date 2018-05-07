def dataCleaning(marriageNum='Full', classNum=2, dropColumns=True):
    
    '''
    This is the data cleaning function for the CE264 final project: Marriage Analysis
    Return a pandas data frame and a numpy array: data (X) and observation (y)
    The name of each column refers to the JGSS data codebook
    For some combined categories in a particular data feature, please refer to the source code
    
    Parameters:
    marriageNum: integer or 'Full'(as default); the number of sampled 'Marriage' class, 
                 should be smaller than its actual number
    classNum: 2(as default), 3 or 'Full'; the class number of the observation;
              if 2, class 1 for 'Currently Marriage' and 2 for other
              if 3, class 1 for 'Currently Marriage', 2 for 'Divorced', and 3 for other
              if 'Full', check the code book for the meaning of each class         
    dropColumns: whether drop the columns that may have correlation with the marriage status (default is True)
    '''
    
    # parameter check
    if classNum not in [2, 3, 'Full']:
        raise ValueError('Invalid class number: should be 2, 3, or "Full".')    
    
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
                   'PPLSTSCH', 'DOLSTSCH', 'XGRADE', 'XSPSCH', 'MARC']
    selectedData = rawData[selectedCol]
    
    # filter data with more than 1500 'NA' values
    NAfilter = []
    for i in selectedCol:
        if len(selectedData[selectedData[i] == 'Not applicable']) < 1500:
            NAfilter += [i]
    selectedData = selectedData[NAfilter]
    
    # sample the marriage class
    if marriageNum != 'Full':
        marriageClass = selectedData[selectedData['MARC'] == 'Currently married']
        dropNum = len(marriageClass) - marriageNum
        if not dropNum > 0:
            raise ValueError('The number of sampled "Marriage" class should be smaller than its actual number. Try another value.')
        drop_id = np.random.choice(marriageClass.index, dropNum, replace=False)
        selectedData = selectedData.drop(drop_id) 
    
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
    
    # drop those terms correlated to marriage status
    selectedData.drop('SSJB1WK', axis=1, inplace=True)
    selectedData.drop('SPAGEX', axis=1, inplace=True)
    selectedData.drop('SPLVTG', axis=1, inplace=True)
    selectedData.drop('INCSP', axis=1, inplace=True)
    selectedData.drop('SSLSTSCH', axis=1, inplace=True)
    selectedData.drop('XSSNBROY', axis=1, inplace=True)
    selectedData.drop('XSSNSISY', axis=1, inplace=True)
    
    if dropColumns == True:
        selectedData.drop('CCNUMTTL', axis=1, inplace=True)
        selectedData.drop('CC01SEX', axis=1, inplace=True)
        selectedData.drop('CC01AGE', axis=1, inplace=True)
        selectedData.drop('SZFFOTHR', axis=1, inplace=True)
        selectedData.drop('SZFFONLY', axis=1, inplace=True)
        selectedData.drop('SZFFTTL', axis=1, inplace=True)
        selectedData.drop('FFHEAD', axis=1, inplace=True)  
    
    selectedData.replace('No answer', 0, inplace=True)
    selectedData.replace('Not applicable', 0, inplace=True)   

    # observation cleaning
    observation = np.array(selectedData['MARC'])
    cleanedObservation = np.zeros(len(observation))
    
    if classNum == 2:    
        for i in range(len(observation)):
            if observation[i] == 'Currently married':
                cleanedObservation[i] = 1
            else:
                cleanedObservation[i] = 2
    elif classNum == 3:
        for i in range(len(observation)):
            if observation[i] == 'Currently married':
                cleanedObservation[i] = 1
            elif observation[i] == 'Divorced':
                cleanedObservation[i] = 2 
            else:
                cleanedObservation[i] = 3
    else:
         for i in range(len(observation)):
            if observation[i] == 'Currently married':
                cleanedObservation[i] = 1
            elif observation[i] == 'Divorced':
                cleanedObservation[i] = 2 
            elif observation[i] == 'Widowed':
                cleanedObservation[i] = 3 
            elif observation[i] == 'Never-married':
                cleanedObservation[i] = 4 
            elif observation[i] == 'Separated':
                cleanedObservation[i] = 5 
            elif observation[i] == 'Cohabiting':
                cleanedObservation[i] = 6 
            else:
                cleanedObservation[i] = 9       
            
    selectedData.drop('MARC', axis=1, inplace=True)
    cleanedData = selectedData.copy()
    cleanedObservation = cleanedObservation.astype(int)
            
    return cleanedData, cleanedObservation

def svm_test():
    #you need to import pandas, numpy, sklearn.svm.SVC, sklearn to use this function
    data = pd.read_csv('cleanedData.csv',header = None)
    data = np.asarray(data)[1:,1:]
    result = pd.read_csv('cleanedObservation.csv',header = None)
    result = np.asarray(result)[1:,1]
    trainSample = np.random.choice(range(5000), 4000, replace=False)
    trainData = data[trainSample,:]
    trainObservation = result[trainSample]
    testSample = np.setdiff1d(np.arange(5003), trainSample)
    testData = data[testSample,:]
    testObservation = result[testSample]
    prediction = clf.predict(testData)
    accuracy = np.sum(np.abs(prediction.astype(int) - testObservation.astype(int)))
    score = sklearn.metrics.accuracy_score(testObservation, prediction)
    return accuracy, score

def decision_tree():
    df1 = pd.read_csv('cleanedData.csv')
    df2 = pd.read_csv('cleanedObservation.csv')
    x = df1[df1.columns[1:]]
    y = df2['MARC']
    x_new = SelectKBest(chi2, k=10).fit_transform(x, y)
    x_train,x_test,y_train,y_test = cross_validation.train_test_split(x_new,y,test_size=0.4,random_state=0)
    score = []
    i_range = range(3,40)
    for i in range(3,40):
        clf = tree.DecisionTreeClassifier(max_depth=i)
        clf = clf.fit(x_train,y_train)
        score.append((clf.score(x_test,y_test)))
    ##plt.plot(i_range, score)
    depth = score.index(max(score)) + 5
    clf = tree.DecisionTreeClassifier(max_depth= depth)
    clf = clf.fit(x_train,y_train)
    score = max(score)
    accuracy = np.sum(np.abs(clf.predict(x_test).astype(int) - y_test.astype(int)))
    return score, accuracy,metrics.confusion_matrix(y_test, clf.predict(x_test))