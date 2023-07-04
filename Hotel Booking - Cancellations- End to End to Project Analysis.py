#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# First of all we need to import the basic required libararies... 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# In[ ]:


# its not important to import the warnings but if we will import this library will we not get warning errors... 
import warnings
warnings.filterwarnings('ignore')


# In[45]:


# this pd.read will read my loaded data... and saved it by the name of df so, now my file will be df
df=pd.read_csv('hotel_booking.csv')


# In[46]:


# here df is my file and want to check header so this will give header columns name with 5 rows of data..
# if we will put some value in head () function then it will show as per value like 3,8,10 or whatever
df.head()


# In[47]:


# shape function will give the count of how many Rows and columns in the file.
df.shape


# In[48]:


# here tail function is giving us last 5 record... i am giving some example here to show something in tail function
df.tail()


# In[85]:


# if i put some value in tail function...  see below
df.tail(12)


# In[50]:


# now you can see we have 12 rows to show how is the data with tail(12)


# In[51]:


# this info function will give us the information of all the columns and there null value count and data types
df.info()


# In[52]:


# describe funtion will work on only numirical value and it gives us the statical things like mean, max, min,std and IQR
df.describe()


# In[53]:


df.columns


# In[54]:


# why i am checking the data information again the in reservation_status_date column data type is object that is not 
# valid for a data and time column. it will be effecting my data analysis
df.info()


# In[86]:


# here i am changing the data type of reservation_status_date from object to datetime. just to analyze the data properly
df['reservation_status_date']=pd.to_datetime(df['reservation_status_date'])


# In[56]:


df.info()


# In[57]:


# we can here that describe function is working or non-numerical column also becouse i have used include = 'object' so 
# this will woek on object also and give these below mention result.
df.describe(include='object')


# In[58]:


df.describe()


# In[59]:


# here you can see i am checking the null values of the rows and in whaere in any column and rows it will show the count
# of null values so that we can do the needful as per our dataset
#df.isnull().sum()


# In[90]:


# here what i am doing that as my motive is to check the cancellation of resevation so if i will drop (remove) the
# these column will not effect my analysis or result.
# inplace = True is saving the data on my file also. it means whatever we are doing in excel ctrl + s is doing inplace
# =True
df.drop(['agent','company'],axis=1, inplace=True)


# In[91]:


# here dropna will drop all the null values we can check now.... everywhere null values is zero
df.dropna(inplace=True)


# In[20]:


df.isnull().sum()


# In[21]:


df.describe()


# In[92]:


# here i am dealing with outliers. describe function showing me the avg amd max value so in 'adr' column there is a 
# outliers and i am dealing with outliers
df=df[df['adr']<5000]


# In[93]:


df.describe()


# In[94]:


# for a quick data analysis we need to import a library that is 
import pandas_profiling


# In[95]:


# after importing library we will check the profile report and this will going to show you each and every thing of 
# dataset/file. its a very useful things.
profile = df.profile_report()
profile


# ## Data Analysis and Visualizaions

# In[64]:


# now i will be doing the analysis of data and visualizations through the many type of graphs plotsss
cancelled_perc = df['is_canceled'].value_counts(normalize=True)


# In[65]:


print(cancelled_perc)


# In[66]:


plt.figure(figsize=(5,4))
plt.title('Reservation status Count')
plt.bar(['Not canceled', 'canceled'], df['is_canceled'].value_counts())


# In[67]:


plt.figure(figsize=(8,4))
ax1=sns.countplot(x='hotel',hue='is_canceled', data=df, palette='Blues')
plt.show()


# In[68]:


resort_hotel=df[df['hotel']=='Resort Hotel']
resort_hotel['is_canceled'].value_counts(normalize=True)


# In[69]:


city_hotel=df[df['hotel']=='City Hotel']
city_hotel['is_canceled'].value_counts(normalize=True)


# In[70]:


resort_hotel=resort_hotel.groupby('reservation_status_date')[['adr']].mean()


# In[71]:


resort_hotel


# In[72]:


city_hotel=city_hotel.groupby('reservation_status_date')[['adr']].mean()


# In[73]:


city_hotel


# In[74]:


plt.figure(figsize=(12,5)) # Set the figure size
plt.title('Average Daily Rate in City and Resort Hotel', fontsize=20) # Set the title of the plot
plt.plot(resort_hotel.index,resort_hotel['adr'],label='Resort Hotel') # Plot the average daily rate for the resort hotel
plt.plot(city_hotel.index,city_hotel['adr'],label='City Hotel') # Plot the average daily rate for the city hotel
plt.legend(fontsize=10) # Add a legend to the plot with a specified font size
plt.show() # Display the plot


# In[75]:




# Assuming you have loaded the data into a DataFrame called `df`

# Convert 'month' column to categorical type
df['month'] = df['reservation_status_date'].dt.month.astype('category')

# Create a figure and set the figure size
plt.figure(figsize=(16, 8))

# Create a countplot with 'month' on the x-axis and 'is_canceled' as hue
ax1 = sns.countplot(x='month', hue='is_canceled', data=df)

# Display the plot
plt.show()


# In[76]:


# you can see here the analysis of data that blue bar graph is showing the Not Cancelled and orange graph is showing the 
# cancelled agains the reservations.


# In[77]:


# here we can see that price is matter for people that 
# we customers see the price is high then customer ask for cancellation plt.figure(figsize = (15,8))
plt.title('ADR per month', fontsize=30)
sns.barplot('month', 'adr', data=df[df['is_canceled']==1].groupby('month')[['adr']].sum().reset_index())
plt.show()


# In[78]:


# here we can see that purtgal coutry having maximum cancellation so becareful when taking the 
# reservation of purtgal specilly.
cancelled_data=df[df['is_canceled']==1]
top_10_country= cancelled_data['country'].value_counts()[:10]
plt.figure(figsize=(8,8))
plt.title('Top 10 countries with reservation canceled')
plt.pie(top_10_country, autopct = '%.2f',labels=top_10_country.index)
plt.show()


# In[79]:


df['market_segment'].value_counts()


# In[80]:


df['market_segment'].value_counts(normalize=True)


# In[81]:


cancelled_data['market_segment'].value_counts(normalize=True)


# In[82]:


cancelled_df_adr=cancelled_data.groupby('reservation_status_date')[['adr']].mean()
cancelled_df_adr.reset_index(inplace=True)
cancelled_df_adr.sort_values('reservation_status_date',inplace=True)

not_cancelled_data=df[df['is_canceled']==0]
not_cancelled_df_adr=not_cancelled_data.groupby('reservation_status_date')[['adr']].mean()
not_cancelled_df_adr.reset_index(inplace=True)
not_cancelled_df_adr.sort_values('reservation_status_date',inplace=True)

plt.figure(figsize=(20,6))
plt.title('Average Daily Rate') 
plt.plot(not_cancelled_df_adr['reservation_status_date'], not_cancelled_df_adr['adr'],label='not_cancelled')
plt.plot(cancelled_df_adr['reservation_status_date'], cancelled_df_adr['adr'],label='cancelled'
plt.legend()


# In[83]:


cancelled_df_adr = cancelled_data.groupby('reservation_status_date')[['adr']].mean()
cancelled_df_adr.reset_index(inplace=True)
cancelled_df_adr.sort_values('reservation_status_date', inplace=True)

not_cancelled_data = df[df['is_canceled'] == 0]
not_cancelled_df_adr = not_cancelled_data.groupby('reservation_status_date')[['adr']].mean()
not_cancelled_df_adr.reset_index(inplace=True)
not_cancelled_df_adr.sort_values('reservation_status_date', inplace=True)

plt.figure(figsize=(20, 6))
plt.title('Average Daily Rate')
plt.plot(not_cancelled_df_adr['reservation_status_date'], not_cancelled_df_adr['adr'], label='not_cancelled')
plt.plot(cancelled_df_adr['reservation_status_date'], cancelled_df_adr['adr'], label='cancelled')
plt.show()


# In[84]:


plt.figure(figsize=(20,6))
plt.title('Average Daily Rate')
plt.plot(not_cancelled_df_adr['reservation_status_data'],not_cancelled_df_adr['adr'],label='not cancelled')
plt.plot(cancelled_df_adr['reservation_status_date'],cancelled_df_adr['adr'],label='cancelled')
plt.legend(fontsize=20)


# # Suggestions

# ### 
# 1. Cancellation rates rise as price does. In order to prevent cancellations of reservations, hotels could work on their pricing strategies and try to lower the rates for specific hotels based on locations. They can also provide some discounts to the consumers.
# 
# 
# 2.  As the ratio of the cancellation and not cancellation of the resort hotel is higher in the resort hotel than the city hotels. So the hotels should provide a reasonable discount on the room prices on weekends or on holidays.
# 
# 
# 3. In the month of January, hotels can start campaigns or marketing with a reasonable amount to increase their revenue as the cancellation in the highest in this month.
# 
# 
# 4. They can also increase the quality of their hotels and their services mainly in Portgal to reduce the cancellation rate.
# 

# In[ ]:




