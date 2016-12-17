#!/usr/bin/env python
# coding=UTF-8

import urllib
import requests, os, bs4
import MySQLdb
import zipfile
import csv
import webbrowser

print("Creating database...")
db = MySQLdb.connect(host="localhost", user = "root", passwd = "6u1t4rh3r0")
cur = db.cursor()
cur.execute('DROP DATABASE IF EXISTS `consumidor`;')
cur.execute('CREATE DATABASE `consumidor`;')
cur.execute('USE `consumidor`;')

for i in open('SQL_Scripts/Create_Complete_Table.sql').read().split(';\n'):
    cur.execute(i)

url ='http://dados.gov.br/dataset/reclamacoes-do-consumidor-gov-br'
directory = "dados"

if not os.path.exists(directory):
    os.makedirs(directory)

print("Requesting Source from page...")
source = requests.get(url)
soup = bs4.BeautifulSoup(source.content, "html.parser")

links = soup.select(".resource-url-analytics")

print("Removing existing files from csv folder...")
files = os.listdir(directory)
for x in files:
	os.remove(directory + "/" + x)

print("Downloading zip files...")
for a in links:
	f = a.get("href")
	filename = f[-11:]
	if filename[-4:] == ".zip":
		print("\tDownloading "+f+"...")
		urllib.urlretrieve(f,'./'+directory+'/'+filename)
		print("\tExtracting "+f+" to "+f[-11:-4]+".csv...")
		zip_ref = zipfile.ZipFile('./'+directory+'/'+filename, 'r')
		zip_ref.extractall('./'+directory+'/')
		zip_ref.close()
		print("\tRemoving "+f+"...")
		os.remove('./'+directory+'/'+filename)

print("Reading csv files starting from 2nd line and inserting data on MySQL Database...")
for f in os.listdir(directory):
		filedata = csv.reader(file('dados/'+f), delimiter=';')
		next(filedata, None)
		print("\tReading "+f+" and inserting data on Database...")
		for row in filedata:
			sql = """INSERT INTO reclamacoes(Regiao, UF, Cidade, Sexo, FaixaEtaria, AnoAbertura, MesAbertura, DataAbertura, 
		    	DataResposta, DataFinalizacao, TempoResposta, NomeFantasia, SegmentoMercado, Area, Assunto, GrupoProblema, Problema, 
		    	ComoComprouContratou, ProcurouEmpresa, Respondida, Situacao, AvaliacaoReclamacao, NotaConsumidor ) 
		    	VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
			cur.execute(sql, row)

meses = ['Janeiro', 'Fevereiro', 'Marco', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
qtt = len(os.listdir(directory))

print("Building Views...")
for f in os.listdir(directory):
	mes = meses[int(f[-6:-4])-1]
	periodo = mes+' de '+f[:4]
	pagecontent1 = """
<!DOCTYPE html>
<html>

<head>

    <title>"""+periodo+"""</title>

    <link href="css/bootstrap.min.css" rel="stylesheet">
    <link href="css/sb-admin.css" rel="stylesheet">
    <link href="font-awesome/css/font-awesome.min.css" rel="stylesheet" type="text/css">

    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">

</head>

<body>

    <div id="wrapper">

        <nav class="navbar navbar-inverse navbar-fixed-top" role="navigation">
            
            <!-- Heading -->
            <div class="navbar-header">
                <a class="navbar-brand" href=\""""+f[:7]+""".html">Mapas - Dispersão de Reclamações - Consumidor.gov.br</a>
            </div>

            <!-- Sidebar Menu -->
            <div class="collapse navbar-collapse navbar-ex1-collapse">
                <ul class="nav navbar-nav side-nav">"""
	pagecontent2 = """
                </ul>
            </div>
        </nav>

        <div id="page-wrapper">

            <div class="container-fluid">

                <!-- Page Heading -->
                <div class="row">
                    <div class="col-lg-12">
                        <h1 class="page-header">
                            """+periodo+"""
                        </h1>
                    </div>
                </div>
            </div>

            <div id="map"></div>

            <script>

var map;
var marker;
function initMap() {

    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: -15, lng: -54},
        zoom: 4,
        minZoom: 4,
        scrollwheel: false,
        disableDoubleClickZoom: true,
        streetViewControl: false
    });

    var geocoder = new google.maps.Geocoder();
    geocodeAddress(geocoder, map);
    
}

function geocodeAddress(geocoder, resultsMap) {

    var Universities = [];"""

	pagecontent3 = """
    var Markers = new Array(Universities.length);
    var i;

    for(i = 0; i < Markers.length; i++){

        var address = Universities[i];

        geocoder.geocode({'address': address}, function(results, status) {
            Markers[i] = new google.maps.Marker({
                map: resultsMap,
                position: results[0].geometry.location
            });
        });

    }
}

            </script>

            <script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyADYPwDBC6vhRiSjDS6RSEj-bQ3-jq3NXQ&callback=initMap" 
            async defer></script>

        </div>

    </div>

</body>

</html>

"""
	print("\tBuilding View for "+f[:7]+".html...")
	Html_file= open("View/"+f[:7]+".html","w")
	Html_file.write(pagecontent1)
	for w in os.listdir(directory):
		mes = meses[int(w[-6:-4])-1]
		periodo = mes+' de '+w[:4]
		menuitem = """
                    <li>
                        <a href=\""""+w[:7]+""".html"><i class="fa fa-fw fa-bar-chart-o"></i> """+periodo+"""</a>
                    </li>"""
		Html_file.write(menuitem)
	Html_file.write(pagecontent2)

	print("\tExecuting database search and creating Maps with Markers for "+f[:7]+".html...")
	sql = "SELECT Cidade, UF FROM reclamacoes where DataAbertura like '%%/%s/%s'" % (f[-6:-4], f[:4])
	cur.execute(sql)
	results = cur.fetchall()
	for row in results:
		markers = """
	Universities.push(\""""+row[0]+"""\",\""""+row[1]+"""\", "Brasil");"""
		Html_file.write(markers)

	Html_file.write(pagecontent3)
	Html_file.close()

print("Opening Browser For Maps Visualization...")
webbrowser.open('View/'+w[:-4]+'.html')

db.commit()
cur.close()