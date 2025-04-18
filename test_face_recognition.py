import requests
import os
from PIL import Image
import io
import re

# URL base del servidor
BASE_URL = 'http://localhost:8000'

def get_csrf_token(session):
    # Obtener el token CSRF de la página de registro
    print("Obteniendo página de registro...")
    response = session.get(f'{BASE_URL}/user/register/')
    print(f"Status Code: {response.status_code}")
    print(f"Headers: {dict(response.headers)}")
    print(f"Contenido: {response.text[:500]}...")  # Mostrar los primeros 500 caracteres
    
    csrf_token = None
    
    # Buscar el token en el HTML
    match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', response.text)
    if match:
        csrf_token = match.group(1)
        print(f"Token CSRF encontrado: {csrf_token}")
    else:
        print("No se encontró el token CSRF en la página")
    
    return csrf_token

def test_registration():
    print("\n=== Probando Registro ===")
    try:
        # Crear una sesión para mantener las cookies
        session = requests.Session()
        
        # Obtener el token CSRF
        csrf_token = get_csrf_token(session)
        if not csrf_token:
            print("No se pudo obtener el token CSRF")
            return False

        # Datos para el registro
        register_data = {
            'username': 'test_user',
            'password': 'test_password',
            'family_group': '',
            'csrfmiddlewaretoken': csrf_token
        }

        # Leer la imagen
        with open('face.jpg', 'rb') as f:
            image_data = f.read()

        # Crear los archivos para la solicitud
        register_files = {
            'face_image': ('face.jpg', image_data, 'image/jpeg')
        }

        # Headers necesarios
        headers = {
            'Referer': f'{BASE_URL}/user/register/'
        }

        # Intentar registro
        response = session.post(
            f'{BASE_URL}/user/register/',
            data=register_data,
            files=register_files,
            headers=headers
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        print(f"Contenido: {response.text}")
        try:
            print(f"JSON: {response.json()}")
        except:
            print("No se pudo parsear la respuesta como JSON")
        return response.status_code == 200
    except Exception as e:
        print(f"Error durante el registro: {str(e)}")
        return False

def test_login():
    print("\n=== Probando Login ===")
    try:
        # Crear una sesión para mantener las cookies
        session = requests.Session()
        
        # Obtener el token CSRF
        csrf_token = get_csrf_token(session)
        if not csrf_token:
            print("No se pudo obtener el token CSRF")
            return False

        # Leer la imagen
        with open('face.jpg', 'rb') as f:
            image_data = f.read()

        # Crear los archivos para la solicitud
        login_files = {
            'face_image': ('face.jpg', image_data, 'image/jpeg')
        }

        # Headers necesarios
        headers = {
            'Referer': f'{BASE_URL}/user/login/',
            'X-CSRFToken': csrf_token
        }

        # Datos del formulario
        login_data = {
            'csrfmiddlewaretoken': csrf_token
        }

        # Intentar login
        response = session.post(
            f'{BASE_URL}/user/login/',
            data=login_data,
            files=login_files,
            headers=headers
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        print(f"Contenido: {response.text}")
        try:
            print(f"JSON: {response.json()}")
        except:
            print("No se pudo parsear la respuesta como JSON")
        return response.status_code == 200
    except Exception as e:
        print(f"Error durante el login: {str(e)}")
        return False

if __name__ == "__main__":
    # Verificar que la imagen existe
    if not os.path.exists('face.jpg'):
        print("Error: No se encontró la imagen face.jpg")
        exit(1)

    # Ejecutar pruebas
    registration_success = test_registration()
    if registration_success:
        login_success = test_login()
        if login_success:
            print("\n¡Prueba exitosa! El sistema de reconocimiento facial funciona correctamente.")
        else:
            print("\nError: El login falló después de un registro exitoso.")
    else:
        print("\nError: El registro falló.") 