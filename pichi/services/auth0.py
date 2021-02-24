from auth0.v3.authentication import GetToken
from auth0.v3.management import Auth0
from cachetools import cached, TTLCache
from fastapi import HTTPException, status
from jose import jwt
from pichi.models.auth0 import Claims, UsersSummary, UserProfile, UserAppMetadata
from pichi.core.config import (
    AUTH0_DOMAIN,
    AUTH0_API_ID,
    AUTH0_CLIENT_ID,
    AUTH0_CLIENT_SECRET,
)
from pydantic.error_wrappers import ValidationError
from typing import List
import requests


ALGORITHMS = ["RS256"]
SEARCH_TERM_SEPARATOR = " "
SEARCH_TERM_MIN_LENGTH = 1


def get_auth0_client() -> Auth0:
    token = GetToken(AUTH0_DOMAIN).client_credentials(
        AUTH0_CLIENT_ID,
        str(AUTH0_CLIENT_SECRET),
        f"https://{AUTH0_DOMAIN}/api/v2/",
    )
    mgmt_api_token = token["access_token"]
    return Auth0(AUTH0_DOMAIN, mgmt_api_token)


@cached(cache=TTLCache(maxsize=1, ttl=30))
def get_jwks():
    return requests.get("https://" + AUTH0_DOMAIN + "/.well-known/jwks.json").json()


def auth0_connection(customer_acronym: str) -> str:
    return f"{customer_acronym}-auth0"


def escape_lucene(term: str) -> str:
    i = len(term)
    escaped = [None] * i
    while i > 0:
        i -= 1
        c = term[i]
        if (
            c == "+"
            or c == "-"
            or c == "&"
            or c == "|"
            or c == "!"
            or c == "("
            or c == ")"
            or c == "{"
            or c == "}"
            or c == "["
            or c == "]"
            or c == "^"
            or c == '"'
            or c == "~"
            or c == "*"
            or c == "?"
            or c == ":"
            or c == "/"
            or c == "\\"
        ):
            escaped[i] = "\\" + c
        else:
            escaped[i] = c

    return "".join(escaped)


def parse_search_terms(terms: str) -> List[str]:
    if terms:
        return [
            t
            for t in list(map(escape_lucene, terms.split(SEARCH_TERM_SEPARATOR)))
            if len(t) >= SEARCH_TERM_MIN_LENGTH
        ]

    return []


def inner_search_query(terms: List[str]) -> str:
    return " AND ".join(
        list(
            map(lambda t: f"(given_name:{t}* OR family_name:{t}* OR email:{t}*)", terms)
        )
    )


def outer_search_query(inner: str) -> str:
    if inner:
        return f" AND ({inner})"

    return ""


def search_query(terms: List[str]) -> str:
    return outer_search_query(inner_search_query(parse_search_terms(terms)))


class Auth0Service:
    _client: Auth0

    def __init__(self):
        self._client = get_auth0_client()

    def verify_token(self, token: str):
        jwks = get_jwks()
        try:
            unverified_header = jwt.get_unverified_header(token)
        except jwt.JWTError as jwt_error:
            raise HTTPException(
                401, "Use an RS256 signed JWT Access Token"
            ) from jwt_error

        if unverified_header["alg"] == "HS256":
            raise HTTPException(401, "Use an RS256 signed JWT Access Token")

        rsa_key = {}
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"],
                }
        if rsa_key:
            try:
                jwt.decode(
                    token,
                    rsa_key,
                    algorithms=ALGORITHMS,
                    audience=AUTH0_API_ID,
                    issuer="https://" + AUTH0_DOMAIN + "/",
                )
            except jwt.ExpiredSignatureError as jwt_expired_sig:
                raise HTTPException(
                    status.HTTP_401_UNAUTHORIZED, "token is expired"
                ) from jwt_expired_sig

            except jwt.JWTClaimsError as jwt_claims:
                raise HTTPException(
                    status.HTTP_401_UNAUTHORIZED,
                    "incorrect claims, please check the audience and issuer",
                ) from jwt_claims

            except Exception as general_error:
                raise HTTPException(
                    status.HTTP_401_UNAUTHORIZED,
                    "Unable to parse authentication token",
                ) from general_error

    def parse_claims(self, token: str) -> Claims:
        try:
            self.verify_token(token)
            user_info = Claims.parse_obj(jwt.get_unverified_claims(token))
        except ValidationError as claims_validation:
            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED, "Unable to parse claims"
            ) from claims_validation

        return user_info

    def user_app_metadata(self, user_id: str) -> UserAppMetadata:
        user = self._client.users.get(user_id, fields=["app_metadata"])
        return UserAppMetadata.parse_obj(user["app_metadata"])

    def users(
        self, customer_acronym: str, page: int, per_page: int, search: str
    ) -> UsersSummary:
        result = self._client.users.list(
            q=f'NOT app_metadata.status:"deleted"{search_query(search)}',
            connection=auth0_connection(customer_acronym),
            fields=["user_id", "given_name", "family_name", "email"],
            sort="email:1",
            page=page,
            per_page=per_page,
            include_totals=True,
            search_engine="v3",
        )

        return UsersSummary.parse_obj(result)

    def user_profile(self, user_id: str, customer_acronym: str) -> UserProfile:
        result = self._client.users.get(user_id)
        return UserProfile.parse_obj(result)

    def register_user(self, customer_acronym: str):
        self._client.users.create(
            {
                "connection": auth0_connection(customer_acronym),
                "given_name": "",
                "family_name": "",
                "email": "",
                "username": "",
                "password": "",
                "email_verified": False,
                "app_metadata": {},
            }
        )
