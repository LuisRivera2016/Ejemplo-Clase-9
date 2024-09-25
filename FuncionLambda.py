import json
import base64
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

def lambda_handler(event, context):
    # Configura el cliente S3
    s3 = boto3.client('s3')
    
    # Definir el nombre del bucket
    bucket_name = 'pruebalambdasemi1'

    try:
        # Extraer el JSON del evento
        body = json.loads(event.get('body', '{}'))
        image_name = body.get('image_name', 'imagen.jpg')  # Nombre de la imagen
        image_base64 = body.get('image_base64', '') # Imagen en base64
        
        if not image_base64:
            return {
                'statusCode': 400,
                'body': json.dumps('Falta la imagen en base64')
            }
        
        # Decodificar la imagen de base64 a bytes
        image_data = base64.b64decode(image_base64)
        
        # Subir la imagen al bucket S3
        s3.put_object(
            Bucket=bucket_name,
            Key=image_name,
            Body=image_data,
            ContentType='image/jpeg'  # Cambia este tipo según el formato de tu imagen
        )
        
        # Devolver una respuesta exitosa
        return {
            'statusCode': 200,
            'body': json.dumps('Imagen subida con éxito')
        }
    
    except NoCredentialsError:
        return {
            'statusCode': 403,
            'body': json.dumps('No se pueden encontrar las credenciales de AWS')
        }
    
    except PartialCredentialsError:
        return {
            'statusCode': 403,
            'body': json.dumps('Credenciales de AWS incompletas')
        }
    
    except Exception as e:
        # Manejo de excepciones
        return {
            'statusCode': 500,
            'body': json.dumps(f'Ocurrió un error: {str(e)}')
        }
