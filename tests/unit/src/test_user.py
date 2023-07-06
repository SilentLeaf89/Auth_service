import pytest

from tests.data.params_user import TEST_PARAMS_USER


@pytest.mark.parametrize(
    TEST_PARAMS_USER["test_add_role_to_user"]["keys"],
    TEST_PARAMS_USER["test_add_role_to_user"]["data"],
)
async def test_add_role_to_user(make_post_request, query, expected_answer):
    # Login as superuser
    body_login, _, cookies_login = await make_post_request(
        path=query["path_login"], query_data=query["data_login"]
    )
    headers_login = {"Authorization": "Bearer {0}".format(body_login["access_token"])}

    # Add role to user
    body_response, status_response, _ = await make_post_request(
        path=query["path_add_role_to_user"],
        query_data=query["data_add_role_to_user"],
        headers=headers_login,
        cookies=cookies_login,
    )

    assert status_response == expected_answer["status"]
    assert len(body_response) >= expected_answer["min_body_len"]


@pytest.mark.parametrize(
    TEST_PARAMS_USER["test_delete_role_from_user"]["keys"],
    TEST_PARAMS_USER["test_delete_role_from_user"]["data"],
)
async def test_delete_role_from_user(
    make_delete_request, make_post_request, query, expected_answer
):
    # Login as superuser
    body_login, _, cookies_login = await make_post_request(
        path=query["path_login"], query_data=query["data_login"]
    )
    headers_login = {"Authorization": "Bearer {0}".format(body_login["access_token"])}

    # Add role to user
    body_response, status_response, _ = await make_delete_request(
        path=query["path_delete_role_from_user"],
        query_data=query["data_delete_role_from_user"],
        headers=headers_login,
        cookies=cookies_login,
    )

    assert status_response == expected_answer["status"]
    assert len(body_response) <= expected_answer["max_body_len"]


@pytest.mark.parametrize(
    TEST_PARAMS_USER["test_check_permission"]["keys"],
    TEST_PARAMS_USER["test_check_permission"]["data"],
)
async def test_check_permission(make_post_request, query, expected_answer):
    # Login as superuser
    body_login, _, cookies_login = await make_post_request(
        path=query["path_login"], query_data=query["data_login"]
    )
    headers_login = {"Authorization": "Bearer {0}".format(body_login["access_token"])}

    # Add role to user
    _, status_response, _ = await make_post_request(
        path=query["path_check_permission"],
        query_data=query["data_check_permission"],
        headers=headers_login,
        cookies=cookies_login,
    )

    assert status_response == expected_answer["status"]
