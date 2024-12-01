from uuid import UUID

from schemas.Twit import CreateTwit
from utils.token_utils import check_token
from database.services.twit import twit_service_db

class TwitService:

    def create_twit(self, data: CreateTwit, token: str):
        token_data = check_token(token)

        return twit_service_db.create_twit(data, token_data["user_id"])


    def get_twits(self, token: str):
        check_token(token)
        return twit_service_db.get_all_twits()

    def get_twit_by_id(self, access_token, id: UUID):
        check_token(access_token)
        return twit_service_db.get_twit_by_id(id)

    def update_twit(self, id, data, access_token):
        data_token = check_token(access_token)
        print(data_token['user_id'])
        return twit_service_db.update_twit(id, data, data_token['user_id'])


twit_service: TwitService = TwitService()

