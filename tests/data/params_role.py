from http import HTTPStatus

test_get_all_roles = [
    (
        # query
        {
            "path_login": "/api/v1/auth/login",
            "data_login": {"login": "superadmin", "password": "secret"},
            "path_all_roles": "/api/v1/role",
        },
        # expected_answer
        {"min_body_length": 1, "status": HTTPStatus.OK},
    ),
]

test_add_new_role = [
    (
        # query
        {
            "path_login": "/api/v1/auth/login",
            "data_login": {"login": "superadmin", "password": "secret"},
            "path_add_new_role": "/api/v1/role",
            "data_add_new_role": {"name": "new_role", "access": "some-access"},
        },
        # expected_answer
        {"body_num_keys": 4, "status": HTTPStatus.OK},
    ),
]

test_get_role_by_id = [
    (
        # query
        {
            "path_login": "/api/v1/auth/login",
            "data_login": {"login": "superadmin", "password": "secret"},
            "path_get_role_by_id": "/api/v1/role/34962672-0a64-4e36-b893-96899142c4d4",
        },
        # expected_answer
        {"body_num_keys": 4, "status": HTTPStatus.OK},
    ),
]

test_update_role_by_id = [
    (
        # query
        {
            "path_login": "/api/v1/auth/login",
            "data_login": {"login": "superadmin", "password": "secret"},
            "path_update_new_role": "/api/v1/role/34962672-0a64-4e36-b893-96899142c4d4",
            "data_update_new_role": {
                "name": "updated_role",
                "access": "updated-access",
            },
        },
        # expected_answer
        {"body_num_keys": 4, "status": HTTPStatus.OK},
    ),
]


test_delete_role_by_id = [
    (
        # query
        {
            "path_login": "/api/v1/auth/login",
            "data_login": {"login": "superadmin", "password": "secret"},
            "path_delete_role_by_id": "/api/v1/role/34962672-0a64-4e36-b893-96899142c4d5",
        },
        # expected_answer
        {
            "msg": "Role 34962672-0a64-4e36-b893-96899142c4d5 deleted successfully",
            "status": HTTPStatus.OK,
        },
    ),
]

TEST_PARAMS_ROLE = {
    "test_get_all_roles": {
        "keys": "query, expected_answer",
        "data": test_get_all_roles,
    },
    "test_add_new_role": {
        "keys": "query, expected_answer",
        "data": test_add_new_role,
    },
    "test_get_role_by_id": {
        "keys": "query, expected_answer",
        "data": test_get_role_by_id,
    },
    "test_update_role_by_id": {
        "keys": "query, expected_answer",
        "data": test_update_role_by_id,
    },
    "test_delete_role_by_id": {
        "keys": "query, expected_answer",
        "data": test_delete_role_by_id,
    },
}
