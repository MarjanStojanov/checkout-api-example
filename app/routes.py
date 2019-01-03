from app import application as App
from flask import render_template, request

import requests, json


@App.route('/products', methods=['GET'])
def products():
	return render_template('products.html')

@App.route('/process', methods=['POST'])
def process():
	headers = {
		'X-Recharge-Access-Token':'abc123',
		'Content-Type':'application/json',
		'Accept':'application/json',
	}

	url = 'https://api.rechargeapps.com/checkouts'
	shipping_address = {
		'first_name':request.form.get('first_name'),
		'last_name':request.form.get('last_name'),
		'zip':request.form.get('zip'),
		'country':request.form.get('country'),
		'province':request.form.get('province'),
		'phone':request.form.get('phone'),
		'company':request.form.get('company'),
		'address1':request.form.get('address1'),
		'address2':request.form.get('address2'),
		'city':request.form.get('city'),
		'state':'Afghanistan'
	}
	data = {}
	data['checkout'] = {}
	data['checkout']['shipping_address'] = shipping_address
	data['checkout']['email'] = request.form['email']
	data['checkout']['line_items'] = [{
		'variant_id':3844924611,
		'quantity':5,
		'price':15,
	}]
	response = requests.post(url, headers=headers, data=json.dumps(data))

	print(response.json())
	payment_info = {
		'charge':{
			'payment_processor':'stripe',
			'customer_token':'cus_EGpI2fyeG8H2DA'
		}
	}
	response = requests.post(url + response.json()['checkout']['token'] + '/charge', headers=headers, data=json.dumps(payment_info))
	return render_template('thanks.html')
@App.route('/checkout', methods=['GET'])
def checkout():
	return render_template('checkout.html')


