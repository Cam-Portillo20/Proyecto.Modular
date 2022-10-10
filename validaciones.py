import re
from werkzeug.security import generate_password_hash

#Función para encriptar contraseña
def encriptar_contrasena(contrasena):
    contrasena_encriptada = generate_password_hash(contrasena)
    return contrasena_encriptada

#Función para validar formato correcto del correo
def validar_correo(email):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$' 
    if(re.search(regex,email)):  
        return True 
    else:  
        return False

#Función para validar contraseña del usuario
#Tener al menos un número.
#Tener al menos un carácter en mayúscula y uno en minúscula.
#Tener al menos un símbolo especial.
#Tener entre 6 y 20 caracteres.
def validar_contrasena(contrasena):
    regex = '^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$'#favor de revisar

    if(re.search(regex,contrasena)):  
        return True 
    else:  
        return False