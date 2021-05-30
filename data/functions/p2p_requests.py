import requests
import json


def get_p2p_payment_url(secret_p2p, bill_id, amount, comment):
    s = requests.Session()
    s.headers = {'content-type': 'application/json'}
    s.headers['authorization'] = 'Bearer ' + secret_p2p
    s.headers['Accept'] = 'application/json'

    params = {'amount': {'value': amount, 'currency': 'RUB', },
              'comment': comment,
              }

    params = json.dumps(params)

    g = s.put(f'https://api.qiwi.com/partner/bill/v1/bills/{bill_id}',
              data=params,
              )

    return g.json()["payUrl"]


def check_p2p_payment(bill_id, secret_p2p):
    s = requests.Session()
    s.headers['authorization'] = 'Bearer ' + secret_p2p
    s.headers['Accept'] = 'application/json'

    params = {'billid': bill_id}

    params = json.dumps(params)

    g = s.get(f'https://api.qiwi.com/partner/bill/v1/bills/{bill_id}',
              data=params,
              )
    return g.json()