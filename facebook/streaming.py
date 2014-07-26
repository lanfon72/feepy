import time
import facebook
import logging

API_VERSION = 'v2.0'

class StreamListener(object):

    def __init__(self):
        pass
    def on_connect(self):
        pass
    def on_data(self, raw_data):
        b =[raw_data['id'],  #feed_id
            raw_data['from']['name'], #uname
            raw_data['from']['id'], #uid
            raw_data['message'], #content
            raw_data['actions'][0]['link'], #feed_url
            raw_data['object_id'], #object_id
            raw_data['created_time'], #created_time
            raw_data['update_time'] ] #update_time
        logging.error(b)

class Stream(object):
    def __init__(self, auth, listener, **options):
        self.auth = auth
        self.listener = listener
        self.running = False
        self.timeout = options.get('timeout')
        self.retry_count = options.get("retry_count")
        # values according to https://dev.twitter.com/docs/streaming-apis/connecting#Reconnecting
        self.retry_time_start = options.get("retry_time", 5.0)
        #self.retry_420_start = options.get("retry_420", 60.0)
        self.retry_time_cap = options.get("retry_time_cap", 320.0)
        self.snooze_time_step = options.get("snooze_time", 0.25)
        self.snooze_time_cap = options.get("snooze_time_cap", 16)
        self.buffer_size = options.get("buffer_size",  1500)

        #self.api = API()
        #self.session = requests.Session()
        #self.session.headers = options.get("headers") or {}
        #self.session.params = None
        self.body = None
        self.retry_time = self.retry_time_start
        self.snooze_time = self.snooze_time_step

    def _run(self):
        # Authenticate
        url = "%s?%s" % (self.url, self.startTime)
        resp = None
        exception = None
        while self.running:
            try:
            # get fb.request feeds + token
            # sleep 5mins
                resp = host.request(url)
            #self.listener.on_connect()
                self._read_loop(resp['data'])
            except Exception as exception:
                # any exception is fatal, so kill loop.
                break

        # clean up
        self.running = False

        if exception:
            # call a hanlder first so that the exception can be logged.
            self.listener.on_exception(exception)
            raise

    def _data(self, data):
        if self.listener.on_data(data) is False:
            self.running = False

    def _read_loop(self, resp):
        # prase feed in feeds.
        while self.running:
            feed = resp.pop()
            self._data(feed)


    def _start(self, async):
        self.running = True
        if async:
            self._thread = Thread(target=self._run)
            self.thread.start()
        else:
            self._run()
    def on_closed(self, resp):
        #
        pass
    def userstream(self,**args):
        pass
    def filter(self,follow=None, async=False, editd=False, delted=False, encoding='utf8'):
        if self.running:
            pass  # *** there should raise ERROR like already connected. *** #
        self.url = '/%s/me/home' & API_VERSION
        self.host = facebook.GraphAPI(access_token = auth)
        self.startTime = time.time()

        if edited:
            pass
        if delted:
            pass

        self._start(async)

    def disconnect(self):
        if self.running is False:
            return
        self.running = False

    #firehose
    #retweet
    #sample
    #sitestream