from bloxplorer import bitcoin_explorer as explorer
import numpy
import pickle
import time

statuses = pickle.load(open('statuses.p', 'rb'))

curr_block = min(statuses.keys()) - 1

while curr_block >= 0:
    try:
        print(curr_block)
        hash = explorer.blocks.get_height(curr_block).data
        txids = explorer.blocks.get_txids(hash).data
        coinbase_txid = txids[0]
        coinbase = explorer.tx.get(coinbase_txid).data
        assert(any([vin['is_coinbase'] for vin in coinbase['vin']]))
        vouts = coinbase['vout']
        values = [vout['value'] for vout in vouts]
        sort_idxs = numpy.argsort(values)[::-1]
        if len(vouts) > 1:
            if vouts[sort_idxs[1]]['value'] > 0:
                print("non-zero second vout for coinbase at height {}".format(curr_block))
        spending_status = explorer.tx.get_spending_status(coinbase_txid, sort_idxs[0]).data
        statuses[curr_block] = spending_status
        pickle.dump(statuses, open('statuses.p', 'wb'))
        curr_block -= 1
    except Exception as e:
        print("Exception {}".format(e))
    finally:
        time.sleep(0.2)
