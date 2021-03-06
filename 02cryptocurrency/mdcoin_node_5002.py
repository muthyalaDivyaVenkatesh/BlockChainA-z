# moduel create a block chain
# flask
#print("Hello world")
#import the libaries
import datetime
import hashlib
import json
from  flask import Flask, jsonify,request
import requests
from uuid import uuid4
from urllib.parse import urlparse
#part1 Building a Block chain
#always self will be intilized in the function call

class Blockchain:

    def __init__(self):
        self.chain = []
        self.transcations = []
        self.create_block(proof = 1, previous_hash = '0')
        self.nodes= set()

    def create_block(self, proof, previous_hash):

        block = {'index' :len(self.chain)+1  ,'timestamp': str(datetime.datetime.now()) ,'proof':proof,
                 'previous_hash' : previous_hash,
                 'transcations':self.transcations}
        self.transcations = []
        self.chain.append(block)
        return block
        #create a methid to call previous model block
    def get_previous_block(self):
            return self.chain[-1]
    def proof_of_work(self,previous_proof):
            new_proof = 1
            check_proof = False
            while check_proof is False:
                hash_operation = hashlib.sha256(str(new_proof**2-previous_proof**2).encode()).hexdigest()
                if hash_operation[ :4] == '0000':
                    check_proof = True
                else :
                    new_proof +=1

            return new_proof
    def hash(self,block):
            encoded_block = json.dumps(block,sort_keys = True).encode()
            return hashlib.sha256(encoded_block).hexdigest()
    def is_chain_valid(self,chain):
            previous_block = chain[0]
            block_index = 1
            while block_index < len(chain):
                block = chain[block_index]
                if block['previous_hash'] != self.hash(previous_block):
                    return False
                previous_proof = previous_block['proof']
                proof = block['proof']
                hash_operation  = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
                if hash_operation[:4] != '0000':
                    return False
                previous_block = block
                block_index +=1
            return True
        
    def add_transaction(self,sender,receiver,amount):
            self.transcations.append({'sender':sender,
                                     'receiver':receiver,
                                     'amount':amount})
            previous_block = self.get_previous_block()
            return previous_block['index']+1
        
    def add_node(self,address):
            parsed_url = urlparse(address)
            self.nodes.add(parsed_url.netloc)
            
    def replace_chain(self):
            network = self.nodes
            longest_chain = None
            max_length = len(self.chain)
            for node  in network:
                response = requests.get(f'http://{node}/get_chain')
                if response.status_code == 200:
                    length = response.json()['length']
                    chain = response.json()['chain']
                    if length > max_length and self.is_chain_valid(chain):
                        max_length = length
                        longest_chain = chain
            if longest_chain:
                self.chain  = longest_chain
                return True
            return False
                        
        




#proof of work is hard to find but easy to verify

#part2 -Minning our block
# creating web App
app = Flask(__name__)

#creating a node in port 5000
node_address = str(uuid4()).replace('-','')
            
#creating block chain            

blockchain = Blockchain()

#mining a new block

@app.route('/mine_block',methods = ['Get'])

def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash =  blockchain.hash(previous_block)
    blockchain.add_transaction(sender = node_address,receiver = 'venkatesh',amount = 1)
    block = blockchain.create_block(proof,previous_hash)
    response = {'message': 'congratulations yo just mined the block',
                'index':block['previous_hash'],
                'timestamp':block['timestamp'],
                'proof' :block['proof'],
                'previous_hash': block['previous_hash'],
                'transcations': block['transcations']}
    return jsonify(response), 200

# Getting the full blockchaina
@app.route('/get_chain',methods = ['Get'])
def get_chain():
     response = {'chain' : blockchain.chain,
                 'length' : len(blockchain.chain) }
     return jsonify(response), 200
#Running the app



@app.route ('/is_valid',methods = ['Get'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message': "All good"}
    else:
        response = {'message':'Block chain is not valid'}
    return jsonify(response), 200

#adding a new transcation to the blockchain
@app.route('/add_transaction',methods = ['post'])

def add_transaction():
    json = request.get_json()
    transaction_keys = ['sender','receiver','amount']
    if not all(key in json for key in transaction_keys):
        return 'some elements of the  transcation are missing',400
    index = blockchain.add_transaction(json['sender'],json['receiver'],json['amount'])
    response = {'message':f'This transcation will be added to block{index}'}
    return jsonify(response),201

    
#connecting new nodes
@app.route('/connect_node', methods = ['post'])
def connect_node():
    json = request.get_json()
    nodes = json.get('nodes')
    if nodes is  None:
        return "No node",400
    for node in nodes:
        blockchain.add_node(node)
    response ={'message':'All the nodes are now connected .the md coin cointains the following nodes:',
               'total_nodes ':list(blockchain.nodes)}
    return jsonify(response),201
#replacing the chain bby the longest chain if needed
@app.route ('/replace_chain',methods = ['Get'])
def replace_chain():
    is_chain_replaced = blockchain.replace_chain()
    
    if is_chain_replaced:
        response = {'message': 'The nodes had diffrent chains so the chain was replaces',
                    'new_chain':blockchain.chain}
    else:
        response = {'message':'The chain is the largest',
                    'actual_chain':blockchain.chain}
    return jsonify(response), 200
#running up the host
app.run(host = '0.0.0.0', port = 5002)

#part-3 decentralizing our blockchain
