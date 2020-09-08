from unittest.mock import patch
from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase


class CommandTests(TestCase):

    # this function asserts the db connection is tried to connect once and success!
    def test_wait_for_db_ready(self):
        """Test waitting for db when db is available"""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.return_value = True
            call_command("wait_for_db")
            self.assertEqual(gi.call_count, 1)
    #replace the `time.sleep` with True so there is no need to wait during 5 attempts to connect to db
    @patch('time.sleep', return_value=True)
    def test_wait_for_db(self, ts):
        """Test wait for db"""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.side_effect = [OperationalError] * 5 + [True]
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 6)


