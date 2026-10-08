import unittest
import numpy as np
from math import exp
from src.options import black76, costless_ceiling, producer_revenues


class OptionTests(unittest.TestCase):
    def test_parity_and_limits(self):
        self.assertAlmostEqual(
            black76(70, 60, 1, 0.4, 0.04) - black76(70, 60, 1, 0.4, 0.04, "put"),
            exp(-0.04) * 10,
        )
        self.assertEqual(black76(50, 60, 0, 0.4, kind="put"), 10)
        self.assertEqual(black76(50, 60, 1, 0, kind="call"), 0)
        with self.assertRaises(ValueError):
            black76(-1, 60, 1, 0.4)

    def test_costless_and_downside(self):
        c = costless_ceiling(70, 60, 1, 0.4, 0.04)
        t = costless_ceiling(70, 60, 1, 0.4, 0.04, 45)
        self.assertGreater(t, c)
        self.assertAlmostEqual(
            black76(70, 60, 1, 0.4, 0.04, "put"), black76(70, c, 1, 0.4, 0.04)
        )
        self.assertAlmostEqual(
            black76(70, 60, 1, 0.4, 0.04, "put") - black76(70, 45, 1, 0.4, 0.04, "put"),
            black76(70, t, 1, 0.4, 0.04),
        )
        x = producer_revenues(
            np.array([-10, 20, 45, 60, 100]), -2, 70, 60, c, t, 45, barrels=1
        )
        np.testing.assert_allclose(x["futures"], 68)
        np.testing.assert_allclose(x["fixed_price_swap"], x["futures"])
        np.testing.assert_allclose(x["costless_collar"][:3], 58)
        np.testing.assert_allclose(x["three_way_collar"][:3], [3, 33, 58])

    def test_no_hedge(self):
        c = costless_ceiling(70, 60, 1, 0.4)
        t = costless_ceiling(70, 60, 1, 0.4, subfloor=45)
        x = producer_revenues([40, 80], -3, 70, 60, c, t, 45, hedge_fraction=0)
        for v in x.values():
            np.testing.assert_allclose(v, x["unhedged"])
