from pydantic import BaseModel

# Modelos para Role
class RoleBase(BaseModel):
    name: str
    description: str | None = None

class RoleCreate(RoleBase):
    pass

class Role(RoleBase):
    id: int

    class Config:
        from_attributes = True  # Para Pydantic v2

# Modelos para User
class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str
    role_id: int

class User(UserBase):
    id: int
    role: Role

    class Config:
        from_attributes = True  # Para Pydantic v2
