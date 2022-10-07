def calculo_resultado(result_incidente, valor):
    if result_incidente == 'Fallecido':
        return valor+5
    elif result_incident == 'NA':
        return valor-5
    else:
        return valor

def funcion_heuristic (tipo_incidente, result_incident):
    valor=0
    if tipo_incidente == 'Robo':
        valor = 90
    elif tipo_incidente == 'Asalto':
        valor = 90
    elif tipo_incidente == 'Secuestro':
        valor = 90
    elif tipo_incidente == 'Acoso':
        valor = 85
    elif tipo_incidente == 'Pelea Callejera':
        valor = 70
    elif tipo_incidente == 'Atropellameinto':
        valor = 75
    elif tipo_incidente == 'Asesinato':
        valor = 100 #Este solo tiene el campo de muerto
    elif tipo_incidente == 'Otro':
        valor = 45

    return calculo_resultado(result_incidente, valor)

gdl_incidentes['riesgo']= gdl_indidentes.apply(
    lambda df: funcion_heuristic (df ['tipo_incidente'],df['lesionado']),axis=1)
        
