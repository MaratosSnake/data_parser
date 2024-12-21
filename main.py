import time

from utils import *



SYMBOLS = ['btc', 'eth', 'bnb', 'xrp', 'sol', 'doge', 'ada', 'trx', 'avax', 'link', 'shib', 'ton', 'dot', 'sui', 'xlm',
           'hbar', 'bch', 'uni', 'pepe', 'ltc', 'leo', 'near', 'apt', 'icp', 'aave', 'pol', 'etc', 'render', 'cro',
           'vet', 'fet', 'bgb', 'tao', 'mnt', 'arb', 'fil', 'xmr', 'kas', 'ftm', 'om', 'stx', 'ena', 'algo', 'atom',
           'okb', 'op', 'imx', 'tia', 'wif', 'bonk', 'inj', 'grt', 'theta', 'ondo', 'virtual', 'sei', 'wld', 'jasmy',
           'rune', 'floki', 'ldo', 'gala', 'sand', 'mkr', 'beam', 'kaia', 'flr', 'brett', 'qnt', 'pyth', 'eos', 'hnt',
           'kcs', 'xtz', 'ray', 'ens', 'jup', 'flow', 'ar', 'aero', 'strk', 'crv', 'move', 'iota', 'dydx', 'egld',
           'bsv', 'neo', 'btt', 'core', 'aioz', 'xdc', 'mana', 'axs', 'ape','not','blur','zk','cake','zro']


def main(symbols):
    data = get_info_dict(format_symbols(symbols))
    add_data_to_data_frames(data, symbols)


if __name__ == '__main__':
    while True:
        main(SYMBOLS)
        print(f'{datetime.now()} - added data')
        time.sleep(900)