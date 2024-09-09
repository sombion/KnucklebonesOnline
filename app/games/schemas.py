from pydantic import BaseModel


class SGame(BaseModel):
	id_pl1: int
	id_pl2: int