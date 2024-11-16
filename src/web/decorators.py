from fastapi import Request

from src.application.interfaces.usecase import UseCase
from src.web.http_helper import HttpHelper

class PermissionUseCaseDecorator(UseCase):
    def __init__(self, use_case: UseCase):
        self.use_case = use_case

    async def execute(self, *args, **kwargs):
        pass

class PermissionDecorator(PermissionUseCaseDecorator):

    def __init__(self, use_case: UseCase, permission_to: str = 'read'):
        super().__init__(use_case)
        self.permission_to = permission_to

    async def execute(self, *args, **kwargs):
        request: Request = kwargs.pop('request')

        state = request.state.__dict__['_state']
        permissions = state['permissions']

        print(self.permission_to)

        if self.permission_to not in permissions:
            return HttpHelper.forbidden(Exception(f'You do not have permission to {self.permission_to} this resource'))

        result = await self.use_case.execute(**kwargs)
        return result
