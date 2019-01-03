from app import application as App


@App.route('/products', methods=['GET'])
def products():
	pass

@App.route('/process', methods=['POST'])
def process():
	pass

@App.route('/checkout', methods=['GET'])
def checkout():
	pass


