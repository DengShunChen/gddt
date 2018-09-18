#!/usr/bin/env python 
import os
import sys
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from struct import Struct 
from gauss_grid import *
from mpl_toolkits.basemap import Basemap
from cwbgfs_model  import *
from matplotlib import gridspec as gspec
from datetime import datetime
from dateutil.relativedelta import *
from pathlib import Path
from PIL import ImageTk, Image
import platform
#from plot_gfs import *

OS = platform.system()

class Application(tk.Frame):
    def __init__(self, master):
        '''
        Notes: 
          self : for tk.Frame 
          master : from Tk()
        '''
        tk.Frame.__init__(self, master)
        master.title('Global DMS Display Tool')
        master.geometry('{}x{}'.format(1000,800))
        master.resizable(width=True, height=True)

        master.columnconfigure(0, weight=1)
        master.columnconfigure(1, weight=1)
        master.columnconfigure(2, weight=1)
        master.columnconfigure(3, weight=1)
        master.columnconfigure(4, weight=1)
        master.columnconfigure(5, weight=1)
        master.columnconfigure(6, weight=1)
        master.columnconfigure(7, weight=1)
        master.columnconfigure(8, weight=1)
        master.columnconfigure(9, weight=1)
        master.columnconfigure(10, weight=1)
        master.columnconfigure(11, weight=1)
        master.columnconfigure(12, weight=1)
        master.columnconfigure(13, weight=1)
        master.columnconfigure(14, weight=1)
        master.columnconfigure(15, weight=1)
        master.columnconfigure(16, weight=1)
        master.columnconfigure(17, weight=1)
        master.columnconfigure(18, weight=1)
        master.columnconfigure(19, weight=1)
        master.columnconfigure(20, weight=1)

        master.rowconfigure(6, weight=1)

        #self.grid()
        self.createWidgets(master)
    
    def clickPlot(self):

        self.progressbar_var.set(0)

        self.progressbar_var.set(self.progressbar_var.get()+10)
        self.update()

        # save cookie
        self.save_cookies()
        self.progressbar_var.set(self.progressbar_var.get()+10)
        self.update()
       
        if self.loop.get() == 1:      
          self.fcsts = np.arange(0,217,6).tolist()
        else:
          self.fcsts = [0 if str(self.tau.get()) == 'Analysis' else str(self.tau.get()).rstrip(' hours')]

        self.plot_data()    


       # print('done !')
   
    def plot_data(self):
      
      # variables 
      self.variables = [cwbgfs_dmsvar_dict[self.var.get()]]

      if self.var.get() == 'Sea Surface Temperature' or self.var.get() == 'Sea Level Pressure':
        self.label['text'] = self.var.get()
        self.levels = [cwbgfs_dmslev_dict[self.var.get()]]
        
      else:
        self.label['text']= self.var.get() +'  '+ self.lev.get()

        # levels 
        if self.vcoor.get() == '0G':
            self.levels = [ 'H00' if self.lev.get().rstrip(' hPa') == '1000' else '%3.3d' % int(str(self.lev.get()).rstrip(' hPa'))]
        elif self.vcoor.get() == 'MG':
            self.levels = [ 'M%2.2d' % int(self.spinbox.get()) ]

      self.expids= self.dbname.get().split(',')
      self.dmsflags = self.dmsflag.get().split(',')
      self.dmsdb_homes = self.dbpath.get().split(',')
      self.dmsfiles = self.dmsfile.get().split(',')

      self.begin_date = self.dtg.get()
      
      label=None 
      self.bdate = datetime.strptime(self.begin_date,'%Y%m%d%H')
      self.edate = self.bdate
      self.save_figure = True
      self.labels = self.expids if label is None else self.expids if len(label) != len(self.expids) else label
 
      self.progressbar_var.set(self.progressbar_var.get()+10)
      self.update()
 
      if self.bdate == self.edate:
        self.title_substr = '%s' % self.bdate.strftime('%Y%m%d%H')
      else:
        self.title_substr = '%s-%s' % (self.bdate.strftime('%Y%m%d%H'),self.edate.strftime('%Y%m%d%H'))
  
      if len(self.expids) > 1 and len(self.dmsdb_homes) == 1:
        self.dmsdb_homes = self.dmsdb_homes * len(self.expids)
  
      if len(self.expids) > 1 and len(self.dmsflags) == 1:
        self.dmsflags = self.dmsflags * len(self.expids)

      if len(self.expids) > 1 and len(self.dmsfiles) == 1:
        self.dmsfiles = self.dmsfiles * len(self.expids)
  
      self.progressbar_var.set(self.progressbar_var.get()+10)
      self.update()

      # loop over levels and variables
      for v,variable in enumerate(self.variables):
        for l,level in enumerate(self.levels):
          self.var_substr = cwbgfs_level_dict[level]+' '+ cwbgfs_variable_dict[variable]
 
          for self.f,self.fcst in enumerate(self.fcsts): 
            data = {}
  
            if self.bdate == self.edate:
              vdate = self.bdate + relativedelta(hours=int(self.fcst)) + relativedelta(hours=8)
              self.vdate_substr = str(vdate.strftime("%Y-%m-%d-%H")) + ' LST'
            else:
              self.vdate_substr = 'Time Mean'
              
            self.fcst_substr = 'Analysis' if int(self.fcst) == 0 else 'f%3.3d' % int(self.fcst)

            for expid,dmsdb_home,dmsflag,data_dir in zip(self.expids,self.dmsdb_homes,self.dmsflags,self.dmsfiles):
              # print('reading files for ...',expid)

              # model configuration
              model = cwbgfs_model_dict[dmsflag[0:2]]
              jcap = model[0] ; self.nlon = model[1] ; self.nlat = model[2]
              lengh = "%7.7d" % (self.nlat*self.nlon)
  
              # set level and variabel
              if level[0] == 'M':
                dmsflag = list(dmsflag)
                dmsflag[2] = 'M'
                dmsflag = ''.join(dmsflag)
              data_name = level + variable + dmsflag + 'H' + lengh
              data_base = dmsdb_home +'/'+ expid + '.ufs'   # experiment
  
              self.progressbar_var.set(self.progressbar_var.get()+10)
              self.update()

              # get field
              data[expid] = self.get_field(data_base,data_name,data_dir)
  
            if self.filenotexist : 
              return 

            self.progressbar_var.set(self.progressbar_var.get()+10)
            self.update()

            # save/show figure
            if self.diff.get() == 1:
              if len(self.expids) == 2:
                fig, ax, m = self.plot_diff(data)
              elif len(self.expids) == 1:
                fig, ax, m = self.plot_field(data)
              else:
                raise ValueError('len(expids)>2')
            elif self.diff.get() == 0:
              fig, ax, m = self.plot_field(data)
            else:
              raise ValueError('unkown values of self.diff.get()')

            if self.save_figure:
               plt.savefig(self.figname,dpi=100)
               plt.close()
               self.show_figure()
            else:
               plt.show()

    def plot_field(self,df):
      if len(self.expids) == 1:
        fig = plt.figure(figsize=(10,6),dpi=100)
        plt.subplots_adjust(top=0.85,bottom=0.15,right=0.95,left=0.05)
        gs = gspec.GridSpec(1,1)
      elif len(self.expids) == 2:
        fig = plt.figure(figsize=(10,8),dpi=100)
        plt.subplots_adjust(top=0.89,bottom=0.05,right=0.95,left=0.05)
        gs = gspec.GridSpec(2,1) 
      else:
        raise ValueError('len(expids)>2')
     
      for e,expid in enumerate(self.expids):
        ax = plt.subplot(gs[e])
        data = np.reshape(df[expid].values,(self.nlat,self.nlon)) 
        # plot map 
        m = Basemap(lon_0=180,ax=ax)
    
        m.drawmapboundary(fill_color='white',linewidth=0.5)
        m.fillcontinents(color='k',lake_color='k',zorder=0)
    
        m.drawparallels(np.arange(-90,91,20), labels=[1,1,0,1])
        m.drawmeridians(np.arange(-180,180,40), labels=[1,1,0,1])

        # gaussian lattitudes
        lats, bonds = gaussian_latitudes(int(float(self.nlat)/2.))
        lats = np.asarray(lats)    

        # longitudes
        lons = np.linspace(0,360,self.nlon,endpoint=False)
    
        X,Y = np.meshgrid(lons,lats)
        x,y = m(X,Y)

        # statistics
        vmax = np.max(np.amax(data,axis=0))
        vmin = np.min(np.amin(data,axis=0))
        mean = np.mean(data)
        std  = np.std(data)
        self.info_str = 'max/min/avg/std = %e %e %e %e' % (vmax,vmin,mean,std)
        self.label1['text'] = self.info_str
        self.label1['fg'] = 'black'

        if self.selfmaxmin.get() == 1 :
          maxmin = self.maxmin.get().split(',') 
          vmax = float(maxmin[0]) 
          vmin = float(maxmin[1])

        if self.f == 0:
          inc = (vmax - vmin)/50.
          self.levels = np.arange(vmin,vmax+10e-10,inc)
          self.clevels = np.arange(vmin,vmax+10e-10,inc*2)

        # plot countourf
        shading = ax.contourf(x, y, data, self.levels, cmap='RdYlBu_r',  alpha=0.75)
        if self.contour.get() == 1 :
          contour = ax.contour(x, y, data, self.clevels, colors='k', linewidths=0.5)
          plt.clabel(contour,inline=True, fontsize=10, fmt='%5.1f')

        if len(self.expids) == 1:
          plt.title(self.labels[e],fontsize='large',fontweight='bold')
          cbar_ax = fig.add_axes([0.15, 0.05, 0.7, 0.02 ])
          fontsize = 'x-large'
          orientation = 'horizontal'
        elif len(self.expids) == 2:
          plt.title(self.labels[e],fontsize='medium',fontweight='bold')
          cbar_ax = fig.add_axes([0.87, 0.1, 0.02, 0.7 ])
          fontsize = 'large'
          orientation = 'vertical'
        else:
          raise ValueError('len(expids)>2')
      plt.suptitle('%s \n%s  %s  - valid at %s' % (self.var_substr,self.title_substr,self.fcst_substr,self.vdate_substr),fontsize=fontsize,fontweight='bold')
      plt.colorbar(shading, cax=cbar_ax, orientation=orientation)
      
      self.progressbar_var.set(self.progressbar_var.get()+10)
      self.update()

      return fig, ax, m
    
    def plot_diff(self,df):
      fig = plt.figure(figsize=(10,6),dpi=100)
      plt.subplots_adjust(top=0.85,bottom=0.15,right=0.95,left=0.05)
      gs = gspec.GridSpec(1,1)
    
      ax = plt.subplot(gs[0])
      data = np.reshape(df[self.expids[1]].values,(self.nlat,self.nlon))
      data = data - np.reshape(df[self.expids[0]].values,(self.nlat,self.nlon))
      # plot map
      m = Basemap(lon_0=180,ax=ax)
      m.drawcoastlines(linewidth=1,color="k")
      m.drawparallels(np.arange(-90,90,20), labels=[1,1,0,1])
      m.drawmeridians(np.arange(-180,180,40), labels=[1,1,0,1])
      # gaussian lattitudes
      lats, bonds = gaussian_latitudes(int(float(self.nlat)/2.))
      lats = np.asarray(lats)
      # longitudes
      lons = np.linspace(0,360,self.nlon,endpoint=False)
      X,Y = np.meshgrid(lons,lats)
      x,y = m(X,Y)

      # statistics
      vmax = np.max(np.amax(data,axis=0))
      vmin = np.min(np.amin(data,axis=0))
      mean = np.mean(data)
      std  = np.std(data)
      self.info_str = 'max/min/avg/std = %e %e %e %e' % (vmax,vmin,mean,std)
      self.label1['text'] = self.info_str
      self.label1['fg'] = 'black'

      range = vmax
      if vmin > vmax:
        range = vmin
      # plot countourf
      #im = ax.contourf(x, y, data, 10, cmap='RdBu', vmin=vmin, vmax=vmax)
      im = ax.contourf(x, y, data, 200, cmap='seismic', vmin=-range, vmax=range)
      label = self.labels[1]+' - '+self.labels[0]
      plt.title(label,fontsize='large',fontweight='bold')
      plt.suptitle('%s Difference \n%s  %s  - valid at %s' % (self.var_substr,self.title_substr,self.fcst_substr,self.vdate_substr),fontsize='x-large',fontweight='bold')
      cbar_ax = fig.add_axes([0.15, 0.05, 0.7, 0.02 ])
      plt.colorbar(im, cax=cbar_ax, orientation='horizontal')
      
      self.progressbar_var.set(self.progressbar_var.get()+10)
      self.update()

      return fig, ax, m
    
    
    def read_records(self,format,f):
      record_struct = Struct(format)
      chunks = iter(lambda : f.read(record_struct.size),b'')
      return (record_struct.unpack(chunk) for chunk in chunks)
    
    def read_dms(self,filename):
      tmp = []
      with open(filename,'rb') as f:
        for rec, in self.read_records('>d',f):
          tmp.append(rec) 
      df = pd.DataFrame(tmp)
      return df
    
    def get_field(self,data_base,data_name,data_dir):
      df = []
      tmp = []
      for adate in pd.date_range(self.bdate,self.edate,freq='6H'):
          adate = str(adate.to_pydatetime().strftime("%Y%m%d%H"))
          data_time = adate + '00' + "%4.4d" % int(self.fcst)     # experiment date
          #data_dir = 'MASOPS'
          filename = data_base +'/'+ data_dir + '/' + data_time + '/' + data_name
    
          # continue if time does not exist
          if not os.path.exists(filename):
            print('\033[1;31m' + '%s does not exist' % filename + '\033[1;m')
            self.label1['text'] = '%s does not exist' % filename
            self.label1['fg'] = 'red'
            self.filenotexist = True
            continue
          else:
            self.label1['text'] = '%s does exist' % filename
            self.label1['fg'] = 'blue'
            self.filenotexist = False
    
          # get data
          df = self.read_dms(filename)
          tmp.append(df)
   
      if os.path.exists(filename): 
        df = pd.concat(tmp,axis=1).mean(axis=1)
    
      return df

    def var_select(self,value):
       self.var.set(value)

    def lev_select(self,value):
       self.lev.set(value)

    def tau_select(self,value):
       self.tau.set(value)

    def save_cookies(self):
       data = {
                'dbpath'  : self.dbpath.get(),
                'dbname'  : self.dbname.get(),
                'dmsfile' : self.dmsfile.get(),
                'dtg'     : self.dtg.get(),
                'dmsflag' : self.dmsflag.get(),
                'var'     : self.var.get(),
                'lev'     : self.lev.get(),
                'tau'     : self.tau.get(),
       }
       with open(self.cookie, 'w') as f:
           json.dump(data, f)

    def show_figure(self): 
        if Path(self.figname).is_file():
          self.image = ImageTk.PhotoImage(Image.open(self.figname))
          self.canvas.create_image(0,0, anchor='nw', image=self.image)
          self.canvas.image = self.image
        else:
          self.canvas.create_text(500,300,anchor='center', font="Times 20 italic bold",text="Click the plot buttom to plot figure.") 
       
        self.progressbar_var.set(100)
        self.update()

    def _on_mousewheel(self, event):
      self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def createWidgets(self, master):

        # clean prvious figure if existing 
        self.figname = str(Path.home())+'/.gddt.png'
        if Path(self.figname).is_file():
          os.remove(self.figname)

        # save cookie for next time defaluts settings
        self.cookie = str(Path.home())+'/.gddtrc'
        if Path(self.cookie).is_file():
          with open(self.cookie, 'r') as f:
            _data = json.load(f)
        else:
          _data = {
                'dbpath'  : "/nwp/ncsagfs/.DMSDATA",
                'dbname'  : "NWPDB",
                'dmsfile' : "MASOPS",
                'dtg'     : (datetime.utcnow()+relativedelta(hours=-6)).strftime('%Y%m%d00'),
                'dmsflag' : "GH0G",
                'var'     : "Variables",
                'lev'     : "Levels",
                'tau'     : "Forecast hours",
          }

        # Title label
        self.label = tk.Label(master, text='Welcome ! This is Global DMS Display Tool.', font=("Helvetica", "20") )
        self.label.grid(row=0, column=0, columnspan=20, sticky="EW")

        # optioins 
        self.label1 = tk.Label(master, text="DMS DB PATH :")
        self.label1.grid(row=1, column=1, columnspan=3, sticky="E")
        self.dbpath = tk.StringVar(master)
        self.dbpath.set(_data['dbpath'])
        self.entry = tk.Entry(master, textvariable=self.dbpath)
        self.entry.grid(row=1, column=4, columnspan=12, sticky="WE")

        self.button = tk.Button(master, text="Quit", command=root.quit, bg = 'gray', fg = 'white')
        self.button.grid(row=1, column=17, columnspan=2, sticky='EW') 

        self.label1 = tk.Label(master, text="DMS DB NAME :")
        self.label1.grid(row=2, column=1, columnspan=3, sticky="E")
        self.dbname = tk.StringVar(master)
        self.dbname.set(_data['dbname'])
        self.entry = tk.Entry(master, textvariable=self.dbname)
        self.entry.grid(row=2, column=4, columnspan=4, sticky="WE")

        self.label1 = tk.Label(master, text="DMS FILE NAME :")
        self.label1.grid(row=2, column=9, columnspan=3, sticky="E")
        self.dmsfile = tk.StringVar(master)
        self.dmsfile.set(_data['dmsfile'])
        self.entry = tk.Entry(master, textvariable=self.dmsfile)
        self.entry.grid(row=2, column=12, columnspan=4, sticky="WE")

        self.label1 = tk.Label(master, text="DATE TIME :")
        self.label1.grid(row=3, column=1, columnspan=3, sticky="E")
        self.dtg = tk.StringVar(master)
        self.dtg.set(_data['dtg'])
        self.entry = tk.Entry(master, textvariable=self.dtg)
        self.entry.grid(row=3, column=4, columnspan=4, sticky="WE")

        self.label1 = tk.Label(master, text="DMS FLAG :")
        self.label1.grid(row=3, column=9, columnspan=3, sticky="E")
        self.dmsflag = tk.StringVar(master)
        self.dmsflag.set(_data['dmsflag'])
        self.entry = tk.Entry(master, textvariable=self.dmsflag)
        self.entry.grid(row=3, column=12, columnspan=4, sticky="WE")

        # for variables 
        self.optionList = cwbgfs_dmsvar_dict.keys()
        
        self.var = tk.StringVar(master)
        self.var.set(_data['var'])
        self.optionmenu = tk.OptionMenu(master, self.var, *self.optionList, command=self.var_select)
        self.optionmenu.grid(row=4, column=1, columnspan=4, sticky='EW')
              
        # for pressure levels
        self.optionList = ("10 hPa","20 hPa","30 hPa","50 hPa",
                           "100 hPa","200 hPa","300 hPa","400 hPa",
                           "500 hPa","600 hPa","700 hPa","850 hPa",
                           "1000 hPa")
        self.lev = tk.StringVar()
        self.lev.set(_data['lev'])
        self.optionmenu = tk.OptionMenu(master, self.lev, *self.optionList, command=self.lev_select)
        self.optionmenu.grid(row=4, column=6, columnspan=2, sticky='EW')

        # for forecast hours
        self.optionList = ( "Analysis","6 hours","12 hours","18 hours","24 hours","30 hours","36 hours","42 hours","48 hours",
                            "54 hours","60 hours","66 hours","72 hours","84 hours","96 hours","108 hours","120 hours",
                            "132 hours","144 hours","156 hours","168 hours","180 hours","192 hours","204 hours","216 hours")
        self.tau = tk.StringVar(master)
        self.tau.set(_data['tau'])
        self.optionmenu = tk.OptionMenu(master, self.tau, *self.optionList, command=self.tau_select)
        self.optionmenu.grid(row=5, column=1, columnspan=4, sticky='EW')
  
        # for sigma levels
        self.spinbox = tk.Spinbox(master, from_= 1, to = 72)
        self.spinbox.grid(row=5, column=6, columnspan=2, sticky="EW")

        # the swicher for vertical coordinate        
        self.vcoor = tk.StringVar()
        self.radiobutton = tk.Radiobutton(master, text='Pressure Level',variable=self.vcoor, value='0G')
        self.radiobutton.grid(row=4, column=8, columnspan=2, sticky="W")
        self.radiobutton.invoke()
        self.radiobutton = tk.Radiobutton(master, text='Sigma Level',variable=self.vcoor, value='MG')
        self.radiobutton.grid(row=5, column=8, columnspan=2, sticky="W")

        # option for ploting difference
        self.diff = tk.IntVar()
        self.checkbutton = tk.Checkbutton(master, text='Difference', variable=self.diff, onvalue=1, offvalue=0)
        self.checkbutton.grid(row=4, column=17, columnspan=2, sticky="NWS")

        # option for ploting contours
        self.contour = tk.IntVar()
        self.checkbutton = tk.Checkbutton(master, text='Contours', variable=self.contour, onvalue=1, offvalue=0)
        self.checkbutton.grid(row=3, column=17, columnspan=2, sticky="NWS")

        # option for looping over the forecast time 
        self.loop = tk.IntVar()
        self.checkbutton = tk.Checkbutton(master, text='Looping', variable=self.loop, onvalue=1, offvalue=0)
        self.checkbutton.grid(row=2, column=17, columnspan=2, sticky="NWS")

        # the main triger for ploting action 
        self.button = tk.Button(master, text="plot", command=self.clickPlot, bg= 'gray', fg = 'white')
        self.button.grid(row=5, column=17, columnspan=2, sticky='NEWS') 

        # option for auto fit
        self.selfmaxmin = tk.IntVar()
        self.checkbutton = tk.Checkbutton(master, text='Max/Min :', variable=self.selfmaxmin, onvalue=1, offvalue=0)
        self.checkbutton.grid(row=4, column=10, columnspan=2, sticky="NES")

        self.maxmin = tk.StringVar(master)
        self.maxmin.set('max,min') 
        self.entry = tk.Entry(master, textvariable=self.maxmin)
        self.entry.grid(row=4, column=12, columnspan=2, sticky="WE")

        # footage 
        self.info_str = 'Copyright © 2018 Deng-Shun Chen. All rights reserved'
        self.label1 = tk.Label(master, text=self.info_str)
        self.label1.grid(row=7, column=0, columnspan=20, sticky='WE')

        # progressbar 
        self.progressbar_var = tk.IntVar()
        self.progressbar = ttk.Progressbar(master, mode='determinate', orient=tk.HORIZONTAL, maximum=100, value=0, variable=self.progressbar_var)
        self.progressbar.grid(row=8, column=0, columnspan=20, sticky='WE')

        # figure display frame 
        self.frame_canvas = tk.Frame(master)
        self.frame_canvas.grid(row=6, column=0, columnspan=20, sticky='NEWS')
        self.frame_canvas.columnconfigure(0, weight=1)
        self.frame_canvas.rowconfigure(0, weight=1)

        # canvas 
        self.canvas = tk.Canvas(self.frame_canvas, width = 1000, height = 600)
        self.canvas.grid(row=0, column=0, sticky='news')

        # scrollbar
        self.vbar = tk.Scrollbar(self.frame_canvas, orient="vertical", command=self.canvas.yview)
        self.vbar.grid(row=0, column=1, sticky='ns')
        self.canvas.configure(yscrollcommand=self.vbar.set)

        if OS == "Linux" :
            self.canvas.bind_all('<4>', self._on_mousewheel)
            self.canvas.bind_all('<5>', self._on_mousewheel)
        else:
            # Windows and MacOS
            self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
 
        # show figure
        self.show_figure()


if __name__ == '__main__':     
        
  # start up the app.
  root = tk.Tk()
  app = Application(root)
  root.mainloop()

  # remove previous figure file
  if Path(app.figname).is_file():
    os.remove(app.figname)


