from domain.info.interface_adapters.repositories.info_repository import InfoRepository

class GetLinkById:

    def __init__(self, info_repo:InfoRepository):
            self._info_repo: InfoRepository = info_repo

    def execute(self, id: str):
        result = self._info_repo.get_one(id)
        return result
