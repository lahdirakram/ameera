import hashlib
from django.utils.crypto import get_random_string


class Hash():

	def generate_id(user):

		rand =get_random_string(length=128)
		m = hashlib.sha256()
		m.update(str.encode(rand)+str.encode(user.vend_user_name))
		hashed=m.hexdigest()
		
		hashed2=Hash.get_id(hashed)

		return {'hashed':hashed,'hashed2':hashed2}

	def get_id(first_hash):
		
		d= hashlib.md5()
		d.update(str.encode(first_hash))
		hashed2=d.hexdigest()

		return hashed2
