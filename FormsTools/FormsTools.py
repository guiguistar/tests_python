#!/usr/bin/env python3
# coding: utf-8

"""
TODO:
 + check the case where there's no file to process
 + make private methods private
 + find antother name for the first class
"""

import pandas
import os
import glob
import re
import math
import argparse
import xlsxwriter

from typing import List

def roundTenth(x):
    if math.isnan(x): return x
    return round(10*x)/10

def arrow(variation):
    if variation > 0: return '↗' 
    if variation < 0: return '↘'
    return '→'

def computeProgressionString(x):
    """Compute this kind of string: ↗ (+4) or ↘ (-2)"""
    if math.isnan(x): return float('nan')
    x = int(x)
    return '{0} ({1:+d})'.format(arrow(x),x) if x else ' (-)'

def means(dataFrame, j_min, j_max):
    """Compute the mean the columns whose index is in [j_min;j_max["""
    return dataFrame.iloc[:,j_min:j_max].mean(axis=1)

def printList(l):
    width = 0
    for item in l:
        if len(item) > width: width = len(item)
    for item in l:
        print('{}'.format(item).rjust(width+2))

class XlsxFilesProcessor:
    """
    Class for processing .xlsx files from Microsoft Forms.
    Regex must have this two following groups:
     - <string> 
     - <number>
    """
    def __init__(self,rString = r'(?P<string>QCM_MF_S1_(?P<number>[1-9]|1[012]))',
                 workingDir='.'):
        self.__regexMCQ = re.compile(rString)

        # Go to the proper directory
        os.chdir(workingDir)
        print('Working directory:\n  {0}'.format(os.getcwd()))

        # Set the xlsx file list
        self.__xlsx_file_list = glob.glob('*.xlsx')
        print('Found {} .xlsx files:'.format(len(self.xlsx_file_list)))
        printList(self.xlsx_file_list)

        # Set the MCQ file list
        self.__MCQ_file_list = XlsxFilesProcessor.__extract_matching_files(self.xlsx_file_list, self.__regexMCQ)
        print('Found {} MCQ files:'.format(len(self.MCQ_file_list)))
        printList(self.MCQ_file_list)
        
    @property
    def xlsx_file_list(self):
        return self.__xlsx_file_list

    @property
    def MCQ_file_list(self):
        return self.__MCQ_file_list

    @staticmethod
    def __extract_matching_files(file_list: List[str], regex) -> List[str]:
        """
          regex has to have two groups: <string> and <number>.
          Return the ordered by number list of matching files.
          Might be public.
        """
        res = []
        for f in file_list:
            print('Processing file: {}'.format(f))
            match = regex.search(f)
            if match:
                gr = match.group
                print('Mcq regex found: {} {}'.format(gr('string'),gr('number')))
                res.append((f,int(gr('number'))))
            else:
                print('Mcq regex not found. File ignored.')
                
        return sorted(res, key=lambda x:x[1])
        
    
class TopN:
    """
    Compute the ranks of the top students. The computation is based
    on .xlsx report files from Microsoft Forms.
    """

    inputNameField = 'Nom'
    inputPointField = 'Total points'

    nameField = 'Name'
    pointField = 'Total points'
    
    namesToRemoveList = ['Filipe Vasconcelos', 'Guillaume Roux']

    pointsField = 'Total points'
    previousMeanField = 'Previous mean'
    previousRankField = 'Previous rank'
    meanField = 'Mean'
    rankField = 'Rank'
    lastMCQField = 'Last MCQ'
    progressionField = 'Progression'
    missField = 'Miss'

    maxMissesNumber = 3
    
    def __init__(self, N=10,title='Title', rString = r'(?P<string>QCM_MF_S1_(?P<number>[1-9]|1[012]))', workingDir='.'):
        # Get the .xlsx files from the current working directory
        self.xlsxProcessor = XlsxFilesProcessor(rString=rString, workingDir=workingDir)
        self.N = N
        self.notesNumber = 0
        self._outputFileName = 'top'+str(self.N)+'.xlsx'
        self.title = title
        self.dataFrame = None
        
        fileList = self.processXlsxFiles()

        if fileList:
            self.dataFrame = self.processMCQFiles(fileList)
            print(self.dataFrame)

            TopN.correctTotalPoints(self.dataFrame)
            self.removeRowsByNames()
            self.processDataFrame()
            
            print(self.dataFrame)
            
        else:
            print('No xlsx file to process.')

    @property
    def outputFileName(self,name):
        return self._outputFileName
    @outputFileName.setter
    def outputFileName(self,name):
        self._outputFileName = name
    
    def removeRowsByNames(self):
        self.dataFrame = TopN.staticRemoveRowsByNames(self.dataFrame,
                                                      self.namesToRemoveList)
            
    def processDataFrame(self):
        self.dataFrame = TopN.staticProcessDataFrame(self.dataFrame)

    def computeCharts(self):
        if self.dataFrame is None:
            print('Can\'t compute charts with no file.')
            return

        numberOfMCQ = sum(self.pointsField in col for col in self.dataFrame.columns)
        lastPointsField = self.dataFrame.columns[numberOfMCQ]
        
        charts = self.dataFrame.loc[:,[self.nameField,self.rankField,self.meanField]]

        if numberOfMCQ > 1:
            charts[self.lastMCQField] = self.dataFrame.loc[:,[lastPointsField]]
            charts[self.progressionField] = self.dataFrame.loc[:, [self.progressionField]]
            charts[self.lastMCQField].fillna('', inplace=True)
            
        charts[self.missField] = self.dataFrame[self.missField]
        
        self.charts = charts

        return charts

    def createXlsx(self):
        if self.dataFrame is None:
            print('Can\'t create .xlsx with no input file.')
            return
        workbook = xlsxwriter.Workbook(self._outputFileName,{'nan_inf_to_errors': True})
        worksheet = workbook.add_worksheet()
        
        bold = workbook.add_format({'bold': True})
        centered = workbook.add_format()
        centered.set_align('center')
        boldAndCentered = workbook.add_format({'bold': True})
        boldAndCentered.set_align('center')

        offset = 2

        worksheet.merge_range(0,0,0,len(self.head().columns)-1,self.title,boldAndCentered)
        
        for j, col in enumerate(self.charts.columns):
            width = len(col)
            if j == 0:
                worksheet.write(0+offset,j,col,bold)
            else:
                worksheet.write(0+offset,j,col,boldAndCentered)
            for i, row in enumerate(self.charts[col]):
                if j == 0:
                    worksheet.write(i+1+offset,j,row)
                else:
                    worksheet.write(i+1+offset,j,row,centered)
                    
                length = len(str(row))
                if length > width:
                    width = length
                if i == self.N-1:
                    break
            worksheet.set_column(j,j,width+2)
            
        workbook.close()
        
    def saveTopN(self):
        self.head().to_excel(self._outputFileName,index=False)

    def head(self):
        if self.dataFrame is None:
            print('Can\'t compute charts head  with no file.')
            return
        return self.charts.head(self.N)
    
    def computeAndSaveTopN(self):
        self.computeCharts()
        self.saveTopN()
    
    def processXlsxFiles(self):
        #self.xlsxProcessor.lsFiles()
        
        #return self.xlsxProcessor.detect_MCQ_files()
        return self.xlsxProcessor.MCQ_file_list
        
    def processMCQFiles(self, fileList):
        dataFrame = None
        self.notesNumber = len(fileList)
        
        for i, fileNameAndNumber in enumerate(fileList):
            fileName, number = fileNameAndNumber
            if i == 0:
                dataFrame = self.openMCQ(fileName)
            else:
                _, lastNumber = fileList[i-1]
                newDataFrame = self.openMCQ(fileName)

                dataFrame = dataFrame.merge(newDataFrame,
                                            on=self.nameField, how='outer',
                                            suffixes=('_{0}'.format(i),'_{0}'.format(i+1)))

                print('Last number: {}, number: {}'.format(lastNumber,number))
                
                if lastNumber == number:
                    dataFrame.iloc[:,-2] = dataFrame.iloc[:,-2].combine_first(dataFrame.iloc[:,-1])
                    dataFrame = dataFrame.iloc[:,:-1] # remove last col
                    self.notesNumber -= 1
                    
        print('Index of last col with points: {0}'.format(i+1))
        print('Number of notes: {}'.format(self.notesNumber))
        
        return dataFrame

    def formatXlsx(self):
        workbook = xlsxwriter.Workbook(self._outputFileName)
        print(workbook)
        workbook.close()
    
    @classmethod
    def openMCQ(cls,fileName):
        dataFrame = pandas.read_excel(fileName)
        dataFrame = dataFrame.rename(columns={cls.inputNameField: cls.nameField,
                                              cls.inputPointField: cls.pointField})
        
        return dataFrame[[cls.nameField, cls.pointField]]

    @classmethod
    def correctTotalPoints(cls,dataFrame,limitMin=5,limitMax=20,weightMCQ=10):
        """
        If the MCQ is noted out of limitMin, asks if the
        note has to be multiplied by weightMCQ / limitMin in order to note 
        the MCQ out of weightMCQ.
        """
        for column in dataFrame.columns:
            M = dataFrame[column].max()
            limit = None
            if isinstance(M, float):
                if M == limitMin: limit = limitMin
                if M > 10: limit = limitMax

            input(f'column: {column}, M: {M}, isinstanceOfFloat: {isinstance(M, float)}, limitMin: {limitMin}, limitMax: {limitMax}, limit: {limit}')
            
            if limit:
                answer = '_'
                while not answer in ['', 'Yes', 'No']: 
                    answer = input('Multiply {0} by {1}? Yes / No (default Yes): '.format(column,weightMCQ/limit))

                if answer in ['Yes', '']:
                    dataFrame[column] = weightMCQ / limit * dataFrame[column]

    @classmethod
    def staticProcessDataFrame(cls,dataFrame):
        numberOfMCQ = sum(cls.pointsField in column for column in dataFrame.columns)

        print('Number of \'{0}\' columns found: {1}'.format(cls.pointsField,numberOfMCQ))

        df = dataFrame.copy()

        missedCol = numberOfMCQ - df.iloc[:,1:1+numberOfMCQ].count(axis=1)

        TopN.replaceExceedingNaNByZero(df,cls.maxMissesNumber)

        if numberOfMCQ > 1:
            df[cls.previousMeanField] = means(df,1,1+numberOfMCQ-1)
            df[cls.previousRankField] = df.loc[:,cls.previousMeanField].rank(ascending=False,method='min')
            df[cls.previousMeanField] = df[cls.previousMeanField].map(roundTenth)

        df[cls.meanField] = means(df,1,1+numberOfMCQ)
        df[cls.rankField] = df.loc[:,cls.meanField].rank(ascending=False,method='min').map(int)
        df[cls.meanField] = df[cls.meanField].map(roundTenth)

        df.sort_values(cls.rankField,inplace=True)

        if numberOfMCQ > 1:
            df[cls.progressionField] = (df[cls.previousRankField] - df[cls.rankField]).map(computeProgressionString)

        df[cls.missField] = missedCol
        
        return df
    
    @staticmethod
    def replaceExceedingNaNByZero(dataframe, maxMissesNumber):
        n, p = dataframe.shape

        for i in range(n):
            lives = maxMissesNumber
            for j in range(p):
                if pandas.isna(dataframe.iloc[i,j]):
                    if lives <= 0:
                        dataframe.iloc[i,j] = 0
                    lives -= 1 
                    
    @staticmethod
    def staticRemoveRowsByNames(dataFrame, namesList, nameField='Name'):
        return dataFrame[dataFrame[nameField].map(lambda x:not x in namesList)]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('title',type=str,help='the title of the table')
    parser.add_argument('-o','--output',type=str,help='output file')
    parser.add_argument('-n','--number',type=int,help='number of top',default=10)
    parser.add_argument('-d','--dir',type=str,help='directory containg xlsx files',default='.')
    parser.add_argument('-r','--regex',type=str,help='python regex for filenames',default='(?P<string>QCM_MF_S1_(?P<number>[1-9]|1[012]))')
    args = parser.parse_args()
    
    topN = TopN(N=args.number, title=args.title, rString=args.regex, workingDir=args.dir)
    #topN.processDataFrame()

    if args.output:
        topN.outputFileName = args.output

    topN.computeCharts()
    
    print(topN.head())

    topN.createXlsx()
