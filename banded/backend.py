from django.contrib.auth.models import User

class EmailAuth:
	def authenticate(self, email = '', password = ''):
		try:
			user = User.objects.get(email = email)
			if user.check_password(password):
				return user
			else:
				return None
		except Exception, e:
			print str(e)
			return None
	def get_user(self, user_id = ''):
		try:
			return User.objects.get(pk = user_id)
		except User.DoesNotExist:
			return None
