from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from .models import User, FamilyGroup
from .forms import UserRegistrationForm
import cv2
import numpy as np
import json
from PIL import Image
import io
import logging

# Configurar el logger
logger = logging.getLogger(__name__)

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                logger.info("Iniciando proceso de registro")
                username = form.cleaned_data['username']
                password = form.cleaned_data['password1']
                face_image = form.cleaned_data['face_image']
                family_group = form.cleaned_data['family_group']

                logger.info(f"Datos recibidos - Usuario: {username}, Grupo familiar: {family_group}")

                # Procesar la imagen facial con OpenCV
                try:
                    logger.info("Procesando imagen facial")
                    # Leer la imagen
                    image_bytes = face_image.read()
                    image = Image.open(io.BytesIO(image_bytes))
                    image_np = np.array(image)
                    
                    # Convertir a escala de grises
                    if len(image_np.shape) == 3:
                        gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
                    else:
                        gray = image_np
                    
                    # Cargar el clasificador de rostros
                    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
                    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

                    if len(faces) == 0:
                        logger.error("No se detectó ningún rostro en la imagen")
                        return JsonResponse({'error': 'No se detectó ningún rostro en la imagen'}, status=400)

                    # Crear usuario
                    logger.info("Creando usuario")
                    user = form.save(commit=False)
                    
                    # Guardar el rostro detectado como encoding
                    x, y, w, h = faces[0]
                    face_roi = gray[y:y+h, x:x+w]
                    face_roi = cv2.resize(face_roi, (100, 100))  # Normalizar tamaño
                    user.face_encoding = face_roi.tobytes()
                    user.save()

                    login(request, user)
                    logger.info(f"Usuario {username} registrado exitosamente")
                    return JsonResponse({'success': True, 'redirect': '/'})
                except Exception as e:
                    logger.error(f"Error al procesar la imagen: {str(e)}")
                    return JsonResponse({'error': f'Error al procesar la imagen: {str(e)}'}, status=400)
            except Exception as e:
                logger.error(f"Error en el registro: {str(e)}")
                return JsonResponse({'error': f'Error en el registro: {str(e)}'}, status=400)
        else:
            errors = dict(form.errors.items())
            return JsonResponse({'error': 'Error en el formulario', 'errors': errors}, status=400)

    form = UserRegistrationForm()
    return render(request, 'user/register.html', {'form': form})

def facial_login(request):
    if request.method == 'POST':
        face_image = request.FILES.get('face_image')
        
        if not face_image:
            return JsonResponse({'error': 'Se requiere una imagen facial'}, status=400)

        # Procesar la imagen de login con OpenCV
        image = Image.open(face_image)
        image_np = np.array(image)
        gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
        
        # Detectar rostros
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        if len(faces) == 0:
            return JsonResponse({'error': 'No se detectó ningún rostro en la imagen'}, status=400)

        # Procesar el rostro detectado
        x, y, w, h = faces[0]
        login_face = gray[y:y+h, x:x+w]
        login_face = cv2.resize(login_face, (100, 100))

        # Buscar coincidencia entre usuarios
        for user in User.objects.all():
            if user.face_encoding:
                stored_face = np.frombuffer(user.face_encoding, dtype=np.uint8).reshape(100, 100)
                
                # Comparar rostros usando la correlación
                correlation = cv2.matchTemplate(login_face, stored_face, cv2.TM_CCOEFF_NORMED)[0][0]
                
                if correlation > 0.7:  # Umbral de similitud
                    login(request, user)
                    return JsonResponse({'success': True, 'redirect': '/'})

        return JsonResponse({'error': 'No se encontró coincidencia facial'}, status=400)

    return render(request, 'user/login.html')

@login_required
def profile(request, username=None):
    if username:
        user = get_object_or_404(User, username=username)
    else:
        user = request.user
        
    tasks = user.assigned_tasks.all()
    created_tasks = user.created_tasks.all()
    
    if user.family_group:
        family_members = User.objects.filter(family_group=user.family_group).order_by('-points')
    else:
        family_members = []

    context = {
        'profile_user': user,
        'tasks': tasks,
        'created_tasks': created_tasks,
        'family_members': family_members
    }
    return render(request, 'user/profile.html', context)

@login_required
def create_family_group(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            family_group = FamilyGroup.objects.create(name=name)
            request.user.family_group = family_group
            request.user.save()
            return JsonResponse({'success': True})
    return JsonResponse({'error': 'Nombre requerido'}, status=400)
