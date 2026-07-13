from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, ConfigDict

class ChatMessageCreate(BaseModel):

    #Payload sent by the client when creating a chat message.
    message: str

class ChatMessageResponse(BaseModel):

    #Response returned after a chat message is stored.
    id : UUID
    team_id: UUID
    sender_id: UUID
    sender_name: str
    message: str
    created_at: datetime 
    
    model_config = ConfigDict(
        from_attributes=True
    )

