import pandas as pd
import numpy as np
import nltk
import re
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import requests
import urllib
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import warnings
warnings.filterwarnings('ignore')
import os
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
lem = WordNetLemmatizer()


nltk.data.path.append("C:\\Users\\PCLP\\AppData\\Roaming\\nltk_data")
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
stop_words = stopwords.words('english')


class data_ingestion:        
    
    def primary(self):
        try:
            data = pd.read_excel(os.path.join("Notebook/data","Input.xlsx"))
            #print(data.head())
            return data
        except Exception as e:
            print(f'Error {e}')

            
    def secondary(self):
        data = pd.read_excel('E:\\For_Job\\Blackcoffer\\Code\\Notebook\\data\\Input.xlsx')
        df = data.copy()  # Create a copy to avoid modifying the original DataFrame
        updated_list = []
        No_Matching_Data = []
        Blank_link = {}
        # Create an empty 'article_words' column
        #df['article_words'] = ''
        
        for i, url in enumerate(df['URL']):
            response_code = requests.get(url)
            soup = bs(response_code.text, 'html.parser')
            article_title = soup.find('title').text
            
            all_text_element = soup.find("div", class_="td-post-content tagdiv-type")

            if all_text_element is not None:
                all_text = all_text_element.get_text(strip=True, separator='\n')
                firstdata = all_text.splitlines()
            else:
                print(f"No matching element found in the HTML for URL: {url}")
                firstdata = []        
                Blank_link[f"blackassign00{i+1}"] = url        
                """Blank = {
                        'URL_ID' : f"blackassign00{i+1}" ,
                        'URL'    : url 
                        }
                No_Matching_Data.append(Blank)"""
                
             
            new_dataframe = {
                    "URL_ID": df["URL_ID"][i],
                    'URL' : url,
                    'article_words':f"{article_title}-{firstdata}"
                }    
            
            updated_list.append(new_dataframe)           
                

            filename = urllib.parse.quote_plus(url)
            file_path = 'E:\For_Job\Blackcoffer\Code\Text_files'
            space = " "
                
            with open(f"{file_path}\{filename}.txt", 'w+',encoding='utf-8') as file1:
                file1.writelines(article_title)
                file1.writelines(space)
                if firstdata is None:
                    firstdata = 'No data found'
                else:
                    file1.writelines(firstdata)
                
            # Update 'article_words' column for the current row
            #df.at[i, 'article_words'] = f"{article_title}-{firstdata}"

        #df.to_csv('E:\\For_Job\\Blackcoffer\\Code\\Notebook\\data\\final.csv', index=False)
        return pd.DataFrame(updated_list),Blank_link
    
    
    def Handdle_Blank_link(self,blank_data:dict):
        updated_list = []
        
        for i,j in blank_data.items():
            response_code = requests.get(j)
            soup = bs(response_code.text, 'html.parser')
            article_title = soup.find('title').text
            
            alldiv = soup.find("div", class_="td_block_wrap tdb_single_content tdi_130 td-pb-border-top td_block_template_1 td-post-content tagdiv-type")

            if alldiv is not None:
                firstdata = alldiv.text
                
                filename = urllib.parse.quote_plus(j)
                file_path = 'E:\For_Job\Blackcoffer\Code\Text_files'
                space = " "
                    
                with open(f"{file_path}\{filename}.txt", 'w+') as file1:
                    file1.writelines(article_title)
                    file1.writelines(space)
                    file1.writelines(firstdata)
                
            
                updated_dict = {
                    'URL_ID': i,
                    'URL': j,
                    'article_words': f"{article_title} - {firstdata}"
                }
                
                
                updated_list.append(updated_dict)
                
            else:
                print(f"No data available for the link: {j}")


        df = pd.DataFrame(updated_list)
        return df

    def merged(self,df1,df2):
        merged_df = pd.merge(df1, df2, on=['URL_ID', 'URL'], how='outer')
        merged_df = merged_df.dropna()
        merged_df.reset_index(drop=True, inplace=True)
        
        merged_df.to_csv('E:\\For_Job\\Blackcoffer\\Code\\Notebook\\data\\final.csv', index=False)
        
        return merged_df
        
                
            
"""            
if __name__ == "__main__":
    obj = data_ingestion()
    obj1=obj.primary()
    df,remain_data=obj.secondary()
    update_df=obj.Handdle_Blank_link(remain_data)"""