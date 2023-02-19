# Django-REST-Framework-Demo
Ejemplo Django REST Framework

## 1 Preparar entorno virtual

    python -m venv .venv 
    .venv\scripts\activate

## 2 Instalar Django REST Framework

    pip install django
    pip install djangorestframework

    django-admin startproject Django-REST-Framework-Demo .

## Definir directorio base

    cd DjangoRESTFrameworkDemo

## Ejecutar migraciones

    python manage.py migrate

## Iniciar Servidor de desarrollo

    python manage.py runserver

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

## Agregar tag al avance 

    git tag -a Sin-decoradores-en-vistas 2c473a6 
    git push origin --tags

## Establecer en archivo de proyecto librerias utilizadas.

    pip freeze > requirements.txt 


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
                    return self.retrive(request)
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



