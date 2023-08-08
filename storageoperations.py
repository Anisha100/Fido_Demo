import os, uuid
from azure.identity import DefaultAzureCredential
from azure.storage.blob import *


    
connect_str='DefaultEndpointsProtocol=https;AccountName=tushki;AccountKey=plkdYHXuyWvmFeSTJ9BEWGn2jev/sw7nBAvay5GCVEg/OIkd2Rru4fwaTo5eJ8mMC1I+TKgElhaR+AStF6NLnA==;EndpointSuffix=core.windows.net'
   
blob_service_client=BlobServiceClient.from_connection_string(connect_str)
container_name='cryptof2'
container_client =blob_service_client.get_container_client(container_name)
  
def uploadpick(data,username):

         blob_client = blob_service_client.get_blob_client(container=container_name,blob=username)
         blob_client.upload_blob(data)   
def downloadpick(username):
         
    aaa=container_client.download_blob(username).readall()
    return aaa
