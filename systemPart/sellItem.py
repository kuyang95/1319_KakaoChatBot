import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import models

def sellItem(reqData):
	print(reqData)
	
	res = {
    "version": "2.0",
    "template": {
        "outputs": [
            {
                "simpleText": {
                    "text": "(아무것도 없음)"
                }
            }
        ]
	}
	}
	
	return res
