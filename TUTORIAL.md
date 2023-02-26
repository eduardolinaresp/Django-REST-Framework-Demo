## Tutorial

    https://morioh.com/p/1a02a4984d13?f=5c21fb01c16e2556b555ab32


## crear api basic

    python manage.py startapp apiBasic

## crear superusuario

    python manage.py createsuperuser

    elinares@email.com
    elinares@email.com
    11223344

## instalar extensiones vscode

    django - Baptiste Darthenay

##  crear modelo de aplicacion apiBasic

    Modelo Article

##  referenciar aplicaciones en setting.py

        INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'rest_framework', 
        'apiBasic',
        
    ]

## Ejecutar migraciones para aplicacion apiBasic

     python manage.py makemigrations
     python manage.py migrate

## definir administracion para modelo de aplicacion apiBasic

    En apiBasic/admin.py

    from django.contrib import admin
    from .models import Article
    admin.site.register(Article)

## Serializers

### definir clase serialize

    En directorio apiBasic  crear archivo serializer.py e importar dependencias
    from rest_framework import serializers
    from .models import Article 

### crear un Article desde el shell de django

    1- crear un objeto artículo

    python manage.py shell
    from apiBasic.models import Article
    from apiBasic.serializer import ArticleSerializerser
    from rest_framework.renderers import JSONRenderer
    from rest_framework.parsers import JSONParser
    a  = Article(title='Titulo', author='ELINARES', email='elinares@email.com')
    a.save()

    2- Ver objeto artículo

    serializer = ArticleSerializerser(a)
    serializer.data

    3- Ver JSON artículo

    content = JSONRenderer().render(serializer.data)
    content

    4- Ver colección de artículo serializados

    serializer = ArticleSerializerser(Article.objects.all(), many=True)
    serializer.data

## Model serializer

### definir clase Model serializer

    AuthorSerializerser(serializers.ModelSerializer):

 ### En shell de django ver propiedades de AuthorSerializerser   
    
    serializer = AuthorSerializerser()
    print(repr(serializer))

## Function Api Views

### Importar dependencias en archivo apiBasic/views.py

    from django.http import HttpResponse, JsonResponse
    from rest_framework import JSONParser
    from .models import Article
    from .serializer import ArticleSerializerser

### Definir metodos en archivo apiBasic/views.py

    def article_list(request):
        if request.method == 'GET':
           articles = Article.object.all()


### Definir rutas en archivo DjangoRESTFrameworkDemo/urls.py

    from django.urls import path , include

     path('', include('apiBasic.urls')),

### Crear archivo urls.py en apiBasic

        from django.urls import path
        from .views import article_list

        urlpatterns = [
            path('article/',  article_list),
        ]

### Comprobar nueva ruta

    http://127.0.0.1:8000/article/

### Omitir validacion csrf

    En apiBasic/views.py agregar para post
    from django.views.decorators.csrf import csrf_exempt

    @csrf_exempt
    def article_list(request):

### Definir rutas para metodos post, put, delete

    En apiBasic/urls.py agregar rutas

    from .views import article_list , article_detail

    urlpatterns = [
        path('article/',  article_list),
        path('detail/<int:pk>/',  article_detail),
        
    ]

### Comprobar nueva ruta
    http://127.0.0.1:8000/detail/2/

## Function Api Views decorators   

    1- Importar dependencias 

        from rest_framework.decorators import api_view
        from rest_framework.response import Response
        from rest_framework  import status
    
    2- Agregar decoradores

        @api_view(['GET','POST'])

    3- Simplificar codigo

        def article_list(request, format=None):
        if request.method == 'GET':
            articles = Article.objects.all()
            serializer = ArticleSerializerser(articles, many=True)
            return Response(serializer.data)      
        elif request.method == 'POST':       
        serializer = ArticleSerializerser(data=request.data)
        if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        @api_view(['GET','PUT','DELETE'])
        def article_detail(request, pk): 
            try:
            article = Article.objects.get(pk=pk)
            except Article.DoesNotExist:
                return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
            if request.method == 'GET':
                serializer = ArticleSerializerser(article) 
                return Response(serializer.data)
            elif request.method == 'PUT':       
                serializer = ArticleSerializerser(article, data=request.data)
                if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            elif request.method == 'DELETE':
                article.delete()
                return HttpResponse(status=status.HTTP_204_NO_CONTENT)
    
    4- resultado
    
       se incorpora un proto swagger para manipular los metodos http

    5-comprobacion 
        http://127.0.0.1:8000/article/
        http://127.0.0.1:8000/detail/1/

## Si se agrega nuevo campo al modelo 
        
        Modificar clase Model serializer por esto asi se obtiene todos los campos 

        #fields = ['id','title', 'author', 'email']
        fields = '__all__'

## Class based api views

### Modificar en apiBasic.views
    
    En apiBasic
    
    1- Importar Librerias en archivo apiBasic.views 

      from rest_framework.views import APIView

    2- Definir clase ArticleAPIview en archivo apiBasic.views  

        class ArticleAPIView(APIView):
        def get(self, request):
            articles = Article.objects.all()
            serializer = ArticleSerializerser(articles, many=True)
            return Response(serializer.data)
        def post(self, request):
            serializer = ArticleSerializerser(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

    3- Importar y Definir ruta en archivo apiBasic.urls

        from .views import article_list , article_detail, ArticleAPIView

        urlpatterns = [
            #path('article/',  article_list),
            path('article/',  ArticleAPIView.as_view()),
            path('detail/<int:pk>/',  article_detail),
        ]
    
]   4- comprobar en http://127.0.0.1:8000/article/
    
      Enviar cuerpo

       {            
            "title": "Titulo3",
            "author": "ELINARES",
            "email": "elinares@email.com",
            "date": "2023-02-19"
        }
    5- resultado OK

    6- Para el resto de operaciones http 
        
        definir clase ArticleDetails

        class ArticleDetails(APIView):
        def get_object(self, id):
            try:
            return Article.objects.get(id=id)
            except Article.DoesNotExist:
                return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
            
        def get(self, request, id):
            article = self.get_object(id)
            serializer = ArticleSerializerser(article) 
            return Response(serializer.data)
        def put(self, request, id):
            serializer = ArticleSerializerser(article, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        def delete(self, request, id):
            article = self.get_object(id)
            article.delete()
            return HttpResponse(status=status.HTTP_204_NO_CONTENT)

  6- Importar y Definir ruta en archivo apiBasic.urls

        from .views import article_list , article_detail, ArticleAPIView, ArticleDetails

        urlpatterns = [
            #path('article/',  article_list),
            path('article/',  ArticleAPIView.as_view()),
            #path('detail/<int:pk>/',  article_detail),
            path('detail/',  ArticleDetails.as_view()),
            
        ]

## Generic Views and mixims

    En apiBasic
    
    1- Importar Librerias en archivo apiBasic.views 

        from rest_framework import generics
        from rest_framework import mixins

    2- Definir clase GenericAPIView

        class GenericAPIView(generics.GenericAPIView,mixins.ListModelMixin,mixins.CreateModelMixin,
                            mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
            serializer_class =   ArticleSerializerser
            queryset = Article.objects.all()
            
            lookup_field = 'id'
            
            def get(self, request, id =None):
                if id:
                    return self.retrieve(request)
                else:    
                    return self.list(request)
            
            def post(self, request):
                return self.create(request)
            
            def put(self, request, id=None):
                return self.update(request, id)
            
            def delete(self,request):
                return self.destroy(request,id)

    3- Importar y Definir ruta en archivo apiBasic.urls

        from .views import article_list , article_detail, ArticleAPIView, ArticleDetails, GenericAPIView

        urlpatterns = [
            #path('article/',  article_list),
            path('article/',  ArticleAPIView.as_view()),
            #path('detail/<int:pk>/',  article_detail),
            path('detail/',  ArticleDetails.as_view()),
            path('generic/article/<int:id>/',  GenericAPIView.as_view()),
            
        ]

## Authentications

   1- Comprobar url antes de autenticación.

       http://127.0.0.1:8000/generic/article/1/

   2- En archivo apiBasic.views importar

        from rest_framework.authentication import SessionAuthentication,BasicAuthentication
        from rest_framework.permissions import IsAuthenticated

   3- En Clase GenericAPIView se agrega autenticacion y permisos

        class GenericAPIView(generics.GenericAPIView,mixins.ListModelMixin,mixins.CreateModelMixin,
                            mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
            serializer_class =   ArticleSerializerser
            queryset = Article.objects.all()
            
            lookup_field = 'id'
            
            authentication_classes = [SessionAuthentication, BasicAuthentication]
            permission_classes = [IsAuthenticated]

   4-   Comprobar url despúes de autenticación

        4.1- Desloguearse de la aplicación, ir a url admin y clickear boton logout
        
           http://127.0.0.1:8000/admin/
        
        4.2- comprobar nuevamente la ruta del articulo. 
        
            http://127.0.0.1:8000/generic/article/1/

            En esta oportunidad el navegador nos indica el siguiente mensaje 

            {
             "detail": "Authentication credentials were not provided."
            }

        4.3- con postman se puede probar basic authentication 


            TODO: agregar extension a visual studio para probar desde acá.

    5- Agregar autenticación por token 

       5.1- Ir a arcvhivo DjangoRESTFrameworkDemo.settings y agregar aplicación 'rest_framework.authtoken'

            INSTALLED_APPS = [
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'rest_framework',
            'apiBasic',
            'rest_framework.authtoken',
            
        ]
        
        NOTA: Grabar archivo!

     5.2- Realizar migraciones para la aplicación 'rest_framework.authtoken'

            python manage.py makemigrations
            python manage.py migrate
     
     5.3- Ir al sitio de administracion de django (loggearse)

           
             http://127.0.0.1:8000/admin/

     5.4- agregar nuevo token 

        5.4.1 Desde el panel de AUTH TOKEN presionar el boton + 
        5.4.2 Seleccionar el usuario, en este caso, "ELINARES@EMAIL.COM"  y guardar.

     5.5- En archivo apiBasic.views importar TokenAuthentication

         from rest_framework.authentication import SessionAuthentication,TokenAuthentication,BasicAuthentication

     5.6- En archivo apiBasic.views, metodo GenericAPIView, habiliar TokenAuthentication

        5.6.1 Comentar #authentication_classes = [SessionAuthentication, BasicAuthentication]
        5.6.2 Agregar authentication_classes = [TokenAuthentication]
    
     5.7- Comprobar autenticacion por tokens

         5.7.1 ir a postman agregar en headers: Key=  authorization value = el token que nos entrego el admin de django para el usuario "ELINARES@EMAIL.COM"
         5.7.2 efectuar peticion a url http://127.0.0.1:8000/generic/article/1/
    
## ViewSet & Routers

    1- En archivo apiBasic.views Importar  

        from rest_framework import viewsets
        from django.shortcuts import get_object_or_404

    2- En archivo apiBasic.views crear clase ArticleViewSet 

        class ArticleViewSet(viewsets.ViewSet):
            def list(self, request):
                articles = Article.objects.all()
                serializer = ArticleSerializerser(articles, many=True)
                return Response(serializer.data)   
            
            def create(self, request):
                serializer = ArticleSerializerser(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
            def retrieve(self,request,pk=None):
                queryset = Article.objects.all()
                article = get_object_or_404(queryset,pk)
                serializer = ArticleSerializerser(articles)
                return Response(serializer.data)   

    3- En archivo apiBasic.url importar 

     3.1 importar ArticleViewSet
     3.2 importar DefaultRouter
     3.3 importar include
     3.3- resultado

           from .views import article_list , article_detail, ArticleAPIView, ArticleViewSet, ArticleDetails, GenericAPIView

           from rest_framework.routers import DefaultRouter
           from django.conf.urls import include

    3- En archivo apiBasic.url crear instancia de DefaultRouter y registrar ArticleViewSet.

        router = DefaultRouter()
        router.register('article', ArticleViewSet, basename="article") #el parametro basename es un alias

    4- En urlpatterns agregar nueva ruta para utilizar router

        router = DefaultRouter()
        router.register('article', ArticleViewSet, basename="article") #el parametro basename es un alias 

        urlpatterns = [
               path('viewset/', include(router.urls)), # El path name puede ser cualquiera  
               #path('article/',  article_list),
               path('article/',  ArticleAPIView.as_view()),
               #path('detail/<int:pk>/',  article_detail),
               path('detail/',  ArticleDetails.as_view()),
               path('generic/article/<int:id>/',  GenericAPIView.as_view()),                
            ] 
    5- Comprobar nueva ruta viewset (LIST)

       http://127.0.0.1:8000/viewset/article/

    6- comprobar ruta base, desde el menu path de la api (Api Root)
        
      6.1 Clickear Api Root -> http://127.0.0.1:8000/viewset/
      
      
        muestra listado de rutas aceptadas, entre ellas viewset/article

        {
            "article": "http://127.0.0.1:8000/viewset/article/"
        }


    7- comprobar desde browser post sobre http://127.0.0.1:8000/viewset/article/

    7.1- Realizar post para comprobar ruta y router

       NOTA: Seleciono el ultimo post y cambio el titulo a: "title": "viewset-data",

            {
                "title": "viewset-data",
                "author": "ELINARES",
                "email": "elinares@email.com",
                "date": "2023-02-19"
            }
    7.2- Verifico que el sistema me entrega 201 HTTP => Implica creo un nuevo registro
    
    7.3- agrego en apiBasic.url

         path('viewset/<int:pk>/', include(router.urls)), " bajo path('viewset/', include(router.urls)), # El path name puede ser cualquiera "

    7.4- Compruebo funcionamiento metodo update de la clase ArticleViewSet

         Se envia este request, por browser o postman

            {
                "id": 4,
                "title": "Esto se actualizó por api-viewset-data",
                "author": "ELINARES",
                "email": "elinares@email.com",
                "date": "2023-02-26"
            }
    7.5 trato de actualizar un registro

        http://127.0.0.1:8000/viewset/article/2/

        Error: not enough values to unpack (expected 2, got 1)



## Generic ViewSet 

    Se comenta clase class ArticleViewSet     
    se crea nueva definicion 
        class ArticleViewSet(viewsets.GenericViewSet,mixins.ListModelMixin)
    se comprueba url  
        http://127.0.0.1:8000/viewset/article/      
        NOTA: Es ok aparece get
    se agrega mixins.CreateModelMixin
        class ArticleViewSet(viewsets.GenericViewSet,mixins.ListModelMixin,mixins.CreateModelMixin)
    se comprueba url 
        http://127.0.0.1:8000/viewset/article/
        NOTA: Es ok aparece post                
    se agrega mixins.UpdateModelMixin
        class ArticleViewSet(viewsets.GenericViewSet,mixins.ListModelMixin,mixins.CreateModelMixin,
                     mixins.UpdateModelMixin   ): 
    se comprueba url 
        http://127.0.0.1:8000/viewset/article/1/ 
        NOTA: Es ok aparece put
    se agrega mixins.RetrieveModelMixin
        class ArticleViewSet(viewsets.GenericViewSet,mixins.ListModelMixin,mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,mixins.RetrieveModelMixin  ):  
    se comprueba url 
        http://127.0.0.1:8000/viewset/article/1/ 
        NOTA: Es ok aparece put  y se cargan valores previos 
    se agrega mixins.DestroyModelMixin.
        class ArticleViewSet(viewsets.GenericViewSet,mixins.ListModelMixin,mixins.CreateModelMixin,
                     mixins.UpdateModelMixin , mixins.RetrieveModelMixin ,mixins.DestroyModelMixin ):
    se comprueba url 
        http://127.0.0.1:8000/viewset/article/1/ 
        NOTA: Es ok aparece boton delete  y se cargan valores previos   

## Modal ViewSets

    se comenta implementacion ArticleViewSet
    se crea nueva implementacion para ArticleViewSet

        class ArticleViewSet(viewsets.ModelViewSet ): # Example REST Framework Modal ViewSets
                serializer_class =   ArticleSerializerser
                queryset = Article.objects.all()
    se comprueba url 
        http://127.0.0.1:8000/viewset/article/
        NOTA: Es ok aparece post y el listado previo de articulos
    se comprueba url 
        http://127.0.0.1:8000/viewset/article/1/ 
        NOTA: Es ok aparece boton delete, put  y se cargan valores previos   

## FIN