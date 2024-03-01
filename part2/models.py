from mongoengine import connect, Document, StringField, EmailField, BooleanField


connect(host='mongodb+srv://userhw8:<PASS>@atlascluster.dkms1wa.mongodb.net/?retryWrites=true&w=majority&appName'
             '=AtlasCluster', ssl=True)


class User(Document):
    fullname = StringField(max_length=150, required=True)
    user_email = EmailField(unique=True, required=True)
    user_phone = StringField(max_length=50, required=True)
    message_sent = BooleanField(default=False)
    pref_method = StringField()
    meta = {"collection": "users"}