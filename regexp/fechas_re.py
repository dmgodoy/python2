#!/usr/bin/python
# -*-coding: utf-8 -*-
import re
import sys

completo=""
if(len(sys.argv) == 2):
    print "Abriendo " + sys.argv[1]
    f = open(sys.argv[1], "r")
    completo = f.read()

elif(len(sys.argv) == 1):
    print "Introduce cadena de texto donde vamos a buscar las fechas"
    EOF = 0
    while not EOF:
        try:
            entrada = raw_input()
            completo = completo + entrada + "\n"
        except EOFError:
            EOF = 1
            #break
else:
    print "Num. args. incorrecto.\nUso %s [file]" % sys.argv[0]

print completo

localidad = '(\w+\s+)+'
meses = '(Ene|Feb|Mar|Abr|May|Jun|Jul|Ago|Sep|Oct|Nov|Dic)'
fecha = '\d\d?/'+ meses +'/\d\d\d\d'
hora = '\d\d?:\d\d\s+(PM|AM)'
#Granada 5/Ago/2012 2:23 AM
fecha_completa = localidad + fecha +'\s+'+ hora

if re.search(fecha_completa, completo,re.IGNORECASE|re.UNICODE):
    print "Lo encontré, que cosas"
else:
    print "No aparece"

