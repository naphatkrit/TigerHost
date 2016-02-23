valid_wsse_headers = [
    ('''UsernameToken Username="bob", PasswordDigest="quR/EWLAV4xLf9Zqyw4pDmfV9OY=", Nonce="d36e316282959a9ed4c89851497a717f", Created="2003-12-15T14:43:07Z"''', {
        'username': 'bob',
        'digest': 'quR/EWLAV4xLf9Zqyw4pDmfV9OY=',
        'nonce': 'd36e316282959a9ed4c89851497a717f',
        'timestamp': '2003-12-15T14:43:07Z'
    })
]

invalid_wsse_headers = [
    '''UsernameToken PasswordDigest="quR/EWLAV4xLf9Zqyw4pDmfV9OY=", Nonce="d36e316282959a9ed4c89851497a717f", Created="2003-12-15T14:43:07Z"''',

    '''UsernameToken Username="bob", Nonce="d36e316282959a9ed4c89851497a717f", Created="2003-12-15T14:43:07Z"''',

    '''UsernameToken Username="bob", PasswordDigest="quR/EWLAV4xLf9Zqyw4pDmfV9OY=", Created="2003-12-15T14:43:07Z"''',

    '''UsernameToken Username="bob", PasswordDigest="quR/EWLAV4xLf9Zqyw4pDmfV9OY=", Nonce="d36e316282959a9ed4c89851497a717f"''',
]

valid_wsse_digests = [{
    'secret': 'taadtaadpstcsm',
    'nonce': 'd36e316282959a9ed4c89851497a717f',
    'timestamp': '2003-12-15T14:43:07Z',
    'digest': 'quR/EWLAV4xLf9Zqyw4pDmfV9OY='
},
]
