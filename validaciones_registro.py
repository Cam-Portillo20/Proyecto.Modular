import re
import geocoder
import numpy as np
from sklearn import preprocessing

#Función para validar formato codigo postal gdl
def validar_codigo_postal(codigo):
    regex = '^44\d{3}$' 
    if(re.search(regex,codigo)):  
        return True 
    else:  
        return False

def obtener_coordenadas(ubicacion):
    #necesito calle, número si es pposible, codigo postal, gdl y jalisco (número es opcional)
    locacion = geocoder.osm(ubicacion)#'Santo Tomas 1996, 44719, Guadalajara, Jalisco'
    coordenadas = locacion.latlng
    return coordenadas #class <list>

#normaliza todos los datos
def ponderacion_para_normalizar(riesgos):
    riesgos = np.array(riesgos).reshape(-1,1)
    print("FUNCION PONDERACION: ", riesgos) 
    scaler = preprocessing.MinMaxScaler(feature_range=(0,3))
    riesgos_normalizados = scaler.fit_transform(riesgos)
    print(riesgos_normalizados)
    return riesgos_normalizados
