import tornado.ioloop
from tornado.web import RequestHandler, Application
from tornado.httpserver import HTTPServer
import tornado.httputil
import tornado.process
import tornado.web
from tornado import gen
import tornado.iostream
from random import randint
from hashlib import md5
import sys


def is_prime(n):
    if n <= 1:
        return False
    elif n <= 3:
        return True
    elif n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i*i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def prime_number_generator():
    yield 2
    prime_number = 3

    while True:
        yield prime_number
        while True:
            prime_number += 2
            if is_prime(prime_number):
                break
            continue


class PrimeNumberHandler(RequestHandler):
    SUPPORTED_METHODS = ("GET",)

    @gen.coroutine
    def get(self, number):
        if not self.get_cookie('cookie'):
            m = md5()
            random_number = randint(10**4, 10**8)
            m.update(str(random_number).encode())
            self.set_cookie('cookie', m.hexdigest())

        prime_number = yield self.get_prime_number(int(number))

        response = {
            'service_name': 'prime_number',
            'index': number,
            'prime_number': prime_number,
        }

        self.write(response)

    @gen.coroutine
    def get_prime_number(self, n):
        '''
        :param n: prime number index
        :return: prime number
        index:  1 2 3 4  5 ...
        number: 2 3 5 7 11 ...
        '''
        if n < 1:
            return {'Error': 'Number must be >= 1'}
        count = 0
        prime_number_gen = prime_number_generator()
        prime_number = 0
        while count < n:
            prime_number = next(prime_number_gen)
            count += 1
        print([prime_number])
        return prime_number


class FactorizationHandler(RequestHandler):
    SUPPORTED_METHODS = ("GET",)

    @gen.coroutine
    def get(self, number):
        if not self.get_cookie('cookie'):
            m = md5()
            random_number = randint(10**4, 10**8)
            m.update(str(random_number).encode())
            self.set_cookie('cookie', m.hexdigest())

        factorization_dict = yield self.factorization(int(number))
        response = {
            'service_name': 'factorization',
            'number': number,
            'factorized_number': factorization_dict,
        }
        self.write(response)

    @gen.coroutine
    def factorization(self, n):
        '''
        :param n: int number >= 2
        :return: dict where key - prime number
                            value - prime number power
        '''
        if n < 2:
            return {'Error', 'Number bust be >= 2'}
        prime_numbers_dict = {}
        mult_list = []
        prime_number_gen = prime_number_generator()
        while n > 1:
            prime_number = next(prime_number_gen)
            while n % prime_number == 0:
                n /= prime_number
                mult_list.append(prime_number)

        for item in set(mult_list):
            prime_numbers_dict[item] = mult_list.count(item)

        return prime_numbers_dict


class PingHandler(RequestHandler):
    SUPPORTED_METHODS = ("GET",)

    @gen.coroutine
    def get(self):
        if not self.get_cookie('cookie'):
            m = md5()
            random_number = randint(10**4, 10**8)
            m.update(str(random_number).encode())
            self.set_cookie('cookie', m.hexdigest())

        response = yield self.ping()
        print('Ping %s' % response)
        self.write('Ping %s' % response)

    @gen.coroutine
    def ping(self):
        return "doesn't work! But the service is alive!"

if __name__ == '__main__':
    port = 8899
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        port = int(sys.argv[1])

    application = Application([
        (r'/primenumber/([0-9]+)', PrimeNumberHandler),
        (r'/factorization/([0-9]+)', FactorizationHandler),
        (r'/ping', PingHandler),
    ])
    httpServer = HTTPServer(application)
    httpServer.bind(port)
    httpServer.start(0)
    tornado.ioloop.IOLoop.current().start()
