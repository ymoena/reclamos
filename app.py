import csv

import unicodedata
import requests
import time
from random import randint
from time import sleep
from bs4 import BeautifulSoup
import pandas as pd
from flask import Flask, render_template, request, url_for, redirect, send_file
from flask_bootstrap import Bootstrap


app = Flask(__name__)
Bootstrap(app)

def elimina_tildes(cadena):
    s = ''.join((c for c in unicodedata.normalize('NFD',cadena) if unicodedata.category(c) != 'Mn'))
    return s
def obtenerReclamo(url):
    req = requests.get(url)
    html = BeautifulSoup(req.text, "html.parser")
    reclamos = html.find('span', {'property': ['v:description']}).text
    fecha = html.find('span', {'property': ['v:dtreviewed']})
    fecha1 = fecha.text.split(', ')[1]
    fecha2 = fecha.text.split(' ')[1].split(',')[0]

    fecha = fecha2 + ' ' + fecha1

    if 'December' in fecha:
        fecha = fecha.replace('December', 'Diciembre')

    return reclamos,fecha
def obtenerURL(categoria,subcategoria):

    if categoria == "educacion":
        if subcategoria == "universidad":
            return "https://www.reclamos.cl/sector/1474?page="
        if subcategoria == "instituto":
            return "https://www.reclamos.cl/sector/1509?page="
        if subcategoria == "preuniversitario":
            return "https://www.reclamos.cl/sector/1475?page="
        else:
            return "https://www.reclamos.cl/educacion?page="

    if categoria == "salud":
        if subcategoria == "isapres":
            return "https://www.reclamos.cl/sector/1465?page="
        if subcategoria == "hospital":
            return "https://www.reclamos.cl/sector/1487?page="
        if subcategoria == "cosmeticas":
            return "https://www.reclamos.cl/sector/1499?page="
        if subcategoria == "farmacias":
            return "https://www.reclamos.cl/sector/1497?page="
        if subcategoria == "opticas":
            return "https://www.reclamos.cl/sector/1504?page="
        if subcategoria == "fonasa":
            return "https://www.reclamos.cl/empresa/fonasa?page="
        if subcategoria == "laboratorios":
            return "https://www.reclamos.cl/sector/1526?page="
        else:
            return "https://www.reclamos.cl/salud?page="

    if categoria == "telecomunicaciones":
            if subcategoria == "telefonia_movil":
                return "https://www.reclamos.cl/sector/1464?page="
            else:
                return "https://www.reclamos.cl/telecomunicaciones?page="

    if categoria == "retail":
            if subcategoria == "grandes_tiendas":
                return "https://www.reclamos.cl/sector/1578?page="
            if subcategoria == "supermercado":
                return "https://www.reclamos.cl/sector/1476?page="
            else:
                return "https://www.reclamos.cl/retail?page="

    if categoria == "bancos_y_financieras":
            if subcategoria == "cobranzas":
                return "https://www.reclamos.cl/sector/1521?page="
            if subcategoria == "tarjetas_de_credito":
                return "https://www.reclamos.cl/sector/1575?page="
            else:
                return "https://www.reclamos.cl/bancos?page="

    if categoria == "gobierno":
            if subcategoria == "municipalidad":
                return "https://www.reclamos.cl/sector/1468?page="
            if subcategoria == "ministerio":
                return "https://www.reclamos.cl/sector/1479?page="
            if subcategoria == "justicia":
                return "https://www.reclamos.cl/sector/1508?page="
            if subcategoria == "superintendencia":
                return "https://www.reclamos.cl/sector/1530?page="
            if subcategoria == "partidos_politicos":
                    return "https://www.reclamos.cl/sector/1576?page="
            else:
                return "https://www.reclamos.cl/gobierno?page="

    if categoria == "servicios_basicos":
            if subcategoria == "electricas":
                return "https://www.reclamos.cl/sector/1589?page="
            if subcategoria == "aguas":
                return "https://www.reclamos.cl/sector/1590?page="
            if subcategoria == "gas":
                return "https://www.reclamos.cl/sector/1588?page="
            else:
                return "https://www.reclamos.cl/servicios_basicos?page="

    if categoria == "automotriz":
            if subcategoria == "autopistas":
                return "https://www.reclamos.cl/sector/1485?page="
            if subcategoria == "bencina":
                return "https://www.reclamos.cl/sector/1587?page="
            else:
                return "https://www.reclamos.cl/automotriz?page="

    if categoria == "construccion":
            if subcategoria == "constructoras":
                return "https://www.reclamos.cl/sector/1481?page="
            if subcategoria == "inmobiliaria":
                return "https://www.reclamos.cl/sector/1480?page="
            else:
                return "https://www.reclamos.cl/construccion?page="

    if categoria == "transportes":
            if subcategoria == "logistica_y_distribucion":
                return "https://www.reclamos.cl/sector/1471?page="
            if subcategoria == "lineas_aereas":
                return "https://www.reclamos.cl/sector/1486?page="
            else:
                return "https://www.reclamos.cl/transportes?page="
def recolectarReclamos(categoria,subcategoria,cant_reclamos):

    #Se designa categoria, subcategoria y cantidad de reclamos a obtener
    categoria = categoria.lower()
    subcategoria = subcategoria.lower()
    #CANTIDAD_RECLAMOS = cant_reclamos
    print ('Cantidad de reclamos', cant_reclamos)
    hora = time.strftime("%X")
    hora = hora.replace(':','')[:4]
    print('Hora:', hora)

    # Se crea Dataframe para almacenar reclamos
    df = pd.DataFrame(columns=('Fecha', 'Institucion', 'Titulo', 'Reclamo'))

    #Obtenemos URL necesaria
    print(categoria,subcategoria,cant_reclamos)
    URL = obtenerURL(categoria,subcategoria)
    print(URL)

    print('Esperando respuesta del servidor...')
    # Realizamos la petición a la web
    req = requests.get(URL)
    print('Pagina web: ', URL)

    # Comprobamos que la petición nos devuelve un Status Code = 200
    status_code = req.status_code

    # Se crea contador para llevar la cuenta de los reclamos
    contador = 1

    if status_code == 200:

        # Variable para determinar el tiempo que se utilizo en recolectar datos
        start_time = time.time()
        print('Recolectando datos...')

        # Se reccore un rango de paginas de las cuales es extraen los reclamos
        for page in range(0, 1):

            # Realiza una peticion
            req = requests.get(URL + str(page))
            # Pausa el for
            sleep(randint(8, 15))
            # Pasamos el contenido HTML de la web a un objeto BeautifulSoup()
            html = BeautifulSoup(req.text, "html.parser")

            # Obtenemos todos los tr donde están las entradas
            reclamos = html.find_all('tr', {
                'class': ['odd', 'even', 'No resuelto odd', 'No resuelto even', 'Respondido even', 'Respondido odd']})

            # Recorremos todas las entradas para extraer el título,fecha y reclamo
            for rec in reclamos:

                # Con el método "getText()" nos devuelve el texto
                titulo = rec.find('td', {'class': 'view-field view-field-node_title'}).getText()
                url = rec.find('a').attrs['href']  # Almacena la url de cada reclamo

                # Evitamos reclamos que no tengan titulo o institucion
                if '-' not in titulo:
                    continue

                # Eliminamos tildes
                titulo = elimina_tildes(titulo)

                # Dividimos titulo del reclamo en titulo e institucion
                reclamo_ = titulo.split(' - ')
                titulo = reclamo_[1]
                institucion = reclamo_[0]

                # Obtenemos el reclamo en si
                reclamo, fecha = obtenerReclamo(url)
                reclamo = elimina_tildes(reclamo)

                # Se guarda informacion en el DataFrame para luego crear csv
                df = df.append([{'Fecha': fecha, 'Institucion': institucion, 'Titulo': titulo, 'Reclamo': reclamo[1:]}],
                               ignore_index=True)

                contador = contador + 1
                print(contador-1,'/',cant_reclamos,' recolectados.')
                # Cuando se recopila la cantidad de datos pedida, termina el loop
                if int(cant_reclamos)+1 == contador:
                    print('Fin bucle 1')
                    break



        print('Datos Recolectados.')
        print('Tiempo de ejecucion: ', (time.time() - start_time), 'segundos')

        #Nombre del archivo
        nombre_archivo = categoria+cant_reclamos+'_'+hora
        print(nombre_archivo)

        # Se crea el csv
        df.to_csv('output/'+nombre_archivo+'.csv', sep=';', encoding='utf-8', index=False)
        print('Archivo .csv creado (', contador, ' filas)')
        return nombre_archivo

    else:
        print("Status Code %d" % status_code)

#Aplicacion Web
@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/recopilar', methods=['GET', 'POST'])
def recopilar():
    if request.method == "POST":
        categoria = request.form.get("categoria", None)
        subcategoria = request.form.get("subcategoria", None)
        cant_reclamos = request.form.get("cant_reclamos", None)
        print(categoria,subcategoria,cant_reclamos)
        if subcategoria!=None:
            nombre_archivo = recolectarReclamos(categoria, subcategoria, cant_reclamos)
            return render_template("index.html", subcategoria = subcategoria,categoria = categoria, cant_reclamos=cant_reclamos, nombre_archivo=nombre_archivo)
    return render_template("index.html")


@app.route('/recopilar/descarga', methods=['GET', 'POST'])
def descarga():
    if request.method == "POST":
        descarga = request.form.get("descarga", None)
        nombre_archivo = request.form.get("nombre_archivo", None)
        if descarga!=None:
            return send_file('output/'+nombre_archivo+'.csv',
                             mimetype='text/csv',
                             attachment_filename=nombre_archivo+'.csv',
                             as_attachment=True)
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)