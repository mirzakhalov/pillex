

import pyrebase

config = {
  "apiKey": "AIzaSyBHCM_96N-9mSl2NJyoxH_QzNayIrc3ZvE",
  "authDomain": "pillex.firebaseapp.com",
  "databaseURL": "https://pillex.firebaseio.com",
  "storageBucket": "pillex.appspot.com",
}

firebase = pyrebase.initialize_app(config)



# upload the image
storage.child("images/example.jpg").put("example2.jpg")

def stream_handler(message):
    if message["event"] == "put":
        print(type(message["data"])) # {'title': 'Pyrebase', "body": "etc..."}
    else:
        print(message["event"])

my_stream = db.child("users/jim/results").stream(stream_handler)