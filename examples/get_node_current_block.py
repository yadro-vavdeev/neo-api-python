import logging
from neoapi import Neo

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

neo = Neo(yaml_config_path='./configs/mainnet.yaml')

for node in neo.get_nodes():
    block_count = neo.get_block_count(node=node)
    logger.debug(f'Node: {node}')
    logger.debug(f'NEO block length on node: {block_count}')
    logger.debug('=======================================')
