import json
import re
import requests
import datetime
import urllib.parse

from bs4 import BeautifulSoup

from stairs.core.flow import Flow, step
from stairs import StopPipelineFlag


GH_URL_REGEX = """http[s]?:\/\/(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"""


class ExtractKagglePageSource(Flow):
    """
    It's a based flow which makes a request and parse html using beautiful soup.

    You can use it as a base class and then reconnect steps as you want.
    """
    JSON_DATA_REGEX = """.push.*\);performance"""

    @step(None)
    def get_json_data(self, html):
        parsed_html = BeautifulSoup(html, 'html.parser')

        div_attrs = {'class': 'site-layout__main-content'}
        div = parsed_html.body.find('div', div_attrs)
        # if div not found stop pipeline for this url only
        if not div:
            raise StopPipelineFlag()

        m = re.search(self.JSON_DATA_REGEX,  div.text)
        json_data = m.group(0)[len(".push("):-len(");performance")]
        return dict(json_data=json.loads(json_data))

    @step(get_json_data)
    def get_html(self, url):
        return dict(html=requests.get(url).text)


class ExtractCompetitions(Flow):
    """
    This flow makes request to kaggle competitions page and parse list of
    competitions.
    """

    def __init__(self, cnt_pages):
        self.cnt_pages = cnt_pages

    def __call__(self, competitions_url):
        print("Start competitions parsing")
        r = self.start_from(self.extract_json_data,
                            competitions_url=competitions_url)

        # return a list because it's a Flow based producer
        # each list has dict with c_title and c_url
        print("COMPETITIONS:", len(r.extract_names_and_urls['competitions']))
        return r.extract_names_and_urls['competitions']

    @step(None)
    def extract_names_and_urls(self, json_data):
        """
        Extracting competitions urls.
        """
        competitions = []
        competitions_groups = json_data['fullCompetitionGroups']
        competitions_groups.append(json_data['pagedCompetitionGroup'])
        for group in competitions_groups:
            if 'competitions' in group:
                for competition in group['competitions']:
                    title = competition['competitionTitle']
                    url = competition['competitionUrl']
                    url = urllib.parse.urljoin('https://kaggle.com', url)

                    competitions.append(dict(c_title=title, c_url=url))

        return dict(competitions=competitions)

    @step(extract_names_and_urls)
    def extract_json_data(self, competitions_url):
        r = requests.get(competitions_url)
        return dict(json_data=r.json())


class ExtractDiscussions(ExtractKagglePageSource):
    """
    Flow for extracting kaggle discussions. Also based on "html parsing" flow.
    """
    def __call__(self, c_title, c_url):

        print("Start dis parsing")
        r = self.start_from(self.get_html,
                            c_title=c_title,
                            url=c_url)

        # return a list because it's a Flow based producer
        return r.extract_discussions_urls['discussions_urls']

    def __reconnect__(self):
        """
        Here we connecting base "html parsing" flow with `extract_discussions_urls`
        """
        self.get_json_data.set_next(self.extract_discussions_urls)

    @step(None)
    def extract_discussions_urls(self, json_data):
        """
        Gettings discussion pages.
        """
        d_urls = []
        for d_data in json_data['discussionTeaser']:
            url = urllib.parse.urljoin('https://kaggle.com', d_data['itemUrl'])
            d_urls.append(dict(discussion_url=url))

        return dict(discussions_urls=d_urls)


class SearchForGHRepos(ExtractKagglePageSource):
    """
    Flow for extracting github links from discussions pages
    """
    def __call__(self, discussion_url):

        print("Start repos parsing")
        r = self.start_from(self.get_html, url=discussion_url)

        # return a list because it's a Flow based producer
        return r.search_for_gh_url['github_urls']

    def __reconnect__(self):
        # Now we are using html and skipping json transformation
        self.get_html.set_next(self.search_for_gh_url)

    @step(None)
    def search_for_gh_url(self, html):
        """
        Trying to find github page in comments.
        """
        urls = re.findall(GH_URL_REGEX, html)
        github_urls = [url for url in urls if "github.com" in url]
        return dict(github_urls=[dict(gh_url=url) for url in github_urls])


class MentionsKaggle(ExtractKagglePageSource):
    """
    Flow for extracting github links from discussions pages
    """

    def __init__(self, terms):
        self.terms = terms

    def __call__(self, discussion_url):

        print("Start repos parsing")
        r = self.start_from(self.get_html, url=discussion_url)

        # return a list because it's a Flow based producer
        print(r.search_for_term, type(r.search_for_term))
        return r.search_for_term

    def __reconnect__(self):
        # Now we are using html and skipping json transformation
        self.get_html.set_next(self.get_json_data)
        self.get_json_data.set_next(self.search_for_term)

    @step(None)
    def search_for_term(self, json_data):
        """
        Trying to find github page in comments.
        """
        if 'dateEnabled' not in json_data:
            raise StopPipelineFlag()

        date = json_data['dateEnabled'].split('T')[0]
        date = datetime.datetime.strptime(date, "%Y-%m-%d")
        json_str = json.dumps(json_data)
        mentions = 0
        for term in self.terms:
            if term.lower() in json_str.lower():
                mentions += 1

        print("MENTIONS", mentions)
        return dict(date=date, cnt_mentions=mentions)
