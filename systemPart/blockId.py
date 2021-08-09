def blockId(reqData):
	req = reqData['userRequest']['block']['id']
	res = {
    "version": "2.0",
    "template": {
        "outputs": [
            {
                "simpleText": {
                    "text": req
                }
            }
        ]
      
    }
}
	return res
