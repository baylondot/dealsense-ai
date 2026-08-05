from pydantic import BaseModel


class Evidence(BaseModel):
    title: str

    quote: str

    source: str