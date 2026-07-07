from datetime import datetime
from pydantic import BaseModel

class SchemaCacheResponse(BaseModel):
    """
    Output serialization schema for returning cached database metadata layouts.
    Useful for populating the schema explorer tree.
    """
    id: int
    connection_id: int
    table_name: str
    column_name: str
    data_type: str
    created_at: datetime

    class Config:
        from_attributes = True
