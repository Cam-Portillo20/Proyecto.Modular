from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout

import psycopg2
import geocoder
import ponderacion

#conexion a la base de datos
conexion = psycopg2.connect(user='postgres',
                            password='admin',
                            host='127.0.0.1',
                            port='5432',
                            database='bd_report')

    #utilizar cursor
cursor = conexion.cursor()

#Funcion para obtener las coordenadas de una ubicacion
def obtener_coordenadas(ubicacion):
    #necesito calle, número si es pposible, codigo postal, gdl y jalisco (número es opcional)
    locacion = geocoder.osm(ubicacion)#'Santo Tomas 1996, 44719, Guadalajara, Jalisco'
    coordenadas = locacion.latlng
    return coordenadas #class <list>


#CLASE PANTALLA REPORTES DE INCIDENTES
class Reportes(Screen):
   #nombre_usuario = ObjectProperty(None)
    tipo_incidente = ObjectProperty(None)
    ubicacion = ObjectProperty(None)
    lesion = ObjectProperty(None)
    muertes = ObjectProperty(None)

    def registroIncidente(self):
        tipo_incidente = (self.ids.tipo_incidente.text)#Tomamos lo ingresado en tipo de incidente
        ubicacion = (self.ids.ubicacion.text)#Tomamos lo ingresado en ubicacion
        
        #De estos campos se debe recibir un sí o un no / algo parecido
        lesion = (self.ids.lesion.text)#Tomamos lo ingresado en lesion
        muertes = (self.ids.muertes.text)#Tomamos lo ingresado en muertos

        #obtener coordenadas del lugar
        coordenadas = obtener_coordenadas(ubicacion)

        if(muertes == 'Sí'):
            ponderacion_resultante = ponderacion.heuristica(tipo_incidente, 'Fallecido')
        elif (muertes == 'No' and lesion == 'No'):
            ponderacion_resultante = ponderacion.heuristica(tipo_incidente, 'NA')
        else:
            ponderacion_resultante = ponderacion.heuristica(tipo_incidente, 'Lesionado')
        
        campos_registro = ('Lesionado', tipo_incidente, coordenadas[0], coordenadas[1], ponderacion_resultante)#Añadimos todo lo ingresado a una variable

        #Insertamos a la bd
        sql_insert_report = "INSERT INTO reportes (integridad_fisica, tipo_incidente, latitud, longitud, ponderacion) VALUES (%s, %s, %s, %s, %s)"
        print(cursor.execute(sql_insert_report, campos_registro))
        conexion.commit()
        count = cursor.rowcount
                            
        if(count == 1):
            print("Registro de usuario exitoso")
        else:
            print("Error, no se realizo el registro")


#clase para manejar pantallas
class windowManager(ScreenManager):
    pass

#documento kv
kv = Builder.load_file('RegistroIncidentes.kv')
sm = windowManager()

#agregando pantallas
sm.add_widget(Reportes(name="Reportes"))

#clase que construye la interfaz gráfica de usuario
class loginMain(App):
    def build(self):
        return sm

#función de controlador
if __name__ == '__main__':
    loginMain().run()