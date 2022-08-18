from multiprocessing import context
from django.shortcuts import render
from web3 import Web3, exceptions
import json

bsc = "https://bsc-dataseed.binance.org"
web3 = Web3(Web3.HTTPProvider(bsc))
print(web3.isConnected())

# Create your views here.
def home(request):
    status = None
    result = ''
    tag = ''

    try:
        if request.method == 'POST':
            transHash = request.POST.get('hash')
            output = web3.eth.get_transaction_receipt(transHash)
            

            if output['status'] == 1:
                tag = 'success'
                status = 'Success'

            elif output['status'] == 0:
                tag = 'danger'
                status = 'Failure'

            else:
                tag = 'danger'
                status = output['status']

            result = f"<p>Transaction status: {status} <br/>The transaction is from {output['from']} and was made to {output['to']}</p>"

    except exceptions.TransactionNotFound:
        tag = 'danger'
        result = "Transaction not found!, program currently works for BSC Network"
        
    context = {
        'result': result,
        'tag': tag
    }

    return render(request, 'index.html', context)
