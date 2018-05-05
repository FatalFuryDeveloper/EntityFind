# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.template import RequestContext, loader
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from twython import Twython
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from dateutil.parser import parse
import json
import requests
import re
def index(request):

	latest_question_list = ""
	#Template
	template = loader.get_template('polls/index.html')
	context = {'latest_question_list': latest_question_list}
	return HttpResponse(template.render(context))

@csrf_exempt
def panelControl(request):
	if request.method == 'POST':
		if request.POST.get('pais', False):
			country_code = request.POST['pais']
			fichero      = "output.txt"               #nombre de Fichero a tratar
			country_code = request.POST['pais']       #Codigo del Pais
			lenguaje     = request.POST['lenguaje']   #Lenguaje del twetts
			filtro(fichero,country_code,lenguaje)

			texto = open('texto.txt', 'r')
			analisis(texto.read())
			entidades = [
				        	{"nombre":"Mauro","tipo":"Rivera","subtipo":"UPV","apariciones":"1","relevancia":"10"},
							{"nombre":"Mauro","tipo":"Rivera","subtipo":"UPV","apariciones":"1","relevancia":"10"},
							{"nombre":"Mauro","tipo":"Rivera","subtipo":"UPV","apariciones":"1","relevancia":"10"}
			];
			topic = "Mauro estas bien"
			latest_question_list = ""
			context = {'topic':topic}
			template = loader.get_template('polls/tablaResultado.html')
			return HttpResponse(template.render(context))
	else:
		context = {}
		template = loader.get_template('polls/panelControl.html')
		return HttpResponse(template.render(context))


# Funcion para filtrar tweets por codigo de Pais
def filtro(fichero,codigo_pais,lenguaje):
    data     = open('data.txt','w')                           #Creacion archivo resultado
    texto    = open('texto.txt','w')                          #Creacion archivo texto resultado
    contador = 0                                              #Creamos un contador iniciado en 0
    with open(fichero) as file1:                              #Cargar fichero "output.txt" contiene tweets en bruto
        for linea in file1:                                   #Leer por linea el fichero de tweets
            tweet = json.loads(linea)                         #Cargar la linea en un formato json
            if tweet.has_key("place"):                        #Buscar por key "place"
                place = tweet["place"]                        #Almacenar "place"
                lang = tweet["lang"]                          #
                text = tweet["text"]
                if place != None:                             #Filtrar los tweet que sean diferentes a None
                    if place["country_code"] == codigo_pais:  #Filtrar los tweet por el Pais
                        if lang == lenguaje:
                            contador = contador + 1           #Incrementamos el contador
                            data.write(linea)                 #Escribimos en el archivo la linea del tweet
                            texto.write(text.encode("utf-8"))


def analisis(texto):
    result      = open('result.json','w')                           #Creacion archivo resultado

    # URL del Servicio.                   Requerido
    url     = "http://api.meaningcloud.com/topics-2.0"

    # Clave de cuenta en meaningcloud.    Requerido
    key     = "cd5cab64be3563feb3f3f43325e65404" # Esta clave es de mi cuenta personal de meaningcloud

    # Formato de salida.                  Opcional
    of    = "json"

    # Lenguaje del texto a analizar.      Requerido
    lang    = "es"

    # Lenguaje del texto a analizar.      Opcional Defecto:ilang=""
    ilang    = ""

    # Los campos txt, doc y url son mutuamente excluyentes (se requiere un parámetro)
    # solo se procesará uno. El orden de precedencia es txt, url y doc.
    # Texto de entrada que se analizará.  Excluyente(txt o url o doc)
    txt     = texto.decode('latin1','replace') #some_string.decode('latin1','replace')
    #print(txt)
    #Formato de texto especifica          Opcional Defecto:txtf ="plain"
    #txtf    = "plain"

    # Archivo de entrada a analizar.      Excluyente(txt o url o doc) Defecto:doc=""
    doc     = ""

    # URL con el contenido a clasificar.  Excluyente(txt o url o doc) Defecto:url=""
    url2    = ""

    # Tipos de Temas a extraer del Texto. Requerido
    tt      = "e"

    # Trata con palabras desconocidas.    Opcional Defecto:uw=n
    uw     = "n"

    # Tratar con la tipografía relajada.  Opcional Defecto:rt=n
    rt     = "n"

    # El diccionario del usuario.         Opcional Defecto:ud=""
    ud     = ""

    # Mostrar subtemas.                   Opcional. Defecto:st=n
    st     = "n"

    # Tipo de desambiguación aplicada.    Opcional Defecto:dm=n
    dm     = "n"

    # Agrupación desambiguación semántica Opcional Defecto:sdg=""
    sdg     = ""

    # Contexto desambiguación Prirización Opcional Defecto:cont=n
    cont     = "n" #Top>Sport| Top>SocialSciences |Top>Organization

    #payload = {"key":key,"lang":lang,"txt":txt,"url":url2,"doc:"doc,"tt":tt,"of":of,"ilang":ilang,"uw":uw,"rt":rt,"ud":ud,"st":st,"dm":dm,"sdg":sdg,"cont":cont}

    payload = {"key="+key+"&lang="+lang+"&txt="+txt+"&url="+url2+"&doc="+doc+"&tt="+tt+"&of="+of+"&ilang="+ilang+"&uw="+uw+"&rt="+rt+"&ud="+ud+"&st="+st+"&dm="+dm+"&sdg="+sdg+"&cont="+cont}
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    print(payload)
    #response = requests.request("POST", url, data=payload, headers=headers)
    #parsed = json.loads(response.text)
    #print (json.dumps(parsed, indent=4, sort_keys=True))
    #result.write(json.dumps(parsed, indent=4, sort_keys=True))

    #print()