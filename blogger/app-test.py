import blogger
import os
import unittest
import tempfile



class BloggerTestCase(unittest.TestCase):

   def setUp(self):
       """ Setup a blank database before running this test."""
       print "running setup test."
       self.db_fd, blogger.app.config['DATABASE'] = tempfile.mkstemp()
       blogger.app.config['TESTING'] = True
       self.app = blogger.app.test_client()
       blogger.db_init()

   def tearDown(self):
        """ Destroy the blank empty database after each run. """
        os.close(self.db_fd)
        os.unlink(blogger.app.config['DATABASE'])
 
   def login(self):
       """ Login helper function. """
       return self.app.post('/login', data=dict(
          username = username,
          password = password), follow_redirects=True)

  
   def logout(self):
       """ logout helper. """
       return self.app.get('/logout',follow_redirects=True)

    
    #Assert functions
 
   def test_empty_db(self):
       """Ensure that the database is empty."""
       rv = self.app.get('/')
       self.assertIn(b'No entries yet. Add some!', rv.data)
  
       

if __name__ == '__main__':
     unittest.main()
