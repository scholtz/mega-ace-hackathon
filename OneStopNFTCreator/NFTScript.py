import hashlib
import json
import os

import requests
from algosdk import transaction

def mintNFT(algod_client, creator_address, creator_private_key, asset_name, asset_unit_name):
    try:
        projectId = os.environ.get('INFURA_PROJECT_ID','2OTaZggJE1rLpCuy6HSH70J6pdy')
        projectSecret = os.environ.get('INFURA_PROJECT_SECRET','95e7f37242fdf1a906b9c9fac387d05a')
        endpoint = "https://ipfs.infura.io:5001"

        data = {
            "name": asset_name,
            "description": asset_name,
            "image": "ipfs://QmWMh1SRT6BMDCoM4yqmsNLXtLxkhyCGGyBMLxUCSTV8oo",
            "image_integrity": "sha256-a4+Jl+/isba7grXSvngy9I0XnhBE9Ir9QDbwe4PESb8=",
            "image_mimetype": "image/svg+xml",
            "external_url":"https://mega-ace.org/hackathon/"
        }
        bytes = json.dumps(data).encode('utf-8')
        hash_object = hashlib.sha256()
        hash_object.update(bytes)
        hex_dig = hash_object.digest()

        files = {
            'file': bytes
        }

        response1 = requests.post(endpoint + '/api/v0/add', files=files, auth=(projectId, projectSecret))
        print("response1",response1)
        hash = response1.text.split(",")[1].split(":")[1].replace('"','')
        print("hash",hash)
        print("algod_client",algod_client)
        params = algod_client.suggested_params() 
        print("hex_dig",hex_dig)
        print("params",params)
        txn = transaction.AssetConfigTxn(
            sender=creator_address,
            sp=params,
            total=1,
            decimals=0,
            unit_name=asset_unit_name,
            asset_name=asset_name,
            url="ipfs:://"+hash+"#arc3",
            default_frozen=False,
            manager=creator_address,
            reserve=creator_address,
            metadata_hash=hex_dig,
            freeze=None,
            clawback=None,
            strict_empty_address_check=False
        )
        #print("creator_private_key",creator_private_key)

        signed_txn = txn.sign(creator_private_key)
        print("signed_txn",signed_txn)
        txid = algod_client.send_transaction(signed_txn)
        
        print("txid",txid)
        result = transaction.wait_for_confirmation(
            algod_client, txid, 4
        )
        print('result',result)
        print(f"txID: {txid} confirmed in round: {result.get('confirmed-round', 0)}")

        print("txId",txid)
        return result['asset-index']
    except Exception as e:
        print(e)
    
    return 0  #your confirmed transaction's asset id should be returned instead


def transferNFT(algod_client, creator_address, creator_private_key, receiver_address, receiver_private_key, asset_id):
    params = algod_client.suggested_params() 

    unsigned_txn = transaction.AssetTransferTxn(
        receiver_address,
        params,
        receiver_address,
        0,
        asset_id
    )
    signed_txn = unsigned_txn.sign(receiver_private_key)
    txid = algod_client.send_transaction(signed_txn)
    print("optin txid",txid)
    unsigned_txn = transaction.AssetTransferTxn(
        creator_address,
        params,
        receiver_address,
        1,
        asset_id
    )
    signed_txn = unsigned_txn.sign(creator_private_key)
    print("signed_txn",signed_txn)
    txid = algod_client.send_transaction(signed_txn)
    
    print("txid",txid)
    transaction.wait_for_confirmation(
        algod_client, txid, 4
    )
    pass

