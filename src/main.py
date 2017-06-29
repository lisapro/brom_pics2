#!/usr/bin/python
# -*- coding: utf-8 -*-

# this comment is important to have 
# at the very first line 
# to use unicode 

'''
Created on 14. des. 2016

@author: E.Protsenko
'''

import math
import os,sys
import numpy as np
from netCDF4 import Dataset,num2date
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QSpinBox,QLabel,QComboBox,QCheckBox

from matplotlib import rc, style
from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas)
from matplotlib.backends.backend_qt4agg import (
    NavigationToolbar2QT as NavigationToolbar)
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotlib.gridspec as gridspec
import matplotlib.dates as mdates

import readdata

class Window(QtGui.QDialog):
    #QDialog - the base class of dialog windows.Inherits QWidget.
    #QMainWindow - 
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        # function to display the names of the window flags        
        # Qt.Window Indicates that the widget is a window, 
        # usually with a window system frame and a title bar
        # ! it is not possible to unset this flag if the widget 
        # does not have a parent.
        
        self.setWindowFlags(QtCore.Qt.Window)   
        self.setWindowTitle("BROM Pictures")
        self.setWindowIcon(QtGui.QIcon('bromlogo2.png'))
              
        self.figure = plt.figure(figsize=(11.69 , 8.27), dpi=100,
                                  facecolor='white') 

        #for unicode text     
        rc('font', **{'sans-serif' : 'Arial', 
                           'family' : 'sans-serif'})  
        rc({'savefig.transparent' : True})
                
        # open file system to choose needed nc file 
        self.fname = str(QtGui.QFileDialog.getOpenFileName(self,
        'Open netcdf ', os.getcwd(), "netcdf (*.nc);; all (*)")) 
          
        totitle = os.path.split(self.fname)[1]
        
        self.totitle = totitle[16:-3]

        
        #filename = self.fname
        self.fh =  Dataset(self.fname)
        self.time =  self.fh.variables['time'][:]
        self.lentime = len(self.time)          
        self.time_units = self.fh.variables['time'].units
        #time_calendar = self.fh.variables['time'].calendar
        #print (time_calendar)
        self.dates = num2date(self.time[:],
                              units= self.time_units)                
        
        #time = dates 

            
        #readdata.readdata_brom(self)           
      
         
              
        # Create widgets
        self.label_choose_var = QtGui.QLabel('Choose variable:')                   
        self.time_prof_box = QtGui.QComboBox()  
        self.qlistwidget = QtGui.QListWidget()      
        self.qlistwidget.setSelectionMode(
            QtGui.QAbstractItemView.ExtendedSelection)

           
                           
        self.dist_prof_button = QtGui.QPushButton() 
        self.scale_all_axes = QtGui.QCheckBox(
            "scale:all columns, all time") 
         
        #self.dist_prof_checkbox = QtGui.QCheckBox(
        #self.choose_scale = QtGui.QComboBox() 
                
        self.yearlines_checkbox = QtGui.QCheckBox(
            'Draw year lines')   
        
        self.datescale_checkbox = QtGui.QCheckBox(
            'Format time axis')   
        #self.injlines_checkbox = QtGui.QCheckBox(
        #    'Draw inject lines')   
            

                  
        self.time_prof_last_year =  QtGui.QPushButton()    
        self.time_prof_all =  QtGui.QPushButton()                   
        self.all_year_test_button =  QtGui.QPushButton()               
        self.numcol_2d = QtGui.QSpinBox()        
            
        self.numday_box = QtGui.QSpinBox() 
        self.numday_stop_box = QtGui.QSpinBox()        
        self.textbox = QtGui.QLineEdit()  
        self.textbox2 = QtGui.QLineEdit()           
        self.fick_box = QtGui.QPushButton() 
        self.help_button = QtGui.QPushButton('? Help')
        
        #w.show()
        #item.setCheckable(True)
        #item_scale_all_column.setCheckState(QtCore.Qt.Unchecked)

        # add items to Combobox        
        #for i in self.var_names_charts_year:
        #    self.all_year_1d_box.addItem(str(i))
        
        '''
        # currentIndex() == 0 
        self.choose_scale.addItem('Scale: All days, 1 column')
        # currentIndex() == 1 
        self.choose_scale.addItem('Scale: 1 day, all columns') 
        # currentIndex() == 2 
        self.choose_scale.addItem('Scale: All days, all columns') '''
        
        ## self.time_prof_box.addItem('plot 1D')  
        ## add only 2d arrays to variables list       
        ## We skip z and time since they are 1d array, 
        ## we need to know the shape of other arrays
        ## If the file includes other 1d var, it 
        ## could raise an err, such var should be skipped also
        
        self.names_vars = [] 
        for names,vars in self.fh.variables.items():
            if names == 'z' or names == 'z2' : 
                self.names_vars.append(names)
            elif names == 'time' or names == 'i' : 
                self.names_vars.append(names) 
            else :
                self.time_prof_box.addItem(names)
                self.names_vars.append(names)  
                
        if 'i' in self.names_vars: 
            self.dist = np.array(self.fh.variables['i'])          
        # sort variables alpahabetically non-case sensitive        
        self.sorted_names =  sorted(self.names_vars, key=lambda s: s.lower())  
        self.qlistwidget.addItems(self.sorted_names)
        
                     
        #read i variable to know number of columns 
        for names,vars in self.fh.variables.items():
            if names == 'z' or names == 'z2' : 
                pass
            elif names == 'time': # or names == 'i' : 
                pass 
            else :
                if 'i' in self.names_vars:
                    #print ("we try")
                    testvar = np.array(self.fh['i'][:])      
                    break  
                
        self.fh.close()  
                
   
        
        self.label_maxday = QtGui.QLabel('max day: '+ str(self.lentime))
        

        if 'i' in self.names_vars:  
            self.textbox.setText(
                'Number of columns = {}'.format(str(
                testvar.shape[0])))                        
            self.numcol_2d.setRange(0, int(testvar.shape[0]-1))
               
            self.numday_box.setRange(0, self.lentime-1)  
            
            self.numday_stop_box.setRange(0, self.lentime-1)             
            self.numday_stop_box.setValue(self.lentime-1)
            
        # Define connection between clicking the button and 
        # calling the function to plot figures         
                          
        #self.all_year_1d_box.currentIndexChanged.connect(
        #    self.all_year_charts)                   
        #self.numcol_2d.valueChanged.connect(
        #    self.time_profile) 
        
        self.time_prof_last_year.released.connect(self.call_print_lyr)
        self.all_year_test_button.released.connect(self.all_year_test)
        self.time_prof_all.released.connect(self.call_print_allyr)        
        self.fick_box.released.connect(self.fluxes)        
        self.dist_prof_button.released.connect(self.dist_profile)           
        
        
        #self.buttonBox.released.connect(self.setPenProperties) 
        #self.help_button.released.connect(self.save_figure)

        # Create widget 2         
        self.all_year_box = QtGui.QComboBox()
        
        # add items to Combobox         
        self.time_prof_all.setText('Time: all year')
        self.fick_box.setText('Fluxes SWI')
        self.all_year_test_button.setText('1D plot')
        self.time_prof_last_year.setText('Time: last year')               
        self.dist_prof_button.setText('Show Dist Profile')       
                         
        self.canvas = FigureCanvas(self.figure)    
        self.toolbar = NavigationToolbar(self.canvas, self) #, self.qfigWidget
        #self.canvas.setMinimumSize(self.canvas.size())
        
        ## The QGridLayout class lays out widgets in a grid          
        self.grid = QtGui.QGridLayout(self)
        
        readdata.widget_layout(self)        
        readdata.readdata2_brom(self,self.fname)   
                 
        if 'Kz'  in self.names_vars :
            readdata.calculate_ywat(self)
            readdata.calculate_ybbl(self)   
            readdata.y2max_fill_water(self)        
            readdata.depth_sed(self)
            readdata.calculate_ysed(self)
            readdata.calculate_ysed(self)
            readdata.calc_nysedmin(self)  
            readdata.y_coords(self)        
        else: 
            self.sediment = False
   
        
        readdata.colors(self)
        readdata.set_widget_styles(self) 
        
  
        self.num = 50. 
        self.dialog = QtGui.QDialog
        
    def fluxes(self): 
        plt.clf()     
        try:
            index = str(self.qlistwidget.currentItem().text())
        except AttributeError:       
            messagebox = QtGui.QMessageBox.about(
                self, "Retry",'Choose variable,please') 
            return None           
        numcol = self.numcol_2d.value() # 
        start = self.numday_box.value() 
        stop = self.numday_stop_box.value() 
        selected_items = self.qlistwidget.selectedItems()
        
        tosed = '#d3b886'
        towater = "#c9ecfd" 
        linecolor = "#1da181" 
        var1 = str(selected_items[0].text())
        
        z = np.array(self.fh.variables[var1])
        z_units = self.fh.variables[var1].units
        
        zz =  z[:,:,numcol] #1column
        
        if len(selected_items)== 1:
            
            #print (zz.shape)
            gs = gridspec.GridSpec(1,1)
            ax00 = self.figure.add_subplot(gs[0])
            ax00.set_xlabel('Julian day')   
            if self.yearlines_checkbox.isChecked() == True:
                for n in range(start,stop):
                    if n%365 == 0: 
                        ax00.axvline(n,
                        color='black',
                        linestyle = '--') 
            #if self.injlines_checkbox.isChecked()== True: 
            #        ax00.axvline(365,color='red', linewidth = 2,
            #                linestyle = '--',zorder = 10) 
            #        ax00.axvline(730,color='red',linewidth = 2,#1825 730
            #                linestyle = '--',zorder = 10)                            
        elif len(selected_items)== 2:
            gs = gridspec.GridSpec(2,1)
            
            ax00 = self.figure.add_subplot(gs[0])
            ax01 = self.figure.add_subplot(gs[1])
            ax01.set_xlabel('Julian day')  
            if self.yearlines_checkbox.isChecked() == True:
                for n in range(start,stop):
                    if n%365 == 0: 
                        ax00.axvline(n,color='black',
                        linestyle = '--') 
                        ax01.axvline(n,color='black',
                        linestyle = '--') 
                # injection   
            if self.injlines_checkbox.isChecked()== True: 
                    ax00.axvline(365,color='red', linewidth = 2,
                            linestyle = '--',zorder = 10) 
                    ax00.axvline(730,color='red',linewidth = 2,#1825 730
                            linestyle = '--',zorder = 10)  
                      
                    ax01.axvline(365,color='red', linewidth = 2,
                            linestyle = '--',zorder = 10) 
                    ax01.axvline(730,color='red',linewidth = 2,
                            linestyle = '--',zorder = 10)    
                                                                       
            #print (str(selected_items[1].text()))
            var2 = str(selected_items[1].text())
            z2_units = self.fh.variables[var2].units
            z2 = np.array(self.fh.variables[str(selected_items[1].text())])
            zz2 =  z2[:,:,numcol] #1column
            ax01.set_title(var2+', '+ z2_units)
            ax01.set_ylabel('Fluxes') #Label y axis
            ax01.set_xlim(start,stop)
            ax01.axhline(0, color='black', linestyle = '--') 
            fick2 = []
            for n in range(start,stop): 
                # take values for fluxes at sed-vat interf
                fick2.append(zz2[n][self.nysedmin])   
            fick2 = np.array(fick2)     
            ax01.plot(self.time[start:stop],fick2, linewidth = 1 ,
                        color = linecolor, zorder = 10)  
            #if self.yearlines_checkbox.isChecked() == True:
            #    for n in range(start,stop):
            #        if n%365 == 0: 
            #            ax01.axvline(n,
            #            color='black', linestyle = '--')      
            ax01.fill_between(self.time[start:stop], fick2, 0,
                               where= fick2 >= 0. , 
                               color = tosed, label= u"down" )
            ax01.fill_between(self.time[start:stop],  fick2, 0 ,
                          where= fick2 < 0.,color = towater, label=u"up")            
            ax01.set_ylim(max(fick2),min(fick2)) 
        else : 
            messagebox = QtGui.QMessageBox.about(
                self, "Retry",'Choose 1 or 2 variables,please') 
            return None  
        
        
        ax00.set_title(var1+', '+ z_units )
        
        self.figure.suptitle(str(self.totitle),fontsize=16)
        #                , fontweight='bold')
        #print (z_units, var1)
        ax00.set_ylabel('Fluxes') #Label y axis
        
        #ax00.text(0, 0, 'column{}'.format(numcol), style='italic')
        #bbox={'facecolor':'red', 'alpha':0.5,'pad':10}
        fick = []
        for n in range(start,stop): 
            # take values for fluxes at sed-vat interf
            fick.append(zz[n][self.nysedmin])
        fick = np.array(fick) 
        ax00.set_xlim(start,stop)
        ax00.axhline(0, color='black', linestyle = '--') 

        ax00.plot(self.time[start:stop],fick, linewidth = 1 ,
                  color = linecolor, zorder = 10)  

        ax00.fill_between(self.time[start:stop],fick,0,
                          where = fick >=0, color = tosed, label= u"down" )
        ax00.fill_between(self.time[start:stop],  fick, 0 ,
                          where= fick < 0.,color = towater, label=u"up")
        ax00.set_ylim(max(fick),min(fick)) 
        #                  where = fick > 0 ,
        #                  , interpolate=True) 
        
        #ax.fill_between(x, y1, y2, where=y2 >= y1,
        # facecolor='green', interpolate=True)         
        #rc({'savefig.transparent' : True})
        self.canvas.draw()
              
    def time_profile(self,start,stop):
        
        plt.clf()
            
        try:
            index = str(self.qlistwidget.currentItem().text())
        except AttributeError:   
            messagebox = QtGui.QMessageBox.about(self, "Retry",
                                                 'Choose variable,please') 
            return None           
        
        ## read chosen variable 
        
        z = np.array(self.fh.variables[index]) 
        # take the value of data units for the title
        data_units = self.fh.variables[index].units
        
        z = z[start:stop] 
        ylen1 = len(self.depth) #95  

        x = np.array(self.time[start:stop]) 

        xlen = len(x)     

        # check if the variable is defined on middlepoints  
        if (z.shape[1])> ylen1: 
            y = self.depth2
            if self.sediment != False:
                #print ('in sed1')                
                y_sed = np.array(self.depth_sed2) 
        elif (z.shape[1]) == ylen1:
            y = self.depth #pass
            if self.sediment != False:
                #print ('in sed1')                
                y_sed = np.array(self.depth_sed) 
        else :
            print ("wrong depth array size") 

        ylen = len(y)           

        z2d = []
        # check wich column to plot 
        numcol = self.numcol_2d.value() # 

        
        if 'i' in self.names_vars:
            # check if we have 2D array 
            if z.shape[2] > 1:
                for n in range(0,xlen): #xlen
                    for m in range(0,ylen):  
                        # take only n's column for brom             
                        z2d.append(z[n][m][numcol]) 
      
                z = np.array(z2d)                     
        z = z.flatten()   
        z = z.reshape(xlen,ylen)       
        zz = z.T  
            
        if 'Kz' in self.names_vars and index != 'pH':
            watmin = readdata.varmin(self,zz,'wattime',start,stop) 
            watmax = readdata.varmax(self,zz,'wattime',start,stop)
            #wat_ticks = readdata.ticks(watmin,watmax) 
           
        elif 'Kz'in self.names_vars and index == 'pH':
            
            # take the value with two decimanl places 
            watmin = round(zz[0:self.ny1max,:].min(),2) 
            watmax = round(zz[0:self.ny1max,:].max(),2) 
            wat_ticks = np.linspace(watmin,watmax,5)    
            wat_ticks = (np.floor(wat_ticks*100)/100.)   
        # if we do not have kz     
        else:  
            self.ny1max = len(self.depth-1)
            self.y1max = max(self.depth)    
            watmin = readdata.varmin(self,zz,'wattime',start,stop) #0 - water 
            watmax = readdata.varmax(self,zz,'wattime',start,stop)
            
        #if #self.choose_scale.currentIndex() == 2:
        if self.scale_all_axes.isChecked(): 
            z_all_columns = np.array(self.fh.variables[index])  
            #print(z_all_columns.shape)
            watmin = round((z_all_columns[start:stop,0:self.ny1max,:].min()),2) 
            watmax = round((z_all_columns[start:stop,0:self.ny1max,:].max()),2) 
            
        wat_ticks = np.linspace(watmin,watmax,5)         
        #wat_ticks = readdata.ticks(watmin,watmax)   
        wat_ticks = (np.floor(wat_ticks*100)/100.)               
        
        if self.sediment == False: 
            gs = gridspec.GridSpec(1, 1) 
            gs.update(left = 0.07,right = 0.9 )
            cax = self.figure.add_axes([0.92, 0.1, 0.02, 0.8])  
        else : 
                             
            gs = gridspec.GridSpec(2, 1) 
            gs.update(left = 0.07,right = 0.9 )
             

            X_sed,Y_sed = np.meshgrid(x,y_sed)
            
            if self.datescale_checkbox.isChecked() == True:
                
                self.format_time = num2date(X_sed,
                                             units= self.time_units)   
                X_sed = self.format_time
            
            ax2 = self.figure.add_subplot(gs[1])  


            if self.scale_all_axes.isChecked(): 
                #z_all_columns = np.array(self.fh.variables[index])  
                #print(z_all_columns.shape)
                sed_min  = round((
                    z_all_columns[start:stop,self.nysedmin-2:,:].min()),2) 
                sed_max = round((
                    z_all_columns[start:stop,self.nysedmin-2:,:].max()),2) 
                sed_ticks = readdata.ticks(sed_min,sed_max)
            else :
                sed_min = readdata.varmin(self,zz,'sedtime',start,stop)
                sed_max = readdata.varmax(self,zz,'sedtime',start,stop)     
                sed_ticks = readdata.ticks(sed_min,sed_max)
                            
            if index == 'pH': 
                sed_min  = (zz[self.nysedmin-2:,:].min()) 
                sed_max  = (zz[self.nysedmin-2:,:].max())                 
                sed_ticks = readdata.ticks(sed_min,sed_max) 
                sed_ticks = (np.floor(sed_ticks*100)/100.)                
   
                   
            ax2.set_ylabel('h, cm',fontsize= self.font_txt) 
            ax2.set_xlabel('Number of day',fontsize= self.font_txt)  
                               
            sed_levs = np.linspace(sed_min,sed_max,
                                 num = self.num) 
            ax2.set_ylim(self.ysedmax,self.ysedmin) #ysedmin
            #ax2.set_xlim(start,stop)


            
                       
            #print (self.dates)
            #x = self.dates

            #   x = self.dates
            #print (self.dates, x )
            #calendar= time_calendar)
            #self.time = self.dates 
 
            #print (X_sed[0])
            CS1 = ax2.contourf(X_sed,Y_sed, zz, levels = sed_levs, #int_
            
                              extend="both", cmap= self.cmap1)
            
            if self.datescale_checkbox.isChecked() == True: 
                if len(x) > 365:
                    ax2.xaxis_date()
                    ax2.xaxis.set_major_formatter(
                        mdates.DateFormatter('%m/%Y'))  
                else : 
                    ax2.xaxis_date()
                    ax2.xaxis.set_major_formatter(
                        mdates.DateFormatter('%d/%m'))                                 
            
            # Add an axes at position rect [left, bottom, width, height]                    
            cax1 = self.figure.add_axes([0.92, 0.1, 0.02, 0.35])
            

            ax2.axhline(0, color='white', linestyle = '--',linewidth = 1 )        
            cb_sed = plt.colorbar(CS1,cax = cax1)
            cb_sed.set_ticks(sed_ticks)   
              
            
  
     
               
            #cb.set_label('Water')   
            cax = self.figure.add_axes([0.92, 0.53, 0.02, 0.35])      
                 
            #if self.yearlines_checkbox.isChecked() == True:
            #    for n in range(start,stop):
            #        if n%365 == 0: 
            #            ax2.axvline(n, color='white', linestyle = '--') 
                        
                      
                        
            #if self.injlines_checkbox.isChecked()== True:             
            #    ax2.axvline(365,color='red', linewidth = 2,
            #            linestyle = '--',zorder = 10) 
            #    ax2.axvline(730,color='red',linewidth = 2,
            #            linestyle = '--',zorder = 10)                       
                                                                   
        X,Y = np.meshgrid(x,y)  
        ax = self.figure.add_subplot(gs[0])
        
        if self.datescale_checkbox.isChecked() == True: 
            X = self.format_time     
                          
        
         

        if watmin == watmax :
            if watmax == 0: 
                watmax = 0.1
                watmin = 0
            else:      
                watmax = watmax + watmax/10.
                 
        if self.sediment != False:        
            if sed_min == sed_max: 
                if sed_max == 0: 
                    sed_max = 0.1
                    sed_min = 0
                else:     
                    sed_max = sed_max + sed_max/10.   
             
        self.ny1min = min(self.depth)
        #ax.set_title(index)
        
        ax.set_title(index + ', ' + data_units) 
        ax.set_ylim(self.y1max,self.ny1min)   

        ax.set_ylabel('h, m',fontsize= self.font_txt)
         
        wat_levs = np.linspace(watmin,watmax,num= self.num)
                                
        ## contourf() draws contour lines and filled contours
        ## levels = A list of floating point numbers indicating 
        ## the level curves to draw, in increasing order    
        ## If None, the first value of Z will correspond to the lower
        ## left corner, location (0,0).  
        ## If â€˜imageâ€™, the rc value for image.origin will be used.
          
        CS = ax.contourf(X,Y, zz, levels = wat_levs, extend="both", #int_
                              cmap= self.cmap)

        
        if self.datescale_checkbox.isChecked() == True: 
            if len(x) > 365:
                ax.xaxis_date()
                ax.xaxis.set_major_formatter(
                    mdates.DateFormatter('%m/%Y'))  
                 
            else : 
                ax.xaxis_date()
                ax.xaxis.set_major_formatter(
                    mdates.DateFormatter('%d/%m'))     
                      
        cb = plt.colorbar(CS,cax = cax)   #, ticks = wat_ticks   
        cb.set_ticks(wat_ticks)
        

                    # 730ection  
        #if self.injlines_checkbox.isChecked() == True:                  
        #    ax.axvline(365,color='red', linewidth = 2,
        #                linestyle = '--',zorder = 10) 
        #    ax.axvline(730,color='red',linewidth = 2,
        #                linestyle = '--',zorder = 10)      
                            
        #self.figure.suptitle(str(self.totitle),fontsize=16)            
        self.canvas.draw()
        
        
        
        # Attempt to make timer for updating 
        # the datafile, while model is running 
        # still does not work 
        
        #timer = QtCore.QTimer(self)
        #timer.timeout.connect(self.update_all_year)
        #timer.start(20000) 
        
        #timer.timeout.connect(test) #(self.call_print_allyr)
        #timer.start(1)
        #QtCore.QTimer.connect(timer, QtCore.SIGNAL("timeout()"), self, QtCore.SLOT("func()"))
        
        #QtCore.QTimer.singleShot(1000, self.updateCost())   
     
             
    ## function to plot figure where 
    ## xaxis - is horizontal distance between columns
    ## yaxis is depth 
    
    def dist_profile(self): 
        plt.clf()
        try:
            index = str(self.qlistwidget.currentItem().text())
        except AttributeError: 
            print ("Choose the variable to print ")        
            messagebox = QtGui.QMessageBox.about(
                self, "Retry", 'Choose variable,please') 
            return None            
        
           
            #os.system("pause")
        #index = str(self.time_prof_box.currentText())
        numday = self.numday_box.value()  
        #z = np.array(self.fh.variables[index]) 
        data = np.array(self.fh.variables[index])
        data_units = self.fh.variables[index].units
        ylen = len(self.depth)        
        xlen = len(self.dist)  

        # for some variables defined at grid middlepoints
        # kz and fluxes 
        if (data.shape[1])> ylen:
            y = self.depth2 # = np.array(self.fh.variables['z2'][:])   
            if self.sediment != False:
                #print ('in sed2')
                y_sed = np.array(self.depth_sed2) 
        elif (data.shape[1]) == ylen :
            y = self.depth 
            if self.sediment != False:
                #print ('in sed1')                
                y_sed = np.array(self.depth_sed)            
        else :
            print ("wrong depth array size") 
        
        ylen = len(y) 

            
        z2d = []
        if data.shape[2] > 1: 
            for n in range(0,xlen): # distance 
                for m in range(0,ylen):  # depth 
                    # take only n's column for brom             
                    z2d.append(data[numday][m][n])                     
            
            z2 = np.array(z2d).flatten() 
            #z = z2  
            z2 = z2.reshape(xlen,ylen)       
            zz = z2.T   
                        


            if self.scale_all_axes.isChecked():                      
                start = self.numday_box.value() 
                stop = self.numday_stop_box.value() 
                print (start,stop)  
            else : # self.dist_prof_checkbox.isChecked() == True:
                start = numday
                stop = numday+1 
                print (start,stop)    
                           
            #if index == 'pH':
            watmin = round(
                data[start:stop,0:self.ny1max].min(),2)
            watmax = round(
                data[start:stop,0:self.ny1max].max(),2) 
            wat_ticks = np.linspace(watmin,watmax,5)
            wat_ticks = (np.floor(wat_ticks*100)/100.)
            
            #else :          
            #    watmin = readdata.varmin(self,data,'watdist',start,stop) 
            #    watmax = readdata.varmax(self,data,'watdist',start,stop)             
            #    wat_ticks = readdata.ticks(watmin,watmax) 
            
            if self.sediment == False:                                 
                gs = gridspec.GridSpec(1, 1)                        
                cax = self.figure.add_axes([0.92, 0.1, 0.02, 0.8])                  
                # cb = plt.colorbar(CS,cax = cax,ticks = wat_ticks)        
                # new comment       
                              
            else :  
                gs = gridspec.GridSpec(2, 1)         
                
                X_sed,Y_sed = np.meshgrid(self.dist,y_sed)                       
                ax2 = self.figure.add_subplot(gs[1])
                               
                if index == 'pH':
                    sed_min = round(
                        data[start:stop,self.nysedmin:].min(),2)
                    sed_max = round(
                        data[start:stop,self.nysedmin:].max(),2)
                    sed_ticks = np.linspace(sed_min,sed_max,5)
                    sed_ticks = (np.floor(sed_ticks*100)/100.)             
                    
                else: 
                    sed_min = readdata.varmin(
                        self,data,'seddist',start,stop)
                    sed_max = readdata.varmax(
                        self,data,'seddist',start,stop)
                    
                    sed_ticks = readdata.ticks(sed_min,sed_max) 
                                
            
                sed_levs = np.linspace(sed_min,sed_max,
                                     num = self.num)            
                #int_wat_levs = []
                #int_sed_levs= []
                                        
                CS1 = ax2.contourf(X_sed,Y_sed, zz, levels = sed_levs,
                                      extend="both", cmap=self.cmap1)      
                ax2.axhline(0, color='white', linestyle = '--',
                            linewidth = 1 )                   

                ax2.set_ylim(self.ysedmax,self.ysedmin) 
                ax2.set_ylabel('h, cm',fontsize= self.font_txt)  #Depth (cm)
                ax2.set_xlabel('distance, m',fontsize= self.font_txt)   #Distance (km)  
                             
                cax1 = self.figure.add_axes([0.92, 0.1, 0.02, 0.35])
                cax = self.figure.add_axes([0.92, 0.53, 0.02, 0.35])   
                               
             
                cb1 = plt.colorbar(CS1,cax = cax1,ticks = sed_ticks)     
                cb1.set_ticks(sed_ticks)
            

            
            X,Y = np.meshgrid(self.dist,y)
            ax = self.figure.add_subplot(gs[0])  
            ax.set_title(index + ', ' + data_units) 
            ax.set_ylabel('h, m',fontsize= self.font_txt) #Depth (m)
            
            wat_levs = np.linspace(watmin,watmax, num = self.num)  
                  
            int_wat_levs = []
                    
            for n in wat_levs:
                n = readdata.int_value(self,n,watmin,watmax)
                int_wat_levs.append(n)            
    
                  
            CS = ax.contourf(X,Y, zz, levels= wat_levs, 
                                 extend="both",  cmap=self.cmap)
            
            cb = plt.colorbar(CS,cax = cax,ticks = wat_ticks)            
            cb.set_ticks(wat_ticks)   
                          
            ax.set_ylim(self.y1max,0)
              
            self.canvas.draw()
                                
                
                                                 
        else:
            messagebox = QtGui.QMessageBox.about(self, "Retry,please",
                                                 'it is 1D BROM')
            pass

        
    def call_print_lyr(self): 
        stop = len(self.time) #175
        start = stop - 365
        #print (start,stop)
        self.time_profile(start,stop) 
            
    def call_print_allyr(self):
        
        #start = min(self.dates)
        #stop = max(self.dates)
        
        start = self.numday_box.value() 
        stop = self.numday_stop_box.value()  
        #stop = len(self.time)
        #start = 0
        self.time_profile(start,stop)   
        
        
        
    def save_figure(self): 
        printer = QtGui.QPrinter(QtGui.QPrinter.HighResolution)
        printer.setPageSize(QtGui.QPrinter.A9)
        printer.setColorMode(QtGui.QPrinter.Color)
        printer.setOutputFormat(QtGui.QPrinter.PdfFormat)
        printer.setOutputFileName(self.edit.text())
        self.render(printer)
        #plt.savefig('pdf_fig.pdf',format = 'pdf')    
        #self.figure.savefig('pic.png', format='png')
    def all_year_test(self):  
        plt.clf()        
        try:
            index = str(self.qlistwidget.currentItem().text())
        except AttributeError: 
            print ("Choose the variable to print ")       
            messagebox = QtGui.QMessageBox.about(self, "Retry",
                                                 'Choose variable,please') 
            return None  
        start = self.numday_box.value() 
        stop = self.numday_stop_box.value() 
        #index = str(self.time_prof_box.currentText())
        #print ('test all year', index) 
        data_units = self.fh.variables[index].units                
        self.figure.patch.set_facecolor('white') 
        gs = gridspec.GridSpec(3,1) 
        gs.update(left=0.3, right=0.7,top = 0.94,bottom = 0.04,
                   wspace=0.2,hspace=0.3) 
        
        ax00 = self.figure.add_subplot(gs[0]) # water         
        ax10 = self.figure.add_subplot(gs[1]) # bbl
        ax20 = self.figure.add_subplot(gs[2]) # sediment 
        
        for axis in (ax00,ax10,ax20):
            axis.yaxis.grid(True,'minor')
            axis.xaxis.grid(True,'major')                
            axis.yaxis.grid(True,'major')    
                         

        numcol = self.numcol_2d.value() # 
        # read chosen variable 
        z = np.array(self.fh.variables[index])
        z = np.array(z[:,:,numcol]) 
        #print (z.shape)
        
        ax00.set_title(index +', ' + data_units) 
        #Label y axis        
        ax00.set_ylabel('h, m', #Depth (m)
                        fontsize= self.font_txt) 
        ax10.set_ylabel('h, m', #Depth (m)
                        fontsize= self.font_txt)   
        ax20.set_ylabel('h, cm', #Depth (cm)
                        fontsize= self.font_txt)
        
        ax00.set_ylim(self.y1max,0) 
        ax00.axhspan(self.y1max,0,color='#dbf0fd',
                     alpha = 0.7,label = "water" )
         
        
        ax10.set_ylim(self.y2max, self.y1max)   
        ax10.axhspan(self.y2max, self.y1max,color='#c5d8e3',
                     alpha = 0.4, label = "bbl"  )                
        
        
        ax20.set_ylim(self.ysedmax, self.ysedmin) 

        ax20.axhspan(self.ysedmin,0,
                     color='#c5d8e3',alpha = 0.4,
                     label = "bbl"  )        
        ax20.axhspan(self.ysedmax,0,
                     color='#b08b52',alpha = 0.4,
                     label = "sediment"  )
        for n in range(start,stop,10):#365
            """if (n>0 and n <60) or (n>=335 and n<365) : #"winter"
            #if n >= 0 and n<=60 or n >= 335 and n <365 : #"winter"                               
                ax00.plot(z[n][0:self.ny2max],
                      self.depth[0:self.ny2max],
                      self.wint,alpha = self.a_w, 
                      linewidth = self.linewidth , zorder = 10) 
             
                ax10.plot(z[n][0:self.ny2max],
                      self.depth[0:self.ny2max],
                      self.wint,alpha = self.a_w, 
                      linewidth = self.linewidth , zorder = 10) 
            
                ax20.plot(z[n][self.nysedmin-1:],
                      self.depth_sed[self.nysedmin-1:],
                      self.wint, alpha = self.a_w,
                      linewidth = self.linewidth, zorder = 10) """  
            #else: 
            ax00.plot(z[n][0:self.ny2max],
                  self.depth[0:self.ny2max],
                  self.spr_aut,alpha = self.a_w, 
                  linewidth = self.linewidth , zorder = 10) 

            ax10.plot(z[n][0:self.ny2max],
                  self.depth[0:self.ny2max],
                  self.spr_aut,alpha = self.a_w, 
                  linewidth = self.linewidth , zorder = 10) 
        
            ax20.plot(z[n][self.nysedmin-1:],
                  self.depth_sed[self.nysedmin-1:],
                  self.spr_aut, alpha = self.a_w,
                  linewidth = self.linewidth, zorder = 10)                          
            #ax20.scatter(z[n][self.nysedmin-1:],
            #      self.depth_sed[self.nysedmin-1:]) 
                          
        self.canvas.draw()     
    '''def all_year_charts(self): 
        #messagebox = QtGui.QMessageBox.about(self, "Next time",
        #                                     'it does not work yet =(')           
        plt.clf()
        gs = gridspec.GridSpec(3,3) 
        gs.update(left=0.06, right=0.93,top = 0.94,bottom = 0.04,
                   wspace=0.2,hspace=0.1)   
        self.figure.patch.set_facecolor('white') 
        #self.figure.patch.set_facecolor(self.background) 
        #Set the background color  
        ax00 = self.figure.add_subplot(gs[0]) # water         
        ax10 = self.figure.add_subplot(gs[1]) # water
        ax20 = self.figure.add_subplot(gs[2]) # water 
 
        ax01 = self.figure.add_subplot(gs[3])          
        ax11 = self.figure.add_subplot(gs[4])
        ax21 = self.figure.add_subplot(gs[5])

        ax02 = self.figure.add_subplot(gs[6])    
        ax12 = self.figure.add_subplot(gs[7])
        ax22 = self.figure.add_subplot(gs[8])
   
        ax00.set_ylabel('Depth (m)',fontsize= self.font_txt) #Label y axis
        ax01.set_ylabel('Depth (m)',fontsize= self.font_txt)   
        ax02.set_ylabel('Depth (cm)',fontsize= self.font_txt) 
                                     
        for n in range(1,len(self.vars)):
            if (self.all_year_1d_box.currentIndex() == n) :
                
                varname1 = self.vars[n][0] 
                varname2 = self.vars[n][1] 
                varname3 = self.vars[n][2] 
                #print (n)
                z123 = readdata.read_all_year_var(self,
                            self.fname,varname1,varname2,varname3)

                z0 = np.array(z123[0])
                z1 = np.array(z123[1])
                z2 = np.array(z123[2])
                
                ax00.set_title(str(self.titles_all_year[n][0]), 
                fontsize=self.xlabel_fontsize, fontweight='bold') 
                
                ax10.set_title(str(self.titles_all_year[n][1]), 
                fontsize=self.xlabel_fontsize, fontweight='bold') 
                
                ax20.set_title(str(self.titles_all_year[n][2]), 
                fontsize=self.xlabel_fontsize, fontweight='bold')                                 
                self.num_var = n  

        for axis in (ax00,ax10,ax20,ax01,ax11,ax21,ax02,ax12,ax22):
            #water          
            axis.yaxis.grid(True,'minor')
            axis.xaxis.grid(True,'major')                
            axis.yaxis.grid(True,'major') 
                    
        ax00.set_ylim(self.y1max,0)   
        ax10.set_ylim(self.y1max,0)  
        ax20.set_ylim(self.y1max,0) 
        
        ax01.set_ylim(self.y2max, self.y2min)   
        ax11.set_ylim(self.y2max, self.y2min)  
        ax21.set_ylim(self.y2max, self.y2min) 

        ax02.set_ylim(self.ysedmax, self.ysedmin)   
        ax12.set_ylim(self.ysedmax, self.ysedmin)  
        ax22.set_ylim(self.ysedmax, self.ysedmin) 
        #
        #n0 = self.varmax(self,z0,1) #[0:self.y2max_fill_water,:].max() 
        start = 0
        stop = 365 
        #### to change""!!!!
        
        
        watmin0 = readdata.varmin(self,z0,"wattime",start,stop) 
        watmin1 = readdata.varmin(self,z1,"wattime",start,stop) 
        watmin2 = readdata.varmin(self,z2,"wattime",start,stop)          

        watmax0 = readdata.varmax(self,z0,"wattime",start,stop) 
        watmax1 = readdata.varmax(self,z1,"wattime",start,stop)
        watmax2 = readdata.varmax(self,z2,"wattime",start,stop)  
                 
        sed_min0 = readdata.varmin(self,z0,"sedtime",start,stop) 
        sed_min1 = readdata.varmin(self,z1,"sedtime",start,stop) 
        sed_min2 = readdata.varmin(self,z2,"sedtime",start,stop)    

        sed_max0 = readdata.varmax(self,z0,"sedtime",start,stop) 
        sed_max1 = readdata.varmax(self,z1,"sedtime",start,stop)         
        sed_max2 = readdata.varmax(self,z2,"sedtime",start,stop)         
        
        if self.num_var == 5: #pH 
            watmax1 = 9
            watmin1 = 6.5
        elif self.num_var == 2: #po4, so4
            watmax0 = 3  
            #watmax1 = 7000.          
            #watmin1 = 4000.            
        else:
            pass
                    
        
        self.m0ticks = readdata.ticks(watmin0,watmax0)
        self.m1ticks = readdata.ticks(watmin1,watmax1)
        self.m2ticks = readdata.ticks(watmin2,watmax2)  
        
        self.sed_m0ticks = readdata.ticks(sed_min0,sed_max0)
        self.sed_m1ticks = readdata.ticks(sed_min1,sed_max1)
        self.sed_m2ticks = readdata.ticks(sed_min2,sed_max2)                 
        #for axis in (ax00,ax10,ax20):             
        
        ax00.set_xlim(watmin0,watmax0)   
        ax01.set_xlim(watmin0,watmax0)         
        ax02.set_xlim(sed_min0,sed_max0)
        
        ax10.set_xlim(watmin1,watmax1)   
        ax11.set_xlim(watmin1,watmax1)         
        ax12.set_xlim(sed_min1,sed_max1)         
         
        ax20.set_xlim(watmin2,watmax2)   
        ax21.set_xlim(watmin2,watmax2)         
        ax22.set_xlim(sed_min2,sed_max2) 
                
        ax10.set_xlim(watmin1,watmax1)   
        ax11.set_xlim(watmin1,watmax1)         
        #ax12.set_xlim(sed_min1,sed_max1) 
                     
        ax20.set_xlim(watmin2,watmax2)   
        ax21.set_xlim(watmin2,watmax2)         
        #ax22.set_xlim(sed_min2,sed_max2)                  
        #water

                     
        ax00.fill_between(
                        self.m0ticks, self.y1max, 0,
                        facecolor= self.wat_col1, alpha=0.1 ) #self.a_w
        ax01.fill_between(
                        self.m0ticks, self.y2min_fill_bbl ,self.y2min,
                        facecolor= self.wat_col1, alpha=0.1 ) #self.a_w    
        ax01.fill_between(self.m0ticks, self.y2max, self.y2min_fill_bbl,
                               facecolor= self.bbl_col1, alpha=self.a_bbl) 
            
        ax02.fill_between(self.sed_m0ticks,self.ysedmin_fill_sed,-10,
                               facecolor= self.bbl_col1, alpha=self.a_bbl)          
        ax02.fill_between(self.sed_m0ticks, self.ysedmax, self.ysedmin_fill_sed,
                               facecolor= self.sed_col1, alpha=self.a_s)          
        
            #axis.fill_between(self.xticks, self.y2max, self.y2min_fill_bbl,
            #                   facecolor= self.bbl_color, alpha=self.alpha_bbl)        
            
        ax10.fill_between(
                        self.m1ticks, self.y1max, 0,
                        facecolor= self.wat_col1, alpha=0.1 ) #self.a_w
        
        ax11.fill_between(
                        self.m1ticks, self.y2min_fill_bbl ,self.y2min,
                        facecolor= self.wat_col1, alpha=0.1 ) #self.a_w    
        ax11.fill_between(self.m1ticks, self.y2max, self.y2min_fill_bbl,
                               facecolor= self.bbl_col1, alpha=self.a_bbl)      
        ax12.fill_between(self.sed_m1ticks,self.ysedmin_fill_sed,-10,
                               facecolor= self.bbl_col1, alpha=self.a_bbl) 
        ax12.fill_between(self.sed_m1ticks, self.ysedmax, self.ysedmin_fill_sed,
                              facecolor= self.sed_col1, alpha=self.a_s)        
        ax20.fill_between(
                        self.m2ticks, self.y1max, 0,
                        facecolor= self.wat_col1, alpha=0.1 ) #self.a_w
        
        ax21.fill_between(
                        self.m2ticks, self.y2min_fill_bbl ,self.y2min,
                        facecolor= self.wat_col1, alpha=0.1 ) #self.a_w    
        ax21.fill_between(self.m2ticks, self.y2max, self.y2min_fill_bbl,
                               facecolor= self.bbl_col1, alpha=self.a_bbl)     
        ax22.fill_between(self.sed_m2ticks,self.ysedmin_fill_sed,-10,
                               facecolor= self.bbl_col1, alpha=self.a_bbl)                         
        ax22.fill_between(self.sed_m2ticks, self.ysedmax, self.ysedmin_fill_sed,
                               facecolor= self.sed_col1, alpha=self.a_s) 
                            

        
                
        for n in range(0,3): #365
            if n >= 0 and n<=60 or n >= 335 and n <365 : #"winter" 
                linewidth = self.linewidth
                                  
                ax00.plot(z0[n],self.depth,self.wint,alpha = 
                          self.a_w, linewidth = linewidth , zorder = 10) 
                ax10.plot(z1[n],self.depth,self.wint,alpha = 
                          self.a_w, linewidth = linewidth , zorder = 10)
                ax20.plot(z2[n],self.depth,self.wint,alpha = 
                          self.a_w, linewidth = linewidth, zorder = 10 )  
                
                ax01.plot(z0[n],self.depth,self.wint,alpha = 
                          self.a_w, linewidth = linewidth, zorder = 10 ) 
                ax11.plot(z1[n],self.depth,self.wint,alpha = 
                          self.a_w, linewidth = linewidth , zorder = 10)
                ax21.plot(z2[n],self.depth,self.wint,alpha = 
                          self.a_w, linewidth = linewidth, zorder = 10 ) 
    
                ax02.plot(z0[n],self.depth_sed,self.wint,alpha = 
                          self.a_w, linewidth = linewidth, zorder = 10 ) 
                ax12.plot(z1[n],self.depth_sed,self.wint,alpha = 
                          self.a_w, linewidth = linewidth, zorder = 10 )
                ax22.plot(z2[n],self.depth_sed,self.wint,alpha = 
                          self.a_w, linewidth = linewidth, zorder = 10 ) 
            elif n >= 150 and n < 249: #"summer"
                ax00.plot(z0[n],self.depth,self.summ,alpha = 
                          self.a_s, linewidth = linewidth, zorder = 10 ) 
                ax10.plot(z1[n],self.depth,self.summ,alpha = 
                          self.a_s, linewidth = linewidth, zorder = 10 )
                ax20.plot(z2[n],self.depth,self.summ,alpha = 
                          self.a_s, linewidth = linewidth, zorder = 10 )  
                
                ax01.plot(z0[n],self.depth,self.summ,alpha = 
                          self.a_s, linewidth = linewidth, zorder = 10 ) 
                ax11.plot(z1[n],self.depth,self.summ,alpha = 
                          self.a_s, linewidth = linewidth, zorder = 10 )
                ax21.plot(z2[n],self.depth,self.summ,alpha = 
                          self.a_s, linewidth = linewidth, zorder = 10 ) 
    
                ax02.plot(z0[n],self.depth_sed,self.summ,alpha = 
                          self.a_s, linewidth = linewidth, zorder = 10 ) 
                ax12.plot(z1[n],self.depth_sed,self.summ,alpha = 
                          self.a_s, linewidth = linewidth, zorder = 10 )
                ax22.plot(z2[n],self.depth_sed,self.summ,alpha = 
                          self.a_s, linewidth = linewidth, zorder = 10 ) 
            else : #"autumn and spring"
                ax00.plot(z0[n],self.depth,self.spr_aut,alpha = 
                          self.a_aut, linewidth = linewidth, zorder = 10 ) 
                ax10.plot(z1[n],self.depth,self.spr_aut,alpha = 
                          self.a_aut, linewidth = linewidth, zorder = 10 )
                ax20.plot(z2[n],self.depth,self.spr_aut,alpha = 
                          self.a_aut, linewidth = linewidth, zorder = 10 )  
                
                ax01.plot(z0[n],self.depth,self.spr_aut,alpha = 
                          self.a_aut, linewidth = linewidth, zorder = 10 ) 
                ax11.plot(z1[n],self.depth,self.spr_aut,alpha = 
                          self.a_aut, linewidth = linewidth, zorder = 10 )
                ax21.plot(z2[n],self.depth,self.spr_aut,alpha = 
                          self.a_aut, linewidth = linewidth, zorder = 10 ) 
    
                ax02.plot(z0[n],self.depth_sed,self.spr_aut,
                          alpha = self.a_aut, zorder = 10) 
                ax12.plot(z1[n],self.depth_sed,self.spr_aut,
                          alpha = self.a_aut, zorder = 10)
                ax22.plot(z2[n],self.depth_sed,self.spr_aut,
                          alpha = self.a_aut, zorder = 10)      


           
            
                          
        self.canvas.draw()  '''   
    def setPenProperties(self):
        
        self.dialog = PropertiesDlg(self)
        self.dialog.setWindowTitle("Title") 
        
        #self.dialog.button.setChecked()   
        #self.value = None
        if self.dialog.exec_():
            self.checker = self.dialog.button
            if self.dialog.button.isChecked(): 
                self.value = True
            else : 
                self.value = False              
            #if self.checker.isChecked():                
            #    print ('1') 
            #else:
            #    print("Nope")
        return self.value 
    
class PropertiesDlg(QtGui.QDialog): 
    def __init__(self, parent=None):
        super(PropertiesDlg, self).__init__(parent)
        #window = Window(self)
        #print (self.Window.value)
        self.okButton = QtGui.QPushButton("&OK")
        self.cancelButton = QtGui.QPushButton("Cancel")
        self.button = QtGui.QCheckBox('test') 
        #if self.value == True or None:
        #    self.dialog.button.setChecked()
                
        layout = QtGui.QGridLayout()
        layout.addWidget(self.button, 0, 0, 1, 1) 
        layout.addWidget(self.okButton, 1, 0, 1, 1) 
        layout.addWidget(self.cancelButton, 1, 1, 1, 1)         
        #layout.addWidget(self.buttonBox, 3, 0, 1, 3)
        self.setLayout(layout) 
        self.okButton.released.connect(self.accept)
        self.cancelButton.released.connect(self.reject)
        
        #if self.button.isChecked():
        #    #self.button_event()
        #    print('is checked')
            
        #def button_event(self):
        #    print ('button event')
        #    self.value1 = True 
        #    return self.value1         
        
        
            
            

            
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    app.setStyle("plastique")
    main = Window()
    main.setStyleSheet("background-color:#d8c9c2;")

    main.show()
    #PySide.QtCore.Qt.WindowFlags
    sys.exit(app.exec_()) 
