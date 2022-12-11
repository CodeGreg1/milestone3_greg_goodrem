try:
    import unittest
    from milestone3 import app

except Exception as e:
    print("Some modules are Missing {} ".format(e))


class FlaskTest(unittest.TestCase):

    # Checking to see if response is 200
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get("/")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    # Checking to see if the content is text/html
    def test_content(self):
        tester = app.test_client(self)
        response = tester.get("/")
        self.assertEqual(response.content_type, "text/html; charset=utf-8")

    # Checking to see if thee content is text/html
    def test_index_data(self):
        tester = app.test_client(self)
        response = tester.get("/")
        self.assertTrue(b'Message' in response.data)


if __name__ == "__main__":
    unittest.main()
