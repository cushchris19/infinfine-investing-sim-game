import random
import pytest
from game import Market


def test_market_update_deterministic():
    random.seed(0)
    market = Market()
    market.update()
    assert market.assets['stock'].price == pytest.approx(101.98343080936132)
    assert market.assets['bond'].price == pytest.approx(99.32171094764942)
    assert market.assets['crypto'].price == pytest.approx(96.80142775960789)
