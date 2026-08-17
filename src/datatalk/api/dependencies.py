from __future__ import annotations

from datatalk.core import container

from datatalk.graph.workflow import DataTalkGraph



def get_graph() -> DataTalkGraph:
    return container.graph



def get_workflow() -> DataTalkGraph:
    return get_graph()
