import numpy as np
import pandas as pd
import time
import xarray as xr
import gc
import sys


############how to use this script##################

#python cal_ms.py "2011" 01" "01"

####################################################


def get_mode_chi(a_raw, chi_type):
    ###reference###
    #http://lagrange.mechse.illinois.edu/pubs/RiWe2013/RiWe2013.pdf
    a=get_mode_ar(a_raw, chi_type)
    
    np_sum = np.nansum(a)
    
    # pa_m is mass fraction of species a in mode m
    pa_m = a/(np.nansum(a,axis=1)[:,None])
    # pm is mass fraction of mode m in population
    pm = np.nansum(a,axis=1)/np_sum
    # pa is mass fraction of species a in population
    pa = np.nansum(a,axis=0)/np_sum
    
    D_m = np.nanprod(np.power(pa_m,-pa_m),axis=1)
    D_alpha=np.nanprod(np.power(D_m,pm))
    D_gamma=np.nanprod(np.power(pa,-pa))
    
    return (D_alpha-1)/(D_gamma-1)


def get_mode_ar(a_raw, chi_type):
    
    if chi_type=="chi_b":
        a=np.empty([3,2]) * np.nan
        
        a[0,0] = a_raw[0] #bc_a1
        a[2,0] = a_raw[1] #bc_a4
        
        a[0,1] = a_raw[2]+a_raw[5]+a_raw[8]+a_raw[10]+a_raw[13] #dst_a1+ncl_a1+pom_a1+so4_a1+soa_a1
        a[1,1] = a_raw[3]+a_raw[6]+a_raw[11]+a_raw[14] #dst_a2+ncl_a2+so4_a2+soa_a2
        #a[2,1] = a_raw[4]+a_raw[7]+a_raw[12] #dst_a3+ncl_a3+so4_a3
        a[2,1] = a_raw[9] #pom_a4
        
        return a
    
    elif chi_type=="chi_c":
        a=np.empty([3,2]) * np.nan
        
        a[0,0] = a_raw[0]+a_raw[8] #bc_a1+pom_a1
        a[1,0] = 0
        a[2,0] = a_raw[1]+a_raw[9] #bc_a4+pom_a4
        
        a[0,1] = a_raw[2]+a_raw[5]+a_raw[10]+a_raw[13] #dst_a1+ncl_a1+so4_a1+soa_a1
        a[1,1] = a_raw[3]+a_raw[6]+a_raw[11]+a_raw[14] #dst_a2+ncl_a2+so4_a2+soa_a2
        a[2,1] = 0
        
        return a
    
    elif chi_type=="chi_h":
        a=np.empty([3,2]) * np.nan
        
        a[0,0] = a_raw[0]+a_raw[2]+a_raw[8]  #bc_a1+dst_a1+pom_a1
        a[1,0] = a_raw[3] #dst_a2
        #a[2,0] = a_raw[4] #dst_a3
        a[2,0] = a_raw[1]+a_raw[9] #bc_a4+pom_a4
        
        a[0,1] = a_raw[5]+a_raw[10]+a_raw[13] #ncl_a1+so4_a1+soa_a1
        a[1,1] = a_raw[6]+a_raw[11]+a_raw[14] #ncl_a2+so4_a2+soa_a2
        #a[2,1] = a_raw[7]+a_raw[12] #ncl_a3+so4_a3
        
        return a
        
    else:
        return("please type the correct chi type")

xr_2d_vari_ls = ['bc_a1_SRF','bc_a4_SRF',
                 'dst_a1_SRF','dst_a2_SRF','dst_a3_SRF',
                 'ncl_a1_SRF','ncl_a2_SRF','ncl_a3_SRF',
                 'pom_a1_SRF','pom_a4_SRF',
                 'so4_a1_SRF','so4_a2_SRF','so4_a3_SRF',
                 'soa_a1_SRF','soa_a2_SRF']


year=sys.argv[1]
month_start=sys.argv[2]
month_end=sys.argv[3]

path="/data/keeling/a/zzheng25/d/mam4_paper_data/mam4_cesm_raw/"
save_path="/data/keeling/a/zzheng25/d/mam4_paper_data/mam4_cesm_cal/"
print("start the year")

#for i in range(1,13):
for i in range(int(month_start),int(month_end)+1):
    ss=time.time()
    month=str(i).zfill(2)
    print("start the month:",month)
    ds=xr.open_dataset(path+str(year)+"_"+month+".nc")
    
    # convert ds to dataframe then numpy array
    s_time=time.time()
    df = ds[xr_2d_vari_ls].to_dataframe().reset_index()
    df_np = df.to_numpy()[:,3:]
    del ds
    gc.collect()
    print(time.time()-s_time)
    
    s_time=time.time()
    print("start chi_b")
    df["chi_b"]=np.apply_along_axis(get_mode_chi, 1, df_np, "chi_b")
    print("start chi_c")
    df["chi_c"]=np.apply_along_axis(get_mode_chi, 1, df_np, "chi_c")
    print("start chi_h")
    df["chi_h"]=np.apply_along_axis(get_mode_chi, 1, df_np, "chi_h")
    print("It took",time.time()-s_time,"to calculate mixing state indexs") 
    del df_np
    gc.collect()
    
    df_cal = df.set_index(["time","lat","lon"]).to_xarray() 
    del df
    gc.collect() 
    
    df_cal.to_netcdf(save_path+year+"_"+month+".nc")
    del df_cal
    gc.collect()
    
    print("It took",time.time()-ss,"to deal with month", month) 
    print("\n")
