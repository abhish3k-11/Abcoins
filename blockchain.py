# Creating a blockchain

# Importing the libbraries
import datetime
import hashlib
import json
from flask import Flask, jsonify

# Part 1 :- Building a blockchain 

class Blockchain:
    
    def __init__(self):
        self.chain = []
        self.create_block(proof = 1, prev_hash = '0')
    
    #this func will be used right after mining a block 
    #mine_block func is different from create_block func
    #in the aspect that it mines the block fr PoW and then a block is created after it
    def create_block(self, proof, prev_hash):
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'prev_hash': prev_hash}
        
        self.chain.append(block)
        return block
    
    def get_prev_block(self):
        return self.chain[-1] 
        # -1 gets the last block of chain
    
    def proof_of_work(self, prev_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - prev_proof**2).encode()).hexdigest()
            # u can make more complex and asymmetric algos
            # more th no. of leading zeroes harder it will be to mine
            if hash_operation[:8] == '00000000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
    # now we will check whether the chain is valid or not.
    
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self, chain):
        prev_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['prev_hash'] != self.hash(prev_block):
                return False
                #self.hash is used to make sure that we use our own variable not the others.
            prev_proof = prev_block['proof']
            curr_proof = block['proof']
            hash_operation = hashlib.sha256(str(curr_proof**2 - prev_proof**2).encode()).hexdigest()
            if hash_operation[:8] != '00000000':
                return False
            prev_block = block
            block_index += 1
        return True
    

# Part 2 :- Mining blockchain. It has two parts.

# Creating a web app, check Flask documentation
app = Flask(__name__)

# Creating a bloockchain
blockchain = Blockchain()

# Mining a new block

@app.route('/mine_block', methods = ['GET'])
def mine_block():
    prev_block = blockchain.get_prev_block()
    prev_proof = prev_block['proof']
    proof = blockchain.proof_of_work(prev_proof)
    prev_hash = blockchain.hash(prev_block)
    # we call hash func cuz we need hash of prev block and the hash contained in prev_block is of it's 
    # previous block
    block = blockchain.create_block(proof, prev_hash)
    # now the block is mined and appended we display a response
    response = {'message': 'Congratulations, you just mined a block!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'prev_hash': block['prev_hash']}
    return jsonify(response), 200
    # Here 200 is a HTTP status code it means "Successful"
    
# Displaying full blockchain in POSTMAN
@app.route('/get_chain', methods = ['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
               'length': len(blockchain.chain)}
    return jsonify(response), 200

# Running the app

app.run(host = '0.0.0.0', port = 5000)
    
    







