from app import application as App
from flask import render_template, request

import requests, json


url = 'https://api.rechargeapps.com/checkouts/'

headers = {
		'X-Recharge-Access-Token':'abc123',
		'Content-Type':'application/json',
		'Accept':'application/json',
	}

@App.route('/products', methods=['GET'])
def products():
	return render_template('products.html')



@App.route('/checkout/', methods=['GET', 'POST'])
def checkout():

	if request.method == 'GET':
		return render_template('checkout.html')

	elif request.method == 'POST':
		#print(json.dumps(request.json,indent=4))
		shipping_address = {
			'first_name':request.json.get('first_name'),
			'last_name':request.json.get('last_name'),
			'zip':request.json.get('zip'),
			'country':request.json.get('country'),
			'province':request.json.get('province'),
			'phone':request.json.get('phone')       if request.json['phone'] else None,
			'company':request.json.get('company')   if request.json['company'] else None,
			'address1':request.json.get('address1'),
			'address2':request.json.get('address2') if request.json['address2'] else None,
			'city':request.json.get('city'),
		}
		data = {}
		data['checkout'] = {}
		#data['checkout']['requires_shipping'] = False
		data['checkout']['shipping_address'] = shipping_address
		data['checkout']['email'] = request.json['email']
		data['checkout']['line_items'] = [{
			'variant_id':3844924611,
			'quantity':5,
		}]

		response = requests.post(url , headers=headers, data=json.dumps(data))

		#print(json.dumps(response.json(),indent=4))

		rates = _get_shipping_rates(response.json()['checkout']['token'])
		#print('/////////////////\n\nPROSAO SAM\n\n////////////////////////')
		_process(response.json()['checkout']['token'])
		return json.dumps({'rates':rates})


def _process(token):
	response = requests.put(url + token, headers=headers, data = json.dumps({'checkout':{'shipping_line':{"handle": "Advanced%20Shipping%20Rules-free-shipping-0.00"}}}))
	print(json.dumps(response.json(),indent=4))
	payment_info = {
		'checkout_charge':{
			'payment_processor':'stripe',
			'payment_token':'cus_EH5MRaoRdCwS8c',
		}
	}
	response = requests.post(url + token + '/charge', headers=headers, data=json.dumps(payment_info))
	print(response.json())
	if response.status_code == 200:
		return render_template('thanks.html')
	else:
		return render_template('checkout.html')


def _get_shipping_rates(token):
	response = requests.get(url + token + '/shipping_rates', headers=headers)
	rates = response.json()['shipping_rates']
	#print(json.dumps(response.json(),indent=4))
	if response.status_code == 200:
			return rates

	else:
		return make_response(jsonify({'error':'rip bro'},400))
