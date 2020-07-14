from typing import Set
from . import (
    Query,
    QueryStart,
    QueryGoal,
    WalkStep,
    FilterStep,
    LabelFilter,
    RelationshipFilter,
    Filter,
)


class QueryBuilder(object):
    def __init__(self, *entities: str, iterables=None):
        start = QueryStart(entities=entities, iterables=iterables)
        self.query = Query(start=start)

    # steps (returns self)

    def walk(
        self,
        *tags: str,
        incoming: bool = True,
        max_hops: int = None,
        passthru: bool = False,
    ):
        walk = WalkStep(
            tags=tags, incoming=incoming, max_hops=max_hops, passthru=passthru,
        )
        self.query.steps.append(walk)
        return self

    def filter(
        self,
        filter: Filter = None,
        label: Set[str] = None,
        exclude: bool = False,
        **kwargs,
    ):
        filter_step = FilterStep(filters=[], exclude=exclude)

        if filter:
            filter_step.filters.append(filter)

        if label:
            label_filter = LabelFilter(label=label)
            filter_step.filters.append(label_filter)

        for tag, entity in kwargs.items():
            rel_filter = RelationshipFilter(tags={tag}, entities={entity})
            filter_step.filters.append(rel_filter)

        if filter_step:
            self.query.steps.append(filter_step)

        return self

    def exclude(self, **kwargs):
        self.filter(exclude=True, **kwargs)
        return self

    # goals (return query)

    def all(self):
        self.query.goal = QueryGoal()
        return self.query

    def limit(self, limit: int):
        self.query.goal = QueryGoal(limit=limit)
        return self.query

    def first(self):
        self.query.goal = QueryGoal(limit=1)
        return self.query


QB = QueryBuilder
