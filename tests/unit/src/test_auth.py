import pytest
from passlib.context import CryptContext

from tests.data.params_auth import TEST_PARAMS_AUTH


@pytest.mark.parametrize(
    TEST_PARAMS_AUTH["test_good_signup"]["keys"],
    TEST_PARAMS_AUTH["test_good_signup"]["data"],
)
async def test_good_signup(make_post_request, query, expected_answer, message):
    # Request data
    body, status, _ = await make_post_request(
        path=query["path"], query_data=query["data"]
    )
    # Check the response
    assert status == expected_answer["status"], message["status"]
    assert body == expected_answer["body"], message["body"]
    # await delete_users()


@pytest.mark.parametrize(
    TEST_PARAMS_AUTH["test_good_login"]["keys"],
    TEST_PARAMS_AUTH["test_good_login"]["data"],
)
async def test_good_login(
    make_post_request,
    signup_user,
    delete_users,
    query,
    expected_answer,
    message,
):
    await signup_user(*query["user_create"])
    # Request data
    _, status, _ = await make_post_request(path=query["path"], query_data=query["data"])
    # Check the response
    assert status == expected_answer["status"], message["status"]
    # await delete_users()


@pytest.mark.parametrize(
    TEST_PARAMS_AUTH["test_failed_login"]["keys"],
    TEST_PARAMS_AUTH["test_failed_login"]["data"],
)
async def test_failed_login(
    make_post_request,
    signup_user,
    delete_users,
    query,
    expected_answer,
    message,
):
    await signup_user(*query["user_create"])
    # Request data
    _, status, _ = await make_post_request(path=query["path"], query_data=query["data"])
    # Check the response
    assert status == expected_answer["status"], message["status"]
    # await delete_users()


@pytest.mark.parametrize(
    TEST_PARAMS_AUTH["test_good_refresh"]["keys"],
    TEST_PARAMS_AUTH["test_good_refresh"]["data"],
)
async def test_good_refresh(
    make_post_request,
    signup_user,
    query,
    expected_answer,
    message,
):
    # add user in db
    await signup_user(*query["user_create"])

    # Request login
    body_login, status, cookies_login = await make_post_request(
        path=query["path_login"], query_data=query["data"]
    )
    headers_login = {"Authorization": "Bearer {0}".format(body_login["access_token"])}

    # Request refresh
    body_refresh, status, _ = await make_post_request(
        path=query["path_refresh"],
        headers=headers_login,
        cookies=cookies_login,
    )

    assert status == expected_answer["status"], message["status_refresh"]
    assert body_login["access_token"] != body_refresh["access_token"], message[
        "refresh"
    ]

    # await delete_users()


@pytest.mark.parametrize(
    TEST_PARAMS_AUTH["test_failed_refresh"]["keys"],
    TEST_PARAMS_AUTH["test_failed_refresh"]["data"],
)
async def test_failed_refresh(
    make_post_request,
    signup_user,
    delete_users,
    query,
    expected_answer,
    message,
):
    # add user in db
    await signup_user(*query["user_create"])

    # without request /login

    # Request refresh
    _, status, _ = await make_post_request(
        path=query["path_refresh"],
        headers={},
        cookies={},
    )

    assert status == expected_answer["status"], message["status_refresh"]

    # await delete_users()


@pytest.mark.parametrize(
    TEST_PARAMS_AUTH["test_good_logout"]["keys"],
    TEST_PARAMS_AUTH["test_good_logout"]["data"],
)
async def test_good_logout(
    make_post_request,
    signup_user,
    delete_users,
    query,
    expected_answer,
    message,
):
    # add user in db
    await signup_user(*query["user_create"])

    # Request login
    body_login, status, cookies_login = await make_post_request(
        path=query["path_login"], query_data=query["data"]
    )
    headers_login = {"Authorization": "Bearer {0}".format(body_login["access_token"])}

    # Request logout
    body_logout, status, _ = await make_post_request(
        path=query["path_logout"],
        headers=headers_login,
        cookies=cookies_login,
    )

    assert status == expected_answer["status"], message["status"]
    assert body_logout == expected_answer["body"], message["body"]
    assert "access_token" not in body_logout, message["token"]

    # await delete_users()


@pytest.mark.parametrize(
    TEST_PARAMS_AUTH["test_good_change"]["keys"],
    TEST_PARAMS_AUTH["test_good_change"]["data"],
)
async def test_good_change(
    make_post_request,
    signup_user,
    delete_users,
    get_all_users,
    query,
    expected_answer,
    message,
):
    # add user in db
    await signup_user(*query["user_create"])

    # Request login
    body_login, status, cookies_login = await make_post_request(
        path=query["path_login"], query_data=query["data_login"]
    )
    headers_login = {"Authorization": "Bearer {0}".format(body_login["access_token"])}

    # Request change
    body_change, status, _ = await make_post_request(
        path=query["path_change"],
        query_data=query["data_change"],
        headers=headers_login,
        cookies=cookies_login,
    )

    assert status == expected_answer["status"], message["status"]
    assert body_change == expected_answer["body"], message["body"]


@pytest.mark.parametrize(
    TEST_PARAMS_AUTH["test_good_history"]["keys"],
    TEST_PARAMS_AUTH["test_good_history"]["data"],
)
async def test_good_history(
    make_post_request,
    signup_user,
    delete_users,
    query,
    expected_answer,
    message,
):
    # add user in db
    await signup_user(*query["user_create"])

    # Request login
    body_login, status, cookies_login = await make_post_request(
        path=query["path_login"], query_data=query["data_login"]
    )
    headers_login = {"Authorization": "Bearer {0}".format(body_login["access_token"])}

    # Request change
    body_history, status, _ = await make_post_request(
        path=query["path_history"],
        headers=headers_login,
        cookies=cookies_login,
    )

    assert status == expected_answer["status"], message["status"]
    assert len(body_history) == expected_answer["len"], message["len"]

    # await delete_users()
