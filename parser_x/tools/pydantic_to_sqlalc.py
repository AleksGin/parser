from schemas import ParseInfoSchema
from models import SpimexTradingResut


def pydantic_to_sqlalchemy(pydantic_obj: ParseInfoSchema) -> SpimexTradingResut:
    return SpimexTradingResut(**pydantic_obj.model_dump())

