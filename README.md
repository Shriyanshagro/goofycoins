# Goofycoins
GoofyCoin is a simple cryptocurrency . There are just two rules of GoofyCoin. The first rule is that a
designated entity, Goofy, can create new coins whenever he wants and these newly created coins belong to
him.

To create a coin, Goofy generates a unique coin ID uniqueCoinID that he’s never generated before and
constructs the string “CreateCoin [ uniqueCoinID ]”. He then computes the digital signature of this string
with his secret signing key. The string, together with Goofy’s signature, is a coin. Anyone can verify that the
coin contains Goofy’s valid signature of a CreateCoin statement, and is therefore a valid coin.
Let’s say Goofy wants to transfer a coin that he created to Amit. To do this he creates a new statement that
says “Pay this to Amit” where “this” is a hash pointer that references the coin in question. And as we saw
earlier, identities are really just public keys, so “Amit” refers to Amit’s public key. Finally, Goofy signs the
string representing the statement. Since Goofy is the one who originally owned that coin, he has to sign any
transaction that spends the coin. Once this data structure representing Goofy’s transaction signed by him
exists, Amit owns the coin. She can prove to anyone that she owns the coin, because she can present the
data structure with Goofy’s valid signature. Furthermore, it points to a valid coin that was owned by Goofy.
So the validity and ownership of coins are self‐evident in the system.
Once Amit owns the coin, she can spend it in turn. To do this she creates a statement that says, “Pay this
coin to Mohit’s public key” where “this” is a hash pointer to the coin that was owned by her. And of course,
Amit signs this statement. Anyone, when presented with this coin, can verify that Mohit is the owner. They
would follow the chain of hash pointers back to the coin’s creation and verify that at each step, the rightful
owner signed a statement that says “pay this coin to [new owner]”.

To summarize, the rules of GoofyCoin are:
* Goofy can create new coins by simply signing a statement that he’s making a
new coin with a unique coin ID.
* Whoever owns a coin can pass it on to someone else by signing a statement
that saying, “Pass on this coin to X” (where X is specified as a public key)
* Anyone can verify the validity of a coin by following the chain of hash
pointers back to its creation by Goofy, verifying all of the signatures along
the way.

## Usage

The program is self-explanatory. It ask users for required actions they want to
perform along with other required inputs.

Also with the initializing of program, 100 coins will be generated by Goofy
among which 50 would then be passed equally to other 5 dummy users by Goofy.

## Rules & Regulations

* Unique public and private key for each user
* Verification and validation of publickeys, privatekeys and transactions
* Validation of coin creation
* A public ledger which maintain all transactions with timestamps
* Individual holding of each user is also recorded
* Creation and passing of each coin is also recorded with public keys for
future validaiton.

## Implementation

* Python language
* Using concepts of OOPS, two classes namely User and Coins are created which
are highly de-coupled
  - User class maintain public-private key map and coin holding of each
  Individual user
  - Class Coin class maintains public transactionledger and blockhain of
  goofycoins
  - Class Coin is responsible for validation and verification of each
  transaction.
* Errors are catched to keep robustness in program
