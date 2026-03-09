from dataclasses import dataclass

@dataclass
class SearchResult:
    title: str
    url: str

@dataclass
class Episode:
    number: int
    url: str