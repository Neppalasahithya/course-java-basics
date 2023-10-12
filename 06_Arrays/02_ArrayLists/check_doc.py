import time
from PyPDF2 import PdfReader
import os
import hashlib
from proc import utils as putil
from proc import Job

def file_as_bytes(file):
        with file:
            return file.read()

def processFiles(paths,path):
                files=[]
                c=0
                for i in paths:
                    info=[]
                    c+=1
                    if c==-1:
                        break
                    if '.pdf' in i:
                        info+=[i]
                        file=path+"/"+i
                        print(file)
                        hash=hashlib.sha256(file_as_bytes(open(file, 'rb'))).hexdigest()
                        info+=[hash]
                        try:
                            reader=PdfReader(file)
                            pages=reader.pages    
                            for j in range(len(pages)): 
                                s=pages[j].extract_text()
                            info+=['valid',len(pages)]
                        except:
                            info+=['invalid',-1]
                    files+=[info]
                return files


if __name__ == '__main__': 

    import pandas as pd
    src='\\\\eunet\chbs-dfs\DATA\PH\AppData\AppsecReports\Attachments\Attachments_Prod/'
    #src='\\\\eunet/chbs-dfs/DATA/PH/APPData/AppsecReports/Attachments/Attachments_Prod/REP/AppSec_REP_AR/Latest_AppSec_REP_AR/'
    st=time.time()

    for lev1 in ['REP/']:
        for lev2 in['REP_DAST','REP_SAST','REP_TM','REP_PT']:
            path=src+lev1+lev2
            paths=os.listdir(path)
            print("Paths found:",len(paths))
            files=[]
            
            def then(res):
                global files
                #print(res)
                files+=res[0]

            n=8
            jobs=[Job(processFiles,[[p],path],then) for p in paths]

            putil.concurrent(jobs,n)

            #print(files)
            
            pd.DataFrame(files,columns=['File','Hash','Status','Pages']).to_csv('Doc Check/Export/{}.csv'.format(lev2),index=False)


        # with open(path,'rb') as f:
        #     print(f.read())

    print(time.time()-st)
