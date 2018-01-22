#implementation of goofycoins

from datetime import datetime
import hashlib
from random import randint

# privatekey of goofy
global goofykey
global initcoin
global inituser

initcoin = 100
inituser = 5

# A class to catch error and exceptions
class GoofycoinError(Exception):

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)

class User(object):

    # mapping
    # {PrivateKey: PublicKey}

    def __init__(self):
        global goofykey
        self.user = {}
        self.keymap = {}
        key = hashlib.sha256()
        key.update("goofy")
        num = "privatekey" + str(randint(0,999999999))
        key.update(num)
        goofykey = key.hexdigest()
        key = hashlib.sha256()
        key.update(goofykey)
        key.update("publickey")
        goofypublickey = key.hexdigest()
        self.user[goofykey] = {'publickey': goofypublickey, 'holdings':[]}
        self.keymap[goofypublickey] = goofykey
        print "privatekey==",goofykey, "\npublickey==", goofypublickey
        print "Goofy Created!!"

    def createuser(self):

        key = hashlib.sha256()
        key.update(self.user.keys()[-1])
        num = "privatekey" + str(randint(0,999999999))
        key.update(num)
        privatekey = key.hexdigest()
        key = hashlib.sha256()
        key.update(privatekey)
        key.update("publickey")
        publickey = key.hexdigest()
        holdings = []
        self.user[privatekey] = {'publickey': publickey, 'holdings':holdings}
        self.keymap[publickey] = privatekey
        return privatekey, publickey, holdings

    # return list of all public keys
    def getPublicKeys(self):
        publickey = []
        for value in self.user.values():
            publickey.append(value['publickey'])
        return publickey

    # return publickey of provided privatekey
    def getPublicKey(self, privatekey):
        if not self.user.get(privatekey):
            raise GoofycoinError("Invalid privatekey")
        return self.user.get(privatekey)['publickey']

    # return coin holdings of provided privatekey
    def getHolding(self, privatekey):
        if not self.user.get(privatekey):
            raise GoofycoinError("Invalid privatekey")
        return self.user.get(privatekey)['holdings']

    def getPrivateKey(self, publickey):
        if not self.keymap.get(publickey):
            raise GoofycoinError("Invalid publickey")
        return self.keymap.get(publickey)

class Coin(object):

    def __init__(self, User):
        self.coin = {}
        self.user = User
        self.ledger = []

    # returns new id for coin creation
    def getnewid(self):
        return (len(self.coin) + 1)

    # cid = unique id of coin
    # pid =  private key of creator
    def createCoin(self, cid, pid):
        global goofykey

        # creation is only allowed for goofy
        if pid==goofykey and cid==self.getnewid():
            self.coin[cid] = []
            # first transaction of cid ; transaction ledger is a list
            self.coin[cid].append(self.user.getPublicKey(pid))

            transaction = {"creator": self.user.getPublicKey(pid),
                    "Coinid": cid,
                    "Timestamp": datetime.now().isoformat(),
            }

            # update ledger
            self.ledger.append(transaction)

            # update holding of user
            self.user.user[pid]['holdings'].append(cid)
            print "Successfull coin creation with id {}".format(cid)

        else:
            raise GoofycoinError("Sorry only Goofy is allowed to create\
             new coins with unique id.")

    # rid = reciever's public key
    # pid = sender's private key
    def passcoin(self, cid, rid, pid):

        # validate coin's existence
        if cid not in self.coin.keys():
            raise GoofycoinError("No such coin exist. Ask Gooofy to create \
            one")

        if rid not in self.user.getPublicKeys():
            raise GoofycoinError("Cross-Check reciever's public key")

        # validate whether user owns that coin?
        if not self.getOwner(cid) == self.user.getPublicKey(pid):
            raise GoofycoinError("Sorry, you doesn't owe coin {0}".format(cid))

        # append coin's blockchain
        self.coin[cid].append(rid)

        # update holding of user
        self.user.user[pid]['holdings'].remove(cid)

        self.user.user[self.user.getPrivateKey(rid)]['holdings'].append(cid)

        transaction = {"sender": self.user.getPublicKey(pid),
                "reciever": rid,
                "Coinid": cid,
                "Timestamp": datetime.now().isoformat(),
        }

        # update ledger
        self.ledger.append(transaction)
        print "Transaction Successfull"

    def getOwner(self, cid):

        if cid not in self.coin.keys():
            raise GoofycoinError("No such coin exist. Ask Gooofy to create \
            one ")

        return self.coin[cid][-1]

    def getledger(self):
        return self.ledger

    def checkvalidy(self, cid):

        if cid not in self.coin.keys():
            raise GoofycoinError("No such coin exist. Ask Gooofy to create \
            one ")

        chain = ""
        for users in self.coin.get(cid):
            chain = chain + users + "--->>"

        return chain

# dummy transctions
def dummy(user, coin):
    global goofykey
    global initcoin
    global inituser

    initialcoins = initcoin

    # dummy creation of coins
    for i in range(0, initialcoins):
        coin.createCoin(coin.getnewid(), goofykey)
        i += 1

    # number of coins to be divided among users
    coinequality = initialcoins/(inituser*2)

    # dummy users and distribution of coins
    for i in range(0, inituser):
        privatekey, publickey, holdings = user.createuser()
        print "privatekey==",privatekey, "\npublickey==", publickey
        for j in range(0, coinequality):
            coin.passcoin(initialcoins, publickey, goofykey)
            initialcoins -= 1

if __name__ == "__main__":
    user = User()
    coin = Coin(user)
    dummy(user, coin)
    while True:
        print "u: create user \n p:passcoin \n c:createcoin\n l:transaction \
        ledger \n h: get your holding \n v: verify validy of coin"

        cmd = raw_input("Your command?")

        try:
            if cmd == 'u':
                privatekey, publickey, holdings = user.createuser()
                print "privatekey==",privatekey, "\npublickey==", publickey

            elif cmd== 'p':
                cid = int(raw_input("coin id?"))
                rid = raw_input("reciever's public key?")
                pid = raw_input("Your privatekey?")

                coin.passcoin(cid, rid, pid)

            elif cmd=='c':
                pid = raw_input("Your privatekey?")

                coin.createCoin(coin.getnewid(), pid)

            elif cmd=='l':
                print coin.getledger()

            elif cmd=='h':
                pid = raw_input("Your privatekey?")
                print user.getHolding(pid)

            elif cmd=='v':
                cid = int(raw_input("coin id?"))
                print coin.checkvalidy(cid)

            else:
                print "Provide valid command"

            print
        except GoofycoinError as e:
            print e.message
