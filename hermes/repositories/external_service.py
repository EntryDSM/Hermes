from typing import Type


class GatewayConnection:
    pass


class ExternalService:
    def __init__(self, gateway_service: Type[GatewayConnection]):
        self.gateway_service = gateway_service

    @classmethod
    async def register_admin_to_gateway(cls, admin_id: str):
        pass

    @staticmethod
    async def delete_admin_from_gateway(admin_id: str):
        pass

    @staticmethod
    async def delete_tokens_from_gateway(consumer_id: str):
        pass

