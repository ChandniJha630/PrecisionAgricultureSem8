from pymongo import MongoClient

uri = 'mongodb+srv://chandnijha630:abc@cluster0.mbrxcya.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
       
client = MongoClient(uri,  tls=True,
    tlsAllowInvalidCertificates=False)

try:
    print(client.list_database_names())
except Exception as e:
    print("Connection error:", e)
