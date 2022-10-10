import psycopg2
import validaciones_registro

#conexion a la base de datos
conexion = psycopg2.connect(user='postgres',
                            password='admin',
                            host='127.0.0.1',
                            port='5432',
                            database='bd_report')

#utilizar cursor
cursor = conexion.cursor()

#insertar a la bd de reportes y de riesgo
def tabla_riesgo_y_registro(tipo_incidente, integridad_fisica, coordenadas, ponderacion_resultante):
    #coordenadas es una lista numerica, convertimos a lista de string 
    coordenadas = [str(x) for x in coordenadas]

    #busca por coincidencia de coordenadas
    sql_select_riesgo = "SELECT id, ponderacion, ponderacion_normalizada FROM riesgo WHERE longitud=%s AND latitud=%s"
    cursor.execute(sql_select_riesgo, coordenadas)#me puede dar error porque debo mandar una tupla
    datos = cursor.fetchone()#datos es tipo tupla

    if (datos):#si ya hay registro

        riesgo_datos = datos[1]#tomamos el valor de ponderacion y lo guardamos en riesgo_datos
        riesgo_datos += ponderacion_resultante#actualizamos el valor de ponderacion
        print("datos + ponderacion", riesgo_datos)

        #tomamos todos los riesgos para mandarlos a la función de normalización
        sql_select_riesgo = "SELECT ponderacion FROM riesgo"
        cursor.execute(sql_select_riesgo)
        riesgos = cursor.fetchall()
        print("RIESGOS:", riesgos)
        
        validaciones_registro.ponderacion_para_normalizar(riesgos, datos[0])
        

        #sql_update_riesgo = "UPDATE riesgo SET ponderacion = %s AND ponderacion_normalizado = %s"

    else:
        sql_insert_riesgo = "INSERT INTO riesgo (longitud, latitud, ponderacion, ponderacion_normalizada) values (%s,%s,%s,%s)"

    #insertar en tabla registros para llevar un historial de los incidentes
    #campos_insert_reporte = (tipo_incidente, integridad_fisica, datos[0])
    #sql_insert_reporte = "INSERT INTO reportes (tipo_incidente, integridad_fisica, id_riesgo) values (%s, %s, %s);"
    #cursor.execute(sql_insert_reporte, campos_insert_reporte)
    #conexion.commit()
    #count = cursor.rowcount



    #si encuentra datos que coincide entonces hacemos un update y actualizamos ponderacion y ponderacion_normalizada
    print(datos)
    #UPDATE tblCustomers SET Email = Null 
    

    #sql_insert_tabla_riesgo = (coordenadas[0], coordenadas[1], ponderacion_resultante)#Añadimos todo lo ingresado a una variable
    #sql_insert_tabla_reportes = (tipo_incidente, integridad_fisica)
