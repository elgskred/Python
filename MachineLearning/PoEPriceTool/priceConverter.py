import requests
import json
import re

def priceIndex(wantedCurrency):
    currencyTypes = ['alt','fuse','alch','chaos','gcp','exa','chrom','jew','chance',
                     'chisel','scour','blessed','regret','regal','divine','vaal', 'aug','mirror', 'silver']
    currencyValue = {}
    
    exchangeUrl = 'http://www.pathofexile.com/api/trade/exchange/Bestiary'
    for s in range(0, len(currencyTypes)):
        have = 0
        want = 0
        search = {
            "exchange":
            {
                "status":
                    {
                        "option":
                            "online"},
                "have":
                    [currencyTypes[s]],
                "want":
                    [wantedCurrency]
            }
        }
        headers = {'content-type': 'application/json', 'X-Requested-With' : 'XMLHttpRequest'}
        
         
        response = requests.get(exchangeUrl, data=json.dumps(search), headers=headers)
        if response.status_code == 200:
            data = response.json()
            result = data['result']
            if len(result) > 20:
                num = 20
            else:
                num = len(result)
            for i in range(0, num, 1):
                if i < 1:
                    fetch = result[i]
                else:
                    fetch = fetch + ',' + result[i]
                
            query = data['id']
        
        
        fetchUrl = 'http://www.pathofexile.com/api/trade/fetch/' + fetch + '?exchange=true&query=' + query    
        response = requests.get(fetchUrl, data=json.dumps(search), headers=headers)
        if response.status_code == 200:
            exchangeData = response.json()
            exchangeData = exchangeData['result']
        
        for i in range(0, len(exchangeData)):
            if i == 0:
                have = exchangeData[i]['info']['exchange']['amount']
                want = exchangeData[i]['info']['item']['amount']
            else:
                have = have + exchangeData[i]['info']['exchange']['amount']
                want = want + exchangeData[i]['info']['item']['amount']
          
        currencyValue[currencyTypes[s]] = want / have
        
    return(currencyValue)
  












