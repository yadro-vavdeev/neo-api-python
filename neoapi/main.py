from typing import Dict, List, Optional
from neoapi.lib import Config
import requests
import json


class Neo:
    _default_node: str = None
    _private_key: str = None
    _nodes: List[str] = None
    _request_id = 0

    def __init__(self, **kwargs):
        if 'yaml_config_path' in kwargs:
            config = Config.load_from_yaml(kwargs.get('yaml_config_path'))
            self._nodes = config.nodes
            self._default_node = config.default_node
        if 'nodes' in kwargs:
            self._nodes = kwargs.get('nodes')
        self._default_node = kwargs.get('default_node', self.get_nodes()[0])
        self._private_key = kwargs.get('private_key', None)

    def _get_request_id(self):
        self._request_id += 1
        return self._request_id

    def get_nodes(self) -> List[str]:
        return self._nodes

    def is_valid_address(self, check_address: str, node: Optional[str] = None) -> bool:
        request_id = self._get_request_id()
        payload = {
            'method': 'validateaddress',
            'params': [check_address],
            'jsonrpc': '2.0',
            'id': request_id,
        }
        response = requests.post(node or self._default_node, json=payload).json()

        assert response["jsonrpc"]
        assert response["id"] == request_id
        if 'error' in response:
            raise RuntimeError(f"EC: {response['error']['code']}\nError: {response['error']['message']}")
        return response['result']['isvalid']

    def get_token_balances(self, check_address: str, node: Optional[str] = None) -> Dict[str, int]:
        request_id = self._get_request_id()
        payload = {
            'method': 'getnep17balances',
            'params': [check_address],
            'jsonrpc': '2.0',
            'id': request_id,
        }
        response = requests.post(node or self._default_node, json=payload).json()

        assert response["jsonrpc"]
        assert response["id"] == request_id
        print(response)
        if 'error' in response:
            raise RuntimeError(f"EC: {response['error']['code']}\nError: {response['error']['message']}")
        return {token['assethash']: token['amount'] for token in response['result']['balance']}

    def get_block_count(self, node: Optional[str] = None):
        request_id = self._get_request_id()
        payload = {
            'jsonrpc': '2.0',
            'method': 'getblockcount',
            'params': [],
            'id': request_id,
        }
        response = requests.post(node or self._default_node, data=json.dumps(payload)).json()
        assert response["jsonrpc"]
        assert response['id'] == request_id
        return int(response['result'])
