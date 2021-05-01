import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import matplotlib.patches as mpatches

def open_nc(path,scale=1.0):  
    ds=(xr.open_dataset(path)*scale)
    ds=ds.assign_coords(lon=(((ds.lon + 180) % 360) - 180))
    ds=ds.reindex(lon=sorted(ds.lon))  
    return ds

def select_data(ds, lat_min, lat_max, lon_min, lon_max):
    """
    select the dataset given the box information
    """
    ds_select = ds.where((ds.lat>=lat_min)&(ds.lat<=lat_max)
                        & (ds.lon>=lon_min) & (ds.lon<=lon_max))
    return ds_select

def year_comp(chi, lat_min, lat_max, lon_min, lon_max):
    file_path = {}
    parent_path = "/data/keeling/a/zzheng25/d/mam4_paper_data/chi_only/comp_analysis/"
    SRF_ls = [
    "bc_a1_SRF","bc_a4_SRF",
    "dst_a1_SRF","dst_a2_SRF",
    "ncl_a1_SRF","ncl_a2_SRF",
    "pom_a1_SRF","pom_a4_SRF",
    "so4_a1_SRF","so4_a2_SRF",
    "soa_a1_SRF","soa_a2_SRF"
    ]

    per_ls = [vari[:-4]+"_per" for vari in SRF_ls]

#     MAM4 = open_nc(file_path["MAM4"]+chi+"_mean.nc",scale=100.0)[chi]
#     ML = open_nc(file_path["MAM4"]+chi+"_mean.nc",scale=100.0)[chi]
#     diff = open_nc(file_path["diff"]+chi+"_mean.nc",scale=100.0)[chi]
    comp = open_nc(parent_path + "2011_year_comp.nc")

    # select the region based on lat and lon
#     MAM4_s = select_data(MAM4,lat_min, lat_max, lon_min, lon_max)
#     ML_s = select_data(ML,lat_min, lat_max, lon_min, lon_max)
#     diff_s = select_data(diff,lat_min, lat_max, lon_min, lon_max)
    comp_s = select_data(comp,lat_min, lat_max, lon_min, lon_max)

    df_mean=comp_s.to_dataframe()[per_ls].mean()

    d = {
        "bc":[0,df_mean["bc_a1_per"],df_mean["bc_a4_per"]],
        "dst":[df_mean["dst_a2_per"],df_mean["dst_a1_per"],0],
        "ncl":[df_mean["ncl_a2_per"],df_mean["ncl_a1_per"],0],
        "pom":[0,df_mean["pom_a1_per"],df_mean["pom_a4_per"]],
        "soa":[df_mean["soa_a2_per"],df_mean["soa_a1_per"],0],
        "so4":[df_mean["so4_a2_per"],df_mean["so4_a1_per"],0]
    }

    df = pd.DataFrame(data=d)
    df = df.rename(index={0: "Aitken", 1: "Accumulation", 2: "Primary carbon"})
    
    return df

def plot_difference_with_anchor(da_mam4,da_ml,da_diff,lat_min, lat_max, lon_min, lon_max):
    """
    Plot the 1 x 3 figures using anchor
    """
    fig = plt.figure(figsize=(16,4))
    ax1 = plt.subplot(131,projection=ccrs.PlateCarree());
    im1=da_mam4.plot(ax=ax1,
                     vmax=100,vmin=0,add_colorbar=False,cmap='RdYlBu_r')
    ax1.add_patch(mpatches.Rectangle(xy=[lon_min, lat_min], 
                                     width=(lon_max-lon_min), 
                                     height=(lat_max-lat_min),
                                     edgecolor="black",
                                     facecolor='None',
                                     lw=1.5))
    ax1.coastlines(alpha=0.66)
    ax1.set_title("mam4")
    plt.colorbar(im1, orientation="horizontal", pad=0.15)
    #plt.show()

    ax2 = plt.subplot(132,projection=ccrs.PlateCarree());
    im2=da_ml.plot(ax=ax2,
                   vmax=100,vmin=0,add_colorbar=False,cmap='RdYlBu_r')
    ax2.add_patch(mpatches.Rectangle(xy=[lon_min, lat_min], 
                                     width=(lon_max-lon_min), 
                                     height=(lat_max-lat_min),
                                 edgecolor="black",
                                 facecolor='None',
                                 lw=1.5))
    ax2.coastlines(alpha=0.66)
    ax2.set_title("ml")
    plt.colorbar(im2, orientation="horizontal", pad=0.15)
    #plt.show()

 
    ax3 = plt.subplot(133,projection=ccrs.PlateCarree());
    im3=da_diff.plot(ax=ax3,
                     vmin=-100,vmax=100,add_colorbar=False,cmap="bwr")
    ax3.add_patch(mpatches.Rectangle(xy=[lon_min, lat_min], 
                                     width=(lon_max-lon_min), 
                                     height=(lat_max-lat_min),
                                     edgecolor="black",
                                     facecolor='None',
                                     lw=2.5))
    ax3.coastlines(alpha=0.66)
    ax3.set_title("diff")
    plt.colorbar(im3, orientation="horizontal", pad=0.15)
    plt.show()
