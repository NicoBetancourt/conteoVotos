# Repos
from domain.info.interface_adapters.repositories.info_repository import InfoRepository
from frameworks.storage.postgres.repositories.info_psql_repo import InfoPSQLRepository

# Uses Cases
from domain.info.app_bussines_rules.use_cases.get_one import GetLinkById
from domain.info.app_bussines_rules.use_cases.create_link import CreateLink
from domain.info.app_bussines_rules.use_cases.update_link import UpdateLink
from domain.info.app_bussines_rules.use_cases.get_links import GetLinks
from domain.info.app_bussines_rules.use_cases.delete_links import DeleteLinks
from domain.info.app_bussines_rules.use_cases.load_links import LoadLinks

# Repos
_info_repo = InfoRepository(InfoPSQLRepository())

# Services

# Use cases
create_link = CreateLink(_info_repo).execute
get_link = GetLinkById(_info_repo).execute
get_all_links = GetLinks(_info_repo).execute
delete_links = DeleteLinks(_info_repo).execute
update_link = UpdateLink(_info_repo).execute
load_links = LoadLinks(_info_repo).execute