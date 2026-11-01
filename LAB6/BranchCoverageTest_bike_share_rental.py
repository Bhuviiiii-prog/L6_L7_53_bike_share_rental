import pytest
from bike_share_rental import ride_cost, dock_status, can_unlock


# ---------------------------------------------------------------
# ride_cost
# ---------------------------------------------------------------
def test_standard_ride():
    assert ride_cost("standard", 45, False, False) == 40


def test_unknown_bike():
    with pytest.raises(ValueError):
        ride_cost("scooter", 30, False, False)


def test_invalid_duration_zero():
    with pytest.raises(ValueError):
        ride_cost("standard", 0, False, False)


def test_invalid_duration_negative():
    with pytest.raises(ValueError):
        ride_cost("standard", -5, False, False)


def test_subscriber_free_block():
    # blocks 1 -> 0, returns 0
    assert ride_cost("standard", 30, True, False) == 0


def test_subscriber_with_remaining_blocks():
    # blocks 2 -> 1, subscriber but still pays
    assert ride_cost("standard", 45, True, False) == 20


def test_peak_surcharge():
    assert ride_cost("electric", 30, False, True) == 50


def test_peak_cargo_no_surcharge():
    assert ride_cost("cargo", 30, False, True) == 50


def test_non_peak_electric():
    assert ride_cost("electric", 30, False, False) == 35


def test_exactly_180_no_penalty():
    assert ride_cost("standard", 180, False, False) == 120


def test_181_penalty():
    assert ride_cost("standard", 181, False, False) == 240


def test_long_ride_penalty():
    assert ride_cost("standard", 200, False, False) == 240


# ---------------------------------------------------------------
# dock_status
# ---------------------------------------------------------------
def test_dock_available():
    assert dock_status(5, 10) == "available"


def test_dock_invalid_capacity_zero():
    with pytest.raises(ValueError):
        dock_status(0, 0)


def test_dock_invalid_capacity_negative():
    with pytest.raises(ValueError):
        dock_status(1, -5)


def test_dock_negative_bikes():
    with pytest.raises(ValueError):
        dock_status(-1, 10)


def test_dock_more_bikes_than_capacity():
    with pytest.raises(ValueError):
        dock_status(11, 10)


def test_dock_empty():
    assert dock_status(0, 10) == "empty"


def test_dock_full():
    assert dock_status(10, 10) == "full"


def test_dock_one_bike():
    assert dock_status(1, 10) == "few bikes"


def test_dock_few_bikes():
    assert dock_status(2, 10) == "few bikes"


def test_dock_three_bikes_is_available():
    assert dock_status(3, 10) == "available"


def test_dock_three_free_slots_is_available():
    assert dock_status(7, 10) == "available"


def test_dock_few_slots():
    assert dock_status(8, 10) == "few slots"


def test_dock_nine_bikes():
    assert dock_status(9, 10) == "few slots"


# ---------------------------------------------------------------
# can_unlock
# ---------------------------------------------------------------
def test_unlock_active_ride():
    assert can_unlock(500, True, 25) is False


def test_unlock_underage():
    assert can_unlock(500, False, 15) is False


def test_unlock_age_16_ok():
    assert can_unlock(100, False, 16) is True


def test_unlock_minor_enough_balance():
    assert can_unlock(100, False, 17) is True


def test_unlock_minor_insufficient_balance():
    assert can_unlock(99, False, 17) is False


def test_unlock_age_18_boundary():
    assert can_unlock(50, False, 18) is True


def test_unlock_adult_enough_balance():
    assert can_unlock(50, False, 30) is True


def test_unlock_adult_insufficient_balance():
    assert can_unlock(49, False, 30) is False