# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from bs4 import BeautifulSoup
import pytest
import requests

from pages.desktop.notes import Notes

link_check = pytest.mark.link_check
nondestructive = pytest.mark.nondestructive
skip_selenium = pytest.mark.skip_selenium


class TestNotes:

    @nondestructive
    def test_that_notes_page_is_reachable(self, mozwebqa):
        notes_page = Notes(mozwebqa)
        notes_page.go_to_page()
        assert 'Notes' in notes_page.firefox_notes_header_text

    @link_check
    @nondestructive
    @skip_selenium
    def test_that_all_links_are_valid(self, mozwebqa):
        notes_page = Notes(mozwebqa)
        url = mozwebqa.base_url + notes_page.notes_page_url
        page_response = requests.get(url)
        html = BeautifulSoup(page_response.content)
        bad_urls = []
        links = html.findAll('a')
        for link in links:
            # see both blog.mozilla.com and blog.mozilla.org domains
            if 'blog.mozilla.' in link['href']:
                # skip for issue 408: blog.m.o links not working via jenkins
                continue
            url = self.make_absolute(link['href'], mozwebqa.base_url)
            response_code = notes_page.get_response_code(url)
            if response_code != requests.codes.ok:
                bad_urls.append('%s is not a valid url - status code: %s.' % (url, response_code))
        assert [] == bad_urls

    def make_absolute(self, url, base_url):
        url = url.strip(" ")
        if url.startswith('http'):
            return url
        elif url.startswith('//'):
            return 'http:' + url

        return base_url + url
