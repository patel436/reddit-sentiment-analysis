from reddit_sentiment_analyzer.utils import SingletonQueue

class CustomMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to run before any view function is called
        print("Running code before API request...")
        q = SingletonQueue()
        q.stream = False
        # Continue to the next middleware or view function
        response = self.get_response(request)

        return response

    def process_request(self, request):
        # This method is for compatibility with older versions of Django (< 3.0)
        pass
