import requests
from database import Database
import time

class ApiConnector:
    def __init__(self):

        self.polyscan_base_url = "https://api.polygonscan.com/api"
        self.coingecko_base_url = "https://api.coingecko.com/api/v3/simple/price"
        self.vs_currency = "usd"
        self.api_key = '9PCFZT1EZ99FXR3BNYQCSRWB7B5FD14PJT'
        self.address = '0x1Fa6a88CFe89A37f44548f386eCCBE0fe23dB268'
        self.polyscan_params = {'module': 'account', 'action': 'tokenbalance', 'contractaddress': '', 'address': self.address, 'tag': 'latest', 'apikey': self.api_key}
        self.coingecko_params = {'ids': '', 'vs_currencies': self.vs_currency}
        self.contracts = [
            {
                'contract_name': 'WMATIC',
                'contract_address': '0x0d500b1d8e8ef31e21c99d1db9a6444d3adf1270',
                'contract_id': 'matic-network'
            },
            {
                'contract_name': 'WETH',
                'contract_address': '0x7ceb23fd6bc0add59e62ac25578270cff1b9f619',
                'contract_id': 'ethereum'
            },
            {
                'contract_name': 'QUICK',
                'contract_address': '0x831753dd7087cac61ab5644b308642cc1c33dc13',
                'contract_id': 'quick'
            },
            {
                'contract_name': 'RVF',
                'contract_address': '0x2ce13e4199443fdfff531abb30c9b6594446bbc7',
                'contract_id': 'rocket-vault-rocketx'
            },
            {
                'contract_name': 'miMATIC',
                'contract_address': '0xa3fa99a148fa48d14ed51d610c367c61876997f1',
                'contract_id': 'mimatic'
            },
            {
                'contract_name': 'Kommunitas',
                'contract_address': '0xc004e2318722ea2b15499d6375905d75ee5390b8',
                'contract_id': 'kommunitas'
            },
            {
                'contract_name': 'USD Coin',
                'contract_address': '0x2791bca1f2de4661ed88a30c99a7a9449aa84174',
                'contract_id': 'usd-coin'
            },
            {
                'contract_name': 'UniLend Finance',
                'contract_address': '0x5b4cf2c120a9702225814e18543ee658c5f8631e',
                'contract_id': 'unlend-finance'
            },
            {
                'contract_name': 'Tether USD',
                'contract_address': '0xc2132d05d31c914a87c6611c10748aeb04b58e8f',
                'contract_id': 'tether'
            },
            {
                'contract_name': 'Unreal Governance Token',
                'contract_address': '0xba4c54ea2d66b904c82847a7d2357d22b857e812',
                'contract_id': 'unreal-finance'
            },
        ]

    def make_request(self, base_url, param):
        #print(param)
        data = requests.get(base_url, params=param)
        return data

    def get_balances(self):
        db = Database()
        db_balances = db.getBalances()

        # if db_balances is not None:
        #     for i in range(5):
        #         print(str(db_balances[i]['token'])+' '+str(db_balances[i]['balance'])+' '+str(db_balances[i]['insertedOn']))



        ts = time.time()
        balances = []
        db_bal = []

        length = len(self.contracts)
        print(length)
        for i in range(length):
            self.polyscan_params['contractaddress'] = self.contracts[i]['contract_address']
            data = self.make_request(self.polyscan_base_url, self.polyscan_params)

            self.coingecko_params['ids'] = self.contracts[i]['contract_id']
            coin_price = self.make_request(self.coingecko_base_url, self.coingecko_params)
            coin_price = coin_price.json()
            coin_price = float(coin_price[self.coingecko_params['ids']][self.vs_currency])
            j_data = data.json()
            bal = j_data['result']
            bal = float(bal)/(10**18)
            #bal_diff = 0
            bal_diff = bal - float(db_balances[i]['balance'])
            print(bal_diff)
            #print(db_balances[i]['balance'])
            vol = (bal*coin_price*2*100000)/15
            vol_change = (bal_diff*coin_price*2*100000)/15
            balances.append({'contract': self.contracts[i]['contract_name'], 'balance': bal, 'balance_diff': bal_diff , 'vol_change':vol_change, 'volume': vol})
            db_bal.append((self.contracts[i]['contract_name'], bal, ts))
        #print(balances)
        #print(db_bal)
        #print(ts)
        #print(float(db_balances[0]['insertedOn']))

        if int(ts*1000 - float(1641886200000))%86400 == 0:
            db.addBalanceHistory(db_bal)

        return balances

