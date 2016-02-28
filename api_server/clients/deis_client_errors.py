class DeisClientError(Exception):
    pass


class DeisClientTimeoutError(Exception):
    pass


class DeisClientResponseError(DeisClientError):

    def __init__(self, response):
        """Create a new ``DeisClientResponseError``.

        @type response: requests.Response
        """
        self.response = response

    def __unicode__(self):
        return """Response Code {code}

        {body}
        """.format(code=self.response.status_code, body=self.response.json())
