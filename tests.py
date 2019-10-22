from datetime import datetime, timedelta
import unittest
from app import app, db
from app.models import User, Gig

class UserModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        u = User(username='susan')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))

    def test_avatar(self):
        u = User(username='john', email='john@example.com')
        self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar/'
                                         'd4c74594d841139328695756648b6bd6'
                                         '?d=identicon&s=128'))

    def test_favorite(self):
        u1 = User(username='john', email='john@example.com')
        u2 = User(username='susan', email='susan@example.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        self.assertEqual(u1.favorited.all(), [])
        self.assertEqual(u1.favoriters.all(), [])

        u1.favorite(u2)
        db.session.commit()
        self.assertTrue(u1.is_favorite(u2))
        self.assertEqual(u1.favorited.count(), 1)
        self.assertEqual(u1.favorited.first().username, 'susan')
        self.assertEqual(u2.favoriters.count(), 1)
        self.assertEqual(u2.favoriters.first().username, 'john')

        u1.unfavorite(u2)
        db.session.commit()
        self.assertFalse(u1.is_favorite(u2))
        self.assertEqual(u1.favorited.count(), 0)
        self.assertEqual(u2.favoriters.count(), 0)

    def test_favorite_gigs(self):
        # create four users
        u1 = User(username='john', email='john@example.com')
        u2 = User(username='susan', email='susan@example.com')
        u3 = User(username='mary', email='mary@example.com')
        u4 = User(username='david', email='david@example.com')
        db.session.add_all([u1, u2, u3, u4])

        # create four Gigs
        now = datetime.utcnow()
        p1 = Gig(detail="Gig from john", employer=u1,
                  timestamp=now + timedelta(seconds=1))
        p2 = Gig(detail="Gig from susan", employer=u2,
                  timestamp=now + timedelta(seconds=4))
        p3 = Gig(detail="Gig from mary", employer=u3,
                  timestamp=now + timedelta(seconds=3))
        p4 = Gig(detail="Gig from david", employer=u4,
                  timestamp=now + timedelta(seconds=2))
        db.session.add_all([p1, p2, p3, p4])
        db.session.commit()

        # setup the favoriters
        u1.favorite(u2)  # john follows susan
        u1.favorite(u4)  # john follows david
        u2.favorite(u3)  # susan follows mary
        u3.favorite(u4)  # mary follows david
        db.session.commit()

        # check the favorited Gigs of each user
        f1 = u1.favorite_gigs().all()
        f2 = u2.favorite_gigs().all()
        f3 = u3.favorite_gigs().all()
        f4 = u4.favorite_gigs().all()
        self.assertEqual(f1, [p2, p4, p1])
        self.assertEqual(f2, [p2, p3])
        self.assertEqual(f3, [p3, p4])
        self.assertEqual(f4, [p4])

if __name__ == '__main__':
    unittest.main(verbosity=2)