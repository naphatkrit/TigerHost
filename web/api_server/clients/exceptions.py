class ClientError(Exception):
    pass


class ClientTimeoutError(Exception):
    pass


class ClientResponseError(ClientError):

    def __init__(self, response):
        """Create a new ``ClientResponseError``.

        @type response: requests.Response
        """
        self.response = response

    def __unicode__(self):
        return """Response Code {code}

        {body}
        """.format(code=self.response.status_code, body=self.response.json())
