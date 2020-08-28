import pytest

from entitykb.fuzzy import FuzzyIndex, FuzzyResolver
from entitykb.model import Entity
from entitykb.pipeline import (
    DefaultTokenizer,
    DefaultNormalizer,
    Pipeline,
    DefaultExtractor,
)


@pytest.fixture()
def resolver():
    tokenizer = DefaultTokenizer()
    normalizer = DefaultNormalizer()
    index = FuzzyIndex(normalizer=normalizer, tokenizer=tokenizer)
    resolver = FuzzyResolver(
        name="people",
        tokenizer=tokenizer,
        normalizer=normalizer,
        index=index,
        max_distance=1,
        max_token_entries=5,
    )

    return resolver


@pytest.fixture()
def index(resolver):
    return resolver.index


@pytest.fixture()
def pipeline(resolver, index):
    pipeline = Pipeline(
        extractor=DefaultExtractor(
            tokenizer=resolver.tokenizer, resolvers=(resolver,)
        ),
        filterers=(),
        tokenizer=resolver.tokenizer,
        normalizer=resolver.normalizer,
        index=index,
        resolvers=(resolver,),
    )
    return pipeline


@pytest.fixture()
def b_obama(index):
    entity = Entity(
        name="Barack Obama",
        label="PRESIDENT",
        synonyms=(
            "Obama, Barack H.",
            "Barack Hussein Obama",
            "President Obama",
        ),
    )
    index.add(entity)
    return entity


@pytest.fixture()
def m_obama(index):
    entity = Entity(
        name="Michelle Obama",
        label="FIRST_LADY",
        synonyms=(
            "Michelle Obama",
            "Obama, Michelle",
            "Michelle LaVaughn Robinson Obama",
        ),
    )
    index.add(entity)
    return entity


@pytest.fixture()
def michel_le(index):
    entity = Entity(
        name="Michel'le",
        label="SINGER",
        synonyms=("Michel'le Denise Toussaint",),
    )
    index.add(entity)
    return entity
