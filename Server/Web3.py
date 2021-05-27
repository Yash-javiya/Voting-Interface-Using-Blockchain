from db import get_voter_key, get_candidate_key, set_voter_key, set_candidate_key, voted

from web3 import Web3
import json

INFURA_PROVIDER = "https://rinkeby.infura.io/v3/API_KEY"
HOST_PRIVATE_KEY = "<Private_key of contract creater>"
CONTRACT_ADDRESS = "<contract Address>"

w3 = Web3(Web3.HTTPProvider(INFURA_PROVIDER))

with open('build/election.json') as file:
    contract_interface = json.load(file)

contract = w3.eth.contract(address=CONTRACT_ADDRESS,
                           abi=contract_interface['abi'])


def create_account():
    """
    Creates an account and return it.
    """
    account = w3.eth.account.create()
    return account


def get_account(private_key):
    """
    Returns account.
    """
    account = w3.eth.account.privateKeyToAccount(private_key)
    return account


class Function:
    def __init__(self, *args, **kwargs):
        """
        Instantiates Function class.
        """
        self.w3 = w3
        self.contract = contract

    def manager(self):
        return contract.functions.manager().call()

    def state(self):
        return contract.functions.state().call()

    def total_voter(self):
        return contract.functions.totalVoter().call()

    def total_candidate(self):
        return contract.functions.totalCandidate().call()

    def vote_dropped(self):
        return contract.functions.voteDropped().call()

    def candidate(self, address):
        return contract.functions.candidates(address).call()

    def voter(self, address):
        return contract.functions.voters(address).call()


class Manager:
    """
    Performs manager operations.
    """

    def __init__(self, *args, **kwargs):
        """
        Instantiates Manager class.
        """
        self.w3 = w3
        self.contract = contract
        self.private_key = HOST_PRIVATE_KEY
        self.account = w3.eth.account.privateKeyToAccount(self.private_key)

    def add_candidate(self, address):
        """
        Adds the candidate with address.

        Parameters
        ----------
            address: candidate address

        Returns
        -------
            receipt: dictionary transaction receipt
        """
        construct_txn = self.contract.functions\
            .addCandidate(address).buildTransaction({
                'from': self.account.address,
                'nonce':
                self.w3.eth.getTransactionCount(self.account.address),
                'gas': 1000000,
                'gasPrice': self.w3.eth.gasPrice
            })

        signed = self.account.signTransaction(construct_txn)
        tx_hash = self.w3.eth.sendRawTransaction(signed.rawTransaction)
        receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)

        return dict(receipt)

    def add_voter(self, address):
        """
        Adds the voter with address.

        Parameters
        ----------
            address: voter address

        Returns
        -------
            receipt: dictionary transaction receipt
        """
        construct_txn = self.contract.functions\
            .addVoter(address).buildTransaction({
                'from': self.account.address,
                'nonce':
                self.w3.eth.getTransactionCount(self.account.address),
                'gas': 1000000,
                'gasPrice': self.w3.eth.gasPrice
            })

        signed = self.account.signTransaction(construct_txn)
        tx_hash = self.w3.eth.sendRawTransaction(signed.rawTransaction)
        receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)

        return dict(receipt)

    def remove_voter(self, address):
        """
        Removes voter.

        Parameters
        ----------
            address: address to remove

        Returns
        -------
            receipt: dictionary transaction receipt
        """
        construct_txn = self.contract.functions\
            .removeVoter(address).buildTransaction({
                'from': self.account.address,
                'nonce':
                self.w3.eth.getTransactionCount(self.account.address),
                'gas': 1000000,
                'gasPrice': self.w3.eth.gasPrice
            })

        signed = self.account.signTransaction(construct_txn)
        tx_hash = self.w3.eth.sendRawTransaction(signed.rawTransaction)
        receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)

        return dict(receipt)

    def start_vote(self):
        """
        Starts a voting phase.

        Returns
        -------
            receipt: dictionary transaction receipt
        """
        construct_txn = self.contract.functions\
            .startVote().buildTransaction({
                'from': self.account.address,
                'nonce':
                self.w3.eth.getTransactionCount(self.account.address),
                'gas': 1000000,
                'gasPrice': self.w3.eth.gasPrice
            })

        signed = self.account.signTransaction(construct_txn)
        tx_hash = self.w3.eth.sendRawTransaction(signed.rawTransaction)
        receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)

        return dict(receipt)

    def end_vote(self):
        """
        Ends a voting phase.

        Returns
        -------
            receipt: dictionary transaction receipt
        """
        construct_txn = self.contract.functions\
            .endVote().buildTransaction({
                'from': self.account.address,
                'nonce':
                self.w3.eth.getTransactionCount(self.account.address),
                'gas': 1000000,
                'gasPrice': self.w3.eth.gasPrice
            })

        signed = self.account.signTransaction(construct_txn)
        tx_hash = self.w3.eth.sendRawTransaction(signed.rawTransaction)
        receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)

        return dict(receipt)

    def do_vote(self, address):
        """
        Votes the candidate.

        Parameters
        ----------
            address: candidate address

        Returns
        -------
            receipt: dictionary transaction receipt
        """
        account = get_account(self.private_key)
        construct_txn = contract.functions\
            .doVote(address).buildTransaction({
                'from': account.address,
                'nonce':
                w3.eth.getTransactionCount(account.address),
                'gas': 1000000,
                'gasPrice': w3.eth.gasPrice
            })

        signed = account.signTransaction(construct_txn)
        tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
        receipt = w3.eth.waitForTransactionReceipt(tx_hash)

        tx_hash = receipt['transactionHash'].hex()
        url = 'https://rinkeby.etherscan.io/tx/{}'.format(tx_hash)

        if receipt['status']:
            voted(account.address)
            message = {'message': ' You successfully Voted. for further information navigate to: ',
                       'url': url,
                       "type": 'success',
                       "display": 'Thank you!!'}
            return message
        else:
            message = {'message': ' Oops! your transaction is failed! for further information navigate to: ',
                       'url': url,
                       "type": 'warning',
                       "display": 'Oops!!'}
            return message

    def get_result(self):
        """
            Votes the candidate.
            Returns
            -------
            Address: winner address
            """
        account = get_account(self.private_key)
        construct_txn = contract.functions.result().buildTransaction({
            'from': account.address,
            'nonce': w3.eth.getTransactionCount(account.address),
            'gas': 1000000,
            'gasPrice': w3.eth.gasPrice
        })

        signed = account.signTransaction(construct_txn)
        tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
        receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        logs = contract.events.electionResult().processReceipt(receipt)
        winner = (dict(logs[0]['args']))

        tx_hash = receipt['transactionHash'].hex()
        url = 'https://rinkeby.etherscan.io/tx/{}'.format(tx_hash)
        if receipt['status'] == 1:
            return winner
        else:
            return None


class Action:

    def __init__(self, *args, **kwargs):
        """
        Instantiates Function class.
        """
        self.w3 = w3
        self.contract = contract

    def voter_generate_id(self, username):
        if get_voter_key(username) != '':
            messages = {'message': 'Public key for ' + username + ' is already exists.',
                        "type": 'warning'}
            return messages

        try:
            account = create_account()
            set_voter_key(username, account.address, account.privateKey.hex())
            message = {'message': 'Public key for ' + username + ' is ' + account.address,
                       "type": 'success'}
            return message
        except:
            message = {'message': "Oops, Error has encountered!",
                       "type": 'warning'}
            return message

    def voter_add_to_eth_net(self, username):
        manager = Manager()
        receipt = manager.add_voter(get_voter_key(username))
        tx_hash = receipt['transactionHash'].hex()
        url = 'https://rinkeby.etherscan.io/tx/{}'.format(tx_hash)

        if receipt['status']:
            message = {'message': ' You successfully added ' + username + ' to eth-net. for further information navigate to: ',
                       'url': url,
                       "type": 'success'}
            return message
        else:
            message = {'message': ' Oops! your transaction is failed! for further information navigate to: ',
                       'url': url,
                       "type": 'warning'}
            return message

    def candidate_generate_id(self, username):
        if get_candidate_key(username) != '':
            messages = {'message': 'Public key for ' + username + ' is already exists.',
                        "type": 'warning'}
            return messages

        try:
            account = create_account()
            set_candidate_key(username, account.address,
                              account.privateKey.hex())
            message = {'message': 'Public key for ' + username + ' is ' + account.address,
                       "type": 'success'}
            return message
        except:
            message = {'message': "Oops, Error has encountered!",
                       "type": 'warning'}
            return message

    def candidate_add_to_eth_net(self, username):
        manager = Manager()
        receipt = manager.add_candidate(get_candidate_key(username))
        tx_hash = receipt['transactionHash'].hex()
        url = 'https://rinkeby.etherscan.io/tx/{}'.format(tx_hash)
        if receipt['status']:
            message = {'message': ' You successfully added ' + username + ' to eth-net. for further information navigate to: ',
                       'url': url,
                       "type": 'success'}
            return message
        else:
            message = {'message': ' Oops! your transaction is failed! for further information navigate to: ',
                       'url': url,
                       "type": 'warning'}
            return message
