Prime number server
===================

Installation
------------

git clone https://github.com/dmitryagapov/primenumberserver

cd primenumber

Run server
-----------

./primenumberserver.py [port_number]

standard port 8899

Using
---------
#primenumber

Write in browser:
    http://localhost:8899/primenumber/10 if you use standard port

    you should get:

    {"service_name": "prime_number", "prime_number": 29, "index": "10"}

In terminal:
    curl localhost:8899/primenumber/100 if you use standard port

    you should get:

    {"service_name": "prime_number", "prime_number": 541, "index": "100"}

#factorization
Write in browser:

    http://localhost:8899/factorization/90 if you use standard port

    you should get:

    {"service_name": "factorization", "number": "90", "factorized_number": {"2": 1, "3": 2, "5": 1}}

    factorized_number store dict where key   - prime number,
                                       value - prime number power

    90 = 2^1 * 3^2 * 5^1

In terminal:

    curl localhost:8899/factorization/900 if you use standard port

    you should get:

    {"service_name": "factorization", "number": "900", "factorized_number": {"2": 2, "3": 2, "5": 2}}

    900 = 2^2 * 3^2 * 5^2

#Using in python script

'''python

import requests

r = requests.get('http://localhost:8899/primenumber/111111')
primenumber_dict = r.json()
print(primenumber_dict)

#{'prime_number': 607, 'index': 111, 'service_name': 'prime_number'}

for key in primenumber_dict:
    print(key, primenumber_dict[key])

#prime_number 607
# index 111
# service_name prime_number

r = requests.get('http://localhost:8899/factorization/123456789')

factorization_dict = r.json()

print(factorization_dict)
#{'factorized_number': {'3': 2, '3803': 1, '3607': 1}, 'service_name': 'factorization', 'number': 123456789}
for key in factorization_dict:
    print(key, factorization_dict[key])

# factorized_number {'3': 2, '3803': 1, '3607': 1}
# service_name factorization
# number 123456789

'''
