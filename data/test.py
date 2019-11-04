import pandas as pd
import seaborn as sns
ordersDF = pd.read_csv("../data/Orders.csv")
ordersDF.head()

import numpy as np
import re
import matplotlib.pyplot as plt

#Question 1 Convert Profit and Sales to numeric
ordersDF['Profit'] = ordersDF.Profit.apply(lambda x: x.replace('$',''))
ordersDF['Profit'] = ordersDF.Profit.apply(lambda x: x.replace(' ',''))
ordersDF['Profit'] = ordersDF.Profit.apply(lambda x: x.replace(',',''))
ordersDF['Profit'] = pd.to_numeric(ordersDF['Profit'])

ordersDF['Sales'] = ordersDF.Sales.apply(lambda x: x.replace('$',''))
ordersDF['Sales'] = ordersDF.Sales.apply(lambda x: x.replace(' ',''))
ordersDF['Sales'] = ordersDF.Sales.apply(lambda x: x.replace(',',''))
ordersDF['Sales'] = pd.to_numeric(ordersDF['Sales'])

#Check Averages
print(ordersDF['Sales'].mean())
print(ordersDF['Profit'].mean())

#Check averages for Order Priority, is there an increase in price for urgency
ordersDF.groupby('Order.Priority').mean()

#Create month column to see if there is seasonility by month
ordersDF['month'] = pd.DatetimeIndex(ordersDF['Order.Date']).month
ordersDF.groupby('month').mean()

# 2 - 1: group by month and sum it up to graph barplot (B)
MonthGroup = ordersDF.groupby('month').sum()
MonthGroup['month'] = MonthGroup.index
MonthGroup
sns.barplot(x='month', y ='Quantity', data = MonthGroup)

# 2 - 2: group by month and category, sum it up and graph barplot (B)
Monthcat = ordersDF.groupby(['Category', 'month']).sum()
Monthcat= Monthcat.reset_index()
Monthcat
sns.barplot(x='month', y ='Quantity', hue= 'Category',data = Monthcat)

# 2 - 2 this one is better? : group by month and category, sum it up and graph barplot (B)
sns.barplot(x='Category', y ='Quantity', hue= 'month',data = Monthcat)

#plot month to see if there is seasonality
sns.barplot(x='month', y='Quantity', data=ordersDF)
ordersDF['monYr'] = pd.to_datetime(ordersDF['Order.Date']).dt.to_period('M')

#Convert Order Date to date time object check seasonality by day,month,year -- can we see an increase in Order amounts
ordersDF['Order.Date']= pd.to_datetime(ordersDF['Order.Date']) 