from schemas.Twit import CreateTwit
from utils.token_utils import check_token
from database.services.twit import twit_service_db

class TwitService:

    def create_twit(self, data: CreateTwit, token: str):
        token_data = check_token(token)

        return twit_service_db.create_twit(data, token_data["user_id"])


    def get_twits(self, token: str):
        token_data = check_token(token)
        return twit_service_db.get_all_twits(token_data["user_id"])

twit_service: TwitService = TwitService()

