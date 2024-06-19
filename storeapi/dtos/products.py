
from pydantic import BaseModel, ConfigDict

class PricingDTO(BaseModel):
    amount: int
    currency: str

class AvailabilityDTO(BaseModel):
    quantity: int
    timestamp: str

class ProductDTO(BaseModel):
    id: int
    name: str
    description: str
    pricing: PricingDTO
    availability: AvailabilityDTO
    category: str
    
class resDTO(BaseModel):
    res: str
