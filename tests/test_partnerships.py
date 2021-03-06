# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
import requests

from pages.desktop.partnerships import Partnerships

link_check = pytest.mark.link_check
nondestructive = pytest.mark.nondestructive


class TestPartnerships:

    @nondestructive
    def test_section_link_destinations_are_correct(self, mozwebqa):
        partnerships_page = Partnerships(mozwebqa)
        partnerships_page.go_to_page()
        bad_links = []
        for link in partnerships_page.section_links_list:
            url = partnerships_page.link_destination(link.get('locator'))
            if not url.endswith(link.get('url_suffix')):
                bad_links.append('%s does not end with %s' % (url, link.get('url_suffix')))
        assert [] == bad_links

    @link_check
    @nondestructive
    def test_section_link_urls_are_valid(self, mozwebqa):
        partnerships_page = Partnerships(mozwebqa)
        partnerships_page.go_to_page()
        bad_urls = []
        for link in partnerships_page.section_links_list:
            url = partnerships_page.link_destination(link.get('locator'))
            response_code = partnerships_page.get_response_code(url)
            if response_code != requests.codes.ok:
                bad_urls.append('%s is not a valid url - status code: %s.' % (url, response_code))
        assert [] == bad_urls

    @nondestructive
    def test_image_srcs_are_correct(self, mozwebqa):
        partnerships_page = Partnerships(mozwebqa)
        partnerships_page.go_to_page()
        bad_images = []
        for image in partnerships_page.images_list:
            src = partnerships_page.image_source(image.get('locator'))
            if not image.get('img_name_contains') in src:
                bad_images.append('%s does not contain %s' % (src, image.get('img_name_contains')))
        assert [] == bad_images

    @nondestructive
    def test_partner_form_is_visible(self, mozwebqa):
        partnerships_page = Partnerships(mozwebqa)
        partnerships_page.go_to_page()
        partner_form = partnerships_page.partner_form
        assert partner_form.is_form_present
        assert partner_form.is_title_visible, 'The title is not visible on the form'
        for field in partner_form.fields_list:
            assert partner_form.is_element_visible(*field), 'The %s field is not visible on the form' % field[1:]
        assert partner_form.is_submit_button_visible, 'The submit button is not visible on the form'
