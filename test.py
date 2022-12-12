try:
    import unittest
    from milestone3 import app

except Exception as e:
    print("Some modules are Missing {} ".format(e))


class FlaskTest(unittest.TestCase):

    # Checking to see if home page responds with statuscode 200
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get("/")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    # Checking to see if login page responds with statuscode 200
    def test_login(self):
        tester = app.test_client(self)
        response = tester.get("/login")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    # Checking to see if register page responds with statuscode 200
    def test_register(self):
        tester = app.test_client(self)
        response = tester.get("/register")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    # Checking to see if the content of the home page is text/html
    def test_content(self):
        tester = app.test_client(self)
        response = tester.get("/")
        self.assertEqual(response.content_type, "text/html; charset=utf-8")

    # Checking to see if the content of the login page is text/html
    def test_content_login(self):
        tester = app.test_client(self)
        response = tester.get("/login")
        self.assertEqual(response.content_type, "text/html; charset=utf-8")

    # Checking to see if the content of the register page is text/html
    def test_content_register(self):
        tester = app.test_client(self)
        response = tester.get("/register")
        self.assertEqual(response.content_type, "text/html; charset=utf-8")

    # Checking to see if string'How it works' is on the page
    def test_index_data(self):
        tester = app.test_client(self)
        response = tester.get("/")
        self.assertTrue(b'How it works' in response.data)

    # Checking to see if string'Log In' is on the page
    def test_login_data(self):
        tester = app.test_client(self)
        response = tester.get("/login")
        self.assertTrue(b'Log In' in response.data)

    # Checking to see if string'Username' is on the page
    def test_register_data(self):
        tester = app.test_client(self)
        response = tester.get("/register")
        self.assertTrue(b'Username' in response.data)


if __name__ == "__main__":
    unittest.main()
