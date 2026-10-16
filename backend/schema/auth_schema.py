from pydantic import BaseModel, EmailStr, Field


class UserRegister(BaseModel):
    email: EmailStr = Field(description="email of the user")
    password: str = Field(description="Un-hashed pasword of the user")
    username: str = Field(description="Username of the user")


class UserLogin(BaseModel):
    email: EmailStr | None = Field(default=None, description="User email address")
    username: str | None = Field(default=None, description="Username of the user")
    password: str = Field(description="Users un-hashed password")

    def __init__(self, **data):
        super().__init__(**data)
        if not (self.email or self.username):
            raise ValueError("Either email or username must be provided.")
