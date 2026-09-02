from __future__ import annotations

import pytest

from strongtowns_data.pipelines.http import download_file


class Response:
    def __init__(self, content: bytes, declared_size: int | None = None):
        self.content = content
        self.headers = {
            "etag": '"version"',
            "content-length": str(len(content) if declared_size is None else declared_size),
        }

    def raise_for_status(self):
        return None

    def iter_content(self, chunk_size):
        yield self.content[:2]
        yield self.content[2:]


class Session:
    def __init__(self, response):
        self.response = response

    def get(self, url, **kwargs):
        return self.response


def test_download_hashes_and_atomically_writes(tmp_path):
    result = download_file(
        "https://example.test/data", tmp_path / "raw.csv",
        session=Session(Response(b"abc")),
    )
    assert result.sha256 == "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
    assert result.path.read_bytes() == b"abc"
    assert result.etag == '"version"'


def test_download_rejects_truncated_response(tmp_path):
    with pytest.raises(ValueError, match="size mismatch"):
        download_file(
            "https://example.test/data", tmp_path / "raw.csv",
            session=Session(Response(b"abc", declared_size=4)),
        )
    assert not (tmp_path / "raw.csv").exists()
