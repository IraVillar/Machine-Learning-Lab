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
#ordersDF['Order.Date']= pd.to_datetime(ordersDF['Order.Date']) 

#Format Order Data to proper time series format
ordersDF['Order.Date']= pd.to_datetime(ordersDF['Order.Date'], format = '%m/%d/%y') 

#Make copy of ordersDF to plot Order date and Quantity
ordersDF2 = ordersDF[['Order.Date','Quantity']].copy(deep=True)

#plot seasonality of all data
ordersDF2.resample('M').sum().plot()
plt.title('Sales Seasonality')
plt.xlabel('Date')
plt.ylabel('Quantity')

#Create new DF to include categories
ordersDFcat = ordersDF[['Order.Date','Quantity','Category']].copy(deep=True)
ordersDFcat.set_index('Order.Date', inplace = True)
ordersDFcat = ordersDFcat.sort_index()

#Create Dfs for each of the categories
ordersDFcatOS = ordersDFcat[ordersDFcat['Category'] == 'Office Supplies'].copy(deep=True)
ordersDFcatFur = ordersDFcat[ordersDFcat['Category'] == 'Furniture'].copy(deep=True)
ordersDFcatTech = ordersDFcat[ordersDFcat['Category'] == 'Technology'].copy(deep=True)

#plot each category
#Office Supplies
ordersDFcatOS['Quantity'].resample('M').sum().plot(color = 'Blue')
plt.title('Office Supplies Seasonality')
plt.xlabel('Date')
plt.ylabel('Quantity')
#Furniture
ordersDFcatFur['Quantity'].resample('M').sum().plot(color = 'Red')
plt.title('Furniture Seasonality')
plt.xlabel('Date')
plt.ylabel('Quantity')
#Tech
ordersDFcatTech['Quantity'].resample('M').sum().plot(color = 'Green')
plt.title('Technology Seasonality')
plt.xlabel('Date')
plt.ylabel('Quantity')

#Mergeing returns with ordersDF
returns.rename(columns = {'Order ID':'Order.ID'}, inplace = True) 
merged = pd.merge(returns,ordersDF,how = "left", on="Order.ID")
merged_copy = merged[merged['Returned'] == 'Yes'].copy(deep=True)

#Creating a Year column and dropping duplicate order IDs to keep 1079 returns.
merged_copy['YEAR'] = pd.DatetimeIndex(merged_copy['Order.Date']).year
merged_copy.drop_duplicates(subset='Order.ID', keep='first', inplace=False)
len(merged_copy['Order.ID'].unique())

#How much they lost per year
merged_copy.groupby('YEAR').sum()['Profit']

#Customers who returned more than once and 5 times.
customer_returns = merged_copy['Customer.ID'].value_counts()
print(customer_returns[customer_returns > 1].count())
customer_returns[customer_returns > 5].count()
