import re

from pydantic import BaseModel, field_validator

VALID_TOKEN_REGEX = re.compile(r"^[a-zA-Z0-9]{32}$")


class TokenValidation(BaseModel):
    token: str

    @field_validator("token")
    def validate_token(cls, t) -> str:
        """This function validates wether the api token complies with
        the token requirements."""
        if not VALID_TOKEN_REGEX.match(t):
            raise ValueError("Not a valid token ...")
        return t
