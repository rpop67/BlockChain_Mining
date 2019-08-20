import datetime
import hashlib
#to import thr dumps function from json library
import json
#for web app and to intteract with blockchain:
from flask import Flask,jsonify

#Part 1 -Building a Blockchain
#define genisis block
#proof_of_work and validation blockchain

class Blockchain:
        def __init__(self):
            self.chain=[]
            #creating genesis block
            self.create_block(proof=1,previous_hash='0')

        def create_block(self,proof,previous_hash):
            block={'index':len(self.chain)+1,
                   'timestamp':str(datetime.datetime.now()),
                   'proof':proof,
                   'previous_hash':previous_hash}
            self.chain.append(block)
            return block

        def get_previous_block(self):
            #-1 gives the left index of the chain
            return self.chain[-1]

        def proof_of_work(self,previous_proof):
            new_proof=1
            check_proof=False
            while check_proof is False:
                #hash_operation will contain string of 64 char
                hash_operation=hashlib.sha256(str(new_proof**2-previous_proof**2).encode()).hexdigest()
                if hash_operation[:4] == '0000':
                    check_proof=True
                else:
                    new_proof+=1
            return new_proof

        #now we will validate the blockchain using 2 checks"
        #...each block has 4 leading zeroes
        #...each block's previous hash== hash of previous block
        #...hence first defining hash function

        def hash(self,block):
            encoded_block=json.dumps(block,sort_keys=True).encode()
            return hashlib.sha256(encoded_block).hexdigest()

        def is_chain_valid(self,chain):
            block_index=1
            previous_block=chain[0]
            while block_index<len(chain):
                current_block=chain[block_index]
                #check1
                if current_block['previous_hash']!=self.hash(previous_block) :
                    return False
                #check2-4 leading zeroes
                previous_proof=previous_block['proof']
                current_proof=current_block['proof']
                hash_operations=hashlib.sha256(str(current_proof**2-previous_proof**2).encode()).hexdigest()
                if hash_operations[:4]!='0000':
                    return False
                previous_block=current_block
                block_index+=1
            return True






#Part 2 - Mining out blockchain

#creating a webapp
app = Flask(__name__)

#creating a blockchain
blockchain=Blockchain()

#mining a new block
@app.route('/mine_block',methods = ['GET'])
def mine_block():
    previous_block=blockchain.get_previous_block()
    previous_proof=previous_block['proof']
    proof=blockchain.proof_of_work(previous_proof)
    previous_hash=blockchain.hash(previous_block)
    block=blockchain.create_block(proof , previous_hash)
    #creating a response dictionary
    response={'message': 'Congrats! You just mined a block',
              'index': block['index'],
              'timestamp': block['timestamp'],
              'proof':block['proof'],
              'previous_hash': block['previous_hash']}
    return jsonify(response),200

#Getting full blockchain
@app.route('/get_chain',methods=['GET'])
def get_chain():
    response={'chain': blockchain.chain,
              'length': len(blockchain.chain)}
    return jsonify(response),200
app.run( host='0.0.0.0' , port=5000)





