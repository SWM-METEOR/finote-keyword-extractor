from pydantic import BaseModel


class BodyRequest(BaseModel):
    bodyString: str
