import json
import re
import requests

import urllib.parse

from bs4 import BeautifulSoup

from stairs.core.flow import Flow, step


class ExtractKagglePageSource(Flow):
    JSON_DATA_REGEX = """.push.*\);performance"""

    @step(None)
    def get_json_data(self, html):
        parsed_html = BeautifulSoup(html)

        div_attrs = {'class': 'site-layout__main-content'}
        text = parsed_html.body.find('div', div_attrs).text

        m = re.search(self.JSON_DATA_REGEX, text)
        json_data = m.group(0)[len(".push("):-len(");performance")]
        return dict(json_data=json.loads(json_data))

    @step(get_json_data)
    def get_html(self, url):
        return dict(html=requests.get(url).text)


class ExtractCompetitions(ExtractKagglePageSource):

    def __call__(self, competitions_url):
        r = self.start_from(self.get_html,
                            url=competitions_url)

        # return a list because it's a Flow based producer
        return r.extract_names_and_urls['competitions']

    def __reconnect__(self):
        self.get_json_data.set_next(self.extract_names_and_urls)

    @step(None)
    def extract_names_and_urls(self, json_data):
        competitions = []

        competitions_groups = json_data['fullCompetitionGroups']
        for group in competitions_groups:
            if 'competitions' in group:
                for competition in group['competitions']:
                    title = competition['competitionTitle']
                    url = competition['competitionUrl']
                    url = urllib.parse.urljoin('https://kaggle.com', url)

                    competitions.append(dict(c_title=title, c_url=url))

        return dict(competitions=competitions)


class ExtractDiscussions(ExtractKagglePageSource):

    def __call__(self, c_title, c_url):
        r = self.start_from(self.get_html,
                            c_title=c_title,
                            url=c_url)

        # return a list because it's a Flow based producer
        return r.extract_discussions_urls.discussions_urls

    def __reconnect__(self):
        self.get_json_data.set_next(self.extract_discussions_urls)

    @step(None)
    def extract_discussions_urls(self, json_data):
        d_urls = []
        for d_data in json_data['discussionTeaser']:
            url = urllib.parse.urljoin('https://kaggle.com', d_data['itemUrl'])
            d_urls.append(dict(discussion_url=url))

        return dict(discussions_urls=d_urls)


class SearchForGHRepos(ExtractKagglePageSource):
    GH_URL_REGEX = """http[s]?:\/\/(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"""

    def __call__(self, discussion_url):
        r = self.start_from(self.get_html, url=discussion_url)

        # return a list because it's a Flow based producer
        return r.search_for_gh_url.github_urls

    def __reconnect__(self):
        # Now we are using html and skipping json transformation
        self.get_html.set_next(self.search_for_gh_url)

    @step(None)
    def search_for_gh_url(self, html):
        github_urls = re.findall(self.GH_URL_REGEX, html)
        return dict(github_urls={'gh_url': url for url in  github_urls})
