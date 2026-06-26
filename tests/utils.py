from pydantic import BaseModel

def prettier(model: BaseModel):
    print(model.model_dump_json(indent=2))