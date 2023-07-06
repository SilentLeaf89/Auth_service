user_responses = {
    404: {
        "description": "Error: Not Found",
        "content": {
            "application/json": {
                "example": {"detail": "Role or user not found."}
            }
        },
    },
}

role_responses = {
    404: {
        "description": "Error: Not Found",
        "content": {
            "application/json": {"example": {"detail": "Role(s) not found."}}
        },
    },
}

validation_example_response = {
    "value": {
        "detail": [{"loc": ["string", 0], "msg": "string", "type": "string"}]
    }
}

access_responses = {
    401: {
        "description": "Unauthorized",
        "content": {
            "application/json": {"example": {"detail": "Unauthorized action."}}
        },
    },
    403: {
        "description": "Forbidden",
        "content": {
            "application/json": {
                "example": {"detail": "You don't have permission."}
            }
        },
    },
}
