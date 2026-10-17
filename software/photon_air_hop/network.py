"""Deterministic multi-hop routing simulator for Photon-Air-Hop.

This models already-decoded packet forwarding over an abstract optical-link graph.
It does NOT model photons, atmospheric radiative transfer, detector noise, or real
hardware. A link exists only when the user explicitly includes it in the graph.
"""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Iterable

from .packet import Frame, FrameError


@dataclass(frozen=True, slots=True)
class SimulationResult:
    delivered: bool
    route: tuple[int, ...]
    hops: int
    reason: str


class OpticalMesh:
    """Small graph model where edges represent currently usable directed links."""

    def __init__(self, links: Iterable[tuple[int, int]] = ()) -> None:
        self._adj: dict[int, set[int]] = {}
        for a, b in links:
            self.add_link(a, b)

    def add_link(self, source: int, destination: int, bidirectional: bool = False) -> None:
        self._adj.setdefault(source, set()).add(destination)
        self._adj.setdefault(destination, set())
        if bidirectional:
            self._adj[destination].add(source)

    def shortest_route(self, source: int, destination: int) -> tuple[int, ...] | None:
        if source == destination:
            return (source,)
        queue = deque([source])
        previous: dict[int, int | None] = {source: None}
        while queue:
            node = queue.popleft()
            for neighbor in sorted(self._adj.get(node, ())):
                if neighbor in previous:
                    continue
                previous[neighbor] = node
                if neighbor == destination:
                    route = [destination]
                    cursor: int | None = destination
                    while cursor is not None:
                        cursor = previous[cursor]
                        if cursor is not None:
                            route.append(cursor)
                    return tuple(reversed(route))
                queue.append(neighbor)
        return None

    def transmit(self, frame: Frame) -> SimulationResult:
        route = self.shortest_route(frame.source, frame.destination)
        if route is None:
            return SimulationResult(False, (), 0, "no route in current link graph")
        hops = len(route) - 1
        if hops > frame.ttl:
            return SimulationResult(False, route, hops, "TTL would be exhausted")
        # Every hop represents a receive/validate/forward operation.
        current = frame
        for relay in route[1:-1]:
            try:
                current = current.forwarded(relay)
            except FrameError as exc:
                return SimulationResult(False, route, hops, str(exc))
        return SimulationResult(True, route, hops, "delivered in idealized graph model")
