from src.scenarios import production_volume_scenarios


def test_lower_production_can_create_overhedged_volume():
    scenarios = production_volume_scenarios(
        expected_production_bbl=100_000,
        hedge_ratio=1.0,
        spot_exit=60,
        futures_entry=75,
        futures_exit=60,
        volume_shocks=(-0.20, 0.0),
    )

    low_case = scenarios.iloc[0]
    base_case = scenarios.iloc[1]

    assert low_case["actual_production_bbl"] == 80_000
    assert low_case["overhedged_bbl"] == 20_000
    assert base_case["overhedged_bbl"] == 0
