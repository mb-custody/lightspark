# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, List, Mapping

from lightspark.requests.requester import Requester

from .Connection import Connection
from .LightsparkNode import LightsparkNode
from .LightsparkNode import from_json as LightsparkNode_from_json
from .PageInfo import PageInfo
from .PageInfo import from_json as PageInfo_from_json


@dataclass
class AccountToNodesConnection(Connection):
    """A connection between an account and the nodes it manages."""

    requester: Requester

    count: int
    """The total count of objects in this connection, using the current filters. It is different from the number of objects returned in the current page (in the `entities` field)."""

    page_info: PageInfo
    """An object that holds pagination information about the objects in this connection."""

    entities: List[LightsparkNode]
    """The nodes for the current page of this connection."""
    typename: str

    def to_json(self) -> Mapping[str, Any]:
        return {
            "__typename": "AccountToNodesConnection",
            "account_to_nodes_connection_count": self.count,
            "account_to_nodes_connection_page_info": self.page_info.to_json(),
            "account_to_nodes_connection_entities": [
                e.to_json() for e in self.entities
            ],
        }


FRAGMENT = """
fragment AccountToNodesConnectionFragment on AccountToNodesConnection {
    __typename
    account_to_nodes_connection_count: count
    account_to_nodes_connection_page_info: page_info {
        __typename
        page_info_has_next_page: has_next_page
        page_info_has_previous_page: has_previous_page
        page_info_start_cursor: start_cursor
        page_info_end_cursor: end_cursor
    }
    account_to_nodes_connection_entities: entities {
        id
    }
}
"""


def from_json(requester: Requester, obj: Mapping[str, Any]) -> AccountToNodesConnection:
    return AccountToNodesConnection(
        requester=requester,
        typename="AccountToNodesConnection",
        count=obj["account_to_nodes_connection_count"],
        page_info=PageInfo_from_json(
            requester, obj["account_to_nodes_connection_page_info"]
        ),
        entities=list(
            map(
                # pylint: disable=unnecessary-lambda
                lambda e: LightsparkNode_from_json(requester, e),
                obj["account_to_nodes_connection_entities"],
            )
        ),
    )
