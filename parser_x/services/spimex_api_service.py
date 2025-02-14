from repos import DataBaseRepository


class SpimexApiService:
    def __init__(self, db_repo: DataBaseRepository) -> None:
        self.db_repo = db_repo

    
    