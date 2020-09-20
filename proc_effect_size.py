#!/usr/bin/env python

import netCDF4 as nc4
import numpy as np
import numpy.ma as ma

import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import sys, math


CasNam1_CN = "/compyfs/yang954/e3sm_scratch/20190918_CNonly_hcru_hcru_ICB20TRCNRDCTCBC/run/20190918_CNonly_hcru_hcru_ICB20TRCNRDCTCBC.clm2.h0."
CasNam2_CN = "/compyfs/yang954/e3sm_scratch/EXP2CO2_20190918_CNonly_hcru_hcru_ICB20TRCNRDCTCBC/run/EXP2CO2_20190918_CNonly_hcru_hcru_ICB20TRCNRDCTCBC.clm2.h0."

CasNam1_CNP = "/compyfs/yang954/e3sm_scratch/20190912_hcru_hcru_ICB20TRCNPRDCTCBC/run/20190912_hcru_hcru_ICB20TRCNPRDCTCBC.clm2.h0."
CasNam2_CNP = "/compyfs/yang954/e3sm_scratch/EXP2CO2_20190912_hcru_hcru_ICB20TRCNPRDCTCBC/run/EXP2CO2_20190912_hcru_hcru_ICB20TRCNPRDCTCBC.clm2.h0."

CasNam1_CNP_noNSC = "/compyfs/yang954/e3sm_scratch/noNSC_20190912_hcru_hcru_ICB20TRCNPRDCTCBC/run/noNSC_20190912_hcru_hcru_ICB20TRCNPRDCTCBC.clm2.h0."
CasNam2_CNP_noNSC = "/compyfs/yang954/e3sm_scratch/noNSC_EXP2CO2_20190912_hcru_hcru_ICB20TRCNPRDCTCBC/run/noNSC_EXP2CO2_20190912_hcru_hcru_ICB20TRCNPRDCTCBC.clm2.h0."



CasePair = [(CasNam1_CN, CasNam2_CN), (CasNam1_CNP, CasNam2_CNP), (CasNam1_CNP_noNSC, CasNam2_CNP_noNSC)]


DaysPerMon = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

#VarNames = ['GPP', 'NPP', 'TOTVEGC', 'TLAI']
VarNames = ['GPP', 'CPOOL']


for vr in VarNames:
    for c1, c2  in CasePair:
        print (c1, c2)
        for iy in range(2000, 2010):
            for im in range(1,13):
                 timestr = "{:04d}-{:02d}".format(iy, im)
                 with nc4.Dataset(c1 + timestr + '.nc', 'r') as ncf1, nc4.Dataset(c2 + timestr + '.nc', 'r') as ncf2:
                      if im == 1:

                         if vr == 'GPP' or vr == 'NPP':
                            Varm1 = ncf1.variables[vr][0, :, :] * 86400 * DaysPerMon[im-1]
                            Varm2 = ncf2.variables[vr][0, :, :] * 86400 * DaysPerMon[im-1]
                         else:
                            Varm1 = ncf1.variables[vr][0, :, :] / 12.0
                            Varm2 = ncf2.variables[vr][0, :, :] / 12.0
                            
                         lon = ncf1.variables['lon'][:]
                         lat = ncf1.variables['lat'][:]
                         area = ncf1.variables['area'][:,:]
                         lndfrac = ncf1.variables['landfrac'][:,:]
                      else:
                         if vr == 'GPP' or vr == 'NPP':
                            Varm1 = Varm1 + ncf1.variables[vr][0, :, :] * 86400 * DaysPerMon[im-1]
                            Varm2 = Varm2 + ncf2.variables[vr][0, :, :] * 86400 * DaysPerMon[im-1]
                         else:
                            Varm1 = Varm1 + ncf1.variables[vr][0, :, :] / 12.0
                            Varm2 = Varm2 + ncf2.variables[vr][0, :, :] / 12.0
            if iy == 2000:
               Vary1 = Varm1
               Vary2 = Varm2
            else:
               Vary1 = Vary1 + Varm1
               Vary2 = Vary2 + Varm2
    
        Vary1 = Vary1/10.
        Vary2 = Vary2/10.

        if vr == 'GPP':
           GPPy1 = Vary1
        
        ESvar = Vary2 / ma.masked_where(GPPy1<=100., Vary1)
    
    
        #lons, lats = np.meshgrid(lon, lat)
    
        #ax = plt.axes(projection=ccrs.Robinson())
        #cf = ax.contourf(lons, lats, ESGPP, cmap='twilight')
        #ax.coastlines()
        #
        #fig = plt.gcf()
        #fig.colorbar(cf, ax=ax)
    
        #plt.savefig('test.ps')
        
        landarea = ma.masked_where(GPPy1<=100., area*lndfrac)
        ESvar_mean = ma.sum(ESvar*landarea)/ ma.sum(landarea)
         
        ESvar_stdv = math.sqrt( ((ESvar-ESvar_mean)**2*landarea).sum() / (landarea).sum() )
    
        print (vr, ESvar_mean, ESvar_stdv)

