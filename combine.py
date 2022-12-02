#import the modules
import time

import numpy as np
import pandas as pd
import os
import pandas as pd
#read the path
cwd = os.path.abspath('combine')
#list all the files from the directory
file_list = os.listdir(cwd)
print(file_list)


df_append = pd.DataFrame()
#append all files together
for file in file_list:
            print(file)
            if(file==".DS_Store"):
                continue
            df_temp = pd.read_csv(f"combine/{file}")
            df_append = df_append.append(df_temp, ignore_index=True)
df_append.to_csv("final.csv")



