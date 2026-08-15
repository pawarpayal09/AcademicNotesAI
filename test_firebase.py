import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


SERVICE_ACCOUNT_PATH = (
    r"D:\MCA Sem 3\LLM\firebase_credentials\firebase_service_account.json"
)

cred = credentials.Certificate(
    SERVICE_ACCOUNT_PATH
)


firebase_admin.initialize_app(
    cred
)


db = firestore.client()


print("Firebase Admin SDK: OK")
print("Firestore connection: OK")