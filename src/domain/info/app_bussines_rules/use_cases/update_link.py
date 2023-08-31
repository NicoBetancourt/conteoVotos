from domain.info.interface_adapters.repositories.info_repository import InfoRepository
from domain.info.entreprise_bussines.entities.info_dom import Info_dom


class UpdateLink:

    def __init__(self, info_repo:InfoRepository):
            self._info_repo: InfoRepository = info_repo

    def execute(self, infoLink, id):
        itemDom = Info_dom(infoLink)
        itemInfo = self._info_repo.get_one(id)
        updatedInfo = itemInfo.update_info(itemDom)
        self._info_repo.update(updatedInfo, id)
        return updatedInfo
