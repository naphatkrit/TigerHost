valid_wsse_headers = [
    ('''UsernameToken Username="jdoe", PasswordDigest="AD4+vZvomtVUcd7jhUAVXMpHUmD/SD2EXMvIu5kzIJQ=", Nonce="Wk5f2woTcpP5YTykn5W9mw==", Created="2015-05-18T14:50:17-04:00"''', {
        'username': 'jdoe',
        'digest': 'AD4+vZvomtVUcd7jhUAVXMpHUmD/SD2EXMvIu5kzIJQ=',
        'nonce': 'Wk5f2woTcpP5YTykn5W9mw==',
        'timestamp': '2015-05-18T14:50:17-04:00'
    })
]

invalid_wsse_headers = [
    '''UsernameToken PasswordDigest="quR/EWLAV4xLf9Zqyw4pDmfV9OY=", Nonce="Wk5f2woTcpP5YTykn5W9mw==", Created="2015-05-18T14:50:17-04:00"''',

    '''UsernameToken Username="jdoe", Nonce="Wk5f2woTcpP5YTykn5W9mw==", Created="2015-05-18T14:50:17-04:00"''',

    '''UsernameToken Username="jdoe", PasswordDigest="quR/EWLAV4xLf9Zqyw4pDmfV9OY=", Created="2015-05-18T14:50:17-04:00"''',

    '''UsernameToken Username="jdoe", PasswordDigest="quR/EWLAV4xLf9Zqyw4pDmfV9OY=", Nonce="Wk5f2woTcpP5YTykn5W9mw=="''',
]

valid_wsse_digests = [{
    'secret': 'secret',
    'nonce': 'Wk5f2woTcpP5YTykn5W9mw==',
    'timestamp': '2015-05-18T14:50:17-04:00',
    'digest': 'AD4+vZvomtVUcd7jhUAVXMpHUmD/SD2EXMvIu5kzIJQ='
},
]
