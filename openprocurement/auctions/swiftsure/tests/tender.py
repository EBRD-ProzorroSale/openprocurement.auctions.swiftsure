# -*- coding: utf-8 -*-
import unittest
from copy import deepcopy

from openprocurement.auctions.core.tests.base import snitch
from openprocurement.auctions.core.tests.tender import (
    AuctionResourceTestMixin, DgfInsiderResourceTestMixin
)
from openprocurement.auctions.core.tests.blanks.tender_blanks import (
    # AuctionTest
    simple_add_auction,
    # AuctionResourceTest
    patch_tender_jsonpatch,
    auction_features_invalid,
    auction_features,
    # AuctionProcessTest
    invalid_auction_conditions,
)

from openprocurement.auctions.swiftsure.models import (
    SwiftsureAuction
)
from openprocurement.auctions.swiftsure.tests.base import (
    test_auction_data, test_organization,
    BaseWebTest, BaseAuctionWebTest,
    test_auction_data_with_schema
)
from openprocurement.auctions.swiftsure.tests.blanks.tender_blanks import (
    # AuctionTest
    create_role,
    edit_role,
    # AuctionResourceTest
    create_auction_invalid,
    create_auction_auctionPeriod,
    create_auction_generated,
    create_auction,
    # AuctionProcessTest
    one_valid_bid_auction,
    one_invalid_bid_auction,
    first_bid_auction,
    suspended_auction,
)


class AuctionTest(BaseWebTest):
    auction = SwiftsureAuction
    initial_data = test_auction_data

    test_simple_add_auction = snitch(simple_add_auction)
    test_create_role = snitch(create_role)
    test_edit_role = snitch(edit_role)


class AuctionResourceTest(BaseWebTest, AuctionResourceTestMixin, DgfInsiderResourceTestMixin):
    initial_status = 'active.tendering'
    initial_data = test_auction_data
    initial_organization = test_organization

    test_create_auction_invalid = snitch(create_auction_invalid)
    test_create_auction_auctionPeriod = snitch(create_auction_auctionPeriod)
    test_create_auction_generated = snitch(create_auction_generated)
    test_create_auction = snitch(create_auction)
    test_auction_features_invalid = unittest.skip("option not available")(snitch(auction_features_invalid))
    test_auction_features = unittest.skip("option not available")(snitch(auction_features))
    test_patch_tender_jsonpatch = snitch(patch_tender_jsonpatch)


class AuctionProcessTest(BaseAuctionWebTest):
    test_financial_organization = None

    #setUp = BaseWebTest.setUp
    def setUp(self):
        super(AuctionProcessTest.__bases__[0], self).setUp()

    test_invalid_auction_conditions = unittest.skip("option not available")(snitch(invalid_auction_conditions))
    test_one_valid_bid_auction = snitch(one_valid_bid_auction)
    test_one_invalid_bid_auction = snitch(one_invalid_bid_auction)
    test_first_bid_auction = snitch(first_bid_auction)
    test_suspended_auction = snitch(suspended_auction)


class AuctionSchemaResourceTest(AuctionResourceTest):
    initial_data = test_auction_data_with_schema

    def test_create_auction_with_bad_schemas_code(self):
        response = self.app.get('/auctions')
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(len(response.json['data']), 0)
        bad_initial_data = deepcopy(self.initial_data)
        bad_initial_data['items'][0]['classification']['id'] = "42124210-6"
        response = self.app.post_json('/auctions', {"data": bad_initial_data},
                                      status=422)
        self.assertEqual(response.status, '422 Unprocessable Entity')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['errors'],
                         [{
                             "location": "body",
                             "name": "items",
                             "description": [{
                                 "schema_properties": ["classification id mismatch with schema_properties code"]
                             }]
                         }])


class AuctionSchemaProcessTest(AuctionProcessTest):
    initial_data = test_auction_data_with_schema


def suite():
    tests = unittest.TestSuite()
    tests.addTest(unittest.makeSuite(AuctionTest))
    tests.addTest(unittest.makeSuite(AuctionResourceTest))
    tests.addTest(unittest.makeSuite(AuctionProcessTest))
    return tests


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
