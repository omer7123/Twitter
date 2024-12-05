from uuid import UUID

from schemas.Twit import CreateTwit, StatusResp
from utils.token_utils import check_token
from database.services.twit import twit_service_db

class TwitService:

    def create_twit(self, data: CreateTwit, token: str):
        token_data = check_token(token)

        return twit_service_db.create_twit(data, token_data["user_id"])


    def get_twits(self, token: str):
        data_token = check_token(token)
        return twit_service_db.get_all_twits(data_token['user_id'])

    def get_twit_by_id(self, access_token, id: UUID):
        data_token = check_token(access_token)
        return twit_service_db.get_twit_by_id(id, data_token['user_id'])

    def update_twit(self, id, data, access_token):
        data_token = check_token(access_token)
        return twit_service_db.update_twit(id, data, data_token['user_id'])

    def delete_twit(self, twit_id, access_token):
        data_token = check_token(access_token)
        if twit_service_db.delete_twit(twit_id, data_token['user_id']) == 0:
            return StatusResp(status=True)
        else:
            return StatusResp(status=False)

twit_service: TwitService = TwitService()

