from http import HTTPStatus

test_add_role_to_user = [
    (
        # query
        {
            "path_login": "/api/v1/auth/login",
            "data_login": {"login": "superadmin", "password": "secret"},
            "path_add_role_to_user": "/api/v1/user/role",
            "data_add_role_to_user": {
                "user_id": "c2b9c859-9803-4d60-9a06-956f33ffec47",
                "role_id": "34962672-0a64-4e36-b893-96899142c4d4",
            },
        },
        # expected_answer
        {"min_body_len": 3, "status": HTTPStatus.OK},
    ),
]


test_delete_role_from_user = [
    (
        # query
        {
            "path_login": "/api/v1/auth/login",
            "data_login": {"login": "superadmin", "password": "secret"},
            "path_delete_role_from_user": "/api/v1/user/role",
            "data_delete_role_from_user": {
                "user_id": "c2b9c859-9803-4d60-9a06-956f33ffec47",
                "role_id": "34962672-0a64-4e36-b893-96899142c4d8",
            },
        },
        # expected_answer
        {"max_body_len": 2, "status": HTTPStatus.OK},
    ),
]

test_check_permission = [
    (
        # query
        {
            "path_login": "/api/v1/auth/login",
            "data_login": {"login": "superadmin", "password": "secret"},
            "path_check_permission": "/api/v1/user/check-permission",
            "data_check_permission": ["superadmin"],
        },
        # expected_answer
        {"status": HTTPStatus.OK},
    ),
]


TEST_PARAMS_USER = {
    "test_add_role_to_user": {
        "keys": "query, expected_answer",
        "data": test_add_role_to_user,
    },
    "test_delete_role_from_user": {
        "keys": "query, expected_answer",
        "data": test_delete_role_from_user,
    },
    "test_check_permission": {
        "keys": "query, expected_answer",
        "data": test_check_permission,
    },
}
