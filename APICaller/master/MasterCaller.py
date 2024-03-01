import sys
sys.path.append('/Users/jfeasby/SynthetixFundingRateArbitrage')

import json

from APICaller.Synthetix.SynthetixCaller import SynthetixCaller
from APICaller.Binance.binanceCaller import BinanceCaller
from APICaller.ByBit.ByBitCaller import ByBitCaller
from APICaller.master.MasterUtils import get_all_target_token_lists, get_target_exchanges

class MasterCaller:
    def __init__(self):
        self.synthetix = SynthetixCaller()
        self.binance = BinanceCaller()
        self.bybit = ByBitCaller()
        self.target_token_list_by_exchange = get_all_target_token_lists()
        self.target_exchanges = get_target_exchanges()
        
    def create_exchange_mapping(self):
        return {
            "Synthetix": (self.synthetix, self.target_token_list_by_exchange[0]),
            "Binance": (self.binance, self.target_token_list_by_exchange[1]),
            "ByBit": (self.bybit, self.target_token_list_by_exchange[2]),
        }

    def get_funding_rates(self) -> list:
        funding_rates = []
        exchange_mapping = self.create_exchange_mapping()

        for exchange_name in self.target_exchanges:
            if exchange_name in exchange_mapping:
                exchange, tokens = exchange_mapping[exchange_name]
                funding_rates.extend(exchange.get_funding_rates(tokens))

        return funding_rates