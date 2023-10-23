# mpesahandler.py
import requests
import json

def initiate_payment(transaction_id, amount, phone_number):
        # M-Pesa API endpoint for STK push initiation
        api_endpoint = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'

        # Construct the payload for the request
        payload = {
            'TransactionID': transaction_id,
            'Amount': amount,
            'PhoneNumber': phone_number,
            'BusinessShortCode': 174379,
            "Password": "MTc0Mzc5YmZiMjc5ZjlhYTliZGJjZjE1OGU5N2RkNzFhNDY3Y2QyZTBjODkzMDU5YjEwZjc4ZTZiNzJhZGExZWQyYzkxOTIwMjMxMDE4MTA1MjA4",
            "Timestamp": "20231018105208",
            "TransactionType": "CustomerPayBillOnline",
            "PartyA": 254799722370,
            "PartyB": 174379,
            "PhoneNumber": 254799722370,
            "CallBackURL": "https://mydomain.com/mpesa_callback",
            "AccountReference": "KwemaRentals",
            "TransactionDesc": "Payment of Sh" + str(amount)
        }

        # Make the request to the M-Pesa API
        headers = {
            'Authorization': 'Bearer uhDrfqmUwHv4STOiT2MK8KBZ2bPp',
            'Content-Type': 'application/json',
        }

        try:
            response = requests.post(api_endpoint, data=json.dumps(payload), headers=headers)
            print(response.json())

            if response.status_code == 200:
                response_data = response.json()
                # Process the response from the M-Pesa API
                print("response data ->:", response_data)
                return True, response_data
            else:
                return False, {'error': 'Failed to initiate STK push'}
        except requests.exceptions.RequestException as e:
            return False, {'error': f'Failed to connect to M-Pesa API: {str(e)}'}
