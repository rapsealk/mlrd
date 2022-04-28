import unittest

from mlrd.session.domain import Session


class SessionDomainTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_enum_recovery(self):
        given_state = Session.State.QUEUED

        self.assertEqual(given_state, Session.State(given_state))
        self.assertEqual(given_state, Session.State(given_state.name))
        self.assertEqual(given_state, Session.State(given_state.value))


if __name__ == "__main__":
    unittest.main()
