import requests
import time
import pandas as pd


base_url = 'http://localhost:8000/api/items/'
results = []

def send_request(method, url, **kwargs):
    start_time = time.time()

    try:
        response = requests.request(
            method,
            url,
            **kwargs
        )

        response.raise_for_status()

        result = {
            'method': response.request.method,
            'url': url,
            'params/body': kwargs.get('json') or kwargs.get('params'),
            'status_code': response.status_code,
            'response_time': time.time() - start_time,
            'response_data': response.json()
        }

    except requests.exceptions.RequestException as e:
        result = {
            'method': method,
            'url': url,
            'params/body': kwargs.get('json') or kwargs.get('params'),
            'status_code': response.status_code if 'response' in locals() else None,
            'response_time': time.time() - start_time,
            'error': type(e).__name__,
            'response_data': str(e)
        }

    results.append(result)
    return result


send_request(
    'GET',
    base_url,
    params={}
)


item = {
    'id': 300,
    'name': 'New Item',
    'value': 99.99,
    'category': 'New Category',
    'active': True,
    'updated_at': '2024-06-01T12:00:00Z'
}

send_request(
    'POST',
    base_url,
    json=item,
    timeout=5
)


put_item = {
    'id': 300,
    'name': 'Updated Item',
    'value': 149.99,
    'category': 'Updated Category',
    'active': False,
    'updated_at': '2024-06-02T12:00:00Z'
}

send_request(
    'PUT',
    f'{base_url}{put_item["id"]}/',
    json=put_item,
    timeout=5
)


patch_field = {
    'value': 10.09
}

send_request(
    'PATCH',
    f'{base_url}{put_item["id"]}/',
    json=patch_field,
    timeout=5
)


send_request(
    'GET',
    f'{base_url}{put_item["id"]}/',
    timeout=5
)


send_request(
    'DELETE',
    f'{base_url}{put_item["id"]}/',
    timeout=5
)


send_request(
    'GET',
    f'{base_url}{put_item["id"]}/',
    timeout=5
)


send_request(
    'GET',
    base_url + '99999'
)


send_request(
    'GET',
    base_url
)


send_request(
    'GET',
    base_url,
    timeout=0.0000001
)


api_log = pd.DataFrame(results)
api_log.to_csv(
    'results/api_log.csv',
    index=False
)

print(api_log.head())