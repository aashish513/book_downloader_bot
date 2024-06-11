
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

load_dotenv()

class Database:
    def __init__(self):
        print("Will connect to mongodb when needed")
        self.uri = f'mongodb+srv://{os.getenv("MONGO_USER")}:{os.getenv("MONGO_PASS")}@libgenidtelegramid.i6kg5nj.mongodb.net/?retryWrites=true&w=majority&appName=libgenIdTelegramId'
        self.client=None
        self.my_collection=None

        

    
    def connect(self, reconnect = False):  #connect if not connected
        if self.client:
            if reconnect:
                try:
                    self.client.admin.command('ping')
                    return
                except:
                    print("[INFO]MongoDb wasn't running")
                    self.disconnect()
            else:
                return
        
        # Create a new client and connect to the server
        self.client = MongoClient(self.uri, server_api=ServerApi('1'))
        self.my_collection = self.client['database_name'].get_collection('libgen_to_tele')
        print("Connected to MongoDB!")
        self.connect()

    def disconnect(self):
        print("Disconnecting MongoDB if client exists")
        if self.client:
            try:
                self.client.close()   #todo use try, except pass
            except Exception as e:
                print("This should only print when self.client was not already connected")
                pass



    def print_all_records(self):
        documents = self.my_collection.find()
        for doc in documents:
            print(doc)


    def insert_row(self, libgen_id, tele_id):
        self.connect()
        new_document = {
            'libgen_id': int(libgen_id),
            'tele_id': int(tele_id)}

        try:
            result = self.my_collection.insert_one(new_document)
            print(f"Inserted document ID: {result.inserted_id}")
        except Exception as e:
            print("Error 11f", e)
            self.connect(reconnect=True)
            result = self.my_collection.insert_one(new_document)
            print(f"Inserted document ID: {result.inserted_id}")


    def find_row(self, libgen_id):
        self.connect()
        query = {'libgen_id': int(libgen_id)}
        try:
            document = self.my_collection.find_one(query)
        except Exception as e:
            print("Error 294", e)
            self.connect(reconnect=True)
            document = self.my_collection.find_one(query)
        
        if document:
            print(f"Found document: {document}")
            return document['tele_id']
        else:
            print("No document found with id1 = 5")
            return None


