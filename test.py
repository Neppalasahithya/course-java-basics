from math import ceil
from typing import Callable
import pandas as pd
import concurrent.futures
#Testing for github code block
class Job:
    def __init__(self,func:Callable,args:list[str or int],then:Callable=lambda x:x,data={}) -> None:
        self.func=func
        self.args=args
        self.then=then
        self.data=data
        self.excp=''

class utils:
    def transform(src:pd.DataFrame,conv)->pd.DataFrame:
        df=pd.DataFrame()  
        src=src.fillna('')     
        for i in conv:            
            # if conv[i] and isinstance(conv[i],str):
            #     df[i]=src[conv[i]]
            # elif isinstance(conv[i],list):
            #     df[i]=src.apply(conv[i][0],axis=1)
            # elif callable(conv[i]):
            #     df[i]= conv[i](src)
            # else:    
            #     df[i]=''
                
            if not conv[i]:
                df[i]=''
            else:
                df[i]=src[conv[i]] if not callable(conv[i]) else src.fillna('').apply(conv[i],axis=1)
        print("Records transformed ",df.shape)
        return df 

    def dfToDict():
        a=1
    
    def concurrent(jobs:list[Job],workers:int=4,use_process=False):        
        executor=concurrent.futures.ProcessPoolExecutor(max_workers=workers) if use_process else concurrent.futures.ThreadPoolExecutor(max_workers=workers)
        #futures={executor.submit(snow.prepareExport, snow.it_incident,arg,True,"csv",False,False): job for job in jobs}
        try:
            futures={executor.submit(job.func,*job.args): job for job in jobs}        
            for future in concurrent.futures.as_completed(futures):
                job=futures[future]
                if future.exception() and job.excp:    
                    job.excp(future.exception())    
                elif job.then:
                    job.then([future.result(),job])
        except KeyboardInterrupt:
            print("Shutting down jobs")
            executor.shutdown(True,cancel_futures=True)
        executor.shutdown()

    def splitArray(a, n):
        k, m = divmod(len(a), n)
        return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))

    def splitDict(d, n):
        keys = list(d.keys())
        n=ceil(len(keys)/n)
        dicts=[]
        for i in range(0, len(keys), n):
            dicts+=[{k: d[k] for k in keys[i: i + n]}]
        return dicts

    # def parallelize_dataframe(df, func, n_cores=4):
    #     df_split = np.array_split(df, n_cores)
    #     pool = Pool(n_cores)
    #     df = pd.concat(pool.map(func, df_split))
    #     pool.close()
    #     pool.join()
    #     return df
    
    # def parallelSearch(df,strings):
    #     a


    
