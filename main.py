## General Interactive Dashboard
## A hopefully idiot-proof self-service reporting tool for the technically illiterate
## Cache McClure


## Import Modules
from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from pyqtgraph.dockarea import *
from sqlalchemy import create_engine
import pandas as pd
import polars as pl
from pickle import load as pload
from pickle import dump as pdump
import plotly.express as px
from datetime import datetime
from dateutil.relativedelta import relativedelta
import dateutil.parser as parser
import re
from os.path import exists
import sys


## Classes
## Dock Area
class DockArea(DockArea):
    ## This is to prevent the Dock from being resized
    def makeContainer(self, typ):
        new = super(DockArea, self).makeContainer(typ)
        new.setChildrenCollapsible(False)
        return new


## Main Window
class mainWindow(QMainWindow):
    ## Initialize Class
    def __init__(self):
        super(mainWindow,self).__init__()
        self.initUI()
    

    ## Initialize User Interface
    def initUI(self):
        ## Initial Setup
        central_widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        ## Dock Area
        dock_area = DockArea(self)

        ## Dock 1
        self.dock1 = Dock('Widget 1',size=(300,500))
        self.dock1.hideTitleBar()
        dock_area.addDock(self.dock1)

        ## Dock 2
        self.dock2 = Dock('Widget 2',size=(400,500))
        self.dock2.hideTitleBar()
        dock_area.addDock(self.dock2,'right',self.dock1)

        ## Add Widgets
        self.widget_one = FilterWidget(self)
        self.widget_two = PlotlyWidget(self)
        
        ## Filter and Label Defs
        self.filter_defs = {1:self.widget_one.filter_one,
                            2:self.widget_one.filter_two,
                            3:self.widget_one.filter_three,
                            4:self.widget_one.filter_four,
                            5:self.widget_one.filter_five,
                            6:self.widget_one.filter_six,
                            7:self.widget_one.filter_seven,
                            8:self.widget_one.filter_eight,
                            9:self.widget_one.filter_nine,
                            10:self.widget_one.filter_ten}
        
        self.label_defs = {1:self.widget_one.label_one,
                           2:self.widget_one.label_two,
                           3:self.widget_one.label_three,
                           4:self.widget_one.label_four,
                           5:self.widget_one.label_five,
                           6:self.widget_one.label_six,
                           7:self.widget_one.label_seven,
                           8:self.widget_one.label_eight,
                           9:self.widget_one.label_nine,
                           10:self.widget_one.label_ten}
        
        self.start_date_filter_defs = {1:self.widget_one.startDate1_filter,
                                       2:self.widget_one.startDate2_filter,
                                       3:self.widget_one.startDate3_filter,
                                       4:self.widget_one.startDate4_filter,
                                       5:self.widget_one.startDate5_filter}
        
        self.start_date_label_defs = {1:self.widget_one.startDate1_label,
                                      2:self.widget_one.startDate2_label,
                                      3:self.widget_one.startDate3_label,
                                      4:self.widget_one.startDate4_label,
                                      5:self.widget_one.startDate5_label}
        
        self.end_date_filter_defs = {1:self.widget_one.endDate1_filter,
                                     2:self.widget_one.endDate2_filter,
                                     3:self.widget_one.endDate3_filter,
                                     4:self.widget_one.endDate4_filter,
                                     5:self.widget_one.endDate5_filter}
        self.end_date_label_defs = {1:self.widget_one.endDate1_label,
                                    2:self.widget_one.endDate2_label,
                                    3:self.widget_one.endDate3_label,
                                    4:self.widget_one.endDate4_label,
                                    5:self.widget_one.endDate5_label}

        ## Buttons
        ## Exit Button
        self.exit_b = QtWidgets.QPushButton(self)
        self.exit_b.setText('Exit')
        self.exit_b.clicked.connect(self.close)

        ## Plot Button
        self.plot_b = QtWidgets.QPushButton(self)
        self.plot_b.setText('Plot')
        self.plot_b.clicked.connect(self.showPlot)

        ## Retrieve Data Button
        self.ret_b = QtWidgets.QPushButton(self)
        self.ret_b.setText('Retrieve Data')
        self.ret_b.clicked.connect(self.retData)
        self.ret_label = QtWidgets.QLabel(self)
        self.ret_label.setText('No Data')
        self.ret_label.setFixedHeight(30)
        self.ret_label.setAlignment(QtCore.Qt.AlignCenter)

        ## Export to CSV Button
        self.export_b = QtWidgets.QPushButton(self)
        self.export_b.setText('Export Plot Data to CSV')
        self.export_b.clicked.connect(self.exportCSV)

        ## Formatting Dock Area
        layout.addWidget(dock_area)
        layout.addWidget(self.ret_label)
        layout.addWidget(self.ret_b)
        layout.addWidget(self.plot_b)
        layout.addWidget(self.export_b)
        layout.addWidget(self.exit_b)
        self.dock1.addWidget(self.widget_one)
        self.dock2.addWidget(self.widget_two)
        self.setGeometry(100,100,900,600)

        ## Connect Date Filter Buttons to Fx
        #self.widget_one.startDate_filter.dateChanged.connect(self.onStartDateChanged)
        #self.widget_one.endDate_filter.dateChanged.connect(self.onEndDateChanged)

        ## Connect Filters to Fx
        #self.widget_one.storefront_filter.activated.connect(self.updateFilters)
        #self.widget_one.partner_filter.activated.connect(self.updateFilters)
        #self.widget_one.brand_filter.activated.connect(self.updateFilters)
        #self.widget_one.category_filter.activated.connect(self.updateFilters)
        #self.widget_one.type_filter.activated.connect(self.updateFilters)
        #self.widget_one.subType_filter.activated.connect(self.updateFilters)
        #self.widget_one.orderType_filter.activated.connect(self.updateFilters)
        #self.widget_one.status_filter.activated.connect(self.updateFilters)
        #self.widget_one.province_filter.activated.connect(self.updateFilters)

        ## Connect Reset Filters button to Fx 
        self.widget_one.reset_b.clicked.connect(self.resetFilters)

        ## Set Initial Filters
#        self.filters = {'report':'Revenue',
#                        'storefront_name':'All',
#                        'partner':'All',
#                        'brand':'All',
#                        'product_category':'All',
#                        'product_type':'All',
#                        'product_subtype':'All',
#                        'order_type':'All',
#                        'order_status':'All',
#                        'province':'All',
#                        'start_date':(datetime.today()-relativedelta(years=1)).strftime('%Y-%m-%d'),
#                        'end_date':datetime.today().strftime('%Y-%m-%d')}
    
    
    def onDateChange(self,
                     field:str,
                     newDate):
        self.filters['datetime'][field]['filter'] = newDate.toString("yyy-MM-dd")
    

    def retData(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename,_ = QFileDialog.getOpenFileName(self,"Choose data file","","All Files (*)",options=options)
        if filename:
            self.readData(filename)
            self.setDimsMets()
            self.setFilters()
            #print(self.dimensions)
            #print(self.metrics)
            #print(self.datetimes)
        return
    
    
    def setFilters(self):
        self.filters = {'dimensions':[],
                        'metrics':[],
                        'datetime':[]}
        iter = 1
        for dim in self.dimensions:
            while iter < 10:
                self.filters['dimensions'][dim] = {'filter':self.filter_defs[iter],
                                                   'label':self.label_defs[iter],
                                                   'filter_entries':['All'],
                                                   'current_selection':'All'}
                iter += 1
                self.filters['dimensions'][dim]['filter_entries'] += self.pldf.select(pl.col(dim)).unique().get_columns()[0].to_list()
                self.filters['dimensions'][dim]['label'].setText(dim)
                self.filters['dimensions'][dim]['filter'].clear()
                self.filters['dimensions'][dim]['filter'].addItems(self.filters['dimensions'][dim]['filter_entries'])
                self.filters['dimensions'][dim]['label'].setVisible(True)
                self.filters['dimensions'][dim]['filter'].setVisible(True)
        iter = 1
        for field in self.datetimes:
            while iter < 5:
                self.filters['datetime'][field] = {'start_filter':self.start_date_filter_defs[iter],
                                                   'start_label':self.start_date_label_defs[iter],
                                                   'end_filter':self.end_date_filter_defs[iter],
                                                   'end_label':self.end_date_label_defs[iter],
                                                   'start_date':(datetime.today()-relativedelta(years=1)).strftime('%Y-%m-%d'),
                                                   'end_date':datetime.today().strftime('%Y-%m-%d')}
                self.filters['datetime'][field]['start_label'].setText(f'Start {dim}')
                self.filters['datetime'][field]['start_label'].setVisible(True)
                self.filters['datetime'][field]['start_filter'].setVisible(True)
                self.filters['datetime'][field]['end_label'].setText(f'End {dim}')
                self.filters['datetime'][field]['end_label'].setVisible(True)
                self.filters['datetime'][field]['end_filter'].setVisible(True)
                iter += 1
        return
    

    def setDimsMets(self):
        self.dimensions = []
        self.metrics = []
        self.datetimes = []
        row_count = self.rawdf.select(pl.count()).collect().item()
        dim_types = [pl.Boolean,
                     pl.Binary,
                     pl.Categorical]
        met_types = [pl.Float32,
                     pl.Float64]
        num_types = [pl.Int8,
                     pl.Int16,
                     pl.Int32,
                     pl.Int64,
                     pl.UInt8,
                     pl.UInt16,
                     pl.UInt32,
                     pl.UInt64]
        unk_types = [pl.Unknown,
                     pl.Object]
        for col in self.rawdf.columns:
            col_type = self.rawdf.select(col).dtypes[0]
            if col_type == pl.Utf8:
                temp = self.rawdf.select(col).filter(~pl.col(col).is_null()).limit(1).collect().item()
                try:
                    test = parser.parse(temp)
                except:
                    test = None
                if test:
                    self.datetimes += [col]
                else:
                    self.dimensions += [col]
            elif col_type in dim_types:
                self.dimensions += [col]
            elif col_type in met_types:
                self.metrics += [col]
            else:
                item_count = self.rawdf.select(pl.col(col)).collect().n_unique()
                if (item_count/row_count) > 0.1:
                    self.metrics += [col]
                else:
                    self.dimensions += [col]
        self.pldf = self.rawdf.collect().select([pl.col(column) for column in self.dimensions]+\
            [pl.col(column) for column in self.metrics]+\
            [pl.col(column).str.strptime(pl.Datetime) for column in self.datetimes])
        return
    
    
    def readData(self,filename):
        with open(filename,'r') as f:
            temp = f.read()
        first_line = temp[:temp.find('\n')]
        common_delim = ['\t',',','|']
        separator = ''
        no_cols = 1
        for delim in common_delim:
            sep_ct = first_line.count(delim)
            if (sep_ct + 1) > no_cols:
                separator = delim 
                no_cols = sep_ct + 1
        del temp
        if no_cols == 1:
            raise Exception('Delimiter cannot be determined')
        self.rawdf = pl.scan_csv(source=filename,separator=separator)
        #print(self.rawdf.select(pl.count()).collect().item())
        return


    def updateFilters_old(self):
        self.filters['storefront_name'] = self.widget_one.storefront_filter.currentText()
        self.filters['partner'] = self.widget_one.partner_filter.currentText()
        self.filters['brand'] = self.widget_one.brand_filter.currentText()
        self.filters['product_category'] = self.widget_one.category_filter.currentText()
        self.filters['product_type'] = self.widget_one.type_filter.currentText()
        self.filters['product_subtype'] = self.widget_one.subType_filter.currentText()
        self.filters['order_type'] = self.widget_one.orderType_filter.currentText()
        self.filters['order_status'] = self.widget_one.status_filter.currentText()
        self.filters['province'] = self.widget_one.province_filter.currentText()

        filterdf = self.rawdf
        filtered_fields = [filter_0 for filter_0 in self.filters if (self.filters[filter_0] != 'All') and 
                           (filter_0 not in ['start_date','end_date','report'])]
        unfiltered_fields = [filter_0 for filter_0 in self.filters if (self.filters[filter_0] == 'All') and 
                           (filter_0 not in ['start_date','end_date','report'])]

        for filter_0 in filtered_fields:
            filterdf = filterdf[filterdf[filter_0]==self.filters[filter_0]]
        
        filter_objects = {'storefront_name':self.widget_one.storefront_filter,
                          'partner':self.widget_one.partner_filter,
                          'brand':self.widget_one.brand_filter,
                          'product_category':self.widget_one.category_filter,
                          'product_type':self.widget_one.type_filter,
                          'product_subtype':self.widget_one.subType_filter,
                          'order_type':self.widget_one.orderType_filter,
                          'order_status':self.widget_one.status_filter,
                          'province':self.widget_one.province_filter}
        
        for filter_0 in unfiltered_fields:
            filter_objects[filter_0].clear()
            filter_objects[filter_0].addItem('All')
            filter_objects[filter_0].addItems(sorted(filter(None,list(set(filterdf[filter_0])))))
    
    
    def updateFilters(self):
        for field in self.filters['dimensions']:
            temp_filter = self.filters['dimensions'][field]
            temp_filter['current_selection'] = temp_filter['filter'].currentText
            self.filterd_df = self.pldf.filter(pl.col(field) == temp_filter['current_selection'])
        for field in self.filters['datetime']:
            temp_filter = self.filters['datetime'][field]
        for field in self.filters['dimensions']:
            if self.filters['dimensions'][field]['current_selection'] == 'All':
                temp_filter = self.filters['dimensions'][field]
                temp_filter['filter_entries'] = self.filtered_df.select(pl.col(field)).unique().get_columns()[0].to_list()
                temp_filter['filter'].clear()
                temp_filter['filter'].addItem('All')
                temp_filter['filter'].addItems(sorted(filter(None,list(set(temp_filter['filter_entries'])))))
        return
    

    def popFilters(self):
        self.widget_one.storefront_filter.addItems(sorted(filter(None,list(set(self.rawdf['storefront_name'])))))
        self.widget_one.partner_filter.addItems(sorted(filter(None,list(set(self.rawdf['partner'])))))
        self.widget_one.brand_filter.addItems(sorted(filter(None,list(set(self.rawdf['brand'])))))
        self.widget_one.category_filter.addItems(sorted(filter(None,list(set(self.rawdf['product_category'])))))
        self.widget_one.type_filter.addItems(sorted(filter(None,list(set(self.rawdf['product_type'])))))
        self.widget_one.subType_filter.addItems(sorted(filter(None,list(set(self.rawdf['product_subtype'])))))
        self.widget_one.orderType_filter.addItems(sorted(filter(None,list(set(self.rawdf['order_type'])))))
        self.widget_one.status_filter.addItems(sorted(filter(None,list(set(self.rawdf['order_status'])))))
        self.widget_one.province_filter.addItems(sorted(filter(None,list(set(self.rawdf['province'])))))
    

    def resetFilters(self):
        self.widget_one.startDate_filter.setDate(QtCore.QDate.currentDate().addYears(-1))
        self.widget_one.endDate_filter.setDate(QtCore.QDate.currentDate())

        self.widget_one.storefront_filter.clear()
        self.widget_one.partner_filter.clear()
        self.widget_one.brand_filter.clear()
        self.widget_one.category_filter.clear()
        self.widget_one.type_filter.clear()
        self.widget_one.subType_filter.clear()
        self.widget_one.orderType_filter.clear()
        self.widget_one.status_filter.clear()
        self.widget_one.province_filter.clear()

        self.widget_one.storefront_filter.addItem('All')
        self.widget_one.partner_filter.addItem('All')
        self.widget_one.brand_filter.addItem('All')
        self.widget_one.category_filter.addItem('All')
        self.widget_one.type_filter.addItem('All')
        self.widget_one.subType_filter.addItem('All')
        self.widget_one.orderType_filter.addItem('All')
        self.widget_one.status_filter.addItem('All')
        self.widget_one.province_filter.addItem('All')

        self.popFilters()


    def showPlot_test(self):
        df = px.data.tips()
        fig = px.box(df,
                     x="day",
                     y="total_bill",
                     color="smoker")
        fig.update_traces(quartilemethod="exclusive")
        self.widget_two.browser.setHtml(fig.to_html(include_plotlyjs='cdn'))
    

    def showPlot(self):
        try:
            self.filters['report'] = self.widget_one.report_type.currentText()
            self.filters['storefront_name'] = self.widget_one.storefront_filter.currentText()
            self.filters['partner'] = self.widget_one.partner_filter.currentText()
            self.filters['brand'] = self.widget_one.brand_filter.currentText()
            self.filters['product_category'] = self.widget_one.category_filter.currentText()
            self.filters['product_type'] = self.widget_one.type_filter.currentText()
            self.filters['product_subtype'] = self.widget_one.subType_filter.currentText()
            self.filters['order_type'] = self.widget_one.orderType_filter.currentText()
            self.filters['order_status'] = self.widget_one.status_filter.currentText()
            self.filters['province'] = self.widget_one.province_filter.currentText()

            ## Filter rawdf
            self.adf = self.rawdf[(self.rawdf['created_at']>datetime.strptime(self.filters['start_date'],"%Y-%m-%d").date()) &
                              (self.rawdf['created_at']<datetime.strptime(self.filters['end_date'],"%Y-%m-%d").date())]
            if self.filters['storefront_name'] != 'All':
                self.adf = self.adf[(self.rawdf['storefront_name']==self.filters['storefront_name'])]
            if self.filters['partner'] != 'All':
                self.adf = self.adf[(self.adf['partner']==self.filters['partner'])]
            if self.filters['brand'] != 'All':
                self.adf = self.adf[(self.adf['brand']==self.filters['brand'])]
            if self.filters['product_category'] != 'All':
                self.adf = self.adf[(self.adf['product_category']==self.filters['product_category'])]
            if self.filters['product_type'] != 'All':
                self.adf = self.adf[(self.adf['product_type']==self.filters['product_type'])]
            if self.filters['product_subtype'] != 'All':
                self.adf = self.adf[(self.adf['product_subtype']==self.filters['product_subtype'])]
            if self.filters['order_type'] != 'All':
                self.adf = self.adf[(self.adf['order_type']==self.filters['order_type'])]
            if self.filters['order_status'] != 'All':
                self.adf = self.adf[(self.adf['order_status']==self.filters['order_status'])]
            if self.filters['province'] != 'All':
                self.adf = self.adf[(self.adf['province']==self.filters['province'])]

            ## Report Chooser
            if self.filters['report'] == 'Revenue':
                self.showPlot_revenue()
            elif self.filters['report'] == 'Orders':
                self.showPlot_orders()
            elif self.filters['report'] == 'AOV':
                self.showPlot_aov()
            elif self.filters['report'] == 'Bottles':
                self.showPlot_bottles()
            elif self.filters['report'] == 'Customers':
                self.showPlot_customers()
        except Exception as err:
            print(str(err)[:250])
            self.ret_label.setText('Please use "Retrieve Data" first before trying to plot data')
    

    def showPlot_revenue(self):
        self.adf = self.adf[['created_at','revenue']]
        self.adf = self.adf.sort_values(by=['created_at'])
        self.adf = self.adf.groupby(['created_at']).sum().reset_index()
        roll_df = self.adf.rolling(7,min_periods=1).agg('mean')
        self.adf['rolling_revenue'] = roll_df['revenue']
        fig = px.line(self.adf,
                      x='created_at',
                      y=['revenue','rolling_revenue'],
                      labels={'rolling_revenue':'Rolling Revenue',
                              'revenue':'Revenue',
                              'created_at':'Order Creation',
                              'value':'Revenue'},
                      title='Revenue')
        newnames = {'rolling_revenue':'Rolling Revenue',
                    'revenue':'Revenue'}
        fig.for_each_trace(lambda t: t.update(name=newnames[t.name],
                                              legendgroup=newnames[t.name],
                                              hovertemplate=t.hovertemplate.replace(t.name,
                                                                                    newnames[t.name])))
        fig.update_layout(yaxis_tickprefix='$',yaxis_tickformat=',.2f',legend_title='Legend')
        self.widget_two.browser.setHtml(fig.to_html(include_plotlyjs='cdn'))
    

    def showPlot_orders(self):
        self.adf = self.adf[['created_at','order_number']]
        self.adf = self.adf.sort_values(by=['created_at'])
        self.adf = self.adf.groupby(['created_at']).agg({'order_number':pd.Series.nunique}).reset_index()
        roll_df = self.adf.rolling(7,min_periods=1).agg('mean')
        self.adf['rolling_order_number'] = roll_df['order_number']
        fig = px.line(self.adf,
                      x='created_at',
                      y=['order_number','rolling_order_number'],
                      labels={'rolling_order_number':'Rolling Order Count',
                              'order_number':'Order Count',
                              'created_at':'Order Creation',
                              'value':'Order Count'},
                      title='Orders')
        newnames = {'rolling_order_number':'Rolling Order Count',
                    'order_number':'Order Count'}
        fig.for_each_trace(lambda t: t.update(name=newnames[t.name],
                                              legendgroup=newnames[t.name],
                                              hovertemplate=t.hovertemplate.replace(t.name,
                                                                                    newnames[t.name])))
        fig.update_layout(legend_title='Legend')
        self.widget_two.browser.setHtml(fig.to_html(include_plotlyjs='cdn'))
    

    def showPlot_aov(self):
        self.adf = self.adf[['created_at','order_number','revenue']]
        self.adf = self.adf.sort_values(by=['created_at'])
        self.adf = self.adf.groupby(['created_at','order_number']).sum().reset_index()
        self.adf = self.adf.drop(columns=['order_number']).groupby(['created_at']).agg('mean').reset_index()
        roll_df = self.adf.rolling(7,min_periods=1).agg('mean')
        self.adf['rolling_revenue'] = roll_df['revenue']
        fig = px.line(self.adf,
                      x='created_at',
                      y=['revenue','rolling_revenue'],
                      labels={'rolling_revenue':'Rolling AOV',
                              'revenue':'AOV',
                              'created_at':'Order Creation',
                              'value':'AOV'},
                      title='Average Order Value')
        newnames = {'rolling_revenue':'Rolling AOV',
                    'revenue':'AOV'}
        fig.for_each_trace(lambda t: t.update(name=newnames[t.name],
                                              legendgroup=newnames[t.name],
                                              hovertemplate=t.hovertemplate.replace(t.name,
                                                                                    newnames[t.name])))
        fig.update_layout(yaxis_tickprefix='$',yaxis_tickformat=',.2f',legend_title='Legend')
        self.widget_two.browser.setHtml(fig.to_html(include_plotlyjs='cdn'))
    

    def showPlot_bottles(self):
        self.adf = self.adf[['created_at','quantity']]
        self.adf = self.adf.sort_values(by=['created_at'])
        self.adf = self.adf.groupby(['created_at']).sum().reset_index()
        roll_df = self.adf.rolling(7,min_periods=1).agg('mean')
        self.adf['rolling_quantity'] = roll_df['quantity']
        fig = px.line(self.adf,
                      x='created_at',
                      y=['quantity','rolling_quantity'],
                      labels={'rolling_quantity':'Rolling Bottle Count',
                              'quantity':'Bottle Count',
                              'created_at':'Order Creation',
                              'value':'Bottle Count'},
                      title='Bottle Count')
        newnames = {'rolling_quantity':'Rolling Bottle Count',
                    'quantity':'Bottle Count'}
        fig.for_each_trace(lambda t: t.update(name=newnames[t.name],
                                              legendgroup=newnames[t.name],
                                              hovertemplate=t.hovertemplate.replace(t.name,
                                                                                    newnames[t.name])))
        fig.update_layout(legend_title='Legend')
        self.widget_two.browser.setHtml(fig.to_html(include_plotlyjs='cdn'))
    

    def showPlot_customers(self):
        self.adf = self.adf[['created_at','customer_id']]
        self.adf = self.adf.sort_values(by=['created_at'])
        self.adf = self.adf.groupby(['created_at']).agg({'customer_id':pd.Series.nunique}).reset_index()
        roll_df = self.adf.rolling(7,min_periods=1).agg('mean')
        self.adf['rolling_customer_id'] = roll_df['customer_id']
        fig = px.line(self.adf,
                      x='created_at',
                      y=['customer_id','rolling_customer_id'],
                      labels={'rolling_customer_id':'Rolling Customer Count',
                              'customer_id':'Customer Count',
                              'created_at':'Order Creation',
                              'value':'Customer Count'},
                      title='Customer Count')
        newnames = {'rolling_customer_id':'Rolling Customer Count',
                    'customer_id':'Customer Count'}
        fig.for_each_trace(lambda t: t.update(name=newnames[t.name],
                                              legendgroup=newnames[t.name],
                                              hovertemplate=t.hovertemplate.replace(t.name,
                                                                                    newnames[t.name])))
        fig.update_layout(legend_title='Legend')
        self.widget_two.browser.setHtml(fig.to_html(include_plotlyjs='cdn'))


    def exportCSV(self):
        try:
            self.adf.to_csv('exported_data.csv',index=False,header=True)
            self.ret_label.setText('Data Exported Successfully!')
        except Exception as err:
            print(str(err)[:250])
            self.ret_label.setText('Data not exported. Make sure a plot is generated before attempting to export!')


## Filter Panel
class FilterWidget(QtWidgets.QWidget):
    ## Initialize Class
    def __init__(self,
                 parent):
        super(FilterWidget,self).__init__(parent)
        self.initWidget()
    

    ## Initialize Widget Elements
    def initWidget(self):
        ## Report Type
        vis_label = QtWidgets.QLabel()
        vis_label.setText('Report Type')
        self.vis_type = QtWidgets.QComboBox()
        self.vis_type.addItems(['Time-series',
                                'Pie Chart',
                                'Bar Chart'])

        ## Filters
        self.filter_one = QtWidgets.QComboBox()
        self.filter_one.addItem('All')
        self.filter_two = QtWidgets.QComboBox()
        self.filter_two.addItem('All')
        self.filter_three = QtWidgets.QComboBox()
        self.filter_three.addItem('All')
        self.filter_four = QtWidgets.QComboBox()
        self.filter_four.addItem('All')
        self.filter_five = QtWidgets.QComboBox()
        self.filter_five.addItem('All')
        self.filter_six = QtWidgets.QComboBox()
        self.filter_six.addItem('All')
        self.filter_seven = QtWidgets.QComboBox()
        self.filter_seven.addItem('All')
        self.filter_eight = QtWidgets.QComboBox()
        self.filter_eight.addItem('All')
        self.filter_nine = QtWidgets.QComboBox()
        self.filter_nine.addItem('All')
        self.filter_ten = QtWidgets.QComboBox()
        self.filter_ten.addItem('All')
        self.startDate1_filter = QtWidgets.QDateEdit()
        self.startDate1_filter.setDate(QtCore.QDate.currentDate().addYears(-1))
        self.endDate1_filter = QtWidgets.QDateEdit()
        self.endDate1_filter.setDate(QtCore.QDate.currentDate())
        self.startDate2_filter = QtWidgets.QDateEdit()
        self.startDate2_filter.setDate(QtCore.QDate.currentDate().addYears(-1))
        self.endDate2_filter = QtWidgets.QDateEdit()
        self.endDate2_filter.setDate(QtCore.QDate.currentDate())
        self.startDate3_filter = QtWidgets.QDateEdit()
        self.startDate3_filter.setDate(QtCore.QDate.currentDate().addYears(-1))
        self.endDate3_filter = QtWidgets.QDateEdit()
        self.endDate3_filter.setDate(QtCore.QDate.currentDate())
        self.startDate4_filter = QtWidgets.QDateEdit()
        self.startDate4_filter.setDate(QtCore.QDate.currentDate().addYears(-1))
        self.endDate4_filter = QtWidgets.QDateEdit()
        self.endDate4_filter.setDate(QtCore.QDate.currentDate())
        self.startDate5_filter = QtWidgets.QDateEdit()
        self.startDate5_filter.setDate(QtCore.QDate.currentDate().addYears(-1))
        self.endDate5_filter = QtWidgets.QDateEdit()
        self.endDate5_filter.setDate(QtCore.QDate.currentDate())

        ## Labels
        self.label_one = QtWidgets.QLabel()
        #self.label_one.setText('Storefront')
        self.label_two = QtWidgets.QLabel()
        #self.label_two.setText('Partner')
        self.label_three = QtWidgets.QLabel()
        #self.label_three.setText('Brand')
        self.label_four = QtWidgets.QLabel()
        #self.label_four.setText('Product Category')
        self.label_five = QtWidgets.QLabel()
        #self.label_five.setText('Product Type')
        self.label_six = QtWidgets.QLabel()
        #self.label_six.setText('Product Sub-type')
        self.label_seven = QtWidgets.QLabel()
        #self.label_seven.setText('Order Type')
        self.label_eight = QtWidgets.QLabel()
        #self.label_eight.setText('Order Status')
        self.label_nine = QtWidgets.QLabel()
        #self.label_nine.setText('Order Status')
        self.label_ten = QtWidgets.QLabel()
        #self.label_ten.setText('Order Status')
        self.startDate1_label = QtWidgets.QLabel()
        #self.startDate_label.setText('Start Date')
        self.endDate1_label = QtWidgets.QLabel()
        #self.endDate_label.setText('End Date')
        self.startDate2_label = QtWidgets.QLabel()
        #self.startDate_label.setText('Start Date')
        self.endDate2_label = QtWidgets.QLabel()
        #self.endDate_label.setText('End Date')
        self.startDate3_label = QtWidgets.QLabel()
        #self.startDate_label.setText('Start Date')
        self.endDate3_label = QtWidgets.QLabel()
        #self.endDate_label.setText('End Date')
        self.startDate4_label = QtWidgets.QLabel()
        self.endDate4_label = QtWidgets.QLabel()
        self.startDate5_label = QtWidgets.QLabel()
        self.endDate5_label = QtWidgets.QLabel()

        ## Reset Button
        self.reset_b = QtWidgets.QPushButton(self)
        self.reset_b.setText('Reset Filters')

        ## Layout
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.reset_b)
        layout.addWidget(vis_label)
        layout.addWidget(self.vis_type)
        layout.addWidget(self.startDate1_label)
        layout.addWidget(self.startDate1_filter)
        layout.addWidget(self.endDate1_label)
        layout.addWidget(self.endDate1_filter)
        layout.addWidget(self.startDate2_label)
        layout.addWidget(self.startDate2_filter)
        layout.addWidget(self.endDate2_label)
        layout.addWidget(self.endDate2_filter)
        layout.addWidget(self.startDate3_label)
        layout.addWidget(self.startDate3_filter)
        layout.addWidget(self.endDate3_label)
        layout.addWidget(self.endDate3_filter)
        layout.addWidget(self.startDate4_label)
        layout.addWidget(self.startDate4_filter)
        layout.addWidget(self.endDate4_label)
        layout.addWidget(self.endDate4_filter)
        layout.addWidget(self.startDate5_label)
        layout.addWidget(self.startDate5_filter)
        layout.addWidget(self.endDate5_label)
        layout.addWidget(self.endDate5_filter)
        layout.addWidget(self.label_one)
        layout.addWidget(self.filter_one)
        layout.addWidget(self.label_two)
        layout.addWidget(self.filter_two)
        layout.addWidget(self.label_three)
        layout.addWidget(self.filter_three)
        layout.addWidget(self.label_four)
        layout.addWidget(self.filter_four)
        layout.addWidget(self.label_five)
        layout.addWidget(self.filter_five)
        layout.addWidget(self.label_six)
        layout.addWidget(self.filter_six)
        layout.addWidget(self.label_seven)
        layout.addWidget(self.filter_seven)
        layout.addWidget(self.label_eight)
        layout.addWidget(self.filter_eight)
        layout.addWidget(self.label_nine)
        layout.addWidget(self.filter_nine)
        layout.addWidget(self.label_ten)
        layout.addWidget(self.filter_ten)
        
        ## Hide Filters and Labels at Init
        self.startDate1_label.setVisible(False)
        self.startDate1_filter.setVisible(False)
        self.endDate1_label.setVisible(False)
        self.endDate1_filter.setVisible(False)
        self.startDate2_label.setVisible(False)
        self.startDate2_filter.setVisible(False)
        self.endDate2_label.setVisible(False)
        self.endDate2_filter.setVisible(False)
        self.startDate3_label.setVisible(False)
        self.startDate3_filter.setVisible(False)
        self.endDate3_label.setVisible(False)
        self.endDate3_filter.setVisible(False)
        self.startDate4_label.setVisible(False)
        self.startDate4_filter.setVisible(False)
        self.endDate4_label.setVisible(False)
        self.endDate4_filter.setVisible(False)
        self.startDate5_label.setVisible(False)
        self.startDate5_filter.setVisible(False)
        self.endDate5_label.setVisible(False)
        self.endDate5_filter.setVisible(False)
        self.label_one.setVisible(False)
        self.filter_one.setVisible(False)
        self.label_two.setVisible(False)
        self.filter_two.setVisible(False)
        self.label_three.setVisible(False)
        self.filter_three.setVisible(False)
        self.label_four.setVisible(False)
        self.filter_four.setVisible(False)
        self.label_five.setVisible(False)
        self.filter_five.setVisible(False)
        self.label_six.setVisible(False)
        self.filter_six.setVisible(False)
        self.label_seven.setVisible(False)
        self.filter_seven.setVisible(False)
        self.label_eight.setVisible(False)
        self.filter_eight.setVisible(False)
        self.label_nine.setVisible(False)
        self.filter_nine.setVisible(False)
        self.label_ten.setVisible(False)
        self.filter_ten.setVisible(False)
        
        
    def setFilterVis(self,
                     filters:list):
        ## TODO: add parsing function to set filters
        ## RETURN: dictionary of field names and filters
        return


## Plotly Dashboard Panel
class PlotlyWidget(QtWidgets.QWidget):
    ## Initialize Class
    def __init__(self,
                 parent):
        super(PlotlyWidget,self).__init__(parent)
        self.initWidget()
    

    ## Initialize Widget Elements
    def initWidget(self):
        self.browser = QtWebEngineWidgets.QWebEngineView(self)
        vlayout = QtWidgets.QVBoxLayout(self)
        vlayout.addWidget(self.browser)


## Main Function
def window():
    app = QApplication(sys.argv)
    win = mainWindow()
    win.setWindowTitle('Interactive Dashboard Builder')
    win.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    window()
