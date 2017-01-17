#!/usr/bin/python
# Filename: readfile.py
# Import standard (i.e., non GOTM-GUI) modules.
import os,sys
from PyQt4 import QtGui,QtCore
from PyQt4.QtGui import QSpinBox,QLabel,QComboBox
#from numpy import nan
from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas)
from matplotlib.backends.backend_qt4agg import (
    NavigationToolbar2QT as NavigationToolbar)
import matplotlib.pyplot as plt
import readdata
#import calc_resolution
import numpy as np
import matplotlib.gridspec as gridspec
from matplotlib import style
import matplotlib.ticker as mtick
import matplotlib as mpl
import math


#print (sys.version_info)

class Window(QtGui.QDialog):
     
    def __init__(self, parent=None, ):
        super(Window, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.Window)   
        self.setWindowTitle("BROM Pictures")
        self.setWindowIcon(QtGui.QIcon('bromlogo.png'))
        
        app1 = QtGui.QApplication(sys.argv)
        screen_rect = app1.desktop().screenGeometry()
        width, height = screen_rect.width(), screen_rect.height()
        font = (height/10000.)
        #print (width, height)
        
        #self.figure = plt.figure(figsize = (width,height), dpi= 200,
        #                          facecolor='white')
        self.figure = plt.figure(figsize = (width,height),dpi= 100,
                                  facecolor='white')        
        
        
        #print(plt.style.available)
        #text(1, 1, 's', fontdict=None, )
        #self.ax.set_text('s')
        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        
        fname = unicode(QtGui.QFileDialog.getOpenFileName(self,
        'Open netcdf ', os.getcwd(), "netcdf (*.nc);; all (*)"))   
        readdata.readdata_brom(self,fname) 
        readdata.colors(self)  
      
        readdata.calculate_ywat(self)
        readdata.calculate_ybbl(self) 
        readdata.depth_sed(self) #calc depthes in cm 
        readdata.depth_sed2(self) #calc depthes in cm for kz         
        readdata.y2max_fill_water(self)                
        readdata.calculate_ysed(self)
        readdata.y_coords(self)  
              
        #readdata.calculate_sedmax(self)  
       
        self.time_prof_box = QtGui.QComboBox()
        for i in self.var_names_profile:
            self.time_prof_box.addItem(str(i))
        self.time_prof_box.currentIndexChanged.connect(
            self.time_profile)        
        
        self.all_year_box = QtGui.QComboBox()
        for i in self.var_names_charts_year:
            self.all_year_box.addItem(str(i))
        self.all_year_box.currentIndexChanged.connect(
            self.all_year_charts) 
         
        self.one_day_box = QtGui.QComboBox()
        oModel=self.one_day_box.model()
        head_item = QtGui.QStandardItem('Day to plot')
        oModel.appendRow(head_item)
        self.numday = 1
        
        for n in range(1, self.monthes_start[1]):
            item = QtGui.QStandardItem(str(n)+ '/1'+ 
                     ' (' + str(self.numday) + ')')
                                       
            oModel.appendRow(item)
            item.setBackground(QtGui.QColor(self.wint))
            self.numday = self.numday + 1 #self.monthes_start[1]        
        for m in range(1,len(self.monthes_start)-1) : #np.arange(1,13):                    
            start_date = self.monthes_start[m]
            next_start_dat = self.monthes_start[m+1]
            for n in range(1, int(next_start_dat - start_date)+1) :
                item = QtGui.QStandardItem(str(n)+ '/' + str(m+1) + 
                     ' (' + str(self.numday) + ')')
                font = item.font()
                #font.setPointSize(10)
                item.setFont(font)                
                oModel.appendRow(item)
                
                self.numday = self.numday + 1 #i+1
                
        self.one_day_box.currentIndexChanged.connect(
            self.one_day_plot)  
       
        self.one_day_box.setStyleSheet(
        'QComboBox {background-color: #c2b4ae; border-width: 10px;'
        '  padding: 6px; font: bold 16px; }')        
        self.all_year_box.setStyleSheet(
        'QComboBox {background-color: #c2b4ae;padding: 6px;border-width: 10px;'
         'font: bold 16px;}')           
        self.time_prof_box.setStyleSheet(
        'QComboBox {background-color: #c2b4ae;padding: 6px;border-width: 10px;'
         'font: bold 16px;}')    
        

        #set the layout
        #layout = QtGui.QGridLayout()
        layout = QtGui.QHBoxLayout()
        layout.addStretch()
        #layout.addWidget(self.toolbar)         
        #layout.addStretch()
        
        self.grid = QtGui.QGridLayout(self)
        self.grid.addLayout(layout, 0, 0)
        self.grid.addWidget(self.canvas, 2, 0,1,4) 
        self.grid.addWidget(self.toolbar,1,0,1,1)    
        self.grid.addWidget(self.time_prof_box,1,1,1,1)  
        self.grid.addWidget(self.all_year_box,1,2,1,1)       
        self.grid.addWidget(self.one_day_box,1,3,1,1) 


               
    def fig2_txt(self):        
        plt.text(1.1, 0.5,'Water ', fontweight='bold', # draw legend to Water
        bbox={'facecolor': self.wat_col, 'alpha':0.5, 'pad':3},
         rotation=90, 
        transform= self.ax50.transAxes) 
        #self.font_txt        
        plt.text(1.1, 0.8,'Water ', fontweight='bold', # draw legend to BBL
        bbox={'facecolor': self.wat_col, 'alpha':0.5, 'pad':3},
        fontsize=self.font_txt, rotation=90,
        transform= self.ax51.transAxes)
        plt.text(1.1, 0.3,'BBL ', fontweight='bold',  
        #draw legend to Sediment
        bbox={'facecolor': self.bbl_col , 'alpha':0.6, 'pad':3},
        fontsize=self.font_txt, rotation=90,
        transform= self.ax51.transAxes)       
        plt.text(1.1, 0.8,'BBL ', fontweight='bold',  # draw legend to BBL
        bbox={'facecolor': self.bbl_col, 'alpha':0.5, 'pad':3},
        fontsize=14, rotation=90,
        transform= self.ax52.transAxes)
        plt.text(1.1, 0.5,'Sediment ', fontweight='bold', #draw legend to Sediment
        bbox={'facecolor': self.sed_col, 'alpha':0.6, 'pad':3},
        fontsize=14, rotation=90,
        transform= self.ax52.transAxes)  
        
        plt.text(0, 1.61,'{}{}'.format('day', self.numday) ,
         fontweight='bold', # Write number of day to Figure
        bbox={'facecolor': self.wat_col, 'alpha':0.5, 'pad':10}, 
        fontsize=14,
        transform= self.ax00.transAxes)        
        
        
    def time_profile(self):

        plt.clf()
        for n in range(1,len(self.var_names_profile)):
            if (self.time_prof_box.currentIndex() == n) :
                z = self.vars[n] #self.po4
                title = self.time_prof_box.currentText() 
                  
                                 
        gs = gridspec.GridSpec(2, 1) 
        x = self.time #np.arange(6)
        y = self.depth #np.arange(5)
        y_sed = self.depth_sed
        
        z1 = np.array(z).flatten()
        zz = z1.reshape((len(x),len(y))).T
        
        watmin = readdata.varmin(self,zz,0) #0 - water 
        watmax = readdata.varmax(self,zz,0)
        sed_min = readdata.varmin(self,zz,1)# 1 - sed
        sed_max = readdata.varmax(self,zz,1)  
        X,Y = np.meshgrid(x,y)
        X_sed,Y_sed = np.meshgrid(x,y_sed)
        ax = self.figure.add_subplot(gs[0])
        ax2 = self.figure.add_subplot(gs[1])        
        #self.figure, (ax, ax2) = plt.subplots(2, 1, sharex=True)
        #f.set_size_inches(11.69,8.27)

        ax.set_title(title)
        ax.set_ylim(self.y1max,0)       
        ax2.set_ylim(self.ysedmax,self.y3min) #ysedmin
        ax.set_xlim(0,len(x))
        self.num = 50.    


        ax.set_ylabel('Depth (m)',fontsize= self.font_txt) #Label y axis 
        ax2.set_ylabel('Depth (cm)',fontsize= self.font_txt) 
        ax2.set_xlabel('Number of day',fontsize= self.font_txt) 

            
        cmap = plt.cm.jet #gnuplot#jet#gist_rainbow
        
        wat_levs = np.linspace(watmin,watmax,num= self.num)
        sed_levs = np.linspace(sed_min,sed_max,
                             num = self.num)
                
        int_wat_levs = []
        int_sed_levs= []
        
        
        for n in wat_levs:
            n = readdata.int_value(self,n,watmin,watmax)
            int_wat_levs.append(n)
            
        for n in sed_levs:
            n = readdata.int_value(self,n,sed_min,
                                   sed_max)
            int_sed_levs.append(n)            
                      
        cmap1 = plt.cm.rainbow #define color maps
       
        CS = ax.contourf(X,Y, zz, levels= int_wat_levs,
                              cmap=cmap,
                              origin='lower')

        CS1 = ax2.contourf(X_sed,Y_sed, zz, levels = int_sed_levs,
                              cmap=cmap1,
                              origin='lower')
       
        cax = self.figure.add_axes([0.92, 0.53, 0.02, 0.35])
        
        
        
        
        #x,y,thick,length
        cax1 = self.figure.add_axes([0.92, 0.1, 0.02, 0.35])
        wat_ticks = readdata.ticks(watmin,watmax)
        cb = plt.colorbar(CS,cax = cax,ticks = wat_ticks)
        cb_sed = plt.colorbar(CS1,cax = cax1 )
        #cb.set_label('Water')
        
        sed_ticks = readdata.ticks(sed_min,sed_max)
        #cb.set_ticks(wat_ticks)
        cb_sed.set_ticks(sed_ticks)  
        ax2.axhline(0, color='white', linestyle = '--')     
        #cb_sed.set_label('BBL, Sediment')
        #cb.ax.set_xticklabels(['Low', 'Medium', 'High']) 
        #loc = clevs + .1
        #cb.set_ticks(loc)
        #cb.set_ticklabels(clevs)
        #cbar = CS.colorbar(cax, )
        #cbar.ax.set_yticklabels(['< -1', '0', '> 1'])
        # vertically oriented colorbar
        #self.figure.suptitle('Berre lagoon', fontsize=25,
        # fontweight='bold')
        #f.savefig('test.png', dpi=300) 
        #plt.show()   

        self.canvas.draw() 
        
    def all_year_charts(self):            
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
                                     
        for n in range(1,len(self.var_names_charts_year)):
            if (self.all_year_box.currentIndex() == n) :
                z0 = np.array(self.vars_year[n][0])
                z1 = np.array(self.vars_year[n][1]) #self.po4
                z2 = np.array(self.vars_year[n][2])
                ax00.set_title(str(self.titles_all_year[n][0]), 
                fontsize=self.xlabel_fontsize, fontweight='bold') 
                ax10.set_title(str(self.titles_all_year[n][1]), 
                fontsize=self.xlabel_fontsize, fontweight='bold') 
                ax20.set_title(str(self.titles_all_year[n][2]), 
                fontsize=self.xlabel_fontsize, fontweight='bold')                                 
                #title0 = self.var_titles_charts_year[n][0] 
                #title1 = self.var_titles_charts_year[n][1] 
                #title2 = self.var_titles_charts_year[n][2]
                
        #ax00.set_title(title0) 
        #ax10.set_title(title1)
        #ax20.set_title(title2)

        #self.ax10.set_xlabel(r'$\rm Fe $',fontsize=14)   
        #self.ax20.set_xlabel(r'$\rm H _2 S $',fontsize=14) 




        for axis in (ax00,ax10,ax20,ax01,ax11,ax21,ax02,ax12,ax22):
            #water          
            axis.yaxis.grid(True,'minor')
            axis.xaxis.grid(True,'major')                
            axis.yaxis.grid(True,'major') 
                    
        ax00.set_ylim(self.y1max,0)   
        ax10.set_ylim(self.y1max,0)  
        ax20.set_ylim(self.y1max,0) 
        
        ax01.set_ylim(self.y2max, self.y1max)   
        ax11.set_ylim(self.y2max, self.y1max)  
        ax21.set_ylim(self.y2max, self.y1max) 

        ax02.set_ylim(self.ysedmax, self.ysedmin)   
        ax12.set_ylim(self.ysedmax, self.ysedmin)  
        ax22.set_ylim(self.ysedmax, self.ysedmin) 
        
                
        for n in range(0,len(self.time)):
            if n >= 0 and n<=60 or n >= 335 and n <365 : #"winter"                  
                ax00.plot(z0[0][n],self.depth,self.wint,alpha = 
                          self.a_w) 
                ax10.plot(z1[0][n],self.depth,self.wint,alpha = 
                          self.a_w)
                ax20.plot(z2[0][n],self.depth,self.wint,alpha = 
                          self.a_w)  
                
                ax01.plot(z0[0][n],self.depth,self.wint,alpha = 
                          self.a_w) 
                ax11.plot(z1[0][n],self.depth,self.wint,alpha = 
                          self.a_w)
                ax21.plot(z2[0][n],self.depth,self.wint,alpha = 
                          self.a_w) 
    
                ax02.plot(z0[0][n],self.depth_sed,self.wint,alpha = 
                          self.a_w) 
                ax12.plot(z1[0][n],self.depth_sed,self.wint,alpha = 
                          self.a_w)
                ax22.plot(z2[0][n],self.depth_sed,self.wint,alpha = 
                          self.a_w) 
            elif n >= 150 and n < 249: #"summer"
                ax00.plot(z0[0][n],self.depth,self.summ,alpha = 
                          self.a_s) 
                ax10.plot(z1[0][n],self.depth,self.summ,alpha = 
                          self.a_s)
                ax20.plot(z2[0][n],self.depth,self.summ,alpha = 
                          self.a_s)  
                
                ax01.plot(z0[0][n],self.depth,self.summ,alpha = 
                          self.a_s) 
                ax11.plot(z1[0][n],self.depth,self.summ,alpha = 
                          self.a_s)
                ax21.plot(z2[0][n],self.depth,self.summ,alpha = 
                          self.a_s) 
    
                ax02.plot(z0[0][n],self.depth_sed,self.summ,alpha = 
                          self.a_s) 
                ax12.plot(z1[0][n],self.depth_sed,self.summ,alpha = 
                          self.a_s)
                ax22.plot(z2[0][n],self.depth_sed,self.summ,alpha = 
                          self.a_s) 
            else : #"autumn and spring"
                ax00.plot(z0[0][n],self.depth,self.spr_aut,alpha = 
                          self.a_aut) 
                ax10.plot(z1[0][n],self.depth,self.spr_aut,alpha = 
                          self.a_aut)
                ax20.plot(z2[0][n],self.depth,self.spr_aut,alpha = 
                          self.a_aut)  
                
                ax01.plot(z0[0][n],self.depth,self.spr_aut,alpha = 
                          self.a_aut) 
                ax11.plot(z1[0][n],self.depth,self.spr_aut,alpha = 
                          self.a_aut)
                ax21.plot(z2[0][n],self.depth,self.spr_aut,alpha = 
                          self.a_aut) 
    
                ax02.plot(z0[0][n],self.depth_sed,self.spr_aut,
                          alpha = self.a_aut) 
                ax12.plot(z1[0][n],self.depth_sed,self.spr_aut,
                          alpha = self.a_aut)
                ax22.plot(z2[0][n],self.depth_sed,self.spr_aut,
                          alpha = self.a_aut)                                 
        self.canvas.draw() 
  
    def one_day_plot(self):
        plt.clf() #clear figure before updating 

        #print (self.one_day_box.currentIndex()) #self.numday
        # function to define 1 figure
        
        self.numday = (self.one_day_box.currentIndex()) #take the input value of numday spinbox
        style.use('ggplot')  ,
        #plt.style.use('presentation')   
 
        self.figure.patch.set_facecolor('white')  #Set the background     
        wspace=0.40                         #define values for grid 
        hspace = 0.05                       #define values for grid
        gs = gridspec.GridSpec(2, 6) 
        gs.update(left=0.06, right=0.93,top = 0.84,bottom = 0.4,
                   wspace=wspace,hspace=hspace)
        gs1 = gridspec.GridSpec(1, 6)
        gs1.update(left=0.06, right=0.93, top = 0.26, bottom = 0.02,
                    wspace=wspace,hspace=hspace)


        #create subplots
        self.ax00 = self.figure.add_subplot(gs[0]) # water
        self.ax10 = self.figure.add_subplot(gs[1])
        self.ax20 = self.figure.add_subplot(gs[2])
        self.ax30 = self.figure.add_subplot(gs[3])        
        self.ax40 = self.figure.add_subplot(gs[4])
        self.ax50 = self.figure.add_subplot(gs[5])
        
        self.ax01 = self.figure.add_subplot(gs[6]) #BBL
        self.ax11 = self.figure.add_subplot(gs[7])
        self.ax21 = self.figure.add_subplot(gs[8])
        self.ax31 = self.figure.add_subplot(gs[9])        
        self.ax41 = self.figure.add_subplot(gs[10])
        self.ax51 = self.figure.add_subplot(gs[11])  
        
        self.ax02 = self.figure.add_subplot(gs1[0]) #sediment
        self.ax12 = self.figure.add_subplot(gs1[1])
        self.ax22 = self.figure.add_subplot(gs1[2])
        self.ax32 = self.figure.add_subplot(gs1[3])        
        self.ax42 = self.figure.add_subplot(gs1[4])
        self.ax52 = self.figure.add_subplot(gs1[5])     
        
        
        #Create axes sharing y              
        self.ax00_1 = self.ax00.twiny()  #water
        self.ax00_2 = self.ax00.twiny()  
        self.ax00_3 = self.ax00.twiny()        

        self.ax10_1 = self.ax10.twiny() #water
        self.ax10_2 = self.ax10.twiny() 
        self.ax10_3 = self.ax10.twiny()        
        self.ax10_4 = self.ax10.twiny()
  
        self.ax20_1 = self.ax20.twiny() 
        self.ax20_2 = self.ax20.twiny() 
        self.ax20_3 = self.ax20.twiny()        
#        ax20_4 = ax20.twiny()  

        self.ax30_1 = self.ax30.twiny() 
        self.ax30_2 = self.ax30.twiny() 
        self.ax30_3 = self.ax30.twiny()        
        self.ax30_4 = self.ax30.twiny()            
        self.ax30_5 = self.ax30.twiny()

        self.ax40_1 = self.ax40.twiny() 
        self.ax40_2 = self.ax40.twiny() 
        self.ax40_3 = self.ax40.twiny()        
        self.ax40_4 = self.ax40.twiny()  
                        
        self.ax50_1 = self.ax50.twiny() #water
        self.ax50_2 = self.ax50.twiny() 
        self.ax50_3 = self.ax50.twiny()        
        self.ax50_4 = self.ax50.twiny() 
        
        
        
        
        self.ax01_1 = self.ax01.twiny() #bbl
        self.ax01_2 = self.ax01.twiny()
        self.ax01_3 = self.ax01.twiny()

        self.ax11_1 = self.ax11.twiny() #bbl
        self.ax11_2 = self.ax11.twiny()
        self.ax11_3 = self.ax11.twiny()
        self.ax11_4 = self.ax11.twiny()  

        self.ax21_1 = self.ax21.twiny() 
        self.ax21_2 = self.ax21.twiny() 
        self.ax21_3 = self.ax21.twiny()        
#        ax21_4 = ax21.twiny()         
        self.ax31_1 = self.ax31.twiny() 
        self.ax31_2 = self.ax31.twiny() 
        self.ax31_3 = self.ax31.twiny()        
        self.ax31_4 = self.ax31.twiny()            
        self.ax31_5 = self.ax31.twiny()        
                 
        self.ax41_1 = self.ax41.twiny() 
        self.ax41_2 = self.ax41.twiny() 
        self.ax41_3 = self.ax41.twiny()        
        self.ax41_4 = self.ax41.twiny() 
     
        self.ax51_1 = self.ax51.twiny() #bbl
        self.ax51_2 = self.ax51.twiny() 
        self.ax51_3 = self.ax51.twiny()        
        self.ax51_4 = self.ax51.twiny()  
        
        self.ax02_1 = self.ax02.twiny() #sediment
        self.ax02_2 = self.ax02.twiny()
        self.ax02_3 = self.ax02.twiny()
                
        self.ax12_1 = self.ax12.twiny() #sediment
        self.ax12_2 = self.ax12.twiny()
        self.ax12_3 = self.ax12.twiny()
        self.ax12_4 = self.ax12.twiny()
        
        self.ax22_1 = self.ax22.twiny() 
        self.ax22_2 = self.ax22.twiny() 
        self.ax22_3 = self.ax22.twiny()          
         
        self.ax32_1 = self.ax32.twiny() 
        self.ax32_2 = self.ax32.twiny() 
        self.ax32_3 = self.ax32.twiny()        
        self.ax32_4 = self.ax32.twiny()            
        self.ax32_5 = self.ax32.twiny()               

        self.ax42_1 = self.ax42.twiny() 
        self.ax42_2 = self.ax42.twiny() 
        self.ax42_3 = self.ax42.twiny()        
        self.ax42_4 = self.ax42.twiny()

        self.ax52_1 = self.ax52.twiny() #sediment
        self.ax52_2 = self.ax52.twiny() 
        self.ax52_3 = self.ax52.twiny()        
        self.ax52_4 = self.ax52.twiny()      

        for axis in (self.ax00, self.ax02,
                     self.ax10, self.ax12,
                     self.ax20, self.ax22,
                     self.ax30, self.ax32,
                     self.ax40, self.ax42,
                     self.ax50, self.ax52): 
            axis.xaxis.set_label_position('top')
          
            axis.xaxis.tick_top() 
            
        #remove axis from bbl
        for axis in (self.ax00,self.ax02,self.ax10,self.ax12,self.ax20,
                     self.ax22,self.ax30,self.ax32,self.ax40,self.ax42,
                     self.ax50,self.ax52,
                     self.ax01,self.ax01_1, self.ax01_2, self.ax01_3,
                     self.ax11,self.ax11_1, self.ax11_2, self.ax11_3,
                     self.ax11_4,
                     self.ax21,self.ax21_1, self.ax21_2, self.ax21_3,
                     self.ax31,self.ax31_1, self.ax31_2, self.ax31_3,
                     self.ax31_4,self.ax31_5,
                     self.ax41,self.ax41_1, self.ax41_2, self.ax41_3,
                     self.ax41_4,
                     self.ax51,self.ax51_1, self.ax51_2, self.ax51_3,
                     self.ax51_4):
            axis.tick_params(
            axis='x',          # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            bottom='off',      # ticks along the bottom edge are off
            top='off',
            labelbottom='off',         # ticks along the top edge are off
            labeltop='off',    # labels along the bottom edge are of
            ) 
            
            #for spine in axis.spines.iteritems():
            #    spine.set_visible(False) 
        #self.ax01.xaxis.set_ticks_position('top')
        #self.ax01.set_title('bottom-left spines')      
        #self.ax01.spines['top'].set_visible(False)  
        
        for axis in (self.ax00_1,self.ax00_2,self.ax00_3,
                     
                     self.ax02_1,self.ax02_2,self.ax02_3,                     
                     self.ax10_1,self.ax10_2,self.ax10_3,self.ax10_4,                     
                     self.ax12_1,self.ax12_2, self.ax12_3, self.ax12_4,                      
                     self.ax20_1,self.ax20_2,self.ax20_3,                      
                     self.ax22_1,self.ax22_2,self.ax22_3,                      
                     self.ax30_1,self.ax30_2,self.ax30_3,self.ax30_4,
                     self.ax30_5,                     
                     self.ax32_1,self.ax32_2,self.ax32_3,self.ax32_4,
                     self.ax32_5,                     
                     self.ax40_1,self.ax40_2,self.ax40_3,self.ax40_4,                     
                     self.ax42_1,self.ax42_2, self.ax42_3,self.ax42_4,                     
                     self.ax50_1,self.ax50_2,self.ax50_3,self.ax50_4,
                     self.ax52_1,self.ax52_2,self.ax52_3,self.ax52_4):
            axis.tick_params(labelsize= self.ticklabel_fontsize,
            pad = 0.5, length=2)              
            
            for spinename, spine in axis.spines.iteritems():
                if spinename != 'top':
                    spine.set_visible(False) 
                                   
        for axis in (self.ax00_1,self.ax02_1,self.ax10_1,self.ax12_1,self.ax20_1,
                     self.ax22_1,self.ax30_1,self.ax32_1,
                     self.ax40_1,self.ax42_1,self.ax50_1,self.ax52_1):
            axis.spines['top'].set_position(('outward', self.axis1))
            axis.spines['top'].set_color('g')                   
        for axis in (self.ax00_2,self.ax02_2,self.ax10_2,self.ax12_2,self.ax20_2,
                     self.ax22_2,self.ax30_2,self.ax32_2,
                      self.ax40_2,self.ax42_2,self.ax50_2,self.ax52_2):    
            axis.spines['top'].set_position(('outward', self.axis2))
            axis.spines['top'].set_color('r')   
        for axis in (self.ax10_3,self.ax12_3,self.ax30_3,self.ax32_3,
                     self.ax40_3,self.ax42_3,
            self.ax50_3,self.ax52_3,self.ax00_3,
            self.ax02_3,self.ax20_3,self.ax22_3):    
            axis.spines['top'].set_position(('outward', self.axis3))
            axis.spines['top'].set_color('b') 
        for axis in (self.ax10_4,self.ax12_4,
                     self.ax30_4,self.ax32_4,self.ax40_4,
            self.ax42_4,self.ax50_4,self.ax52_4):
            axis.spines['top'].set_position(('outward', self.axis4))
            axis.spines['top'].set_color('m')
            #self.readdata.spines(axis)
        for axis in (self.ax30_5,self.ax32_5):
            axis.spines['top'].set_position(('outward', self.axis5))
            axis.spines['top'].set_color('c')              

        self.fig2_txt()
        
        for axis in (self.ax00,self.ax10,self.ax20,self.ax30,self.ax40,
            self.ax50,
            self.ax01,self.ax11,self.ax21,self.ax31,self.ax41,
            self.ax51,
            self.ax02,self.ax12,self.ax22,self.ax32,self.ax42,
            self.ax52):
            readdata.y_lim1(self,axis)  
             

        
        readdata.setmaxmin(self,self.ax00,self.kz,0) 
        readdata.setmaxmin(self,self.ax01,self.kz,0)
        readdata.setmaxmin(self,self.ax02,self.kz,1)       
                         
        readdata.setmaxmin(self,self.ax00_1,self.kz,0)
        readdata.setmaxmin(self,self.ax01_1,self.kz,0)  
        readdata.setmaxmin(self,self.ax02_1,self.kz,1)  
                      
        readdata.setmaxmin(self,self.ax00_2,self.sal,0)
        readdata.setmaxmin(self,self.ax01_2,self.sal,0) 
        readdata.setmaxmin(self,self.ax02_2,self.sal,1) 
                      
        readdata.setmaxmin(self,self.ax00_3,self.temp,0)
        readdata.setmaxmin(self,self.ax01_3,self.temp,0) 
        readdata.setmaxmin(self,self.ax02_3,self.temp,1)  
###########################################################  
       
        readdata.setmaxmin(self,self.ax10,self.o2,0) 
        readdata.setmaxmin(self,self.ax11,self.o2,0)
        readdata.setmaxmin(self,self.ax12,self.o2,1)        
                         
        readdata.setmaxmin(self,self.ax10_1,self.o2,0)
        readdata.setmaxmin(self,self.ax11_1,self.o2,0)  
        readdata.setmaxmin(self,self.ax12_1,self.o2,1)  
                      
        readdata.setmaxmin(self,self.ax10_2,self.nh4,0)
        readdata.setmaxmin(self,self.ax11_2,self.nh4,0) 
        readdata.setmaxmin(self,self.ax12_2,self.nh4,1) 
                       
        readdata.setmaxmin(self,self.ax10_3,self.no2,0)
        readdata.setmaxmin(self,self.ax11_3,self.no2,0) 
        readdata.setmaxmin(self,self.ax12_3,self.no2,1)                  

        readdata.setmaxmin(self,self.ax10_4,self.no3,0)
        readdata.setmaxmin(self,self.ax11_4,self.no3,0) 
        readdata.setmaxmin(self,self.ax12_4,self.no3,1)  
        
###############################################################        
        readdata.setmaxmin(self,self.ax20,self.po4,0) 
        readdata.setmaxmin(self,self.ax21,self.po4,0)
        readdata.setmaxmin(self,self.ax22,self.po4,1)        
                         
        readdata.setmaxmin(self,self.ax20_1,self.po4,0)
        readdata.setmaxmin(self,self.ax21_1,self.po4,0)  
        readdata.setmaxmin(self,self.ax22_1,self.po4,1)  
                      
        readdata.setmaxmin(self,self.ax20_2,self.pon,0)
        readdata.setmaxmin(self,self.ax21_2,self.pon,0) 
        readdata.setmaxmin(self,self.ax22_2,self.pon,1) 
                       
        readdata.setmaxmin(self,self.ax20_3,self.don,0)
        readdata.setmaxmin(self,self.ax21_3,self.don,0) 
        readdata.setmaxmin(self,self.ax22_3,self.don,1)                  


###############################################################        
        readdata.setmaxmin(self,self.ax30,self.mn2,0) 
        readdata.setmaxmin(self,self.ax31,self.mn2,0)
        readdata.setmaxmin(self,self.ax32,self.mn2,1)        
                         
        readdata.setmaxmin(self,self.ax30_1,self.mn2,0)
        readdata.setmaxmin(self,self.ax31_1,self.mn2,0)  
        readdata.setmaxmin(self,self.ax32_1,self.mn2,1)  
                      
        readdata.setmaxmin(self,self.ax30_2,self.mn3,0)
        readdata.setmaxmin(self,self.ax31_2,self.mn3,0) 
        readdata.setmaxmin(self,self.ax32_2,self.mn3,1) 
                       
        readdata.setmaxmin(self,self.ax30_3,self.mn4,0)
        readdata.setmaxmin(self,self.ax31_3,self.mn4,0) 
        readdata.setmaxmin(self,self.ax32_3,self.mn4,1)                  

        readdata.setmaxmin(self,self.ax30_4,self.mns,0)
        readdata.setmaxmin(self,self.ax31_4,self.mns,0) 
        readdata.setmaxmin(self,self.ax32_4,self.mns,1)
        
        readdata.setmaxmin(self,self.ax30_5,self.mnco3,0)
        readdata.setmaxmin(self,self.ax31_5,self.mnco3,0) 
        readdata.setmaxmin(self,self.ax32_5,self.mnco3,1)        
###############################################################        
        readdata.setmaxmin(self,self.ax40,self.fe2,0) 
        readdata.setmaxmin(self,self.ax41,self.fe2,0)
        readdata.setmaxmin(self,self.ax42,self.fe2,1)        
                         
        readdata.setmaxmin(self,self.ax40_1,self.fe2,0)
        readdata.setmaxmin(self,self.ax41_1,self.fe2,0)  
        readdata.setmaxmin(self,self.ax42_1,self.fe2,1)  
                      
        readdata.setmaxmin(self,self.ax40_2,self.fe3,0)
        readdata.setmaxmin(self,self.ax41_2,self.fe3,0) 
        readdata.setmaxmin(self,self.ax42_2,self.fe3,1) 
                       
        readdata.setmaxmin(self,self.ax40_3,self.fes,0)
        readdata.setmaxmin(self,self.ax41_3,self.fes,0) 
        readdata.setmaxmin(self,self.ax42_3,self.fes,1)                  

        readdata.setmaxmin(self,self.ax40_4,self.fes2,0)
        readdata.setmaxmin(self,self.ax41_4,self.fes2,0) 
        readdata.setmaxmin(self,self.ax42_4,self.fes2,1)
        
###############################################################        
        readdata.setmaxmin(self,self.ax50,self.so4,0) 
        readdata.setmaxmin(self,self.ax51,self.so4,0)
        readdata.setmaxmin(self,self.ax52,self.so4,1)        
                         
        readdata.setmaxmin(self,self.ax50_1,self.so4,0)
        readdata.setmaxmin(self,self.ax51_1,self.so4,0)  
        readdata.setmaxmin(self,self.ax52_1,self.so4,1)  
                      
        readdata.setmaxmin(self,self.ax50_2,self.s0,0)
        readdata.setmaxmin(self,self.ax51_2,self.s0,0) 
        readdata.setmaxmin(self,self.ax52_2,self.s0,1) 
                       
        readdata.setmaxmin(self,self.ax50_3,self.h2s,0)
        readdata.setmaxmin(self,self.ax51_3,self.h2s,0) 
        readdata.setmaxmin(self,self.ax52_3,self.h2s,1)                  

        readdata.setmaxmin(self,self.ax50_4,self.s2o3,0)
        readdata.setmaxmin(self,self.ax51_4,self.s2o3,0) 
        readdata.setmaxmin(self,self.ax52_4,self.s2o3,1)                                
            

        '''label = self.ax00_1.set_xlabel('Xlabel', fontsize = 9)
        ax.xaxis.set_label_coords(1.05, -0.025)'''
        
        for n in (self.ax00_1,self.ax02_1):         
            n.annotate(r'$\rm Kz $',
            xy=(self.labelaxis_x,self.labelaxis1_y),
            ha='left', va='center', xycoords='axes fraction',
            fontsize = self.xlabel_fontsize,color='g')  

        for n in (self.ax00_2,self.ax02_1): 
            n.annotate(r'$\rm S $',
        xy=(self.labelaxis_x,self.labelaxis2_y),
        ha='left', va='center', xycoords='axes fraction',
        fontsize = self.xlabel_fontsize,color='r')

        
        for n in (self.ax00_3,self.ax02_1):         
            n.annotate(r'$\rm T $',
        xy=(self.labelaxis_x,self.labelaxis3_y),
        ha='left', va='center', xycoords='axes fraction',
        fontsize = self.xlabel_fontsize,color='b')
                     
        '''for n in (self.ax00_2,self.ax02_2): 
            n.annotate(r'$\rm S $',
        xy=(self.labelaxis_x,self.labelaxis2_y),
        ha='left', va='center', xycoords='axes fraction',
        fontsize = self.xlabel_fontsize,color='r')

        
        for n in (self.ax00_3,self.ax02_3):         
            n.annotate(r'$\rm T $',
        xy=(self.labelaxis_x,self.labelaxis3_y),
        ha='left', va='center', xycoords='axes fraction',
        fontsize = self.xlabel_fontsize,color='b') '''
                 
        for n in (self.ax10_1,self.ax12_1):   
            n.annotate(r'$\rm O _2 $',
        xy=(self.labelaxis_x,self.labelaxis1_y),
        ha='left', va='center', xycoords='axes fraction',
        fontsize = self.xlabel_fontsize,color='g')   

        for n in (self.ax10_2,self.ax12_2):          
            n.annotate(r'$\rm NH _4 $',
        xy=(self.labelaxis_x,self.labelaxis2_y),
        ha='left', va='center', xycoords='axes fraction',
        fontsize = self.xlabel_fontsize, color='r') 
        
        for n in (self.ax10_3,self.ax12_3):  
            n.annotate(r'$\rm NO _2 $',
        xy=(self.labelaxis_x,self.labelaxis3_y),
        ha='left', va='center', xycoords='axes fraction',
        fontsize = self.xlabel_fontsize,color='b') 

        for n in (self.ax10_4,self.ax12_4):   
            n.annotate(r'$\rm NO _3 $',
        xy=(self.labelaxis_x,self.labelaxis4_y),
        ha='left', va='center',xycoords='axes fraction',
        fontsize = self.xlabel_fontsize,color='m')    
              
        for n in (self.ax20_1,self.ax22_1):           
            n.annotate(r'$\rm PO _4 $',
        xy=(self.labelaxis_x,self.labelaxis1_y),
        ha='left', va='center',xycoords='axes fraction',
        fontsize = self.xlabel_fontsize,color='g')                                 
              
        for n in (self.ax20_2,self.ax22_2):              
            n.annotate(r'$\rm PON $',
        xy=(self.labelaxis_x,self.labelaxis2_y),
        ha='left', va='center', xycoords='axes fraction',
        fontsize = self.xlabel_fontsize,color='r')    
         
        for n in (self.ax20_3,self.ax22_3):        
            n.annotate(r'$\rm DON $',
        xy=(self.labelaxis_x,self.labelaxis3_y),
        ha='left', va='center', xycoords='axes fraction',
        fontsize = self.xlabel_fontsize,color='b')
                            
        for n in (self.ax30_1,self.ax32_1):
            n.annotate(r'$\rm MnII $',
        xy=(self.labelaxis_x,self.labelaxis1_y),
        ha='left', va='center', xycoords='axes fraction', 
        fontsize = self.xlabel_fontsize,color='g') 
         
        for n in (self.ax30_2,self.ax32_2):          
            n.annotate(r'$\rm MnIII $',
        xy=(self.labelaxis_x,self.labelaxis2_y),
        ha='left', va='center', xycoords='axes fraction', 
        fontsize = self.xlabel_fontsize, color='r')  
                 
        for n in (self.ax30_3,self.ax32_3):          
            n.annotate(r'$\rm MnIV $',
        xy=(self.labelaxis_x,self.labelaxis3_y),
        ha='left', va='center', xycoords='axes fraction',
        fontsize = self.xlabel_fontsize,color='b')     

        for n in (self.ax30_4,self.ax32_4):                      
            n.annotate(r'$\rm MnS $',
        xy=(self.labelaxis_x,self.labelaxis4_y),
        ha='left', va='center',xycoords='axes fraction',
        fontsize = self.xlabel_fontsize,color='m')                    
  
        for n in (self.ax30_5,self.ax32_5):                      
            n.annotate(r'$\rm MnCO _3 $',
        xy=(self.labelaxis_x,self.labelaxis5_y),
        ha='left', va='center', xycoords='axes fraction',
        fontsize = self.xlabel_fontsize,color='c')  
                             
        for n in (self.ax40_1,self.ax42_1):                                                      
            n.annotate(r'$\rm FeII $',
        xy=(self.labelaxis_x,self.labelaxis1_y),
        ha='left', va='center',xycoords='axes fraction',
        fontsize = self.xlabel_fontsize,color='g')

        for n in (self.ax40_2,self.ax42_2):                                                              
            n.annotate(r'$\rm FeIII $',
        xy=(self.labelaxis_x,self.labelaxis2_y),
        ha='left', va='center', xycoords='axes fraction',
        fontsize = self.xlabel_fontsize,color='r')  
                                                                     
        for n in (self.ax40_3,self.ax42_3):
            n.annotate(r'$\rm FeS $',
        xy=(self.labelaxis_x,self.labelaxis3_y),
        ha='left', va='center', xycoords='axes fraction',
        fontsize = self.xlabel_fontsize, color='b')                                                                 

        for n in (self.ax40_4,self.ax42_4):
            n.annotate(r'$\rm FeS _2 $',
        xy=(self.labelaxis_x,self.labelaxis4_y),
        ha='left', va='center', xycoords='axes fraction',
        fontsize = self.xlabel_fontsize, color='m')
                                            
        for n in (self.ax50_2,self.ax52_1):   
            n.annotate(r'$\rm SO _4 $',
        xy=(self.labelaxis_x,self.labelaxis1_y),
        ha='left', va='center',xycoords='axes fraction',
        fontsize = self.xlabel_fontsize, color='g') 
        
        for n in (self.ax50_2,self.ax52_2):
            n.annotate(r'$\rm S ^0 $',
            xy=(self.labelaxis_x,self.labelaxis2_y),
            ha='left', va='center',xycoords='axes fraction',
            fontsize = self.xlabel_fontsize,color='r') 
            
        for n in (self.ax50_3,self.ax52_3):
            n.annotate(r'$\rm H _2 S $',
        xy=(self.labelaxis_x,self.labelaxis3_y),
        ha='left', va='center', xycoords='axes fraction',
        fontsize = self.xlabel_fontsize, color='b') 

        
        for n in (self.ax50_4,self.ax52_4):        
            n.annotate(r'$\rm S _2 O _3 $',
        xy=(self.labelaxis_x,self.labelaxis4_y),
        ha='left', va='center', xycoords='axes fraction',
        fontsize = self.xlabel_fontsize,color='m')
        
                                                                                                                                                


                  
        # plot data
        self.ax00_1.plot(self.kz[self.numday],self.depth2,'g-')  
        self.ax01_1.plot(self.kz[self.numday],self.depth2,'go-')  #
                
        self.ax02_1.plot(self.kz[self.numday],self.depth_sed2,'go-')                          
        self.ax00_2.plot(self.sal[self.numday],self.depth,'r-')   
        self.ax01_2.plot(self.sal[self.numday],self.depth,'ro-')   
        self.ax02_2.plot(self.sal[self.numday],self.depth_sed,'ro-') 
        self.ax00_3.plot(self.temp[self.numday],self.depth,'b-') 
        self.ax01_3.plot(self.temp[self.numday],self.depth,'bo-')  
        self.ax02_3.plot(self.temp[self.numday],self.depth_sed,'bo-')                 
                            
        self.ax10_1.plot(self.o2[self.numday], self.depth, 'g-')
        self.ax11_1.plot(self.o2[self.numday], self.depth, 'go-')
        self.ax12_1.plot(self.o2[self.numday], self.depth_sed, 'go-')                 
        self.ax10_2.plot(self.nh4[self.numday], self.depth, 'r-')
        self.ax11_2.plot(self.nh4[self.numday], self.depth, 'ro-') 
        self.ax12_2.plot(self.nh4[self.numday], self.depth_sed, 'ro-')                
        self.ax10_3.plot(self.no2[self.numday], self.depth, 'b-')
        self.ax11_3.plot(self.no2[self.numday], self.depth, 'bo-') 
        self.ax12_3.plot(self.no2[self.numday], self.depth_sed, 'bo-')                 
        self.ax10_4.plot(self.no3[self.numday], self.depth, 'm-')        
        self.ax11_4.plot(self.no3[self.numday], self.depth, 'mo-')  
        self.ax12_4.plot(self.no3[self.numday], self.depth_sed, 'mo-') 
                       
        self.ax20_1.plot(self.po4[self.numday], self.depth, 'g-') 
        self.ax21_1.plot(self.po4[self.numday], self.depth, 'go-') 
        self.ax22_1.plot(self.po4[self.numday], self.depth_sed, 'go-')  
                      
        self.ax20_2.plot(self.pon[self.numday], self.depth, 'r-')
        self.ax21_2.plot(self.pon[self.numday], self.depth, 'ro-')
        self.ax22_2.plot(self.pon[self.numday], self.depth_sed, 'ro-')   
                     
        self.ax20_3.plot(self.don[self.numday], self.depth, 'b-') 
        self.ax21_3.plot(self.don[self.numday], self.depth, 'bo-')  
        self.ax22_3.plot(self.don[self.numday], self.depth_sed, 'bo-')                
               
        self.ax30_1.plot(self.mn2[self.numday], self.depth, 'g-') 
        self.ax31_1.plot(self.mn2[self.numday], self.depth, 'go-') 
        self.ax32_1.plot(self.mn2[self.numday], self.depth_sed, 'go-')               
        self.ax30_2.plot(self.mn3[self.numday], self.depth, 'r-')
        self.ax31_2.plot(self.mn3[self.numday], self.depth, 'ro-') 
        self.ax32_2.plot(self.mn3[self.numday], self.depth_sed, 'ro-')                
        self.ax30_3.plot(self.mn4[self.numday], self.depth, 'b-') 
        self.ax31_3.plot(self.mn4[self.numday], self.depth, 'bo-') 
        self.ax32_3.plot(self.mn4[self.numday], self.depth_sed, 'bo-')                
        self.ax30_4.plot(self.mns[self.numday], self.depth, 'm-')  
        self.ax31_4.plot(self.mns[self.numday], self.depth, 'mo-') 
        self.ax32_4.plot(self.mns[self.numday], self.depth_sed, 'mo-')                     
        self.ax30_5.plot(self.mnco3[self.numday], self.depth, 'c-')   
        self.ax31_5.plot(self.mnco3[self.numday], self.depth, 'co-')  
        self.ax32_5.plot(self.mnco3[self.numday], self.depth_sed, 'co-')                       

        self.ax40_1.plot(self.fe2[self.numday], self.depth, 'g-') 
        self.ax41_1.plot(self.fe2[self.numday], self.depth, 'g-')  
        self.ax42_1.plot(self.fe2[self.numday], self.depth_sed, 'go-')               
        self.ax40_2.plot(self.fe3[self.numday], self.depth, 'r-')
        self.ax41_2.plot(self.fe3[self.numday], self.depth, 'ro-') 
        self.ax42_2.plot(self.fe3[self.numday], self.depth_sed, 'ro-')                
        self.ax40_3.plot(self.fes[self.numday], self.depth, 'b-') 
        self.ax41_3.plot(self.fes[self.numday], self.depth, 'bo-')  
        self.ax42_3.plot(self.fes[self.numday], self.depth_sed, 'bo-')              
        self.ax40_4.plot(self.fes2[self.numday], self.depth, 'm-')  
        self.ax41_4.plot(self.fes2[self.numday], self.depth, 'mo-')
        self.ax42_4.plot(self.fes2[self.numday], self.depth_sed, 'mo-')
        self.ax50_1.plot(self.so4[self.numday], self.depth, 'g-') 
        self.ax51_1.plot(self.so4[self.numday], self.depth, 'go-') 
        self.ax52_1.plot(self.so4[self.numday], self.depth_sed, 'go-')                
        self.ax50_2.plot(self.s0[self.numday], self.depth, 'r-')
        self.ax51_2.plot(self.s0[self.numday], self.depth, 'ro-') 
        self.ax52_2.plot(self.s0[self.numday], self.depth_sed, 'ro-')                
        self.ax50_3.plot(self.h2s[self.numday], self.depth, 'b-') 
        self.ax51_3.plot(self.h2s[self.numday], self.depth, 'bo-')  
        self.ax52_3.plot(self.h2s[self.numday], self.depth_sed, 'bo-')              
        self.ax50_4.plot(self.s2o3[self.numday], self.depth, 'm-')  
        self.ax51_4.plot(self.s2o3[self.numday], self.depth, 'mo-')
        self.ax52_4.plot(self.s2o3[self.numday], self.depth_sed, 'mo-')


        self.canvas.draw()        
        
        
                
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    app.setStyle("plastique")
    main = Window()#None, QtCore.Qt.WindowSystemMenuHint | 
                    #     QtCore.Qt.WindowTitleHint)#QtGui.QWidget()
    #main.setWindowFlags(
    #    main.windowFlags() | QtCore.Qt.FramelessWindowHint)

    
    #setWindowFlags(windowFlags() & ~Qt::WindowContextHelpButtonHint);
    #main = QtGui.QDialog
    main.setStyleSheet("background-color:#d8c9c2;")
    main.show()
    #PySide.QtCore.Qt.WindowFlags
    sys.exit(app.exec_()) 
