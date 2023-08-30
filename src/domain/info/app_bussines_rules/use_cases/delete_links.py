from domain.info.interface_adapters.repositories.info_repository import InfoRepository

class DeleteLinks:

    def __init__(self, info_repo:InfoRepository):
            self._info_repo: InfoRepository = info_repo

    def execute(self, filters):
        result = self._info_repo.delete(filters)
        return result
