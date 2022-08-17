import logging
from neoapi import Neo

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

neo = Neo(yaml_config_path='./configs/mainnet.yaml')


check_address = 'AN6WBdhf8U8QzaguEH89aiDLBG5MBYYS4d'

is_valid = bool(neo.is_valid_address(check_address))
assert is_valid, 'Bad address'

balances = neo.get_token_balances(check_address)

logger.debug(f'Account: {check_address}')
logger.debug(f'Account balances:')
for token, balance in balances.items():
    logger.debug(f'\t-{token}: {balance}')
