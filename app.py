#---imports
import ijson
from datetime import datetime
from dateutil import tz
import urllib.request
import time
import sys
import os
#---static variables
global fileType
fileType = []
global fileDate
fileDate = []
global TotalFileNum
global DownloadsFailed
global DownloadsOK
global DownloadsExist
timeStart = None
global debug
#---debug switch
debug = False #Simulate application flow without actually downloading files
#---debug switch

#Gets the total number of files to process
def GetTotalFileNum(fileName, jsonObject):
    global TotalFileNum
    TotalFileNum = 0
    objects = ijson.kvitems(open(fileName),jsonObject)
    memories = (k for v, k in objects if v == 'Media Type')
    for memory in memories:
        TotalFileNum = TotalFileNum + 1
#Gets the files filetype
def GetFileTypes(fileName, jsonObject):
    global TotalFileNum
    global fileTypes
    TotalFileNum = 0
    objects = ijson.kvitems(open(fileName),jsonObject)
    fileTypes = (l for m, l in objects if m == 'Media Type')
    print('---Getting Filetypes---')
    for ftype in fileTypes:
        if(ftype == 'VIDEO'):
            fileType.append('.mp4')
        elif(ftype == 'PHOTO'):
            fileType.append('.jpg')
        TotalFileNum = TotalFileNum + 1 
#Gets the files filedates
def GetFileDates(fileName, jsonObject):
    global fileDate
    objects = ijson.kvitems(open(fileName),jsonObject)
    fileDates = (i for j, i in objects if j == 'Date')
    print('---Getting Filedates---')
    for fdate in fileDates:
        fileDate.append(datetime.strptime(fdate,'%Y-%m-%d %H:%M:%S UTC'))
#Gets the files incl. error-handling, logging, duplicate checking...
def GetFiles():
    #variables
    k = 0
    global DownloadsFailed
    DownloadsFailed = 0
    global DownloadsOK
    DownloadsOK = 0
    global DownloadsExist
    DownloadsExist = 0
    global TotalFileNum
    global fileDate
    global fileType
    dupCount = 1
    filePath = './media/'
    #write first line into downloaded.txt
    txtDownloaded = open('downloaded.txt','a')
    txtDownloaded.write('---' + datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + ' Downloaded files:\n')
    txtDownloaded.close()
    #parse json file
    objects = ijson.kvitems(open('memories_history.json'),'Saved Media.item')
    fileLinks = (v for k, v in objects if k == 'Download Link')
    print('---Downloading Files---')
    #create filePath if not exists
    if os.path.exists(filePath) == False:
        os.makedirs(filePath)
    #foreach file
    for flink in fileLinks:
        #set current file number starting from 0
        currFileNumStr = str(k + 1)
        #assign fileDate and fileType to current fileNum and build filename
        fileName = 'Snapchat-' + fileDate[k].astimezone(tz.tzoffset('UTC',10800)).strftime('%Y%m%d_%H%M%S') + fileType[k] #tzoffset('tz',offset in seconds from UTC-2) so 10800(3hrs)=UTC+1
        try:
            #the following if-else clause is needed because snapchat saves some files under the exact same timestamp thus resulting in overwriting files createt under one timestamp if not handled
            #when current file is not available on disk
            if os.path.isfile(filePath + fileName) == False:
                print('- Downloading file: ' + fileName + ' (' + currFileNumStr + '/' + str(TotalFileNum) + ')' + ' ---')
                #download current file if debug is disabled
                if debug == False:
                    urllib.request.urlretrieve(flink,filePath + fileName)
                #when debug mode is enabled mock file download
                else:
                    open(filePath + fileName,'a')
                #log the link of downloaded file
                txtDownloaded = open('downloaded.txt','a')
                txtDownloaded.write(flink + '\n')
                txtDownloaded.close()
                #count download as success
                DownloadsOK = DownloadsOK + 1
                #reset duplicate counter of last highest duplicate file
                dupCount = 1
            #when file is available on disk
            else:
                #check if link was already downloaded
                linkDownloaded = False
                txtDownloadedRead = open('downloaded.txt','r')
                for txtLine in txtDownloadedRead:
                    if txtLine == flink + '\n':
                        linkDownloaded = True
                txtDownloadedRead.close()
                #when already downloaded skip file
                if linkDownloaded == True:
                    print('- Skipping file: "' + fileName + '"' + ' (' + currFileNumStr + '/' + str(TotalFileNum) + ')' + ' already exists!')
                    DownloadsExist = DownloadsExist + 1
                #when not downloaded already download file and handle recursive file naming
                else:
                    #adding dupplicate count to file name
                    fileNameDup = 'Snapchat-' + fileDate[k].strftime('%Y%m%d_%H%M%S') + '_' + str(dupCount) + fileType[k]
                    print('- Downloading file: ' + fileNameDup + ' (' + currFileNumStr + '/' + str(TotalFileNum) + ')' + ' ---')
                    #when debug mode is disabled download file
                    if debug == False:
                        urllib.request.urlretrieve(flink,filePath + fileNameDup)
                    #when debug mode is enabled mock file download
                    else:
                        open(filePath + fileName,'a')
                    #log the link of downloaded file
                    txtDownloaded = open('downloaded.txt','a')
                    txtDownloaded.write(flink + '\n')
                    txtDownloaded.close()
                    #count download as success
                    DownloadsOK = DownloadsOK + 1
                    #increment the dupplicate counter by one for possible next duplicate
                    dupCount = dupCount + 1
        #for some reason some files fail to download from snapchat servers because they expired, so we handle this and log failed files
        except Exception as e:
            #e = sys.exc_info() [0]
            print('- Error downloading file: ' + fileName + ' ("' + flink + '")' + ' Exception: ' + repr(e))
            #log failed fileName and fileLink to errors.txt
            txtError = open('errors.txt','a')
            txtError.write(datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + ' Error downloading file: ' + fileName + ' ("' + flink + '")' + 'Exception: ' + repr(e) + '\n')
            txtError.close()
            #count download as failed
            DownloadsFailed = DownloadsFailed + 1
        #no matter if the current file downloaded correctly, was skipped or failed downloading we have to increment the cureent file counter by one (for assigning fileType and fileDate to the enxt file and log the progress)
        finally:
            k = k + 1

#---calling code
timeStart = datetime.now()
print('---Starting file download at ' + str(timeStart).split('.',1)[0] + '---')
GetTotalFileNum('memories_history.json','Saved Media.item')
GetFileTypes('memories_history.json','Saved Media.item')
GetFileDates('memories_history.json','Saved Media.item')
GetFiles()
timeEnd = datetime.now()
timeDuration = timeEnd - timeStart
#---printing stats
print('---FINISH---')
print(' Download stats:')
print(' - Files present on Snapchat servers:\t' + str(TotalFileNum))
print(' - Files downloaded from Snapchat:\t' + str(DownloadsOK))
print(' - Files already existed on disk:\t' + str(DownloadsExist))
print(' - Files failed downloading:\t\t' + str(DownloadsFailed))
print(' - Download start:\t' + str(timeStart).split('.',1)[0])
print(' - Download end:\t' + str(timeEnd).split('.',1)[0])
print(' - Download duration:\t' + str(timeDuration).split('.',1)[0] + ' (H:MM:SS)')