from domain.info.interface_adapters.repositories.info_repository import InfoRepository

class GetLinks:

    def __init__(self, info_repo:InfoRepository):
            self._info_repo: InfoRepository = info_repo

    def execute(self, filters):
        result = self._info_repo.get_all(filters)
        return result
