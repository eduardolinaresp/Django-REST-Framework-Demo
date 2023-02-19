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

## definir clase serialize

    En directorio apiBasic  crear archivo serializer.py e importar dependencias
    from rest_framework import serializers
    from .models import Article 

## crear un Article desde el shell de django

    python manage.py shell
    from apiBasic.models import Article
    from apiBasic.serializer import ArticleSerializerser
    from rest_framework.renderers import JSONRenderer
    from rest_framework.parsers import JSONParser
    a  = Article(title='Titulo', author='ELINARES', email='elinares@email.com')
    a.save()


