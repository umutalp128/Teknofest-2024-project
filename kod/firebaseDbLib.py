import firebase_admin
from firebase_admin import credentials,firestore,storage
from google.cloud.datastore.helpers import GeoPoint

credentialData = credentials.Certificate("./credentials.json")
firebase_admin.initialize_app(credentialData,{
    'storageBucket': 'teknofest-2024.appspot.com'
})
firestoreDb = firestore.client()
bucket=storage.bucket()
current_id = ""
plakaFile = open("plaka.txt","r")
plaka = plakaFile.readline()
plakaFile.close()

def init():
    docs = (
        firestoreDb.collection("MainCollection")
        .where(filter=firestore.FieldFilter("Plaka", "==", plaka))
        .stream()
    )
    a = 0
    for doc in docs:
        if a == 0:
            print(f"{doc.id} => {doc.to_dict()}")
            current_id = doc.id
        else:
            print("database error")
            exit(1)
    a = a + 1
    arac_ref = firestoreDb.collection("MainCollection").document(current_id)
    return arac_ref, doc, current_id

#arac_ref, doc, current_id = init()
#gpsEnabled = doc.to_dict().get("GpsEnabled")

def algilanmaArttir():
    arac_ref, doc, current_id = init()
    count = doc.to_dict().get("Algilandi")
    count = count + 1
    arac_ref.set({"Algilandi" : count}, merge=True)
    


def upload_file(blob_adi:str,data): 
    arac_ref, doc, current_id = init()
    dosya_adi = current_id + "/" + blob_adi
    blob = bucket.blob(dosya_adi)
    blob.upload_from_file(data, content_type="image/jpeg")
    arac_ref.set({"sonResimAdi" : blob_adi}, merge=True)

#def update_gps_data(longitude:int, latitude:int):
#    arac_ref, doc, current_id = init()
#    GpsData = GeoPoint(float(longitude), float(latitude))
#    arac_ref.set({"Gps" : GpsData}, merge=True)
