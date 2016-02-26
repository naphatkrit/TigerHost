# lumbroso, 2015
# flake8: noqa

# WSSE Handlers for urllib2
#
# References:
# - http://www.xml.com/pub/a/2003/12/17/dive.html
# - http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0.pdf
# - http://www.w3.org/TR/NOTE-datetime



import base64, hashlib, os, random
import datetime, time
import urllib2



##########################################################################
##
## Set up logging.
##
##########################################################################


import logging

if "logger" not in vars():
  logger = logging.getLogger(__name__)
  logger.disabled = True




##########################################################################
##########################################################################
# CLIENT MODULE ##########################################################
##########################################################################
##########################################################################


##########################################################################
##
## Helper class and methods.
##
##########################################################################


class _str(str):
  """
  Helper function to prevent capitalization of strings sent as
  HTTP header.
  """
  # BUG: https://bugs.python.org/issue12455
  def capitalize(s):
    #print "capitalize() bypassed: sending value: %s" % ( s )
    return s

  def title(s):
    #print "title() bypassed: sending value: %s" % ( s )
    return s


def _parse_auth_scheme(www_auth_header):
  """
  Helper function to parse a `WWW-Authenticate` header, which, strictly
  speaking, is responsible for describing the format with which to return
  the authentication token. This class implements the `UsernameToken`
  profile.
  """

  # Assuming format:
  #
  # WWW-Authenticate: WSSE profile="", realm="", profile="UsernameToken"

  try:
    scheme, params_raw = map(str.strip, www_auth_header.strip().split(' ', 1))

    params_list = map(lambda x: map(str.strip, x.strip().split("=", 1)),
                      params_raw.split(","))

    params_dict = {}
    realm = None
    profile = None

    for (key, value) in params_list:
      if (len(value) <= 1 or
          value[0] != value[-1] or value[0] not in ['"', "'"]):
        logger.debug("Auth param '%s' was unquoted" % key)
      else:
        # strip quotes
        value = value[1:-1]
      params_dict[key] = value

      if key.lower() == 'realm':
        realm = value

      if key.lower() == 'profile':
        profile = value

    if realm == None:
      logger.debug("WWW-Authenticate provided no realm: using default.")
      realm = ""

    if profile == None:
      logger.debug("WWW-Authenticate provided no profile: " +
                   "assuming UsernameToken'.")
      profile = "UsernameToken"

    return { 'scheme':  scheme,
             'realm':   realm,
             'profile': profile,
             'raw' :    params_dict }
  except:
    # Log exception and propagate stack trace
    logger.warning("Could not parse malformed WWW-Authenticate header.",
                   exc_info = True)
    return None




##########################################################################
##
## WSSE token building class and top-level method.
##
##########################################################################


class WSSETokenBuilder(object):

  def __init__(self, username, password):
    """
    Create a `WSSETokenBuilder` class for the given `username` and
    `password`, that will allows for the generation of WSSE
    authentication tokens.
    """
    self.__username = username
    self.__password = password

  def generate_nonce(self, length = 16, fast = False):
    """
    Generate a (non-cryptographic) nonce. If `fast` is `True`, then a
    very short nonce is generated; this is sufficient if the server
    authentication does not store expired nonces. Otherwise more care
    is given to generate a more likely to be unique nonce.
    """

    nonce = None

    if fast:
      # This will do for most auth systems.
      nonce = ''.join([str(random.randint(0, 9)) for i in range(length)])
    else:
      # This should be used if nonces start to get repeated.
      # The nonces should be more varied this way.
      length = max(length, 64)
      nonce = base64.b64encode(os.urandom(length),altchars=b'-_').rstrip('=')

    return nonce

  def __make_timestamp_nonce(self, drift_seconds = 10):
    """
    Generate a UTC timestamp and nonce pair; allows for a fixed number
    of `drift_seconds` to account for the fact that the server clock might
    be late.
    """

    drift = datetime.timedelta(seconds = drift_seconds)
    timestamp = datetime.datetime.utcnow() - drift
    timestamp_str = timestamp.strftime("%Y-%m-%dT%H:%M:%SZ")
    nonce = self.generate_nonce()

    return (timestamp_str, nonce)

  def make_token(self, ts_nonce = None, drift_seconds = 10):
    """
    Create a WSSE token given the class' stored username and password.
    Optionally take `ts_nonce` a timestamp/nonce pair, otherwise one will
    be generated for this token. Token token is returned as a string of
    concatenated fields.
    """

    if ts_nonce == None:
      ts_nonce = self.__make_timestamp_nonce(drift_seconds = drift_seconds)

    (timestamp, nonce) = ts_nonce
    digest_list = [ nonce, timestamp, self.__password]

    encoded_digest = base64.b64encode(
      hashlib.sha256(''.join(digest_list)).digest())
    encoded_nonce = base64.b64encode(nonce)

    fields = [ ('Username',        self.__username),
               ('PasswordDigest',  encoded_digest),
               ('Nonce',           encoded_nonce),
               ('Created',         timestamp) ]

    str_fields = ', '.join(['%s="%s"' % kv
                            for kv in fields ])

    return str_fields


def make_token(username, password, profile = None):
  """
  Create a UsernameToken token for the given combination of `username`
  and `password` by instanciating a `WSSETokenBuilder` object.
  """

  # (Superfluous?) profile check

  if profile == None:
    logger.debug("Call to top-level 'make_token' with not WSSE Auth profile " +
                 "specified, assuming UsernameToken.")

  elif profile != 'UsernameToken':
    logger.warning("Call to top-level 'make_token' with unsupported WSSE Auth " +
                   "profile '%s'." % profile)

  token = WSSETokenBuilder(username, password).make_token()
  logger.debug("Created WSSE token '%s'" % token)

  return token




##########################################################################
##
## Hooks to urllib2.
##
## - AbstractWSSEAuthHandler
##
##########################################################################


class AbstractWSSEAuthHandler(object):

  # XXX this allows for multiple auth-schemes, but will stupidly pick
  # the last one with a realm specified.

  def __init__(self, password_mgr = None):
    if password_mgr is None:
      password_mgr = HTTPPasswordMgr()

    self.passwd = password_mgr
    self.add_password = self.passwd.add_password

  def http_error_auth_reqed(self, authreq, host, req, headers):
    # host may be an authority (without userinfo) or a URL with an
    # authority
    # XXX could be multiple headers
    authreq = headers.get(authreq, None)
    if authreq:
      ret = _parse_auth_scheme(authreq)
      if ret:
        if ret['scheme'].lower() == 'wsse':
          return self.retry_http_wsse_auth(host, req,
                                           ret['realm'], ret['profile'])

  def add_auth_header(self, req,
                      user = None, pw = None,
                      realm = None, host = None, profile = None):

    if (not user or not pw) and host != None:

      # If user and password are not specified, but we know the
      # host, try to lookup username+password in attached
      # password manager

      user, pw = self.passwd.find_user_password(realm, host)

    if pw is not None:
      # If we have a password, produce a token and add to header.

      token = self.make_token(user, pw, profile = profile)
      auth = '%s %s' % (profile, token)

      logger.debug("WSSE urllib2 client: adding header '%s'." %
                   auth)

      req.add_unredirected_header(_str(self.auth_header), auth)

      return req #self.parent.open(req, timeout=req.timeout)

    logger.debug("WSSE urllib2 client: 'add_auth_header' failed; " +
                 "could not obtain username/password pair.")

    return None

  def retry_http_wsse_auth(self, host, req, realm, profile):
    """
    If a request `req` has failed, retry it after adding a WSSE
    authentication header; only do this if the existing request does not
    already contain a WSSE header (which would indicate that absence of
    the header is not the problem).
    """
    if req.get_header(self.auth_header, None) == None:
      new_req = self.add_auth_header(req,
                                     realm = realm, host = host,
                                     profile = profile)

      if new_req == None:
        logger.debug("WSSE urllib2 client: 'retry_http_wsse_auth' " +
                     " called on request which already failed.")
        return None

      req = new_req

    return self.parent.open(req, timeout=req.timeout)


class WSSEAuthHandler(AbstractWSSEAuthHandler,
                      urllib2.BaseHandler):
  """

  """

  handler_order = 600
  auth_header = 'X-WSSE'

  def __init__(self,
               password_mgr = None, preempt = False,
               user = None, pw = None, realm = None, host = None):
    super(WSSEAuthHandler, self).__init__(password_mgr = password_mgr)

    self.preempt = preempt
    self.user = user
    self.pw = pw
    self.realm = realm
    self.host = host

    if preempt:
      # change priority as has to happen before basic handler
      self.handler_order = 400

  def make_token(self, username, password, profile = None):
    """
    Return a WSSE UsernameToken (wrapper for actual top-level method).
    """

    if username == None:
      username = self.user

    if password == None:
      password = self.pw

    return make_token(username = username,
                      password = password,
                      profile = profile)

  def http_request(self, req):
    if self.preempt:
      logger.debug("WSSE urllib2 client: preempting WSSE request " +
                   "and adding authentication header.")

      auth_req = self.add_auth_header(req,
                                      user = self.user,
                                      pw = self.pw,
                                      realm = self.realm,
                                      host = self.host)
      if auth_req == None:
        auth_req = self.add_auth_header(req,
                                        realm = None,
                                        host = req.get_full_url())
      if auth_req:
        return auth_req

    return req

  https_request = http_request

  def http_error_401(self, req, fp, code, msg, headers):
    logger.debug("WSSE urllib2 client: got 401 Forbidden; assuming " +
                 "a WSSE authentication header is needed and retrying.")

    url = req.get_full_url()
    response = self.http_error_auth_reqed('www-authenticate',
                                          url, req, headers)

    return response




##########################################################################
##
## Hooks for 'requests' module (if it exists).
##
## - WSSEAuth
##
##########################################################################


try:
  import requests
  # We need specifically:
  # - requests.auth.AuthBase
  # - requests.auth.extract_cookies_to_jar

  class WSSEAuth(requests.auth.AuthBase):
    """
    Attaches HTTP Digest Authentication to the given Request object.

    Usage:

         requests.get(url, auth=WSSEAuth(user, pass))

    The auth object is of course reusable, and can be defined separately
    if several requests will be made with the same username+password pair.
    """

    def __init__(self, username, password):
      self.username = username
      self.password = password
      self.chal = {}
      self.pos = None
      self.num_401_calls = 1

    def handle_redirect(self, r, **kwargs):
      """Reset num_401_calls counter on redirects."""
      if r.is_redirect:
          self.num_401_calls = 1

    def handle_401(self, r, **kwargs):
      """Takes the given response and tries digest-auth, if needed."""

      if self.pos is not None:
          # Rewind the file position indicator of the body to where
          # it was to resend the request.
          r.request.body.seek(self.pos)

      num_401_calls = getattr(self, 'num_401_calls', 1)
      s_auth = r.headers.get('www-authenticate', '')

      ret = _parse_auth_scheme(s_auth)

      if ret and ret['scheme'].lower() == 'wsse' and num_401_calls < 2:

        self.num_401_calls += 1
        self.chal = ret

        # Consume content and release the original connection
        # to allow our new request to reuse the same one.
        r.content
        r.close()
        prep = r.request.copy()
        requests.auth.extract_cookies_to_jar(prep._cookies, r.request, r.raw)
        prep.prepare_cookies(prep._cookies)

        token = make_token(self.username, self.password,
                           profile = self.chal['profile'])

        prep.headers['X-WSSE'] = '%s %s' % (self.chal['profile'], token)

        _r = r.connection.send(prep, **kwargs)
        _r.history.append(r)
        _r.request = prep

        return _r

      self.num_401_calls = 1
      return r

    def __call__(self, r):
        try:
            self.pos = r.body.tell()
        except AttributeError:
            # In the case of HTTPDigestAuth being reused and the body of
            # the previous request was a file-like object, pos has the
            # file position of the previous body. Ensure it's set to
            # None.
            self.pos = None
        r.register_hook('response', self.handle_401)
        r.register_hook('response', self.handle_redirect)
        return r

except ImportError:
  # No 'requests' library
  logger.debug("WSSE Client: defining auth class for 'requests' module " +
               "failed; 'requests' not installed.")
  pass




##########################################################################
##
## Example client code.
##
##########################################################################

# Example of how to use the urllib2 auth handler

def setup_wsse_handler(base_url, username, password, preempt = True):
  """
  Configure urllib2 to try/use WSSE authentication, with a specific
  `username` and `password` when visiting any page that have a given
  `base_url`. Once this function has been called, all future requests
  through urllib2 should be able to handle WSSE authentication.
  """

  # Create a password manager
  passman = urllib2.HTTPPasswordMgrWithDefaultRealm()

  # Add username/password for domain defined by base_url
  passman.add_password(None, base_url, username, password)

  # Create the auth handler and install it in urllib2
  authhandler = WSSEAuthHandler(passman, preempt = preempt)
  opener = urllib2.build_opener(authhandler)
  urllib2.install_opener(opener)


# Example of how to use without handlers

def make_wsse_request(url,
                      wsse = None,
                      username = None, password = None,
                      no_exception = False):
  """
  Make a single WSSE-authentified request without installing any
  handler. Either a `WSSETokenBuilder` must be provided; or a `username`
  and `password`.
  """
  wsse_token = None

  if wsse != None:
    wsse_token = wsse.make_token()

  if username != None and password != None:
    wsse_token = WSSETokenBuilder(username = username,
                                  password = password).make_token()

  req = None

  try:
    # Create a request for the provided url and attached the WSSE
    # authentication header.

    req = urllib2.Request(url)
    req.add_header(_str('X-WSSE'), 'UsernameToken %s' % wsse_token)

    logger.debug("make_wsse_request: " + req.header_items())

    # Make the request and return its result (if successful).
    f = urllib2.urlopen(req)
    return f.read()

  except urllib2.HTTPError, err:
    logger.exception("make_wsse_request: HTTPError\n%r\n%r\n%r\n%r\n%r" %
                     (err.url, err.code, err.msg, err.hdrs, err.fp.read()),
                     exc_info = True)

    if not no_exception:
      # propagate exception
      raise
    else:
      return req




##########################################################################
##########################################################################
## SERVER MODULE #########################################################
##########################################################################
##########################################################################






##########################################################################
##
## Testing the WSSE token building mechanism.
##
##########################################################################

class TestWSSETokenBuilder(WSSETokenBuilder):
  def __init__(self):
    super(TestWSSETokenBuilder, self).__init__("jdoe", "secret")
    self.__fake_nonce = "ZN_\xdb\n\x13r\x93\xf9a<\xa4\x9f\x95\xbd\x9b"
    self.__fake_timestamp = "2015-05-18T14:50:17-04:00"

  def make_token(self):
    return super(TestWSSETokenBuilder, self).make_token(ts_nonce =
                                                        (self.__fake_timestamp,
                                                         self.__fake_nonce))

def unit_test():
  expected = ('Username="jdoe", ' +
              'PasswordDigest="AD4+vZvomtVUcd7jhUAVXMpHUmD/SD2EXMvIu5kzIJQ=", ' +
              'Nonce="Wk5f2woTcpP5YTykn5W9mw==", ' +
              'Created="2015-05-18T14:50:17-04:00"')

  obtained = TestWSSETokenBuilder().make_token()

  return expected == obtained

assert(unit_test())
