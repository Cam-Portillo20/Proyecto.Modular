import geocoder

loc = geocoder.osm('1996 Santo Tomas, Guadalajara, México')
print(loc.latlng)
loc = geocoder.osm('813 Rivas Guillen, Guadalajara, México')
print(loc.latlng)




g = geocoder.google("453 Booth Street, Ottawa ON")
print(g.city)

g = geocoder.google([20.6798651, -103.2972999], method='reverse')
print(g.state)