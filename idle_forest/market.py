"""Simple in-memory market for tradable equipment."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from uuid import uuid4

from .models import Equipment


@dataclass
class MarketListing:
    id: str
    item: Equipment
    seller_id: str
    price: int
    created_tick: int
    active: bool = True
    buyer_id: str | None = None
    sold_tick: int | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "seller_id": self.seller_id,
            "buyer_id": self.buyer_id,
            "price": self.price,
            "created_tick": self.created_tick,
            "sold_tick": self.sold_tick,
            "active": self.active,
            "item": self.item.to_dict(),
        }


class Market:
    def __init__(self) -> None:
        self._listings: dict[str, MarketListing] = {}

    def create_listing(
        self, item: Equipment, seller_id: str, price: int, current_tick: int
    ) -> MarketListing:
        if not item.tradable:
            raise ValueError("item is not tradable")
        if price <= 0:
            raise ValueError("price must be greater than zero")

        listing = MarketListing(
            id=f"listing_{uuid4().hex[:12]}",
            item=item,
            seller_id=seller_id,
            price=price,
            created_tick=current_tick,
        )
        self._listings[listing.id] = listing
        return listing

    def buy(self, listing_id: str, buyer_id: str, current_tick: int) -> Equipment:
        listing = self.get_listing(listing_id)
        if not listing.active:
            raise ValueError("listing is not active")
        if buyer_id == listing.seller_id:
            raise ValueError("seller cannot buy their own listing")

        listing.active = False
        listing.buyer_id = buyer_id
        listing.sold_tick = current_tick
        listing.item.owner_id = buyer_id
        return listing.item

    def get_listing(self, listing_id: str) -> MarketListing:
        listing = self._listings.get(listing_id)
        if listing is None:
            raise KeyError(f"listing not found: {listing_id}")
        return listing

    def active_listings(self) -> list[MarketListing]:
        return [listing for listing in self._listings.values() if listing.active]

    def all_listings(self) -> list[MarketListing]:
        return list(self._listings.values())

    def to_dict(self) -> dict[str, Any]:
        return {
            "active": [listing.to_dict() for listing in self.active_listings()],
            "history": [listing.to_dict() for listing in self.all_listings()],
        }
