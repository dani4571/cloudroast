"""
Copyright 2013 Rackspace

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from random import randint

from cafe.drivers.unittest.decorators import tags
from cloudcafe.compute.common.datagen import rand_name
from cloudcafe.compute.common.exceptions import ActionInProgress
from test_repo.compute.fixtures import ComputeAdminFixture

class CreateFlavorsAdminTest(ComputeAdminFixture):

    @classmethod
    def setUpClass(cls):
        super(CreateFlavorsAdminTest, cls).setUpClass()
        cls.flavor_id = randint(1, 99999)
        cls.flavor_name = rand_name('flavor')
        cls.admin_flavors_client.create_flavor(
            name=cls.flavor_name, ram='64',vcpus='1', disk='10',
            id=cls.flavor_id, is_public=True)

    @classmethod
    def tearDownClass(cls):
        super(CreateFlavorsAdminTest, cls).tearDownClass()
        cls.admin_flavors_client.delete_flavor(cls.flavor_id)

    def test_create_server_from_new_flavor(self):
        self.server_behaviors.create_active_server(flavor_ref=self.flavor_id)

    def test_create_flavor_with_duplicate(self):
        with self.assertRaises(ActionInProgress):
            self.admin_flavors_client.create_flavor(
                name=self.flavor_name, ram='64',vcpus='1', disk='10',
                id=self.flavor_id, is_public=True)

