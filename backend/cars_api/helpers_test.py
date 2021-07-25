import unittest

from cars_api.helpers import exists_in_nhtsa


class TestExistInNHTSAMethod(unittest.TestCase):
    def test_car_exists(self):
        """
        Return True if a car exists
        """

        exisitng_car = ("Ford", "Mustang")
        self.assertTrue(exists_in_nhtsa(*exisitng_car))

    def test_car_does_not_exist(self):
        """
        Return False if a car doesn't exist
        """

        not_exisitng_car1 = ("Ford", "Mustan")
        not_exisitng_car2 = ("For", "Mustang")
        self.assertFalse(exists_in_nhtsa(*not_exisitng_car1))
        self.assertFalse(exists_in_nhtsa(*not_exisitng_car2))


if __name__ == "__main__":
    unittest.main()
