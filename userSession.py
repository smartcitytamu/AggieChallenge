import random as rand
import string

# todo Super insecure only did it cause it was quick

class SessionManager:
    def __init__(self):
        self.id_lens = 20  # length of id's that will be generated
        self.sessions = {}  # key: session id, value: UserSession

    def generate_session_id(self):
        my_id = ''.join(rand.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(self.id_lens))
        if self.sessions.get(my_id) is not None:
            my_id = self.generate_session_id()
        return my_id

    def create_session(self):
        my_session = SessionManager.UserSession(self.generate_session_id())
        self.sessions[my_session.session_id] = my_session
        return my_session.session_id

    def get_session(self, sess_id):
        try:
            my_session = self.sessions.get(sess_id)
            if my_session is None:
                raise Exception("No session with id: " + sess_id)

            return my_session

        except Exception as e:
            print("Failed to close session: " + str(e))

    def close_session(self, sess_id):
        try:
            my_session = self.sessions.get(sess_id)
            if my_session is None:
                raise Exception("No session with id: " + sess_id)
            my_session.close()
            del self.sessions[sess_id]

        except Exception as e:
            print("Failed to close session: " + str(e))

    class UserSession:
        def __init__(self, session_id):
            self.session_id = session_id
            self.bounding_box = []
            self.crawler_id = 0
            self.tweets = []

        def set_bounding_box(self, bounding_box):
            self.bounding_box = bounding_box

        def start_crawler(self):
            # todo stub
            print("Starting a crawler")
            self.crawler_id = 0

        def extend_tweets(self, tweets):
            # self.tweets = {**self.tweets, **tweets}
            self.tweets.extend(tweets)

        def close(self):
            # todo stub
            print("Closing Session!")