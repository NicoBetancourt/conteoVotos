import json
from domain.info.interface_adapters.repositories.info_repository import InfoRepository
from domain.info.entreprise_bussines.entities.info_dom import Info_dom, MakeInfo

class CreateLink:

    def __init__(self, info_repo:InfoRepository):
            self._info_repo: InfoRepository = info_repo

    def execute(self, infoLink):
        make_info = MakeInfo()
        # entity = make_info.execute(Info_dom(infoLink))
        data_dict = json.loads(json.dumps(infoLink))
        info_dom_object = Info_dom(**data_dict)
        # entity = Info_dom(*infoLink)
        result = self._info_repo.create(info_dom_object)
        return result
