from string import Template
from contextlib import closing

from requests import get
from requests.exceptions import RequestException


class Requester():
    def __init__(self, url):
        self.url = url

    def get(self):
        try:
            if not isinstance(self.url, str):
                raise TypeError('simple_get(): requires a string')

            with closing(get(self.url, stream = True)) as response:
                if self.is_good_response(response):
                    return response.content
                else:
                    return None
        except RequestException as e:
            temp = Template('${url} : ${msg}')
            print(temp.substitute(url = self.url, msg = str(e)))
            return None
        except TypeError as e:
            print(e)
            return None

    def is_good_response(self, response):
        content_type = response.headers['Content-Type'].lower()
        return (response.status_code == 200
                and content_type is not None
                and content_type.find('html') > -1)
