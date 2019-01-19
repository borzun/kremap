import webbrowser


class WebBrowser(object):

    def __init__(self):
        self.web_browser = webbrowser.get("windows-default")

        if self.web_browser is None:
            raise ValueError("ERROR: {0} can't get default Windows browser".format(
                self.__class__.__name__))

    def open_url(self, url, new=2):
        return self.web_browser.open(url, new=new, autoraise=True)
