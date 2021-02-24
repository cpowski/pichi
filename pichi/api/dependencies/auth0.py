from fastapi import Depends
from fastapi.requests import Request
from fastapi.security import OAuth2PasswordBearer
from pichi.models.auth0 import Claims
from pichi.services.auth0 import Auth0Service


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="bearer")


def get_auth0_service(request: Request):
    return request.app.state.auth0_service


def get_current_user(
    auth0: Auth0Service = Depends(get_auth0_service),
    token: str = Depends(oauth2_scheme),
) -> Claims:
    """verify a token and extract the claims"""
    return auth0.parse_claims(token)
