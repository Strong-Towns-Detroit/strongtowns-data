"""Explicit asset and pipeline registry with dependency-DAG validation."""

from __future__ import annotations

from collections import defaultdict, deque

from krabby_real_estate.data.model import DataAsset, PipelineDefinition


class AssetRegistry:
    def __init__(self):
        self.assets: dict[str, DataAsset] = {}
        self.pipelines: dict[str, PipelineDefinition] = {}
        self.producers: dict[str, str] = {}

    def register_asset(self, asset: DataAsset) -> DataAsset:
        if asset.asset_id in self.assets:
            raise ValueError(f"duplicate asset id: {asset.asset_id}")
        self.assets[asset.asset_id] = asset
        return asset

    def register_pipeline(self, pipeline: PipelineDefinition) -> PipelineDefinition:
        if pipeline.pipeline_id in self.pipelines:
            raise ValueError(f"duplicate pipeline id: {pipeline.pipeline_id}")
        for output in pipeline.outputs:
            if output in self.producers:
                raise ValueError(
                    f"asset {output} has multiple producers: "
                    f"{self.producers[output]} and {pipeline.pipeline_id}"
                )
            self.producers[output] = pipeline.pipeline_id
        self.pipelines[pipeline.pipeline_id] = pipeline
        return pipeline

    def validate(self) -> None:
        for pipeline in self.pipelines.values():
            unknown = sorted((set(pipeline.inputs) | set(pipeline.outputs)) - set(self.assets))
            if unknown:
                raise ValueError(f"pipeline {pipeline.pipeline_id} uses unknown assets: {unknown}")
            for output in pipeline.outputs:
                declared = self.assets[output].producer_pipeline_id
                if declared != pipeline.pipeline_id:
                    raise ValueError(
                        f"asset {output} declares producer {declared!r}, "
                        f"registry has {pipeline.pipeline_id!r}"
                    )
        self.topological_pipelines()

    def topological_pipelines(self, selected: set[str] | None = None) -> list[str]:
        dependencies: dict[str, set[str]] = defaultdict(set)
        dependents: dict[str, set[str]] = defaultdict(set)
        for pipeline in self.pipelines.values():
            for asset_id in pipeline.inputs:
                producer = self.producers.get(asset_id)
                if producer and producer != pipeline.pipeline_id:
                    dependencies[pipeline.pipeline_id].add(producer)
                    dependents[producer].add(pipeline.pipeline_id)
            dependencies.setdefault(pipeline.pipeline_id, set())
        indegree = {name: len(parents) for name, parents in dependencies.items()}
        queue = deque(sorted(name for name, degree in indegree.items() if degree == 0))
        ordered = []
        while queue:
            name = queue.popleft()
            ordered.append(name)
            for child in sorted(dependents[name]):
                indegree[child] -= 1
                if indegree[child] == 0:
                    queue.append(child)
        if len(ordered) != len(dependencies):
            cycle = sorted(name for name, degree in indegree.items() if degree)
            raise ValueError(f"pipeline dependency cycle: {cycle}")
        if selected is None:
            return ordered
        required = set(selected)
        changed = True
        while changed:
            changed = False
            for pipeline_id in tuple(required):
                for parent in dependencies[pipeline_id]:
                    if parent not in required:
                        required.add(parent)
                        changed = True
        return [name for name in ordered if name in required]

    def graph_edges(self) -> list[tuple[str, str, str]]:
        edges = []
        for pipeline in self.pipelines.values():
            for asset_id in pipeline.inputs:
                producer = self.producers.get(asset_id)
                if producer:
                    edges.append((producer, pipeline.pipeline_id, asset_id))
        return sorted(edges)


registry = AssetRegistry()
