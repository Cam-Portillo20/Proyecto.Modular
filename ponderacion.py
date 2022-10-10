#función para la heuristica según el tipo de incidente, sin contemplar muertes o lesionados
def heuristica(tipo_incidente, integridad_fisica):
    valor=0
    if tipo_incidente == 'Robo':
        valor = 85
    elif tipo_incidente == 'Asalto':
        valor = 85
    elif tipo_incidente == 'Secuestro':
        valor = 85
    elif tipo_incidente == 'Acoso':
        valor = 80
    elif tipo_incidente == 'Pelea Callejera':
        valor = 65
    elif tipo_incidente == 'Atropellameinto':
        valor = 70
    elif tipo_incidente == 'Asesinato':
        valor = 95 #Este solo tiene el campo de muerto
    elif tipo_incidente == 'Otro':
        valor = 40

    return resultado_ponderacion(integridad_fisica, valor)#mandamos llamar la función con lo que recibe como resultado del incidente y del valor

#Esta función nos ayuda a sumar puntaje si hubo fallecidos o  lesionados
def resultado_ponderacion(integridad_fisica, valor):
    if integridad_fisica == 'Lesionado':
        valor+=5
    elif integridad_fisica == 'Fallecido':
        valor+=10
    return valor

#gdl_incidentes['riesgo']= gdl_indidentes.apply(
#    lambda df: funcion_heuristic (df ['tipo_incidente'],df['lesionado']),axis=1)