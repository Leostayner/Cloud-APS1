import boto3

Owner    = input("Owner: ")
Key_pub  = input("Public Key dir: ") 
key_name = input("New key Name: ")
SecurityGroup = input("Security Group Name: ")

def save(name, data):
    outfile = open(name,'w')
    outfile.write(data)
    outfile.close()
    print("Key Pair Saved")

def create_key_pair(client):
    try:
        response = client.delete_key_pair(
            KeyName=key_name,
        )
        print("Delete old Key Pair")

    except:
        pass

    k = open(Key_pub, "r")
    response = client.import_key_pair(
    KeyName = key_name,
    PublicKeyMaterial = k.read()
    )         

def create_security_group(client):
    try:
        client.delete_security_group(
            GroupName= SecurityGroup,
        )
        print("Delete Old Security Group")
    
    except:
        pass

    s_gp = client.create_security_group(
        Description='Security group',
        GroupName = SecurityGroup,
    )
    print("Create Security Group")

    client.authorize_security_group_ingress(
        GroupName =SecurityGroup,
        IpPermissions = [{
                'IpProtocol' :"tcp",
                'FromPort' : 5000,
                'ToPort'  : 5000,
                'IpRanges': [{"CidrIp" : "0.0.0.0/0"}]
                },
                {
                'IpProtocol' :"tcp",
                'FromPort' : 22,
                'ToPort' : 22,        
                'IpRanges': [{"CidrIp" : "0.0.0.0/0"}]
                }
            ]
        
    )
    print("Authorize Security Group")

def create_instance(ec2):
    instances = ec2.create_instances(
        ImageId='ami-0ac019f4fcb7cb7e6',
        MinCount= 1,
        MaxCount= 1,
        InstanceType = 't2.micro',
        SecurityGroups = [SecurityGroup],
        KeyName= "key_name",
        TagSpecifications=[
            {
                'ResourceType': 'instance',

                'Tags': [
                    {
                        'Key': 'Owner',
                        'Value': Owner + " LB",
                    },
                ]
            }          
        ],
        UserData = """#!/bin/bash
        git clone https://github.com/Leostayner/Cloud-APS1
        cd /Cloud-APS1  
        . install_load.sh
        """
    )

    print("Create Instance")
    

def check_terminate(ec2, client):
    print("Check Treminate")
    list_instances = ec2.instances.filter(Filters=[{
    'Name': 'instance-state-name',
    'Values': ['running']}])
    
    list_id = []
    
    for instance in list_instances:
        list_tags = (instance.tags)

        try:
            for tag in list_tags:
                if (tag["Key"] == "Owner") and (Owner in tag["Value"]):
                    list_id.append(instance.id)
                             
        except:
            pass
        
    if len(list_id) > 0:
        terminate_instances(client, list_id)

def terminate_instances(client, list_id):
    waiter = client.get_waiter('instance_terminated')
    client.terminate_instances(
        InstanceIds = list_id
    )
    print("Wait Delete {0} Instance".format(len(list_id)))
    waiter.wait(InstanceIds=list_id)
    print("Instances Deleted: {0}".format(len(list_id)))



#Client and Resource
client = boto3.client('ec2')
ec2 = boto3.resource('ec2')

#Teminate instances
check_terminate(ec2, client)

#Create Key Par
create_key_pair(client)

# Create Security Group
create_security_group(client)

# Create Instance
create_instance(ec2)






