#implementation of goofycoins

from datetime import datetime

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
        pass

    # return list of all public keys
    def getPublicKey(self):
        pass

    # return publickey of provided privatekey
    def getPublicKey(self, privatekey):
        pass

class Coin(object):

    def __init__(self):
        self.coin = {}
        self.publickey = User.getPublicKey()
        self.ledger = []

    # returns new id for coin creation
    def getnewid(self):
        return (len(self.coin) + 1)

    # cid = unique id of coin
    # pid =  private key of creator
    def createCoin(self, cid, pid):

        # creation is only allowed for goofy
        if pid=="goofy" and cid==self.getnewid():
            self.coin[cid] = []
            # first transaction of cid ; transaction ledger is a list
            self.coin[cid][0] = pid

            transaction = {"creator": User.getPublicKey(pid),
                    "Coinid": cid,
                    "Timestamp": datetime.now().isoformat(),
            }

            # update ledger
            self.ledger.append = transaction

            print "Successfull coin creation"

        else:
            raise GoofycoinError("Sorry only Goofy is allowed to create\
             new coins with unique id.")

    # rid = reciever's public key
    # pid = sender's private key
    def passcoin(self, cid, rid, pid):

        # validate coin's existence
        if cid not in self.coin.keys():
            raise GoofycoinError("No such coin exist. Ask Gooofy to create \
            one ¯\_(ツ)_/¯")

        if rid not in self.publickey:
            raise GoofycoinError("Cross-Check reciever's public key")

        # validate whether user owns that coin?
        if not self.getOwner(cid) == User.getPublicKey(pid):
            raise GoofycoinError("Sorry, you doesn't owe coin {0}".format(cid))

        # append coin's blockchain
        self.coin[cid].append = rid

        transaction = {"sender": User.getPublicKey(pid),
                "reciever": rid,
                "Coinid": cid,
                "Timestamp": datetime.now().isoformat(),
        }

        # update ledger
        self.ledger.append = transaction
        print "Transaction Successfull"

    def getOwner(self, cid):

        if cid not in self.coin.keys():
            raise GoofycoinError("No such coin exist. Ask Gooofy to create \
            one ¯\_(ツ)_/¯")

        return self.coin[cid][-1]

    def getledger(self);
        return self.ledger
