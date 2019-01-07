import unittest
from unittest.mock import patch, mock_open, MagicMock

import yagmail

from preschool_bill import PreschoolBill


class TestsPreSchoolBill(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.text = "<h2>Topic</h2><h3>There is to pay 100.12 EU.</h3>"

    def setUp(self):
        self.pb = PreschoolBill()
        self.pb.emails = ['test1@gmail.com', 'test2@gmail.com']
        self.pb.gmail_user = 'test@gmail.com'
        self.pb.gmail_pass = 'pass'

    def test_parse_data(self):
        text = "<h2>Topic</h2><h3>There is to pay 100.12 EU.</h3>"
        out_amount = self.pb.parse_data(text)
        self.assertEqual(out_amount, '100.12')

    @patch('preschool_bill.yagmail.SMTP.send')
    @patch('preschool_bill.open', new_callable=mock_open())
    def test_check_email_send(self, mock_send, mock_open):
        yagmail.SMTP('test@gmail.com', 'pass').send = MagicMock()
        data_text = ''
        amount = '300.00'
        self.pb.check_mail_and_send(data_text, amount)
        yagmail.SMTP('test@gmail.com', 'pass').send.assert_called_with(
            contents='There is a bill for 2019 January for amount 300.00 zl',
            subject='Pre-School Bill 2019 January', to='test2@gmail.com')


if __name__ == '__main__':
    unittest.main()
