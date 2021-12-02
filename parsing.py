import xml.etree.ElementTree as ET
import pandas as pd
import requests
from bs4 import BeautifulSoup

#Parse XML file

path_to_xml_file = ('put file path to xml data here') #replace this text with the path to your version of the xml file

tree = ET.parse(path_to_xml_file)
root = tree.getroot()

marc = {'marc': 'http://www.loc.gov/MARC21/slim'}

num_list = range(0,6800) # 6800 is the number of ballad results returned from my search result; edit as appropriate.

url_list_df = []

for num in num_list:
        url_list = root[num].findall("marc:datafield[@tag='856']",marc)
        for url in url_list:
                current_url = url.find("marc:subfield[@code='u']",marc).text
                url_list_df.append(current_url+'citation')

df_list = []

for url in url_list_df:
        id_num = url.split('/')[4]
        print(id_num)
        page = requests.get(url)
        soup = BeautifulSoup(page.content,"html.parser")
        empty_dict = {}

        results = soup.find("table")
        row = results.find_all("tr")
        for x in row:
                if x.find(class_="leftcell") != None:
                        title_of_row = x.find(class_="leftcell")
                        title_text = title_of_row.text.strip('\n')
                        next_siblings = title_of_row.find_next_siblings("td")
                        list_of_siblings = [x for x in next_siblings]
                        new_list2 = [list(y.stripped_strings) for y in list_of_siblings]
                        flat_list = [item for sublist in new_list2 for item in sublist]
                        value_text = "|".join(flat_list).replace('\r\n','')
                        empty_dict[title_text] = value_text
        empty_dict['url'] = url


        df = pd.DataFrame(empty_dict,index=[id_num])
        df.index.name = 'ballad_id'
        df.to_csv('ebba_outputs/{}_trial.txt'.format(id_num),sep="\t") # Writes each dataframe, so that outputs are saved as you go along. Make sure you have a folder with the name 'ebba_outputs' for these to save in (they'll be 6800 files).
        df_list.append(df)

combined_df = pd.concat(df_list)
combined_df = combined_df.reset_index()


combined_df['Pages'] = combined_df['Pages'].fillna(combined_df['Page']) # Condense the two 'Page' column variants


# Limit the output to these files
combined_df = combined_df[['ballad_id','Date Published','Author','Standard Tune','Imprint','License','Collection','Location','Shelfmark','ESTC ID','Keyword Categories','MARC Record','Title','Tune Imprint','First Lines','Refrain','Condition','Ornament','url','Pepys Categories','Album Page','Notes','Pages']]


combined_df.to_csv('ebba_1500_1800.tsv',sep="\t",index=False)
