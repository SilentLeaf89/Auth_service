import pytest

from tests.data.params_role import TEST_PARAMS_ROLE


@pytest.mark.parametrize(
    TEST_PARAMS_ROLE["test_get_all_roles"]["keys"],
    TEST_PARAMS_ROLE["test_get_all_roles"]["data"],
)
async def test_get_all_roles(
    make_get_request, make_post_request, query, expected_answer
):
    # Login as superuser
    body_login, _, cookies_login = await make_post_request(
        path=query["path_login"], query_data=query["data_login"]
    )
    headers_login = {"Authorization": "Bearer {0}".format(body_login["access_token"])}

    # Request all roles
    body_response, status_response, _ = await make_get_request(
        path=query["path_all_roles"],
        headers=headers_login,
        cookies=cookies_login,
    )

    assert status_response == expected_answer["status"]
    assert len(body_response) >= expected_answer["min_body_length"]


@pytest.mark.parametrize(
    TEST_PARAMS_ROLE["test_add_new_role"]["keys"],
    TEST_PARAMS_ROLE["test_add_new_role"]["data"],
)
async def test_add_new_role(make_post_request, query, expected_answer):
    # Login as superuser
    body_login, _, cookies_login = await make_post_request(
        path=query["path_login"], query_data=query["data_login"]
    )
    headers_login = {"Authorization": "Bearer {0}".format(body_login["access_token"])}

    # Add new role
    body_response, status_response, _ = await make_post_request(
        path=query["path_add_new_role"],
        query_data=query["data_add_new_role"],
        headers=headers_login,
        cookies=cookies_login,
    )

    assert status_response == expected_answer["status"]
    assert len(body_response.keys()) == expected_answer["body_num_keys"]


@pytest.mark.parametrize(
    TEST_PARAMS_ROLE["test_get_role_by_id"]["keys"],
    TEST_PARAMS_ROLE["test_get_role_by_id"]["data"],
)
async def test_get_role_by_id(
    make_get_request, make_post_request, query, expected_answer
):
    # Login as superuser
    body_login, _, cookies_login = await make_post_request(
        path=query["path_login"], query_data=query["data_login"]
    )
    headers_login = {"Authorization": "Bearer {0}".format(body_login["access_token"])}

    # Request role by id
    body_response, status_response, _ = await make_get_request(
        path=query["path_get_role_by_id"],
        headers=headers_login,
        cookies=cookies_login,
    )

    assert status_response == expected_answer["status"]
    assert len(body_response.keys()) == expected_answer["body_num_keys"]


@pytest.mark.parametrize(
    TEST_PARAMS_ROLE["test_update_role_by_id"]["keys"],
    TEST_PARAMS_ROLE["test_update_role_by_id"]["data"],
)
async def test_update_role_by_id(
    make_put_request, make_post_request, query, expected_answer
):
    # Login as superuser
    body_login, _, cookies_login = await make_post_request(
        path=query["path_login"], query_data=query["data_login"]
    )
    headers_login = {"Authorization": "Bearer {0}".format(body_login["access_token"])}

    # Update role
    body_response, status_response, _ = await make_put_request(
        path=query["path_update_new_role"],
        query_data=query["data_update_new_role"],
        headers=headers_login,
        cookies=cookies_login,
    )

    assert status_response == expected_answer["status"]
    assert len(body_response.keys()) == expected_answer["body_num_keys"]


@pytest.mark.parametrize(
    TEST_PARAMS_ROLE["test_delete_role_by_id"]["keys"],
    TEST_PARAMS_ROLE["test_delete_role_by_id"]["data"],
)
async def test_delete_role_by_id(
    make_delete_request, make_post_request, query, expected_answer
):
    # Login as superuser
    body_login, _, cookies_login = await make_post_request(
        path=query["path_login"], query_data=query["data_login"]
    )
    headers_login = {"Authorization": "Bearer {0}".format(body_login["access_token"])}

    # Request role by id
    body_response, status_response, _ = await make_delete_request(
        path=query["path_delete_role_by_id"],
        headers=headers_login,
        cookies=cookies_login,
    )

    assert status_response == expected_answer["status"]
    assert body_response["msg"] == expected_answer["msg"]
