## 1 Preparar entorno virtual

    python -m venv .venv 
    .venv\scripts\activate

## 2 Instalar Django REST Framework

    pip install django
    pip install djangorestframework

    django-admin startproject Django-REST-Framework-Demo .

## 3 Definir directorio base

    cd DjangoRESTFrameworkDemo

## 4 Ejecutar migraciones

    python manage.py migrate

## Iniciar Servidor de desarrollo

    python manage.py runserver


## Agregar tag al avance 

    git tag -a Sin-decoradores-en-vistas 2c473a6 
    git push origin --tags

## Establecer en archivo de proyecto librerias utilizadas.

    pip freeze > requirements.txt 