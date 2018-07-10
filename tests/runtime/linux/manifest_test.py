"""Unit test for treadmill.runtime.linux._manifest.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import unittest

import mock

# Disable W0611: Unused import
import tests.treadmill_test_skip_windows   # pylint: disable=W0611

from treadmill.runtime.linux import _manifest as app_manifest


class Docker2RuntimeManifestTest(unittest.TestCase):
    """Tests for treadmill.runtime.linux._manifest."""

    def setUp(self):
        self.tm_env = mock.Mock(
            root='/var/tmp/treadmill/app/approot',
            cell='testcell',
            zkurl='zookeeper://foo@foo:123',
            apps_dir='apps',
        )

    def tearDown(self):
        pass

    @mock.patch(
        'treadmill.subproc.resolve', mock.Mock(return_value='/treadmill-bind')
    )
    def test_generate_command(self):
        """Test docker command parsing/generation.
        """
        # pylint: disable=protected-access

        cmd = app_manifest._generate_command(
            {'name': 'foo', 'command': 'sleep 10'},
        )
        self.assertEqual(cmd, ('sleep 10', False))

        cmd = app_manifest._generate_command(
            {'name': 'foo', 'image': 'testwt2'},
        )
        self.assertEqual(
            cmd[0],
            (
                'exec $TREADMILL/bin/treadmill sproc docker'
                ' --name foo'
                ' --envdirs /env,/docker/env,/services/foo/env'
                ' --volume /var/tmp:/var/tmp:rw'
                ' --volume /var/spool:/var/spool:rw'
                ' --volume /docker/etc/hosts:/etc/hosts:ro'
                ' --volume /env:/env:ro'
                ' --volume /treadmill-bind:/opt/treadmill-bind:ro'
                ' --image testwt2'
            )
        )
        self.assertTrue(cmd[1])

        cmd = app_manifest._generate_command(
            {'name': 'foo', 'image': 'testwt2', 'args': ['foo', 'bar']},
        )
        self.assertEqual(
            cmd[0],
            (
                'exec $TREADMILL/bin/treadmill sproc docker'
                ' --name foo'
                ' --envdirs /env,/docker/env,/services/foo/env'
                ' --volume /var/tmp:/var/tmp:rw'
                ' --volume /var/spool:/var/spool:rw'
                ' --volume /docker/etc/hosts:/etc/hosts:ro'
                ' --volume /env:/env:ro'
                ' --volume /treadmill-bind:/opt/treadmill-bind:ro'
                ' --image testwt2'
                ' --'
                ' foo bar'
            )
        )
        self.assertTrue(cmd[1])

        cmd = app_manifest._generate_command(
            {'name': 'foo', 'image': 'testwt2',
             'args': ['60'], 'command': 'sleep'},
        )
        self.assertEqual(
            cmd[0],
            (
                'exec $TREADMILL/bin/treadmill sproc docker'
                ' --name foo'
                ' --envdirs /env,/docker/env,/services/foo/env'
                ' --volume /var/tmp:/var/tmp:rw'
                ' --volume /var/spool:/var/spool:rw'
                ' --volume /docker/etc/hosts:/etc/hosts:ro'
                ' --volume /env:/env:ro'
                ' --volume /treadmill-bind:/opt/treadmill-bind:ro'
                ' --entrypoint sleep'
                ' --image testwt2'
                ' --'
                ' 60'
            )
        )
        self.assertTrue(cmd[1])


if __name__ == '__main__':
    unittest.main()
