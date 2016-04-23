# ================= Imports =================
from django.shortcuts import render
from django.http import HttpResponse
from models import noticias
from django.views.decorators.csrf import csrf_exempt
import urllib2
# SAXs
from xml.sax.handler import ContentHandler
from xml.sax import make_parser


# ================= Variables Globales =================
eso = 'EsO'


# ================= Funciones =================
# ----------------- decorateHTML -----------------
def decorateHTML (text):
    return ("<html><body>" + text + "</body></html>")
    
# ----------------- myURL -----------------
def myURL ():
    return 'http://127.0.0.1:8000'

# ----------------- getDBLength -----------------
def getDBLength (DB_in):
    DB = DB_in.objects.all()
    length = 0
    for item in DB:
        length = length + 1
    return length

# ================= Clases =================
class myContentHandler(ContentHandler): 
    line = ''
    seqN = 1

    def __init__ (self):
        self.inItem = False
        self.inContent = False
        self.theContent = ""
        self.newtitle =''
        self.newlink =''

    def startElement (self, name, attrs):
        if name == 'item':
            self.inItem = True
        elif self.inItem:
            if name == 'title':
                self.inContent = True
            elif name == 'link':
                self.inContent = True
            elif name == 'description':
                self.inContent = True
            
    def endElement (self, name):
        if name == 'item':
            self.inItem = False
        elif self.inItem:
            if name == 'title':
                self.line = "Title: " + self.theContent + "."
                self.newtitle = self.theContent
                print self.line.encode('utf-8') 
                self.inContent = False
                self.theContent = ""
            elif name == 'link':
                self.newlink = self.theContent
#                noticiasAUX = noticias(titulo=self.line[7:], id = self.seqN,\
#                                        link=self.theContent)
#                noticiasAUX.save()
#                self.seqN += 1;
                print " Link: " + self.theContent + "."
                self.inContent = False
                self.theContent = ""
            elif name == 'description':
                noticiasAUX = noticias(titulo=self.newtitle, id=self.seqN,\
                                        link=self.newlink, body= self.theContent)
                noticiasAUX.save()
                self.seqN += 1;
                self.inContent = False
                self.theContent = ""

    def characters (self, chars):
        if self.inContent:
            self.theContent = self.theContent + chars


# ================= Vistas =================
# ----------------- homePage -----------------
def homePage(request):
    # Obtencion del rss desde internet
    f = urllib2.urlopen('http://barrapunto.com/index.rss')
    fBody = f.read()
    # Inicializacion del Parser
    theParser = make_parser()
    theHandler = myContentHandler()
    theParser.setContentHandler(theHandler)
    # Escritura Dummy en archivo .xml
    try:
        print ('Abriando .rr ...')
        xmlFile = open('barrapunto.rss',"r")
        fBody_aux = xmlFile.read()
        xmlFile.close()
        if fBody_aux == fBody:
            print('Iguales!!!!')
            """
            Al existir y ser iguales de contenido, no sera necesario almacenar 
            ni procesar nada nuevo, por lo que no hago nada para ahorrar tiempo.
            """
        else:
            print('Distintos...')
            xmlFile = open('barrapunto.rss',"w")
            xmlFile.writelines(fBody)
            xmlFile.close()
            # Apertura dummy del archivo .xml
            xmlFile = open('barrapunto.rss',"r")
            # Borrar base de datos vieja...
            noticias.objects.all().delete()
            # Parse
            print ('')
            print ('Inicio del Parser...')
            theParser.parse(xmlFile)    # Launch Parse
            xmlFile.close()
            print ('Fin del Parser...')
            print ('')

    except:
        print ('No existia .rr, creando ...')
        xmlFile = open('barrapunto.rss',"w")
        xmlFile.writelines(fBody)
        xmlFile.close()
        xmlFile = open('barrapunto.rss',"w")
        xmlFile.writelines(fBody)
        xmlFile.close()
        # Apertura dummy del archivo .xml
        xmlFile = open('barrapunto.rss',"r")
        # Parse
        print ('')
        print ('Inicio del Parser...')
        theParser.parse(xmlFile)    # Launch Parse
        xmlFile.close()
        print ('Fin del Parser...')
        print ('')
    
    # Respuesta HTML, mpresion de datos desde SqL
    respuesta = '<h4>Titulares y Enlaces:</h4><br>'
    noticiasL = noticias.objects.all()
    respuesta+='<br>Noticias almacenadas:<ol>'
    for noticia in noticiasL:
        respuesta += '<li><a href="' + noticia.link + '">'\
                    + noticia.titulo + '</a>'
    respuesta += '</ol>'
    print ('Terminado !!!')
    
    return HttpResponse(decorateHTML(respuesta))

# ----------------- favicon -----------------
def favicon(request):
    respuesta=''
    return HttpResponse(respuesta)

# ----------------- la404 -----------------
def la404(request):
    return HttpResponse('Not Found')

# ----------------- Picknew -----------------
def Picknew(request, recurso):
    # Carga inicial
    respuesta = '<h4>Titulares y Enlaces:</h4><br>'
    noticiasL = noticias.objects.all()
    respuesta+='<br>Noticias almacenadas:<ol>'
    for noticia in noticiasL:
        respuesta += '<li>'+noticia.titulo+ ' URL >>> ' + '<a href="'\
                    + noticia.link + '">' + noticia.link + '</a>'
    respuesta += '</ol>'
    
    # Carga Puntual
    try:
        print int(recurso)
        noticia = noticias.objects.get(id=recurso)
        respuesta += '<br><strong>Noticia: </strong>'+noticia.titulo
        respuesta += '<br><br>' + noticia.body
        
    except:
        respuesta += 'Recurso no encontrado, tenemos '\
                    + str(getDBLength(noticias)) +' noticias'

    return HttpResponse(decorateHTML(respuesta))
    















# ================= USEFULL CODE =================
"""
# Espacio en blanco &nbsp;

@csrf_exempt
def homePage(request):
    seqNumb = getDBLength(urlLargas)
    print('Longitud de urlLargas = ' +  str(seqNumb))
    if request.method == 'GET':
        # _________________ GET _________________
        respuesta = '<html><body>'\
                    +'<form method="POST" action="">'\
                    +'URL: <input type="text" name="url"><br>'\
                    +'<input type="submit" value="Enviar">'\
                    +'</form>'
        urls = urlLargas.objects.all()
        respuesta+='<br>URLs En Cache:<ol>'
        for url in urls:
            respuesta += '<li>' + url.urlCorta + '=>' + url.urlLarga
        respuesta += '</ol>'\
        +'</body><title>Acortador</title>'\
        +'</html>'
                    
    elif request.method == 'POST' or request.method == 'PUT':
        # _________________ POST or PUT _________________
        print 'Recibido POST or PUT...'
        cuerpo=request.body.replace('%3A',':') # Recibo estos strings...
        cuerpo=cuerpo.replace('%2F','/')
        if cuerpo[0:4] == 'url=': # POST de formulario o poster con "url..."
            cuerpo = cuerpo[4:] # Quito el url=
        if cuerpo[0:7] != 'http://': # http:// en caso de no haberlo
            cuerpo = 'http://' + cuerpo
        print (cuerpo)
        try:
            # Por si acaso estoy metiendo una corta...
            print ('Buscando coincidencia entre las cortas...')
            urlLarga = urlCortas.objects.get(urlCorta=cuerpo)
            urlLarga = urlLarga.urlLarga # el objeto obtengo la string
            urlCorta = cuerpo
            respuesta = decorateHTML('<title>URL Acortada</title>'\
                                    +'<h3>URL corta ya incluida:</h3>'\
                                    +'<p1>URL Larga: <a href= '\
                                    +urlLarga + '>' + urlLarga + '</a></p>'\
                                    +'<p>URL Corta: <a href= '\
                                    +urlCorta + '>'\
                                    +urlCorta + '</a></p>')
            print ('Encontrada!')
        except:
            # Buscar la url larga recibida y devolver o crear
            try:
                print ('Buscando coincidencia entre las largas...')
                urlCorta = urlLargas.objects.get(urlLarga=cuerpo)
                urlCorta = urlCorta.urlCorta # el objeto obtengo la string
                print 'URL encontrada, devolviendo almacenada'
            except:
                print 'URL no encontrada, creando...'
                urlCorta = myURL()+'/'+str(seqNumb)
                # Almacenando en BD...
                urlAux = urlLargas(urlLarga=cuerpo, urlCorta=urlCorta)
                urlAux.save()
                urlAux = urlCortas(urlCorta=urlCorta, urlLarga=cuerpo)
                urlAux.save()
                print ('Creada!')
            respuesta = decorateHTML('<title>URL Acortada</title>'\
                                    +'<p1>URL Larga: <a href= '\
                                    +cuerpo + '>' + cuerpo + '</a></p>'\
                                    +'<p>URL Corta: <a href= '\
                                    +urlCorta + '>'\
                                    +urlCorta + '</a></p>')
            print ('homePage.POSTorPUT OK!')
    else:
        # _________________ FAIL METHOD _________________
        print 'Error: Recibido metodo desconocido'
        respuesta = ''
    
    return HttpResponse(respuesta)

# ----------------- GetShort ----------------- FALTA PROBARLA TRAS POST !!!!!!!
def GetShort(request, recurso):
    # Creates file "URLs.pkl" for further use, if doesn't exists 
#    urlsCortas = 'URLsShort'
#    initFile((urlsCortas+'.pkl'))
#    urlCortas = {} # SeqN  URL
#    urlCortas = LoadURLs(urlsCortas)
    print('Recibido GET/...')
    urlCorta = myURL()+'/'+str(int(recurso))
    
    try:
        print('Buscando en cortas...')
        urlLarga = urlCortas.objects.get(urlCorta=urlCorta)
        urlLarga = urlLarga.urlLarga
        respuesta = decorateHTML('<meta http-equiv="Refresh" content="0;'\
                                +'url='+urlLarga+'">')
        print('Encontrado!')
    except:
        print 'Detectada peticion inconsistente'
        respuesta = decorateHTML('<h3>Recurso no disponible</h3>'\
                                +'<p>Codigo de error: 404</p>')    
    return HttpResponse(respuesta)
"""
    
    
    
    
    
    
    
 
