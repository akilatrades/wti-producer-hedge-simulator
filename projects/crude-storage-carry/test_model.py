import unittest
from model import CarryCosts,storage_economics


class CarryTests(unittest.TestCase):
    def test_no_costs_and_breakeven(self):
        c=CarryCosts(3,0,0,0,0)
        x=storage_economics(70,73,c)
        self.assertEqual(x["net_carry"],3)
        self.assertEqual(x["breakeven_monthly_storage"],1)
        self.assertEqual(storage_economics(70,73,CarryCosts(3,1,0,0,0))["net_carry"],0)

    def test_cost_monotonicity(self):
        a=storage_economics(70,75)
        b=storage_economics(70,75,CarryCosts(storage_per_month=1))
        self.assertAlmostEqual(a["net_carry"]-b["net_carry"],1.5)
        self.assertLess(storage_economics(70,69)["net_carry"],0)

    def test_bad_inputs(self):
        with self.assertRaises(ValueError):CarryCosts(months=0)
        with self.assertRaises(ValueError):storage_economics(float("nan"),70)
        with self.assertRaises(ValueError):storage_economics(-10,70)
