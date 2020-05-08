import requests
import csv


with open("contractaddress.csv", 'r') as file:
    reader = csv.reader(file)
    i = 0
    for row in reader:

        if i == 5000:
            break
        if i < 2:
            i += 1
            continue
        address = row[1]
        data = {"jsonrpc": "2.0", "method": "eth_getCode", "params": [address, "latest"], "id": 1}
        response = requests.post(
            'https://mainnet.infura.io/v3/0438481f94734a508f1aac4e7598c135', json=data)
        response_json = response.json()

        if "result" in response_json:
            with open("contracts/" + address + ".evm", 'w') as output:
                output.write(response_json["result"][2:])
        i += 1
