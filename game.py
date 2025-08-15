import random
from dataclasses import dataclass, field
from typing import Dict


@dataclass
class Asset:
    """Represents a tradable asset with random price movements."""
    name: str
    price: float
    drift: float  # Expected daily return
    volatility: float  # Standard deviation of returns

    def update_price(self) -> None:
        """Update price using a random walk."""
        growth = random.gauss(self.drift, self.volatility)
        # Ensure prices stay positive
        self.price = max(0.01, self.price * (1 + growth))


class Market:
    """Collection of assets that update together."""

    def __init__(self) -> None:
        self.assets: Dict[str, Asset] = {
            "stock": Asset("stock", 100.0, 0.001, 0.02),
            "bond": Asset("bond", 100.0, 0.0002, 0.005),
            "crypto": Asset("crypto", 100.0, 0.002, 0.05),
        }

    def update(self) -> None:
        for asset in self.assets.values():
            asset.update_price()


@dataclass
class Portfolio:
    """Track cash and asset holdings."""
    cash: float = 1000.0
    holdings: Dict[str, float] = field(default_factory=dict)

    def buy(self, market: Market, asset_name: str, amount: float) -> None:
        asset = market.assets.get(asset_name)
        if not asset:
            print(f"Unknown asset: {asset_name}")
            return
        cost = asset.price * amount
        if cost > self.cash:
            print("Not enough cash.")
            return
        self.cash -= cost
        self.holdings[asset_name] = self.holdings.get(asset_name, 0.0) + amount

    def sell(self, market: Market, asset_name: str, amount: float) -> None:
        if self.holdings.get(asset_name, 0.0) < amount:
            print("Not enough holdings.")
            return
        asset = market.assets[asset_name]
        revenue = asset.price * amount
        self.cash += revenue
        self.holdings[asset_name] -= amount

    def value(self, market: Market) -> float:
        total = self.cash
        for name, qty in self.holdings.items():
            total += qty * market.assets[name].price
        return total


class Game:
    """Interactive investing simulation."""

    def __init__(self) -> None:
        self.market = Market()
        self.portfolio = Portfolio()
        self.day = 1

    def display_status(self) -> None:
        print(f"\nDay {self.day}")
        for asset in self.market.assets.values():
            print(f"{asset.name:>6}: ${asset.price:8.2f}")
        print(f"Cash : ${self.portfolio.cash:8.2f}")
        print(f"Value: ${self.portfolio.value(self.market):8.2f}")

    def process_command(self, command: str) -> bool:
        parts = command.strip().split()
        if not parts:
            return True
        action = parts[0].lower()
        if action in {"quit", "q", "exit"}:
            return False
        if action == "buy" and len(parts) == 3:
            self.portfolio.buy(self.market, parts[1], float(parts[2]))
        elif action == "sell" and len(parts) == 3:
            self.portfolio.sell(self.market, parts[1], float(parts[2]))
        elif action == "help":
            print("Commands: buy <asset> <amt>, sell <asset> <amt>, help, quit")
        else:
            print("Invalid command. Type 'help' for options.")
        return True

    def run(self) -> None:
        print("Welcome to the Infinite Investing Simulator!")
        print("Type 'help' for a list of commands.")
        while True:
            self.display_status()
            command = input("> ")
            if not self.process_command(command):
                break
            self.market.update()
            self.day += 1
        print("Thanks for playing!")


def main() -> None:
    Game().run()


if __name__ == "__main__":
    main()
