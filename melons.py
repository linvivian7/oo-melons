"""This file should have our order classes in it."""
from random import randint
import datetime as dt


class TooManyMelonsError(ValueError):
    """Base class for other exceptions"""
    pass


class AbstractMelonOrder(object):
    """ A superclass for melon orders"""

    def __init__(self, species, qty, country_code):
        self.species = species
        self.qty = qty
        self.country_code = country_code
        self.shipped = False
        self.order_time = dt.datetime.now()
        self.order_hour = self.order_time.hour
        self.order_weekday = dt.date.today().isoweekday()

        if self.qty > 100:
            raise TooManyMelonsError("No more than 100 melons!")


    def get_base_price(self):
        """ Calculate splurge pricing """

        # Splurge pricing
        self.base_price = randint(5, 9)

        # Christmas melon surcharge
        if self.species == "Christmas melon":
            self.base_price = self.base_price * 1.5

        # Morning rush hour surcharge
        if (self.order_hour >= 8 and self.order_hour < 11 and
            self.order_weekday <= 5):

            self.base_price += 4

        return self.base_price

    def get_total(self, fee=0):
        """Calculate price."""

        self.get_base_price()

        total = (1 + self.tax) * self.qty * self.base_price + fee
        return total

    def mark_shipped(self):
        """Set shipped to true."""

        self.shipped = True

    def get_country_code(self):
        """Return the country code."""

        return self.country_code


class DomesticMelonOrder(AbstractMelonOrder):
    """A domestic (in the US) melon order."""

    order_type = "domestic"
    tax = 0.08

    def __init__(self, species, qty):
        """Initialize melon order attributes"""
        super(DomesticMelonOrder, self).__init__(species, qty, "USA")


class InternationalMelonOrder(AbstractMelonOrder):
    """An international (non-US) melon order."""

    order_type = "international"
    tax = 0.17

    def get_total(self):
        if self.qty < 10:
            return super(InternationalMelonOrder, self).get_total(3)
        else:
            return super(InternationalMelonOrder, self).get_total()


class GovernmentMelonOrder(AbstractMelonOrder):
    """All government melon orders"""

    order_type = "government"
    tax = 0

    def __init__(self, species, qty):
        """Initialize melon order attributes"""
        super(GovernmentMelonOrder, self).__init__(species, qty, "USA")
        # Initialize without inspection pass
        self.passed_inspection = False

    def mark_inspection(self):
        self.passed_inspection = True
