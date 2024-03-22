import pyrebase
import os
import requests
from datetime import datetime

class Firebase:
    def __init__(self):
        
        # firebase API keys
        config = {
            "apiKey": "AIzaSyAf0T76wl4Xil88rTg7sLX0wN3_AXzay6Q",
            "authDomain": "ai-smart-classroom.firebaseapp.com", 
            "databaseURL": "https://ai-smart-classroom-default-rtdb.asia-southeast1.firebasedatabase.app", 
            "storageBucket": "1:717041352251:web:e1c2e4ce912b5d0d4de61e"
        }
        firebase = pyrebase.initialize_app(config)
        self.db = firebase.database() # real time database

    def firebase_insert(self,data):
        try:
            requests.head("http://www.google.com/", timeout=3)
        
            date_object = datetime.fromtimestamp(data["last_trigger_time"])
        
            # Format datetime object as "Month day year" and "hour:minute AM/PM"
            formatted_date = date_object.strftime("%B %d %Y")
            formatted_time = date_object.strftime("%I:%M %p")
        
            data_insert = {
                "person_status": data["person_status"],
                "date": formatted_date,
                "time": formatted_time
            }

            self.db.child("History").push(data_insert)
            
        except requests.exceptions.Timeout:
            pass
            print("firebase_insert: Request timed out")

        except requests.exceptions.RequestException as e:
            pass
            print(f"firebase_insert: Request failed - {e}")
       
        except Exception as e:
            pass
            print(f"firebase_insert: Request failed - {e}")
           
        

        
        
        
           
        