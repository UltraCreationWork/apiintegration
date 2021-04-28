import random
import string
from django.conf import settings
from django.core.cache import cache

def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))


def unique_order_id_generator(instance):
	order_new_id= random_string_generator()

	Klass= instance.__class__

	qs_exists= Klass.objects.filter(order_id= order_new_id).exists()
	if qs_exists:
		return unique_order_id_generator(instance)
	return order_new_id


 # def _set_cache_storage():
	# pass

 # def _get_cache_storage():
	# pass