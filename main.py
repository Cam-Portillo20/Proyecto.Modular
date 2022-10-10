from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from werkzeug.security import check_password_hash

import conexion_db
import validaciones
cursor = conexion_db.conexion.cursor()

#CLASE PARA PANTALLA DE INICIO DE SESIÓN
class InicioSesion(Screen):
    nombre_usuario = ObjectProperty(None)
    contrasena = ObjectProperty(None)

    #Función para ocultar y mostrar lo agregado en contraseña
    def mostrar_ocultar(self):
        contrasena = ObjectProperty(None)

        if self.contrasena.password == True:
            self.contrasena.password = False
        elif self.contrasena.password == False:
            self.contrasena.password = True

    #Función principal para iniciar sesión
    def iniciar_sesion(self):
        nombre_usuario = (self.ids.nombre_usuario.text)#Tomamos lo ingresado en nombre de usuario
        contrasena = (self.ids.contrasena.text)#Tomamos lo ingresado en contraseña

        if(nombre_usuario and contrasena):#Validamos que ningún campo este vacio

            nombre_u = (self.ids.nombre_usuario.text,)#guardamos el valor como tupla para el query
            sql_verificar_contrasena = "SELECT contrasena FROM usuarios WHERE nombre_usuario=%s"
            cursor.execute(sql_verificar_contrasena, nombre_u)
            
            password = cursor.fetchone()#guardamos la contraseña que obtiene si existe el usuario

            if(password):#si reconoce el usuario devuleve un valor y contraseña no esta vacía
                #devuelve tupla, convertimos de tupla a string
                contrasena_string = ','.join(password)

                if(check_password_hash(contrasena_string, contrasena)):# si devuelve true es porque las contraseñas coinciden
                    print("Todo esta bien")
                    self.nombre_usuario.text = ""
                    self.contrasena.text = ""
                    #DIRECCIONA A LA VISTA PARA GENERAR RUTA
                    #sm.current = 'ruta'

                else:#si las contraseñas no coinciden
                    print("Usuario y/o contraseña incorrecto")

            else:#Si no hay contraseña que coincida con usuario es porque el usuario no existe
                print("Usuario y/o contraseña incorrecto")
        
        else:#si alguno o ambos campos están vacioS
            print("INGRESAR TODOS LOS CAMPOS")
        
#CLASE PARA PANTALLA DE REGISTRO DE USUARIOS
class Registro(Screen):
    nombre_usuario = ObjectProperty(None)
    email = ObjectProperty(None)
    contrasena = ObjectProperty(None)

    #Función para ocultar y mostrar lo agregado en contraseña
    def mostrar_ocultar(self):
        contrasena = ObjectProperty(None)

        if self.contrasena.password == True:
            self.contrasena.password = False
        elif self.contrasena.password == False:
            self.contrasena.password = True
    
    #Función para hacer el insert a la bd, después de hacer validaciones
    def registro(self):
        nombre_usuario = (self.ids.nombre_usuario.text,)#Tomamos lo ingresado en nombre de usuario
        email = (self.ids.email.text)#Tomamos lo ingresado en email
        contrasena = (self.ids.contrasena.text)#Tomamos lo ingresado en contraseña

        if(nombre_usuario and contrasena and email):#Validamos que ambos campos no estén vacios
            #validamos que no exista el nombre de usuario ya registrado
            sql_validar_nombre_usuario = "SELECT * FROM usuarios WHERE nombre_usuario=%s"
            cursor.execute(sql_validar_nombre_usuario, nombre_usuario)
            check_nombre_usuario = cursor.fetchall()

            if(check_nombre_usuario):#Si retorna algo es porque el usuario ya existe
                print("usuario ya existe")
            else:#Si el usuario no existe
                if(validaciones.validar_correo(email)):#validamos que el correo tenga un formato correcto y que no exista
                    email = (self.ids.email.text,)
                    sql_validar_email = "SELECT * FROM usuarios WHERE email=%s"
                    cursor.execute(sql_validar_email, email)
                    check_email = cursor.fetchall()
                    if(check_email):#Si retorna algo es porque el correo ya fue registrado
                        print("Correo ya existe")
                    else:#Si el correo no existe
                        if(validaciones.validar_contrasena(contrasena)):#validamos que se ingrese una contraseña segura
                            #se encripta contraseña para mandarla así a la bd
                            contrasena = validaciones.encriptar_contrasena(contrasena)

                            campos_registro = (nombre_usuario, email, contrasena)#Añadimos todo lo ingresado a una variable
                            
                            #Insertamos a la bd
                            sql_insert_user = "INSERT INTO usuarios (nombre_usuario, email, contrasena) VALUES (%s, %s, %s)"
                            cursor.execute(sql_insert_user, campos_registro)
                            conexion_db.conexion.commit()
                            count = cursor.rowcount
                            
                            if(count == 1):
                                print("Registro de usuario exitoso")
                            else:
                                print("Error, no se realizo el registro")
                        else:
                            print("Ingresar contraseña segura")
                else:
                    print("Formato de correo electronico inválido")
        else:
            print("Deben de estar llenos todos los campos")

#clase para manejar pantallas
class windowManager(ScreenManager):
    pass

#documento kv
kv = Builder.load_file('disenios_kv/designLoginAndRegister.kv')
sm = windowManager()

#agregando pantallas
sm.add_widget(InicioSesion(name="InicioSesion"))
sm.add_widget(Registro(name="Registro"))

#clase que construye la interfaz gráfica de usuario
class loginMain(App):
    def build(self):
        return sm

#función de controlador
if __name__ == '__main__':
    loginMain().run()