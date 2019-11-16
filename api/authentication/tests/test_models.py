import nose.tools as nt

from nose.tools.nontrivial import raises

from django.core.signing import (TimestampSigner, b64_encode)
from django.core import mail

from django.test import TestCase

from authentication.models import StdUser


TEST_EMAIL      = "test_email@gmail.com"
TEST_PASSWORD   = "Str0ngp4ss!"
TEST_NAME       = "Alexandr"
TEST_SURNAME    = "Alexandrov"
TEST_PATRONIM   = "Alexandrovich"

MSG_ACCOUNT_ACTIVATED = 'Your account has been activated.'

MAIL_SUBJECT = 'subject'

class TestAdminUser(TestCase):
    pass

class TestStdUser(TestCase):

    ''' This method creates base data for tests '''
    @classmethod
    def setUpTestData(cls):
        cls.user = StdUser.objects.create_user(email=TEST_EMAIL, password=TEST_PASSWORD)
        cls.user.first_name = TEST_NAME
        cls.user.last_name  = TEST_SURNAME
        cls.user.patronymic = TEST_PATRONIM

    ''' Func _create_user must raise error if email is not set '''
    @raises(ValueError)
    def test_user_without_email(self):
        self.bad_user = StdUser.objects.create_user(email=None, password=TEST_PASSWORD)

    ''' Test verification code to make user active '''
    def test_get_verification_code(self):
        signer = TimestampSigner()
        code = b64_encode(bytes(signer.sign(TEST_EMAIL), encoding='utf-8'))
        
        nt.assert_equal(self.user.get_verification_code(TEST_EMAIL), code)

    ''' Test email verification with code from previous test '''
    def test_verify_email(self):
        code = self.user.get_verification_code(TEST_EMAIL)
        
        nt.assert_equal(self.user.verify_email(code.decode('utf-8')), 
                (True, MSG_ACCOUNT_ACTIVATED))
    
    ''' Test password change verification '''
    def test_verify_password(self):
        code = self.user.get_verification_code(TEST_EMAIL)
        
        nt.assert_equal(self.user.verify_password(code.decode('utf-8'), TEST_PASSWORD), 
                True)

    ''' Test password verification without code '''
    @raises(ValueError)
    def test_verify_password_no_code(self):
        self.user.verify_password(None, TEST_PASSWORD)

    ''' Test password verification when user not exist '''
    @raises(ValueError)
    def test_verify_password_error(self):
        code = self.user.get_verification_code(TEST_EMAIL)
        self.user.verify_password(code, TEST_PASSWORD)

    ''' Test case when error occurs in verify_email func '''
    @raises(ValueError)
    def test_verify_email_error(self):
        self.user.is_active = True
        self.user.save()
        code = self.user.get_verification_code(TEST_EMAIL)
        self.user.verify_email(code.decode('utf-8')) 

    ''' If code is None '''
    @raises(ValueError)
    def test_verify_email_no_code(self):
        self.user.verify_email(code=None)

    ''' Sending of verification email test '''
    def test_send_mail(self):
        self.user.send_mail(TEST_EMAIL)
       
        nt.assert_equal(len(mail.outbox), 1)
        nt.assert_equal(mail.outbox[0].subject, MAIL_SUBJECT)
        nt.assert_equal(mail.outbox[0].to, [TEST_EMAIL, ])

    ''' Sending of password restoration mail '''
    def test_send_revovery_password(self):
        self.user.send_recovery_password(TEST_EMAIL)

        nt.assert_equal(len(mail.outbox), 1)
        nt.assert_equal(mail.outbox[0].subject, MAIL_SUBJECT)
        nt.assert_equal(mail.outbox[0].to, [TEST_EMAIL, ])

    ''' Work only when user has is_active status '''
    def test_login(self):
        self.user.is_active = True
        self.user.save()
        
        login = self.client.login(email=TEST_EMAIL, password=TEST_PASSWORD)
        
        nt.assert_true(login)

    ''' When user not is_active he cant log in '''
    def test_not_login(self):
        login = self.client.login(email=TEST_EMAIL, password=TEST_PASSWORD)
        
        nt.assert_false(login)

    ''' Test get_short_name() func '''
    def test_get_short_name(self):
        short_name = self.user.get_short_name()
        
        nt.assert_equal(short_name, "%s" % (TEST_NAME))

    ''' Test get_full_name() func '''
    def test_get_full_name(self):
        full_name = self.user.get_full_name()
        
        nt.assert_equal(full_name, "%s %s %s" % (
            TEST_NAME, 
            TEST_SURNAME, 
            TEST_PATRONIM))