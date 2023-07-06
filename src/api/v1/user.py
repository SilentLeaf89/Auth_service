from fastapi import APIRouter, Depends

from utils.responses import (
    user_responses,
    validation_example_response,
    access_responses,
)
from schemas.user import UserRoleAction
from schemas.role import RoleResponseModel
from services.auth_service import AuthService, get_auth_service
from services.role_service import RoleService, get_role_service

router = APIRouter(tags=["User"])


@router.post(
    "/role",
    response_model=list[RoleResponseModel],
    responses={
        **user_responses,
        **access_responses,
        422: {
            "description": "Error: Unprocessable Entity",
            "content": {
                "application/json": {
                    "examples": {
                        "UserRoleActionError": {
                            "value": {
                                "detail": "Failed add role to user. "
                                "Possible role has already been added."
                            }
                        },
                        "ValidationError": validation_example_response,
                    }
                }
            },
        },
    },
)
async def add_role_to_user(
    item: UserRoleAction,
    role_service: RoleService = Depends(get_role_service),
    auth_service: AuthService = Depends(get_auth_service),
) -> list[RoleResponseModel]:
    """Add a role to a user.

    Parameters:
    - `item`: An instance of `UserRoleAction` representing the role and user information.
        - `user_id`: UUID of the user.
        - `role_id`: UUID of the role.

    Returns:
    - A list of `RoleResponseModel` instances representing the updated roles assigned to the user.

    Raises:
    - `HTTPException(401)`: If unauthorized action.
    - `HTTPException(403)`: If don't have permission.
    - `HTTPException(404)`: If the user or role does not exist.
    - `HTTPException(422)`: Failed add role to user. A possible role has already been added.
    - `HTTPException(422)`: If error validation in request parameters.
    - `HTTPException(500)`: If an internal server error occurs.

    """
    await auth_service.check_access(["role_admin"])
    return await role_service.add_role_to_user(item)


@router.delete(
    "/role",
    response_model=list[RoleResponseModel],
    responses={
        **user_responses,
        **access_responses,
        422: {
            "description": "Error: Unprocessable Entity",
            "content": {
                "application/json": {
                    "examples": {
                        "RoleNotAssigned": {
                            "value": {
                                "detail": "Role `role_id` not assigned "
                                "to user `user_id`."
                            }
                        },
                        "UserRoleActionError": {
                            "value": {"detail": "Failed to remove role."}
                        },
                        "ValidationError": validation_example_response,
                    }
                }
            },
        },
    },
)
async def delete_role_from_user(
    item: UserRoleAction,
    role_service: RoleService = Depends(get_role_service),
    auth_service: AuthService = Depends(get_auth_service),
) -> list[RoleResponseModel]:
    """
    Delete a role from a user.

    This endpoint removes a role from a user, based on the provided `UserRoleAction` data.

    Parameters:
    - `item`: An instance of `UserRoleAction` representing the role and user information.
        - `user_id`: The unique identifier of the user.
        - `role_id`: The unique identifier of the role.

    Returns:
    - A list of `RoleResponseModel` instances representing the updated roles assigned to the user after the role deletion.

    Raises:
    - `HTTPException(401)`: If unauthorized action.
    - `HTTPException(403)`: If don't have permission.
    - `HTTPException(404)`: If the user or role does not exist.
    - `HTTPException(422)`: If role not assigned to user.
    - `HTTPException(422)`: If failed remove role from user.
    - `HTTPException(422)`: If error validation in request parameters.
    - `HTTPException(500)`: If an internal server error occurs.
    """
    await auth_service.check_access(["role_admin"])
    result = await role_service.delete_role_from_user(item)
    return result


@router.post(
    "/check-permission",
    responses={
        **access_responses,
    },
)
async def check_permission(
    access: list[str],
    auth_service: AuthService = Depends(get_auth_service),
) -> None:
    """
    Check permission.

    This endpoint checks if the user has the required access permissions.

    Parameters:
    - `access`: A list of strings representing the required access permissions.

    Returns:
    - None

    Raises:
    - `HTTPException(401)`: If unauthorized action.
    - `HTTPException(403)`: If don't have permission.
    - `HTTPException(500)`: If an internal server error occurs.
    """
    await auth_service.check_access(access)
    return
