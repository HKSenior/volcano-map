import folium as fm

from .VolcanoData import VolcanoData


class Map():
    def __init__(self, url):
        self.vd = VolcanoData(url)
        self.df = self.vd.getData()

    def getColor(self, elevation):
        if elevation < 1000:
            return 'green'
        elif 1000 < elevation < 3000:
            return 'orange'
        else:
            return 'red'

    def createMap(self):
        try:
            # Create the map
            map = fm.Map(location=[44.63, 28.77], zoom_start=3, 
                         width='100%', height='100%')

            # Create a feature group and add markers
            fg = fm.FeatureGroup(name='volcanoes')
            for _, row in self.df.iterrows():
                fg.add_child(
                    fm.Marker(location=[float(row['LAT']), float(row['LON'])],
                        popup=row['NAME'],
                        icon=fm.Icon(color=self.getColor(int(row['ELEV'])))
                    )
                )

            # Add feature group and save map
            map.add_child(fg)
            map.save('templates/volcano.html')

        except Exception as e:
            print(e)
