from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from foundation import ADMIN_KEY
from admin.utils import verify_password
from data_base.orm_query import select_superuser


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]

        admin = await select_superuser(username=username)

        if not admin or not verify_password(password, admin.password):
            return False
                                       
        request.session.update({"token": "..."})

        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")

        if not token:
            return False

        return True

authentication_backend = AdminAuth(secret_key=ADMIN_KEY)
