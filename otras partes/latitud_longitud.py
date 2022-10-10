import geocoder
'''
import pandas as pd
from geopy.geocoders import Nominatim
import time

geolocator = Nominatim(user_agent="cctmexico")
df = pd.DataFrame({'direcc':
            ['2094 Valentine Avenue,Bronx,NY,10457',
             'Santo Tomas 1996, 44719, Guadalajara, Jalisco']})
start = time.time()

from geopy.extra.rate_limiter import RateLimiter
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

df['location'] = df['direcc'].apply(geocode)
df['coordenadas'] = df['location'].apply(lambda x: (x.latitude, x.longitude))#lambda para que se corra a toda la columna

end = time.time()
elapsed = end - start

print(df)
print(str(elapsed)+"segundos")
'''
#necesito calle, número si es pposible, codigo postal, gdl y jalisco (número es opcional)
loc = geocoder.osm('Santo Tomas 1996, 44719, Guadalajara, Jalisco')#sí es importante que tenga gdl
coordenadas = loc.latlng
print(type(coordenadas))
print(coordenadas)