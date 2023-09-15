from unittest.mock import patch

from django.core.management import call_command
from django.test import TestCase 
from django.db.utils import OperationalError


class ManagementCommandsTestCase(TestCase):
    """
        tests for call_db
    """
    def test_wait_for_db_runs(self):
        """
            Tests that call_db will be called
        """
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.return_value = True
            call_command('call_db')
            self.assertEqual(gi.call_count, 1)

    @patch('time.sleep', return_value=True)
    def test_waits_then_retires(self ,ts):
        """
            Tests after encountering a failuire it 
            will call call_db againg
        """
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.side_effect = [OperationalError] * 3 + [True]
            call_command('call_db')
            self.assertEqual(gi.call_count, 4)
                        



            