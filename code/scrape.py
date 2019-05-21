from bs4 import BeautifulSoup
import requests
import pandas as pd
import lxml
import urllib.request

url = 'http://www.agriculture.gov.au/pests-diseases-weeds/plant#indentify-pests-diseases'
specimens=requests.get(url)
soup=BeautifulSoup(specimens.content,'lxml')
main_div=soup.find(class_="flex-container")

base_url="http://www.agriculture.gov.au"
disease_data=[]
disease_name=[]
disease_url=[]
disease_image=[]
#---------------ITERATING OVER HTML
for i in main_div:
    ds_name=i.find('a').text.strip()
    ds_url=i.find('a').get('href')
    ds_image=i.find('img').get('src')

    disease_name.append(ds_name)
    disease_url.append(str(base_url)+str(ds_url))
    disease_image.append(str(base_url)+str(ds_image))

#----------------n-name, w-weblink, p- picture
for n, w, p in zip(disease_name,disease_url,disease_image):
    try:
        url= w
        data=requests.get(url)
        soup=BeautifulSoup(data.content,'lxml')
        base_tag=soup.find(class_="pest-header-content")
        x={}
        for i in base_tag:
            tag=i.findAll('strong')
            for j in tag:
                if len(j.text)>1:
                    x['disease_name']=n
                    x['disease_url']=w
                    x['disease_image']=p
                    x[j.text.strip()] = j.next_sibling.strip()
        disease_data.append(x)

    except Exception as e:
        x={}
        x['disease_name'] = n
        x['disease_url'] = w
        x['disease_image'] = p
        disease_data.append(x)

#-----------pandas utilization
df=pd.DataFrame(disease_data)
df.drop(['At','At risk:','risk:','Likely pathway of entry:'],axis=1,inplace=True)
df.fillna('Not Found')
df.to_csv('data.csv')

#-----------saving images to local disk
for image_url in disease_image:
    disease = image_url.split('http://www.agriculture.gov.au/SiteCollectionImages/pests-diseases-weeds/')[1]
    urllib.request.urlretrieve(image_url, f"Images/{disease}")

