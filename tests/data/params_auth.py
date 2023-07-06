from http import HTTPStatus

test_good_signup = [
    (
        # query
        {
            "path": "/api/v1/auth/signup",
            "data": {
                "login": "abc1",
                "password": "abc1",
                "first_name": "first",
                "last_name": "last",
            },
        },
        # expected_answer
        {"body": {"msg": "User abc1 create successful"}, "status": HTTPStatus.OK},
        # message
        {
            "body": "Signup user 'abc1' failed",
            "status": "Status of response is unsuccessful!",
        },
    ),
]

test_good_login = [
    (
        # query
        {
            "user_create": ["abc2", "abc2", "first", "last"],
            "path": "/api/v1/auth/login",
            "data": {"login": "abc2", "password": "abc2"},
        },
        # expected_answer
        {"status": HTTPStatus.OK},
        # message
        {"status": "Status of response is unsuccessful!"},
    ),
]

test_failed_login = [
    (
        # query
        {
            "user_create": ["abc3", "abc3", "first", "last"],
            "path": "/api/v1/auth/login",
            "data": {"login": "abc3", "password": "cba"},
        },
        # expected_answer
        {"status": HTTPStatus.UNAUTHORIZED},
        # message
        {"status": "Logged in with wrong password"},
    ),
    (
        # query
        {
            "user_create": ["abc4", "abc4", "first", "last"],
            "path": "/api/v1/auth/login",
            "data": {"login": "cba", "password": "abc4"},
        },
        # expected_answer
        {"status": HTTPStatus.UNAUTHORIZED},
        # message
        {"status": "Logged in with wrong login"},
    ),
]

test_good_refresh = [
    (
        # query
        {
            "user_create": ["abc6", "abc6", "first", "last"],
            "path_login": "/api/v1/auth/login",
            "path_refresh": "/api/v1/auth/refresh",
            "data": {"login": "abc6", "password": "abc6"},
        },
        # expected_answer
        {"status": HTTPStatus.OK},
        # message
        {"status_refresh": "Refresh is failed", "refresh": "Access_token not updated"},
    ),
]

test_failed_refresh = [
    (
        # query
        {
            "user_create": ["abc7", "abc7", "first", "last"],
            "path_refresh": "/api/v1/auth/refresh",
            "data": {"login": "abc7", "password": "abc7"},
        },
        # expected_answer
        {"status": HTTPStatus.UNAUTHORIZED},
        # message
        {"status_refresh": "Refresh without tokens"},
    ),
]

test_good_logout = [
    (
        # query
        {
            "user_create": ["abc8", "abc8", "first", "last"],
            "path_login": "/api/v1/auth/login",
            "path_logout": "/api/v1/auth/logout",
            "data": {"login": "abc8", "password": "abc8"},
        },
        # expected_answer
        {"status": HTTPStatus.OK, "body": {"msg": "logged out successful"}},
        # message
        {
            "status": "Logout is failed",
            "body": "Body request incorrect",
            "token": "Access tokens not clear after logout",
        },
    ),
]

test_good_change = [
    (
        # query
        {
            "user_create": ["abc9", "abc9", "first", "last"],
            "path_login": "/api/v1/auth/login",
            "path_change": "/api/v1/auth/change",
            "data_login": {"login": "abc9", "password": "abc9"},
            "data_change": {
                "old_password": "abc9",
                "new_login": "abc10",
                "new_password": "abc10",
            },
        },
        # expected_answer
        {
            "status": HTTPStatus.OK,
            "body": {"msg": "login and (or) password has been change"},
        },
        # message
        {
            "status": "Changes failed",
            "body": "Body request incorrect",
            "login": "Incorrect login after change",
            "password": "Incorrect password after change",
        },
    ),
]

test_good_history = [
    (
        # query
        {
            "user_create": ["abc11", "abc11", "first", "last"],
            "path_login": "/api/v1/auth/login",
            "data_login": {"login": "abc11", "password": "abc11"},
            "path_history": "/api/v1/auth/history",
        },
        # expected_answer
        {"status": HTTPStatus.OK, "len": 1},
        # message
        {"status_login": "Token not found", "len": "Number of records is not correct"},
    ),
]

TEST_PARAMS_AUTH = {
    "test_good_signup": {
        "keys": "query, expected_answer, message",
        "data": test_good_signup,
    },
    "test_good_login": {
        "keys": "query, expected_answer, message",
        "data": test_good_login,
    },
    "test_failed_login": {
        "keys": "query, expected_answer, message",
        "data": test_failed_login,
    },
    "test_good_refresh": {
        "keys": "query, expected_answer, message",
        "data": test_good_refresh,
    },
    "test_failed_refresh": {
        "keys": "query, expected_answer, message",
        "data": test_failed_refresh,
    },
    "test_good_logout": {
        "keys": "query, expected_answer, message",
        "data": test_good_logout,
    },
    "test_good_change": {
        "keys": "query, expected_answer, message",
        "data": test_good_change,
    },
    "test_good_history": {
        "keys": "query, expected_answer, message",
        "data": test_good_history,
    },
}
