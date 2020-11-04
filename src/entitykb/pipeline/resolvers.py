from typing import Iterable, List

from entitykb import create_component, Entity

from .handlers import TokenHandler
from .normalizers import Normalizer
from .tokenizers import Tokenizer


class Resolver(object):
    def __init__(
        self, *, tokenizer: Tokenizer, normalizer: Normalizer, kb, **_,
    ):
        self.tokenizer = tokenizer
        self.normalizer = normalizer
        self.kb = kb

    def __repr__(self):
        return self.__class__.__name__

    @classmethod
    def get_handler_class(cls):
        return TokenHandler

    @classmethod
    def is_relevant(cls, labels: Iterable[str]):
        return True

    def resolve(self, term: str) -> List[Entity]:
        raise NotImplementedError

    def is_prefix(self, term: str) -> bool:
        raise NotImplementedError

    @classmethod
    def create(cls, value=None, **kwargs) -> "Resolver":
        return create_component(value, Resolver, TermResolver, **kwargs)


class TermResolver(Resolver):
    def resolve(self, term: str) -> List[Entity]:
        term_iter = self.kb.terms.iterate_term_keys(term=term)

        entities = []
        for key in term_iter:
            entity = self.kb.graph.get_node(key)
            entities.append(entity)

        return entities

    def is_prefix(self, term: str) -> bool:
        return self.kb.terms.is_prefix(term)
