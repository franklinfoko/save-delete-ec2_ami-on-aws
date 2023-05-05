import boto3
from datetime import datetime
from datetime import datetime, timedelta

# Créer une session AWS
session = boto3.Session(
    aws_access_key_id='AWS_ACCESS_KEY_ID',
    aws_secret_access_key='AWS_SECRET_ACCESS_KEY',
    region_name='REGION'
)

# Créer une connexion à AWS EC2
ec2 = boto3.client('ec2')

# Obtenir une liste de toutes les instances EC2
instances = ec2.describe_instances()

now = datetime.now()
dt = now.strftime("%d/%m/%Y""-""%H.%M.%S")
print()
print("Debut de sauvegarde des AMIs")

# Parcourir toutes les instances et créer une image AMI
for reservation in instances['Reservations']:
    for instance in reservation['Instances']:
        tags = instance['Tags']
        server_name = tags[0]['Value']
        instance_id = instance['InstanceId']
        image_name = f"{server_name}-AMI-backup-{dt}"
        print(image_name)
        response = ec2.create_image(InstanceId=instance_id, Name=image_name)
        print(f"Instance ID: {instance_id}, Image ID: {response['ImageId']}, Image Name: ${image_name}")


print()
print("Fin de sauvegarde de AMIs")
print()


print("Debut de suppression des anciennes AMIs datant de 7 jours")
# Définir la durée de rétention des images AMI (en jours)
retention_days = 7

# Obtenir une liste de toutes les images AMI
images = ec2.describe_images(Owners=['self'])['Images']

# Parcourir toutes les images et supprimer celles qui ont dépassé la durée de rétention
for image in images:
    image_id = image['ImageId']
    creation_date = datetime.strptime(image['CreationDate'], '%Y-%m-%dT%H:%M:%S.%fZ')
    retention_date = datetime.now() - timedelta(days=retention_days)
    if creation_date < retention_date:
        ec2.deregister_image(ImageId=image_id)
        print(f"Image ID: {image_id} a été supprimée.")
    else:
        print("Pas d'anciennes images a supprimer")
        
