import os
import time
from entitykb.kb.storage import DefaultStorage


def test_backup_dirs(root_dir):
    expected = os.path.join(root_dir, "backups")
    assert os.path.exists(expected) is False

    storage = DefaultStorage(root_dir=root_dir)
    assert expected == storage.backup_dir
    assert os.path.exists(expected)


def test_info(root_dir):
    storage = DefaultStorage(root_dir=root_dir)
    info = storage.info()
    assert {"path", "disk_space", "last_commit"} == info.keys()
    assert os.path.join(root_dir, "index.db") == storage.index_path
    assert os.path.join(root_dir, "index.db") == info["path"]


def test_save_load(root_dir):
    storage = DefaultStorage(root_dir=root_dir)
    assert storage.exists is False

    # good save
    storage.save("test")
    assert "test" == storage.load()

    # bad pickle save
    file_obj = open(storage.index_path, mode="w+b")
    file_obj.write(b"back-pickle")
    file_obj.close()

    assert storage.load() is None


def test_archive_clean_backups(root_dir):
    storage = DefaultStorage(root_dir=root_dir)
    assert 5 == storage.max_backups

    for i in range(storage.max_backups + 5):
        paths = os.listdir(storage.backup_dir)
        assert min(i, storage.max_backups) == len(paths), f"What? {paths} {i}"

        assert storage.exists is False
        storage.save(i)

        assert storage.exists is True
        assert i == storage.load()

        storage.archive()
        time.sleep(0.0001)

    assert storage.max_backups == len(os.listdir(storage.backup_dir))


def test_sizeof(root_dir):
    assert DefaultStorage.sizeof({}) == "248.00 B"
    assert DefaultStorage.sizeof("abc") == "52.00 B"
    assert DefaultStorage.sizeof("a" * 1000) == "1.02 KiB"

    storage = DefaultStorage(root_dir=root_dir)
    storage.save("abc")
    assert DefaultStorage.sizeof(storage.index_path) == "13.00 B"