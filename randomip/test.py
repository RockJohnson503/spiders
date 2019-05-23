# encoding: utf-8

"""
File: test.py
Author: Rock Johnson
"""
from treq import request, content
from twisted.internet import reactor, defer, task

def scheduler_install(customer):
    def scheduler_install_wordpress():
        def one_done():
            print('Callback: Finished installation for', customer)
        print('Scheduling: Installation for', customer)
        return task.deferLater(reactor, 3, one_done)

    def all_done(_):
        print('All Done for', customer)

    d = scheduler_install_wordpress()
    d.addCallback(all_done)
    return d

def get_content(con):
    # print(con.decode())
    print(1)

@defer.inlineCallbacks
def one_done(args):
    print(args.code)
    res = content(args)
    res.addCallback(get_content)
    yield res

@defer.inlineCallbacks
def inline_install(customer):
    print('Scheduling: Installation for', customer)
    res = request('GET', 'https://baidu.com')
    res.addCallback(one_done)
    yield res
    print('Callback: Finished installation for', customer)
    print('All done for', customer)

def twisted_developer_day():
    customers = ['Customer %d' % i for i in range(1, 3)]
    print('Good morning from Twisted developer')
    work = (inline_install(customer) for customer in customers)
    coop = task.Cooperator()
    join = defer.DeferredList([coop.coiterate(work) for i in range(30)])
    join.addCallback(lambda _: reactor.stop())
    print('Bye from Twisted developer')

twisted_developer_day()
reactor.run()