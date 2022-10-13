
# from domain.info.entreprise_bussines.entities.info_dom import Info_dom
# from frameworks.storage.client.interfaces.ioperations import psql_operations


# class build:
#     def execute(id: str, item: Info_dom):
#         try:
#             info = psql_driver.get_one(id)
#             print(info)
#             if info != None:
#                 return jsonify(info)
#             else:
#                 return jsonify({}), 404
#         except Exception as ex:
#             return jsonify({'message': str(ex)}), 500
