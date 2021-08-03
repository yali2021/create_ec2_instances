import boto3
import os

AMI = os.environ['AMI']
REGION = os.environ['REGION']
INSTANCE_TYPE = os.environ['INSTANCE_TYPE']
SUBNET_ID = os.environ['SUBNET_ID']
KEY_NAME = os.environ['KEY_NAME']

ec2 = boto3.resource('ec2', region_name = REGION)

def lambda_handler(event, context):
    message = event['message']
    init_script = """#!/bin/bash 
                yum -y install httpd 
                systemctl enable httpd 
                systemctl start httpd 
                echo """ + message + """ > /var/www/html/index.html
                """
    instance = ec2.create_instances(
        ImageId = AMI,
        InstanceType = INSTANCE_TYPE,
        KeyName = KEY_NAME,
        SubnetId = SUBNET_ID,
        UserData = init_script,
        MaxCount = 1,
        MinCount = 1
    )

    print("New instance created:", instance[0].id)