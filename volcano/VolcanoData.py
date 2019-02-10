from bs4 import BeautifulSoup
from unidecode import unidecode
import pandas as pd

from .Requester import Requester


class VolcanoData(Requester):
    def __init__(self, url):
        self.req = Requester(url)

    def removeChar(self, char, string):
        pos = string.find(char)

        if pos == -1:
            return string
        else:
            return string.replace(char, '')

    def getData(self):
        raw_html = self.req.get()
        
        if not raw_html is None:
            soup = BeautifulSoup(raw_html, 'html.parser')
            
            # Set the dataframe columns
            col = ['NAME', 'COUNTRY', 'TYPE', 'LAT', 'LON', 'ELEV']
            df = pd.DataFrame(columns=col)

            df_index = 0
            td_tags = soup.find_all('td')
            for index in range(0, len(td_tags), 6):
                # Get the name and remove any commas
                name = td_tags[index].get_text().strip()
                name = self.removeChar(',', name)

                # Get other pieces of information
                country = td_tags[index + 1].get_text().strip()
                vol_type = td_tags[index + 2].get_text().strip()
                lat = td_tags[index + 3].get_text().strip()
                lon = td_tags[index + 4].get_text().strip()

                # Check if latitude and longitude are given
                if lat == '' or lon == '':
                    continue

                # Convert any non english characters
                name = unidecode(name)
                country = unidecode(country)

                # Get the elevation
                elev = td_tags[index + 5].get_text().strip()

                # Add data to dataframe and increment index
                df.loc[df_index] = [name, country, vol_type, lat, lon, elev]
                df_index = df_index + 1

        return df
