from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout

import ponderacion
import validaciones_registro
import insertar_riesgo_reporte

#Funcion para obtener las coordenadas de una ubicacion        

class Reportes(Screen):
    tipo_incidente : ObjectProperty(None)
    muertes : ObjectProperty(None)
    lesion : ObjectProperty(None)
    ubicacion_calle : ObjectProperty(None)
    ubicacion_codigo_postal : ObjectProperty(None)
    ubicacion_numero : ObjectProperty(None)

    def registrar_reporte(self):
        tipo_incidente = (self.ids.tipo_incidente.text)
        ubicacion_calle = (self.ids.ubicacion_calle.text)
        ubicacion_codigo_postal = (self.ids.ubicacion_codigo_postal.text)
        ubicacion_numero = (self.ids.ubicacion_numero.text)
        muertes = (self.ids.muertes.text)
        lesionados = (self.ids.lesionados.text)

        if (ubicacion_calle and ubicacion_codigo_postal):#validamos que no dejen vacíos los campos de direccion - número es opcional

            #--------------------------------VALIMOS CÓDIGO POSTAL--------------------------------
            if(validaciones_registro.validar_codigo_postal(ubicacion_codigo_postal)):#si tiene formato correcto seguimos

                #--------------------------------OBTENER COORDENADAS--------------------------------
                if(ubicacion_numero):#Si se ingreso número de la calle se concatena un espacio para mandar correctamente la ubicación
                    ubicacion_numero = ' ' + ubicacion_numero

                #Asignación de datos de dirección a una variable
                ubicacion = ubicacion_calle + ubicacion_numero + ', Guadalajara, Jalisco, ' + ubicacion_codigo_postal
                print("ubicación: ",ubicacion)

                #mandamos llamar funcion para obtener coordenadas
                coordenadas = validaciones_registro.obtener_coordenadas(ubicacion)
                print(coordenadas)

                if(coordenadas != None):#si retorna coordenadas es porque la dirección es correcta
                    #--------------------------------MANDAMOS LLAMAR FUNCIÓN PARA PONDERAR--------------------------------
                    integridad_fisica = 'NA'
                    if(muertes == 'Sí'):
                        integridad_fisica = 'Fallecido'
                        ponderacion_resultante = ponderacion.heuristica(tipo_incidente, integridad_fisica)
                    elif (muertes == 'No' and lesionados == 'No'):
                        ponderacion_resultante = ponderacion.heuristica(tipo_incidente, integridad_fisica)
                    else:
                        integridad_fisica = 'Lesionado'
                        ponderacion_resultante = ponderacion.heuristica(tipo_incidente, integridad_fisica)
                    print("PONDERACION: ", ponderacion_resultante)
                    
                    #una vez teniendo la ponderación insertamos a la base de datos :3
                    insertar_riesgo_reporte.tabla_riesgo_y_registro(tipo_incidente, integridad_fisica, coordenadas, ponderacion_resultante)

                else:
                    print("No se encuentra dirección con esos datos")
            else:
                print("Código postal incorrecto - verifique y recuerde que solo debe reportar dentro de gdl")
        else:
            print("Para dirección debe ingresar calle y código postal")


#clase para manejar pantallas
class windowManager(ScreenManager):
    pass

#documento kv
kv = Builder.load_file('disenios_kv/disenioReportes.kv')
sm = windowManager()

#agregando pantallas
#sm.add_widget(InicioSesion(name="InicioSesion"))
sm.add_widget(Reportes(name="Reportes"))

#clase que construye la interfaz gráfica de usuario
class loginMain(App):
    def build(self):
        return sm

#función de controlador
if __name__ == '__main__':
    loginMain().run()