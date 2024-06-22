import json


def get_privileges(role, relations):
    privileges = set()
    print("Role:", role)
    if 'union' in relations[role]:
        for item in relations[role]['union']:
            if 'this' in item:
                privileges.add(role)
            if 'computed_userset' in item:
                related_role = item['computed_userset']['relation']
                privileges.update(get_privileges(related_role, relations))
    else:
        privileges.add(role)
        return privileges

    return privileges


def get_all_roles_with_privileges(data):
    roles_with_privileges = {}
    relations = data['relations']
    for role in relations.keys():
        roles_with_privileges[role] = list(get_privileges(role, relations))
    return roles_with_privileges

