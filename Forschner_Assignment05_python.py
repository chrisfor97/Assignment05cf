# %% [markdown]
# # DS400: Assignment III (Python)
# 
# ##### Christopher Forschner (Student ID: 6290771)
# ##### January 31, 2022
# I worked together with Janik Müller and Simon Andres in Python and R

# %% [markdown]
# ## Setting up a new GitHub repository
# (1) Register on github.com in case you have not done this already.<br>
# (2) Initialize a new public repository for this assignment on GitHub.<br>
# (3) For the following exercises of this assignment, follow the standard Git workflow (i.e., pull the latest
# version of the project to your local computer, then stage, commit, and push all the modifications that you
# make throughout the project). Every logical programming step should be well documented on GitHub
# with a meaningful commit message, so that other people (e.g., your course instructor) can follow and
# understand the development history. You can do this either using Shell commands or a Git GUI of your
# choice. <br>
# (4) In the HTML file that you submit, include the hyperlink to the project repository (e.g., https://github.
# com/yourUserName/yourProjectName)

# %% [markdown]
# https://github.com/chrisfor97/Assignment05cf.git

# %% [markdown]
# ## Getting to know the API
# (5) Visit the documentation website for the API provided by ticketmaster.com (see here). Familiarize yourself
# with the features and functionalities of the Ticketmaster Discovery API. Have a particular look at
# rate limits.<br>

# %% [markdown]
# Features of the Ticketmaster Discovery API:<br>
# * Searching events by keyword in a certain location (lat/long)
# * Getting events for a particular artist OR venue in a specific country/city/zip code/DMA/etc
# * Getting hi-res images for a particular event or artist.
# * Search events of a certain genre in a particular location for a certain promoter
# * rate limits: 5000 API calls per day and rate limitation of 5 requests per second
# + increasing rate limit is also possible but specific conditions need to be fullfilled. However, fo this Assignment, this is not necessary
# 

# %% [markdown]
# (6) Whithin the scope of this assignment, you do not have to request your own API key. Instead retrieve
# a valid key from the API Explorer. This API key enables you to perform the GET requests needed
# throughout this assignment. Even though this API key is not secret per se (it is publicly visible on the
# API Explorer website), please comply to the common secrecy practices discussed in the lecture and the
# tutorial: Treat the API key as a secret token. Your API key should neither appear in the code that you
# are submitting nor in your public GitHub repository.<br>

# %%
import os
os.chdir('C:/Users/chris/Desktop/Uni/Uni_tuebingen/semester_1/dspm/Assignment05cf')

# %%
with open("ticketmaster_api.py") as script:
    exec(script.read())

# %% [markdown]
# ## Interacting with the API - the basics
# (7) Perform a first GET request, that searches for event venues in Germany (countryCode = "DE"). Extract
# the content from the response object and inspect the resulting list. Describe what you can see.<br>

# %%
#importing libraries
import numpy as np
import pandas as pd
import requests
import time

# %%
#perform the get request
tickets_content=requests.get('https://app.ticketmaster.com/discovery/v2/venues',
                params = {"apikey": api_key1, "countryCode": "DE",'locale':'*'}).json()  
tickets_content #checking if request worked correctly                                   

# %% [markdown]
# We see that the output of the request is a nested dictionary. The venues are stored in ["_embedded"]["venues"] and comtains 20 elements. In the dicitonary  'page', we have the total numbers of pages 647 and the total number of elements. Therefore, the API contains 12934 elements.

# %%
#extract content from the response object
len(tickets_content['_embedded']['venues']) #we have 20 entries in this list
a=type(tickets_content['_embedded']['venues'])
b=type(tickets_content['_embedded']['venues'][0]) #exemplary check type of the first entry of this list 
print(a,b)
pages=tickets_content['page']['totalPages']
pages

# %% [markdown]
# (8) Extract the name, the city, the postalCode and address, as well as the url and the longitude
# and latitude of the venues to a data frame.

# %%
tickets_length=len(tickets_content['_embedded']['venues'])
tickets=tickets_content['_embedded']['venues'] #this is a list of dictionaries

names=[]
city=[]
postal_Code=[]
address=[]
url=[]
longitude=[]
latitude=[]


for i in tickets_content['_embedded']['venues']:
    if 'name' in i:
        names.append(i['name'])
    else:
        names.append('N/A')
    if 'city' in i:
        city.append(i['city']['name'])
    else:
        city.append('N/A')            
    if 'postalCode' in i:
        postal_Code.append(i['postalCode'])
    else:
        postal_Code.append('N/A')
    if 'address' in i:
        address.append(i['address']['line1'])
    else:
        address.append('N/A')
    if 'url' in i:
        url.append(i['url'])
    else:
        url.append('N/A')
    if 'location' in i:
        longitude.append(i['location']['longitude'])
        latitude.append(i['location']['latitude'])
    else:
        longitude.append('NA')
        latitude.append('NA')                    

#store them in a data frame
var_dict={'name':names,
            'city':city,
            'postalCode':postal_Code,
            'address':address,
            'url':url,
            'longitude':longitude,
            'latitude':latitude}
tickets_content_df=pd.DataFrame(var_dict) 
print(tickets_content_df)        
  
   


# %%
tickets_content_df

# %% [markdown]
# ## Interacting with the API - advanced
# (9) Have a closer look at the list element named page. Did your GET request from exercise (7) return all
# event locations in Germany? Obviously not - there are of course much more venues in Germany than
# those contained in this list. Your GET request only yielded the first results page containing the first
# 20 out of several thousands of venues. Check the API documentation under the section Venue Search.
# How can you request the venues from the remaining results pages? Iterate over the results pages and
# perform GET requests for all venues in Germany. After each iteration, extract the seven variables name,
# city, postalCode, address, url, longitude, and latitude. Join the information in one large
# data frame. Print the first 10 rows and the shape of the resulting data frame. The resulting data frame
# should look something like this (note that the exact number of search results may have changed since
# this document has been last modified):

# %%
# creating a function for the request object
def requester(api_key,country_Code,page):
    api_Key=api_key
    countryCode=country_Code
    venues_list=requests.get('https://app.ticketmaster.com/discovery/v2/venues', params={"apikey": api_Key, "countryCode": countryCode, 'page':page,'locale':'*','size':499}).json() #use page size of 499 so that every element can be caught
    return(venues_list)
#create a function to extract the values from the task before

# %%
#test if the function works
venues_info=requester(api_key1,'DE',0)   

# %%
venues_Liste=[None]*(venues_info['page']['totalPages']) #preparing the environment
pages=list(range(venues_info['page']['totalPages']))
for p in pages:
    time.sleep(0.2)
    venues_Liste[p]=requester(api_key1,'DE',p)

# %%
venues_Liste=[None]*(venues_info['page']['totalPages']) #had to run it a second time, because in the first request does not catch all pages
pages=list(range(venues_info['page']['totalPages']))
for p in pages:
    time.sleep(0.2)
    venues_Liste[p]=requester(api_key1,'DE',p)

# %%
#find entries in the list with an error message
error_pages=list()
for e in pages:
    if '_embedded' in venues_Liste[e]:
        continue
    else:
        page_index=e
        error_pages.append(page_index)
#print the error message
print(error_pages)
for i in error_pages:
    print(venues_Liste[i])
#reverse order of error pages
error_pages.reverse()
print(error_pages)
venues_Liste2=venues_Liste.copy()

# %%
#remove entries with error message
for i in error_pages:
   venues_Liste2.pop(i)
vpages=len(venues_Liste2)
vpages=list(range(vpages))   

# %%
#create a new data frame with every page
venues_de=pd.DataFrame()

for p in vpages:
    names_de=[]
    city_de=[]
    postal_Code_de=[]
    address_de=[]
    url_de=[]
    longitude_de=[]
    latitude_de=[]
    for i in venues_Liste2[p]['_embedded']['venues']:
        if 'name' in i:
            names_de.append(i['name'])
        else:
            names_de.append(np.NaN)
        if 'city' in i:
            city_de.append(i['city']['name'])
        else:
            city_de.append(np.NaN)            
        if 'postalCode' in i:
            postal_Code_de.append(i['postalCode'])
        else:
            postal_Code_de.append('N/A')
        if 'address' in i:
            if 'line1' in i['address']:
                address_de.append(i['address']['line1'])
            else:
                address_de.append(np.NaN)    
        else:
            address_de.append(np.NaN)
        if 'url' in i:
            url_de.append(i['url'])
        else:
            url_de.append(np.NaN)
        if 'location' in i:
            longitude_de.append(i['location']['longitude'])
            latitude_de.append(i['location']['latitude'])
        else:
            longitude_de.append(np.NaN)
            latitude_de.append(np.NaN)                    

    #store them in a data frame
    var_dict={'name':names_de,
            'city':city_de,
            'postalCode':postal_Code_de,
            'address':address_de,
            'url':url_de,
            'longitude':longitude_de,
            'latitude':latitude_de}
    venues_df=pd.DataFrame(var_dict)
    venues_de=pd.concat([venues_de,venues_df]) 
venues_de.shape
    

# %%
venues_de.head(10)

# %% [markdown]
# ## Visualizing the extracted data
# (10) Below, you can find code that produces a map of Germany. Add points to the map indicating the
# locations of the event venues across Germany.<br>

# %%
#import necessary packages
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon

# %%

crs={'init':'epsg:4326'}

# %%
venues_de['longitude'] = pd.to_numeric(venues_de['longitude'])
venues_de['latitude'] = pd.to_numeric(venues_de['latitude'])

# %%
#create geometric points for the map
geometry=[Point(xy) for xy in zip(venues_de['longitude'],venues_de['latitude'])]

# %%
#create a geopandas data frame
geo_df=gpd.GeoDataFrame(venues_de, crs=crs, geometry=geometry)
geo_df.head()

# %%
#check if the created points work
geo_df.plot()

# %%
fig,ax=plt.subplots(figsize=(7,7))

# get a base map of Germany
map = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
map = map[map.name == "Germany"]
# plot the map
map.plot(ax = ax, color='grey',alpha=1,linewidth=1,cmap='cividis',zorder=1)
# add geodata to to the map
geo_df.plot(ax=ax,color='red',markersize=1,zorder=2)
#add title
plt.title('Event locations across Germany')

plt.show()


# %% [markdown]
# (11) You will find that some coordinates lie way beyond the German borders and can be assumed to be faulty.
# Set coordinate values to NA where the value of longitude is outside the range (5.866, 15.042) or
# where the value of latitude is outside the range (47.270, 55.059) (these coordinate ranges have
# been derived from the extreme points of Germany as listed on Wikipedia (see here). For extreme points
# of other countries, see here). <br>

# %%
#set values outside the intervals to NaN
venues_de[['longitude','latitude']]=venues_de[['longitude','latitude']].where(((venues_de['longitude']>5.866)&(venues_de['longitude']<15.042))&((venues_de['latitude'] > 47.270) & (venues_de['latitude'] < 55.059)))

# %%
#set values outside the intervals to NaN
venues_de[['longitude','latitude']]=venues_de[['longitude','latitude']].where(((venues_de['longitude']>5.866)&(venues_de['longitude']<15.042))&((venues_de['latitude'] > 47.270) & (venues_de['latitude'] < 55.059)))
geometry2=[Point(xy) for xy in zip(venues_de['longitude'],venues_de['latitude'])]
geo_df2=gpd.GeoDataFrame(venues_de, crs=crs, geometry=geometry2)
geo_df2.plot()

# %%
fig,ax=plt.subplots(figsize=(7,7))

# get a base map of Germany
map = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
map = map[map.name == "Germany"]
# plot the map

# plot the map
base=map.plot(ax = ax, color='grey',alpha=1,linewidth=1,cmap='cividis',zorder=1)
# add geodata to to the map
geo_df2.plot(ax=ax,color='red',markersize=1,zorder=2)
#add title
plt.title('Event locations across Germany')

plt.show()


# %% [markdown]
# ## Event locations in other countries
# (12) Repeat exercises (9)–(11) for another European country of your choice. (Hint: Clean code pays off! If
# you have coded the exercises efficiently, only very few adaptions need to be made.)

# %%
#exercise 9 country of choice Switzerland ('CountryCode:CH')
tickets_ch=requests.get('https://app.ticketmaster.com/discovery/v2/venues',
                params = {"apikey": api_key1, "countryCode": "CH",'locale':'*'}).json()  
vpages_ch=list(range(tickets_ch['page']['totalPages'])) 
print(vpages_ch)

# %%
venues_list_ch=[None]*(tickets_ch['page']['totalPages']) 
for p in vpages_ch:
    time.sleep(0.2)
    venues_list_ch[p]=requests.get('https://app.ticketmaster.com/discovery/v2/venues',
                params = {"apikey": api_key1, "countryCode": "CH",'locale':'*','page':p}).json()  

# %%
#find entries in the list with an error message
error_pages3=list()
for p in vpages_ch:
    if '_embedded' in venues_list_ch[p]:
        continue
    else:
        page_index=p
        error_pages3.append(page_index)
#print the error message
print(error_pages3)
for i in error_pages3:
    print(venues_list_ch[i])
#reverse order of error pages
error_pages3.reverse()
print(error_pages3)
venues_list_ch2=venues_list_ch.copy()

# %%
for i in error_pages3:
   venues_list_ch2.pop(i)
vpages_ch2=len(venues_list_ch2)
vpages_ch2=list(range(vpages_ch2)) 

# %%
#create a new data frame with every page
venues_ch=pd.DataFrame()

for p in vpages_ch2:
    names=[]
    city=[]
    postal_Code=[]
    address=[]
    url=[]
    longitude=[]
    latitude=[]
    for i in venues_list_ch2[p]['_embedded']['venues']:
        if 'name' in i:
            names.append(i['name'])
        else:
            names.append(np.NaN)
        if 'city' in i:
            city.append(i['city']['name'])
        else:
            city.append(np.NaN)            
        if 'postalCode' in i:
            postal_Code.append(i['postalCode'])
        else:
            postal_Code.append('N/A')
        if 'address' in i:
            if 'line1' in i['address']:
                address.append(i['address']['line1'])
            else:
                address.append(np.NaN)    
        else:
            address.append(np.NaN)
        if 'url' in i:
            url.append(i['url'])
        else:
            url.append(np.NaN)
        if 'location' in i:
            longitude.append(i['location']['longitude'])
            latitude.append(i['location']['latitude'])
        else:
            longitude.append(np.NaN)
            latitude.append(np.NaN)                    

    #store them in a data frame
    var_dict={'name':names,
            'city':city,
            'postalCode':postal_Code,
            'address':address,
            'url':url,
            'longitude':longitude,
            'latitude':latitude}
    venues_df=pd.DataFrame(var_dict)
    venues_ch=pd.concat([venues_ch,venues_df]) 
    

# %%
venues_ch.head(10)

# %%
#exercise 10
fig,ax=plt.subplots(figsize=(7,7))
# get a base map of Switzerland
map = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
map = map[map.name == "Switzerland"]
# plot the map
map.plot(ax = ax, color='grey',alpha=1,linewidth=1,cmap='cividis',zorder=1)

# %%
venues_ch['longitude'] = pd.to_numeric(venues_ch['longitude'])
venues_ch['latitude'] = pd.to_numeric(venues_ch['latitude'])
geometry3=[Point(xy) for xy in zip(venues_ch['longitude'],venues_ch['latitude'])]
geo_df3=gpd.GeoDataFrame(venues_ch, crs=crs, geometry=geometry3)
geo_df3.plot()


# %%
fig,ax=plt.subplots(figsize=(7,7))
# get a base map of Switzerland
map = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
map = map[map.name == "Switzerland"]
# plot the map
map.plot(ax = ax, color='grey',alpha=1,linewidth=1,cmap='cividis',zorder=1)
#add the points
geo_df3.plot(ax=ax,color='red',markersize=1,zorder=2)
#add title
plt.title('Event locations across Switzerland')

plt.show()

# %% [markdown]
# Extreme points for switzerland: 
# * Longitude : [5.57, 10.29]
# * Latitude: [45.49, 47.48}

# %%
#set values outside the intervals to NaN
venues_ch[['longitude','latitude']]=venues_ch[['longitude','latitude']].where(((venues_ch['longitude']>5.57)&(venues_ch['longitude']<10.29))&((venues_ch['latitude'] > 45.49) & (venues_ch['latitude'] < 47.48)))
geometry4=[Point(xy) for xy in zip(venues_ch['longitude'],venues_ch['latitude'])]
geo_df4=gpd.GeoDataFrame(venues_ch, crs=crs, geometry=geometry4)
geo_df4.plot()

# %%
fig,ax=plt.subplots(figsize=(7,7))
# get a base map of Switzerland
map = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
map = map[map.name == "Switzerland"]
# plot the map
map.plot(ax = ax, color='grey',alpha=1,linewidth=1,cmap='cividis',zorder=1)
#add the points
geo_df4.plot(ax=ax,color='red',markersize=1,zorder=2)
#add title
plt.title('Event locations across Germany')

plt.show()


