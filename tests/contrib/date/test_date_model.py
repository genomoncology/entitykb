import datetime

from entitykb.contrib.date import Date
from entitykb import Node


def test_create_from_dict_via_label_to_date():
    entity = Node.create(dict(year=2000, month=1, day=2, label="DATE"))
    assert isinstance(entity, Date)
    assert entity.name == "2000-01-02"
    assert repr(entity) == "<Date: year=2000 month=1 day=2>"


def test_create_from_dict_via_cls():
    date = Date.create(dict(year=2000, month=1, day=2))
    assert date.year == 2000
    assert date.month == 1
    assert date.day == 2
    assert repr(date) == "<Date: year=2000 month=1 day=2>"


def test_init_date():
    date = Date(year=2001, month=2, day=3)
    assert date.name == "2001-02-03"
    assert date.as_date == datetime.date(2001, 2, 3)
    assert date.dict() == dict(
        name="2001-02-03",
        key="2001-02-03|DATE",
        year=2001,
        month=2,
        day=3,
        label="DATE",
        synonyms=(),
        data=None,
    )
