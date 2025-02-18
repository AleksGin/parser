from schemas import ParseInfoSchema
from models import SpimexTraidingResut


def pydantic_to_sqlalchemy(pydantic_obj: ParseInfoSchema) -> SpimexTraidingResut:
    return SpimexTraidingResut(**pydantic_obj.model_dump())

