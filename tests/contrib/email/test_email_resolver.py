from entitykb.contrib.email import EmailResolver, Email

resolver = EmailResolver()


def test_is_relevant():
    assert EmailResolver.is_relevant(None)
    assert EmailResolver.is_relevant([])
    assert EmailResolver.is_relevant(["DATE", "EMAIL"])
    assert not EmailResolver.is_relevant(["DATE"])


def test_is_prefix():
    assert resolver.is_prefix("first")
    assert resolver.is_prefix("first.")
    assert resolver.is_prefix("first.last")
    assert resolver.is_prefix("first.last@")
    assert resolver.is_prefix("first.last@domain")
    assert resolver.is_prefix("first.last@domain.")
    assert resolver.is_prefix("first.last@domain.com")
    assert resolver.is_prefix("first.last@sub.domain.com")


def test_is_not_prefix():
    assert not resolver.is_prefix("@")
    assert not resolver.is_prefix(" ")
    assert not resolver.is_prefix("word ")
    assert not resolver.is_prefix("word@ ")
    assert not resolver.is_prefix("word@domain ")


def test_resolve():
    entities = resolver.resolve("username@gmail.com")
    assert 1 == len(entities)

    entity = entities[0]
    assert isinstance(entity, Email)
    assert "EMAIL" == entity.label
    assert "username" == entity.username
    assert "gmail.com" == entity.domain
