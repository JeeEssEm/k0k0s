from fastapi import status
from fastapi import HTTPException

CategoryNotFound = HTTPException(status.HTTP_404_NOT_FOUND,
                                 'Category not found')

ItemNotFound = HTTPException(status.HTTP_404_NOT_FOUND, 'Item not found')
OrderNotFound = HTTPException(status.HTTP_404_NOT_FOUND, 'Order not found')
UserNotFound = HTTPException(status.HTTP_404_NOT_FOUND, 'User not found')
InvalidToken = HTTPException(status.HTTP_401_UNAUTHORIZED, 'Invalid token')
TokenExpired = HTTPException(status.HTTP_401_UNAUTHORIZED, 'Token expired')
IncorrectPassword = HTTPException(status.HTTP_401_UNAUTHORIZED,
                                  'Incorrect password')

UserAlreadyExists = HTTPException(status.HTTP_400_BAD_REQUEST,
                                  'User with such name or email already exists')

NotEnoughRights = HTTPException(status.HTTP_403_FORBIDDEN, 'Not enough rights')
NotAuthorized = HTTPException(status.HTTP_401_UNAUTHORIZED, 'not authorized')
