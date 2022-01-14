import pydantic
from datetime import datetime

    
class ReceivedEventModel(pydantic.BaseModel):
    message_id: int
    date_received: datetime = datetime.now()
    domain: str