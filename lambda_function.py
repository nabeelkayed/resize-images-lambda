import boto3
from PIL import Image
import io

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    object_key = event['Records'][0]['s3']['object']['key']
    
    response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
    image_data = response['Body'].read()
    
    image = Image.open(io.BytesIO(image_data))
    
    resized_image = image.resize((200, 200))
    
    buffer = io.BytesIO()
    resized_image.save(buffer, format=image.format)
    buffer.seek(0)
    
    s3_client.put_object(Bucket='processed-images-nabeel' , Key=f'resized/{object_key}', Body=buffer)
    
    return {
        'status': 'Done',
        'body': f'Resized image uploaded as resized/{object_key}'
    }
