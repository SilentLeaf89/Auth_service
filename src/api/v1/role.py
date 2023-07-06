from uuid import UUID

from fastapi import APIRouter, Depends

from schemas.role import RoleModel, RoleResponseModel, RoleUpdateModel, RoleDeleteMessage
from services.auth_service import AuthService, get_auth_service
from services.role_service import RoleService, get_role_service
from utils.responses import role_responses

router = APIRouter(tags=["Role"])


@router.post(
    "/",
    response_model=RoleResponseModel,
    responses={
        409: {
            "description": "Conflict",
            "content": {
                "application/json": {
                    "examples": {
                        "AlreadyExistError": {
                            "value": {
                                "detail": "Role `role_id` already exist."
                            }
                        },
                    }
                }
            },
        },
    },
)
async def add_new_role(
    role: RoleModel,
    role_service: RoleService = Depends(get_role_service),
    auth_service: AuthService = Depends(get_auth_service),
) -> RoleResponseModel:
    """
    Add a new role.

    This endpoint allows the addition of a new role based on the provided `RoleModel` data.

    Parameters:
    - `role`: An instance of `RoleModel` representing the role information to be added.
        - `name`: str name of the role. Unique value.
        - `access`: str of the access. Access value separated by comma.
    Returns:
    - A `RoleResponseModel` instance representing the newly created role.

    Raises:
    - `HTTPException(401)`: If unauthorized action.
    - `HTTPException(403)`: If don't have permission.
    - `HTTPException(422)`: If error validation in request parameters.
    - `HTTPException(409)`: If role already exist.
    - `HTTPException(500)`: If an internal server error occurs.
    """
    await auth_service.check_access(["role_manage"])
    return await role_service.add(role)


@router.get(
    "/", response_model=list[RoleResponseModel], responses={**role_responses}
)
async def get_all_roles(
    role_service: RoleService = Depends(get_role_service),
    auth_service: AuthService = Depends(get_auth_service),
) -> list[RoleResponseModel]:
    """
    Get all roles.

    This endpoint retrieves all available roles.

    Returns:
    - A list of `RoleResponseModel` instances representing all roles.

    Raises:
    - `HTTPException(401)`: If unauthorized action.
    - `HTTPException(403)`: If don't have permission.
    - `HTTPException(404)`: If no one roles.
    - `HTTPException(500)`: If an internal server error occurs.
    """
    await auth_service.check_access(["role_manage"])
    return await role_service.get_all()


@router.get(
    "/{role_id}",
    response_model=RoleResponseModel,
    responses={
        **role_responses,
    },
)
async def get_role_by_id(
    role_id: UUID,
    role_service: RoleService = Depends(get_role_service),
    auth_service: AuthService = Depends(get_auth_service),
) -> RoleResponseModel:
    """
    Get role by ID.

    This endpoint retrieves a role by its unique identifier (`role_id`).

    Parameters:
    - `role_id`: The UUID of the role.

    Returns:
    - A `RoleResponseModel` instance representing the role with the specified ID.

    Raises:
    - `HTTPException(401)`: If unauthorized action.
    - `HTTPException(403)`: If don't have permission.
    - `HTTPException(404)`: If the role does not exist.
    - `HTTPException(422)`: If uuid is not valid.
    - `HTTPException(500)`: If an internal server error occurs.
    """
    await auth_service.check_access(["role_manage"])
    return await role_service.get(role_id)


@router.delete("/{role_id}", responses={**role_responses})
async def delete_role_by_id(
    role_id: UUID,
    role_service: RoleService = Depends(get_role_service),
    auth_service: AuthService = Depends(get_auth_service),
) -> RoleDeleteMessage:
    """
    Delete role by ID.

    This endpoint deletes a role by its unique identifier (`role_id`).

    Parameters:
    - `role_id`: The UUID of the role to be deleted.

    Returns:
    - A string message indicating the success of the deletion.

    Raises:
    - `HTTPException(401)`: If unauthorized action.
    - `HTTPException(403)`: If don't have permission.
    - `HTTPException(404)`: If the role does not exist.
    - `HTTPException(422)`: If error validation in request parameters.
    - `HTTPException(500)`: If an internal server error occurs.
    """
    await auth_service.check_access(["role_manage"])
    return await role_service.delete(role_id)


@router.put(
    "/{role_id}",
    response_model=RoleResponseModel,
    responses={**role_responses},
)
async def update_role_by_id(
    role_id: UUID,
    role: RoleUpdateModel,
    role_service: RoleService = Depends(get_role_service),
    auth_service: AuthService = Depends(get_auth_service),
) -> RoleResponseModel:
    """
    Update role by ID.

    This endpoint updates a role with the specified unique identifier (`role_id`) based on the provided `RoleUpdateModel` data.

    Parameters:
    - `role_id`: The UUID of the role to be updated.
    - `role`: An instance of `RoleUpdateModel` representing the updated role information.
        - `name`: str name of the role. Unique value.
        - `access`: str of the access. Access value separated by comma.

    Returns:
    - A `RoleResponseModel` instance representing the updated role.

    Raises:
    - `HTTPException(401)`: If unauthorized action.
    - `HTTPException(403)`: If don't have permission.
    - `HTTPException(404)`: If the role does not exist.
    - `HTTPException(422)`: If error validation in request parameters.
    - `HTTPException(500)`: If an internal server error occurs.
    """
    await auth_service.check_access(["role_manage"])
    return await role_service.update(role_id, role)
