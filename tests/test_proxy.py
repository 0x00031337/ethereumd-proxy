from collections import Mapping

import pytest


from ethereumd.proxy.base import DEFAUT_FEE, GAS_PRICE
from ethereumd.utils import hex_to_dec
from ethereumd.exceptions import BadResponseError

from .base import BaseTestRunner, is_hex


class TestBaseProxy(BaseTestRunner):

    run_with = ['node', 'rpc']

    @pytest.mark.asyncio
    async def test_call_help(self):
        for proxy in self.proxies:
            response = await proxy.help()
            assert isinstance(response, str)

    @pytest.mark.asyncio
    async def test_call_getdifficulty(self):
        for proxy in self.proxies:
            response = await proxy.getdifficulty()
            assert isinstance(response, (int, float))

    @pytest.mark.asyncio
    async def test_call_settxfee(self):
        for proxy in self.proxies:
            gas_price = hex_to_dec(await proxy._call('eth_gasPrice'))
            gas = await proxy._paytxfee_to_etherfee()
            assert gas_price == gas['gas_price']

    @pytest.mark.asyncio
    async def test_call_settxfee_with_custom_fee(self):
        for proxy in self.proxies:
            response = await proxy.settxfee(DEFAUT_FEE)
            assert response is True
            gas = await proxy._paytxfee_to_etherfee()
            assert GAS_PRICE == gas['gas_price']

    @pytest.mark.asyncio
    async def test_call_listaccounts(self):
        for proxy in self.proxies:
            response = await proxy.listaccounts()
            assert isinstance(response, Mapping)
            # default 1 account on start
            assert len(response) == 1

    @pytest.mark.asyncio
    async def test_call_gettransaction_not_exist(self):
        for proxy in self.proxies:
            txhash = '0xc0c90cf2ea02dd40263f04f699366ba9b2f74f3a3d69f8050e50876802f4a5a8'
            try:
                await proxy.gettransaction(txhash)
            except BadResponseError as e:
                assert e.args[0]['error']['code'] == -5  # does not exists
            else:
                assert False, "Transaction must not be exists."

    @pytest.mark.asyncio
    async def test_call_getblockcount(self):
        for proxy in self.proxies:
            response = await proxy.getblockcount()
            assert isinstance(response, int)

    @pytest.mark.asyncio
    async def test_call_getbestblockhash(self):
        for proxy in self.proxies:
            response = await proxy.getbestblockhash()
            assert is_hex(response)

    @pytest.mark.asyncio
    async def test_call_getblock(self):
        for proxy in self.proxies:
            bhash = '0x12b5f772e7764cdfd140d098db6fcee56bfbc0cb2dcac67aadfb8755b1b56f6d'
            try:
                await proxy.getblock(bhash)
            except BadResponseError as e:
                assert e.args[0]['error']['code'] == -5  # does not exists
            else:
                assert False, "Block must not be exists."
