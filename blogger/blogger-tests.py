import blogger 
import unittest
import os
import tempfile

class BasicTestCase(unittest.TestCase):

   def test_index(self):
      tester = blogger.app.test_client(self)
      response = tester.get('/',content_type='html/text')
      self.assertEqual(response.status_code, 404)


   def test_database(self):
       tester = os.path.exists("blogger.db")
       self.assertTrue(tester)

class BloggerTestCase(unittest.TestCase):
   """All test cases for the blogger application."""

   def setUp(self):
      """set up a blank empty database before each run."""
      self.db_fd,blogger.app.config['DATABASE'] = tempfile.mkstemp()
      blogger.app.config['TESTING'] = True
      self.app = blogger.app.test_client()
      blogger.db_init()

   def tearDown(self):
       """Destroy blank temp database after each run."""
       os.close(self.db_fd)
       os.unlink(blogger.app.config['DATABASE'])

   def login(self,username,password):
       """Test user login and authentication. """
       return self.app.post('/login', data=dict(
          username = username,
          password = password), follow_redirects=True)

   def logout(self): 
       """Test user logout"""
       """ logout helper. """
       return self.app.get('/logout',follow_redirects=True)


   # All test methods go here
   def test_empty_db(self):
       """Ensure that the database is empty."""
       rv = self.app.get('/')
       assert b'No entries so far.' in rv.data
   
   def test_login_logout(self):
        """Test login and logout using helper functions"""
        rv = self.login(blogger.app.config['USERNAME'],blogger.app.config['PASSWORD'])
        assert b'You were logged in' in rv.data
        rv = self.logout()
        assert b'You were logged out' in rv.data
        rv = self.login(blogger.app.config['USERNAME'] + 'x',blogger.app.config['PASSWORD'])
        assert b'Invalid username' in rv.data
        rv = self.login(blogger.app.config['USERNAME'],blogger.app.config['PASSWORD'] + 'x')
        assert b'Invalid password' in rv.data

   def test_messages(self):
        """Ensure that user can post messages"""
        self.login(blogger.app.config['USERNAME'],blogger.app.config['PASSWORD'])
        rv = self.app.post('/add', data=dict(
            title='<Hello>',
            text='<strong>HTML</strong> allowed here'
        ), follow_redirects=True)
        assert b'No entries here so far' not in rv.data
        assert b'&lt;Hello&gt;' in rv.data
        assert b'<strong>HTML</strong> allowed here' in rv.data
    

if __name__ == '__main__':
    unittest.main()
