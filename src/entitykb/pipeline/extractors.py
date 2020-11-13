from typing import List, Tuple, Iterable

from entitykb import Doc, DocToken, DocEntity, create_component

from .handlers import TokenHandler
from .resolvers import Resolver
from .tokenizers import Tokenizer

Labels = Iterable[str]


class Extractor(object):
    def __init__(
        self, tokenizer: Tokenizer, resolvers: Tuple[Resolver, ...],
    ):
        self.tokenizer = tokenizer
        self.resolvers = resolvers

    def __call__(self, text: str, labels: Labels = None) -> Doc:
        return self.extract_doc(text, labels)

    def extract_doc(self, text: str, labels: Labels = None) -> Doc:
        raise NotImplementedError

    @classmethod
    def create(cls, value=None, **kw):
        return create_component(value, Extractor, DefaultExtractor, **kw)


class DefaultExtractor(Extractor):
    def extract_doc(self, text: str, labels: Labels = None) -> Doc:
        doc = Doc(text=text)
        handlers = self.get_handlers(doc=doc, labels=labels)
        self.process_tokens(doc, handlers, text)
        self.process_entities(doc, handlers, labels)
        return doc

    def get_handlers(self, doc: Doc, labels: Labels) -> List[TokenHandler]:
        handlers: List[TokenHandler] = []
        for resolver in self.resolvers:
            if resolver.is_relevant(labels):
                handler_cls = resolver.get_handler_class()
                handlers.append(handler_cls(doc=doc, resolver=resolver))
        return handlers

    def process_tokens(self, doc, handlers, text):
        offset = 0
        doc_tokens = []
        iter_tokens = self.tokenizer.tokenize(text)
        for token in iter_tokens:
            doc_token = DocToken(doc=doc, token=token, offset=offset)
            doc_tokens.append(doc_token)

            for handler in handlers:
                handler.handle_token(doc_token)

            offset += 1

        doc.tokens = tuple(doc_tokens)
        return doc_tokens

    @classmethod
    def process_entities(cls, doc, handlers, labels):
        doc_entities: List[DocEntity] = []
        for handler in handlers:
            doc_entities += handler.finalize()
        if labels:
            doc_entities = (
                doc_ent for doc_ent in doc_entities if doc_ent.label in labels
            )
        doc.entities = tuple(doc_entities)
