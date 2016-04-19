#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Blockstack
    ~~~~~
    copyright: (c) 2014-2015 by Halfmoon Labs, Inc.
    copyright: (c) 2016 by Blockstack.org

    This file is part of Blockstack

    Blockstack is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Blockstack is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with Blockstack. If not, see <http://www.gnu.org/licenses/>.
""" 

import testlib
import pybitcoin
import json

wallets = [
    testlib.Wallet( "5JesPiN68qt44Hc2nT8qmyZ1JDwHebfoh9KQ52Lazb1m1LaKNj9", 100000000000 ),
    testlib.Wallet( "5KHqsiU9qa77frZb6hQy9ocV7Sus9RWJcQGYYBJJBb2Efj1o77e", 100000000000 ),
    testlib.Wallet( "5Kg5kJbQHvk1B64rJniEmgbD83FpZpbw2RjdAZEzTefs9ihN3Bz", 100000000000 ),
    testlib.Wallet( "5JuVsoS9NauksSkqEjbUZxWwgGDQbMwPsEfoRBSpLpgDX1RtLX7", 100000000000 ),
    testlib.Wallet( "5KEpiSRr1BrT8vRD7LKGCEmudokTh1iMHbiThMQpLdwBwhDJB1T", 100000000000 )
]

consensus = "17ac43c1d8549c3181b200f1bf97eb7d"

def scenario( wallets, **kw ):

    testlib.blockstack_namespace_preorder( "test", wallets[1].addr, wallets[0].privkey )
    testlib.next_block( **kw )

    testlib.blockstack_namespace_reveal( "test", wallets[1].addr, 52595, 250, 4, [6,5,4,3,2,1,0,0,0,0,0,0,0,0,0,0], 10, 10, wallets[0].privkey )
    testlib.next_block( **kw )

    testlib.blockstack_namespace_ready( "test", wallets[1].privkey )
    testlib.next_block( **kw )

    resp = testlib.blockstack_name_preorder( "foo.test", wallets[2].privkey, wallets[3].addr )
    if 'error' in resp:
        print json.dumps(resp)

    testlib.next_block( **kw )

    # no name operations should work on this name, except register
    resp = testlib.blockstack_name_update( "foo.test", "11" * 20, wallets[3].privkey )
    if 'error' in resp:
        print json.dumps(resp)

    testlib.next_block( **kw )

    resp = testlib.blockstack_name_renew( "foo.test", wallets[3].privkey )
    if 'error' in resp:
        print json.dumps(resp)

    testlib.next_block( **kw )

    resp = testlib.blockstack_name_transfer( "foo.test", wallets[4].addr, True, wallets[3].privkey )
    if 'error' in resp:
        print json.dumps(resp)

    testlib.next_block( **kw )

    # try both addresses (should both fail)
    resp = testlib.blockstack_name_revoke( "foo.test", wallets[4].privkey )
    if 'error' in resp:
        print json.dumps(resp)

    testlib.next_block( **kw )

    resp = testlib.blockstack_name_revoke( "foo.test", wallets[3].privkey )
    if 'error' in resp:
        print json.dumps(resp)
    

def check( state_engine ):

    # not revealed, but ready 
    ns = state_engine.get_namespace_reveal( "test" )
    if ns is not None:
        return False 

    ns = state_engine.get_namespace( "test" )
    if ns is None:
        return False 

    if ns['namespace_id'] != 'test':
        return False 

    # preordered
    preorder = state_engine.get_name_preorder( "foo.test", pybitcoin.make_pay_to_address_script(wallets[2].addr), wallets[3].addr )
    if preorder is None:
        return False
    
    # NOT registered 
    name_rec = state_engine.get_name( "foo.test" )
    if name_rec is not None:
        return False 

    return True
