from typing import Annotated

from ocelescope import (
    OCEL,
    OCEL_FIELD,
    EventTypeFilter,
    ObjectTypeFilter,
    OCELAnnotation,
    Plugin,
    PluginInput,
    plugin_method,
)
from ocelescope.resource.default.petri_net import PetriNet

from .resource import ProcessTree
from .util.util import apply_ocim, convert_ocpn


class OCIMInput(PluginInput):
    object_types: list[str] = OCEL_FIELD(
        title="Object Types",
        field_type="object_type",
        ocel_id="ocel",
        default_frequency=0.5,
        theme="r4pm",
    )
    activities: list[str] = OCEL_FIELD(
        title="Activities",
        field_type="event_type",
        ocel_id="ocel",
        default_frequency=0.5,
        theme="r4pm",
    )


class OCIM(Plugin):
    label = "Object-Centric Inductive Miner"
    description = "Discover Object-Centric Process Models with Inductive Miner"
    version = "1.0.2"

    @plugin_method(
        label="Object-Centric Process Tree",
        description="Discover Object-Centric Process Tree with Inductive Miner",
    )
    def discover_ocpt(
        self, ocel: Annotated[OCEL, OCELAnnotation(label="Event Log")], input: OCIMInput
    ) -> ProcessTree:

        return apply_ocim(
            ocel.filter(
                [
                    ObjectTypeFilter(object_types=input.object_types, mode="include"),
                    EventTypeFilter(event_types=input.activities, mode="include"),
                ]
            )
        )

    @plugin_method(
        label="Object-Centric Petri Net",
        description="Discover Object-Centric Petri Net with Inductive Miner",
    )
    def discover_ocpn(
        self, ocel: Annotated[OCEL, OCELAnnotation(label="Event Log")], input: OCIMInput
    ) -> PetriNet:
        return convert_ocpn(
            ocel.filter(
                [
                    ObjectTypeFilter(object_types=input.object_types, mode="include"),
                    EventTypeFilter(event_types=input.activities, mode="include"),
                ]
            )
        )
