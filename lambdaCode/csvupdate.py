# Dependancies >>>
import requests
import json
import pandas as pd 
import boto3
from io import StringIO
from datetime import datetime

s3 = boto3.client('s3')


def lambda_handler(event, context):
    #Time tracing
    now = datetime.now()
    nowStr = now.strftime("%d_%m_%Y_%H_%M_%S")
    # s3 Bucket variabels
    bucketEngg = "yash-aws-data-engg-bucket"
    bucketCsv ='yash-all-csv-bucket'
    objectKey = 'completeDf.csv'


    # API variabels
    api = "b1e187f92fce4dacaf9d7b010fb369aa"
    query = "Tech"
    language = ["en","de"]
    url = f"https://newsapi.org/v2/everything?q={query}&language={language[0]}&apiKey={api}"

    # Geting response from API
    response = requests.get(url)
    data = response.json()
    json_object = json.dumps(data, indent = 4) 
    print(f"Received json_object from API and now converting it into a pandas file")

    # Upload json to s3 bucket 'yash-aws-data-engg-bucket'
    fileName = f"NewsApi_{nowStr}.json"
    uploadByte = bytes(json.dumps(data).encode('UTF-8'))
    s3.put_object(Bucket=bucketEngg,Key=fileName,Body=uploadByte)

    # Received json_object from API and now converting it into a pandas file
    df = pd.read_json(json_object)
    bn=pd.DataFrame(df.articles.values.tolist())
    cn=pd.DataFrame(bn.source.values.tolist())
    newDf = pd.concat([cn,bn],axis=1)
    newDf.drop('source',axis=1,inplace=True)
    print(f"Latest pandas file from the API with data cleanning done as newDf")

    ## Latest pandas file from the API with data cleanning done as "newDf" 

    # Colecting old data from s3 bucket 'yash-all-csv-bucket'
    csv_obj = s3.get_object(Bucket=bucketCsv, Key=objectKey)
    body = csv_obj['Body']
    csv_string = body.read().decode('utf-8')
    oldDf = pd.read_csv(StringIO(csv_string))
    print(f"Colecting old data from s3 bucket")

    # Concatinating both "newDf" and "oldDf" together
    completeDf = pd.concat([oldDf,newDf],axis=0)
    print(f'Concatinating both "newDf" and "oldDf" togethe')

    # Upload "completeDf" to s3 'yash-all-csv-bucket'
    csv_buffer = StringIO()
    completeDf.to_csv(csv_buffer,index=False)
    s3_resource = boto3.resource('s3')
    s3_resource.Object(bucketCsv, 'completeDf.csv').put(Body=csv_buffer.getvalue())

    print(f'All Completed')