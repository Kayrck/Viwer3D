from dataclasses import dataclass, field


@dataclass
class SegmentState:
    name: str = ""
    color: str = ""
    segment_id: str = ""
    is_visible: bool = True
    source_volume_id: str = ""
    available_volumes: list = field(default_factory=list)
