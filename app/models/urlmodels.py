from pydantic import BaseModel


class Item(BaseModel):
    urls_vid: list[str]
