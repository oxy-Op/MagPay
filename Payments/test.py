import json

def add(id,method,no):
   with open(f'database/{id}.json','w') as db:
       data = {
           id:{
               'method':method,
               'payid':no
           }
       }
       json.dump(data,db,indent=2)

add(1234567,'googlepay',9771537292)
add(5432,'paypal',9122153224)

def get(id):
    with open(f'database/{id}.json','r') as x:
        db = json.load(x)
        data = db[f'{id}']['method']
        payid = db[f'{id}']['payid']
        print("Method - ",data,", Authentication - ",payid)
        
get(1234567)
get(5432)