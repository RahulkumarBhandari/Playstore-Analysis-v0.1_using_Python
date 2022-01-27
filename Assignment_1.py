#!/usr/bin/env python
# coding: utf-8

# # Google_Play_Store_Data_Analysis
# 

# In[7]:


import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# In[8]:


# First Import the data 

df=pd.read_csv("C:/Users/Rahul/Desktop/New folder (2)/P-1/playstore_analysis.csv")


# In[147]:


df.head(5)


# In[9]:


df.shape


# In[193]:


df.info()


# In[10]:


df.isnull().sum()


# In[11]:


df_1=df.dropna(subset=['Rating'])


# In[12]:


df_1.isnull().sum()


# In[13]:


df_1["Android Ver"].isnull().sum()


# In[14]:


df_1[df_1.isna().any(axis=1)]


# In[15]:


df_1[df_1["App"]==("Life Made WI-Fi Touchscreen Photo Frame")]


# In[16]:


df_2=df_1.drop(index=10472)


# In[212]:


df_2[df_2["App"]==("Life Made WI-Fi Touchscreen Photo Frame")]


# In[226]:


df_2[df_2.isna().any(axis=1)]


# In[17]:


df_2["Android Ver"].unique()


# In[19]:


list_1=[3.0,4.2,1.5,4.0,4.0]


# In[20]:


import statistics
print(statistics.mode(list_1))


# In[21]:


df_2["Android Ver"].fillna(statistics.mode(list_1),inplace=True)


# In[22]:


df_2[df_2.isna().any(axis=1)]


# In[23]:


#C. Current ver – replace with most common value
df_2["Current Ver"].value_counts()


# In[24]:


df_2["Current Ver"].fillna("Varies with device ",inplace=True)


# In[25]:


df_2.isnull().sum()


# # 2.          Data clean up – correcting the data types

# In[26]:


df_2.info()


# In[27]:


df_2['Reviews'] = df_2['Reviews'].astype(int)
df_2['Size'] = df_2['Size'].astype(int)
df_2['Last Updated'] = df_2['Last Updated'].astype('datetime64[ns]')


# In[28]:


df_2.info()


# In[29]:


#Price variable – remove $ sign and convert to float
df_2['Price'] = df_2['Price'].str.replace('$','')


# In[30]:


df_2['Price'] = df_2['Price'].astype(float)


# In[31]:


df_2.info()


# In[32]:


df_2.head(5)


# #. Installs – remove ‘,’ and ‘+’ sign, convert to integer

# In[33]:


df_2["Installs"]=df_2["Installs"].str.replace(',','')


# In[34]:


df_2["Installs"]=df_2["Installs"].str.replace('+','')


# In[35]:


df_2["Installs"]=df_2["Installs"].astype(int)


# In[36]:


df_2.info()


# In[ ]:


d. Convert all other identified columns to numeric


# # 3. Sanity checks – check for the following and handle accordingl

# In[ ]:


#a. Avg. rating should be between 1 and 5, as only these values are allowed on the play store.


# In[37]:


pd.unique(df_2[['Rating']].values.ravel())


# In[38]:


#b. Reviews should not be more than installs as only those who installed can review the app
df_3 = pd.DataFrame()
df_3 = df_2[df_2.Reviews <= df_2.Installs]


# In[39]:


df_3.head()


# 4. Identify and handle outliers –

# In[40]:


#i. Make suitable plot to identify outliers in price

sns.catplot(y="Price",data=df_3,kind="box")
plt.ylabel('Unit Price')
plt.title('Unit Price')
plt.grid(linestyle='-')
plt.show()


# ii. Do you expect apps on the play store to cost $200? Check out these case

# In[41]:


df_3[df_3["Price"]==200]


# iii. After dropping the useless records, make the suitable plot again to identify 
# outliers 

# In[42]:


useful_data=df_2[df_2["Price"]!=0]
useful_data.head()


# In[43]:


useful_data.shape


# In[44]:


plt.subplots(figsize=(12,8))
sns.boxplot(y=useful_data.Price)

plt.ylabel('Unit Price')
plt.title('Unit Price')
plt.grid()
plt.show()


# iv. Limit data to records with price < $30

# In[45]:


limit_data=df_2[df_2["Price"]<30]
limit_data.head()


# In[46]:


limit_data.shape


# # b. Reviews column
# 

# i. Make suitable plot

# In[47]:


review_df=df_2.groupby('Category')['Reviews'].sum().sort_values()
review_df.sort_values(ascending=False)


# In[48]:


plt.subplots(figsize=(15,8))
review_df.plot(kind='barh', fontsize=14)
plt.show()


# ii. Limit data to apps with < 1 Million reviews

# In[49]:


limit_data_by_review = df_2[df_2['Reviews'] < 1000000]
limit_data_by_review.head()


# In[50]:


limit_data_by_review.shape


# # c. Installs
# 

# #i. What is the 95th percentile of the installs?

# In[51]:


percentile_df= df_2.Installs.quantile(0.95) 
print(percentile_df)


# ii. Drop records having a value more than the 95th percentile

# In[52]:


drop_value=df_2.Installs.quantile() > percentile_df
drop_value


# # Data analysis to answer business questions

# 5. What is the distribution of ratings like? (use Seaborn) More skewed towards higher/lower 
# values?

# In[79]:


plt.subplots(figsize=(10,))
sns.distplot(df_2['Rating'])
plt.show()


# # 6. What are the top Content Rating values?

# b. What is the implication of this on your analysis?

# In[54]:


df_2["Content Rating"].value_counts()


# In[55]:


Adult_rating = df_2[df_2['Content Rating'] == 'Adults only 18+'].index.to_list()
unrated =df_2[df_2['Content Rating'] == 'Unrated'].index.to_list()
df_2.drop(Adult_rating, inplace = True)
df_2.drop(unrated, inplace = True)
df_2['Content Rating'].value_counts()


# # 7. Effect of size on rating
# 

# a. Make a joinplot to understand the effect of size on rating

# In[82]:


sns.jointplot(x=df_2['Size'],y=df_2['Rating'],data=df_2,kind='hex')
plt.show()


# In[ ]:


#b. Do you see any patterns?


# In[ ]:


#c. How do you explain the pattern?


# # 8. Effect of price on rating

# a. Make a jointplot (with regression line)

# In[62]:


sns.jointplot(x ="Rating" , y = "Price" ,data = df_2)
plt.show()


# b. What pattern do you see?c. How do you explain the pattern?
#  ans: As price increasing then rating is also increases.

# d. Replot the data, this time with only records with price > 0

# In[63]:


Price_greaterthan_zero = df_2[df_2['Price'] > 0]
sns.jointplot(x ="Price" , y = "Rating" ,data = Price_greaterthan_zero, kind = "reg" )
plt.show()


# In[65]:


sns.lmplot(x='Price', y='Rating', hue ='Content Rating', data=df_2)
plt.show()


# f. What is your overall inference on the effect of price on the rating

# # 9. Look at all the numeric interactions together –

# a. Make a pairplort with the colulmns - 'Reviews', 'Size', 'Rating', 'Price'b

# In[67]:


sns.pairplot(df_2,vars=['Rating','Size', 'Reviews', 'Price'])
plt.show()


# # 10. Rating vs. content rating

# In[ ]:


a. Make a bar plot displaying the rating for each content rating


# In[68]:


a = df_2['Rating'].groupby(df_2['Content Rating']).median().plot(kind = 'bar')
a.set(xlabel ='Rating of content', ylabel = 'Average of Ratings')
plt.show()


# b. Which metric would you use? Mean? Median? Some other quantile?:Mean

# c. Choose the right metric and plot

# In[85]:


df_2.groupby(['Content Rating'])['Rating'].count().plot.bar(color="g")
plt.ylabel('Rating')
plt.show()


# 11. Content rating vs. size vs. rating – 3 variables at a time

# a. Create 5 buckets (20% records in each) based on Size

# In[70]:


sns.distplot(df_2["Size"], bins=5)
plt.show()


# In[71]:


bins=[0, 4600, 12000, 21516, 32000, 100000]
df_2['Size_Buckets'] = pd.cut(df_2['Size'], bins, labels=['VERY LOW','LOW','MED','HIGH','VERY HIGH'])
pd.pivot_table(df_2, values='Rating', index='Size_Buckets', columns='Content Rating')


# b. By Content Rating vs. Size buckets, get the rating (20th percentile) for each 
# combination

# In[72]:


df_2.Size.quantile([0.2, 0.4,0.6,0.8])


# In[73]:


df_2.Rating.quantile([0.2, 0.4,0.6,0.8])


# c. Make a heatmap of this

# In[ ]:


i. Annotated


# In[74]:


Size_Buckets =pd.pivot_table(df_2, values='Rating', index='Size_Buckets', columns='Content Rating', 
                     aggfunc=lambda x:np.quantile(x,0.2))
Size_Buckets


# In[75]:


sns.heatmap(Size_Buckets, annot = True)
plt.show()


# ii. Greens color map

# In[76]:


sns.heatmap(Size_Buckets, annot=True, cmap='Greens')
plt.show()

