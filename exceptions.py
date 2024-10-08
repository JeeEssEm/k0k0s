from starlette import status
from fastapi import HTTPException

CategoryNotFound = HTTPException(status.HTTP_404_NOT_FOUND,
                                 'Category not found')
ItemNotFound = HTTPException(status.HTTP_404_NOT_FOUND,
                             'Item not found')
OrderNotFound = HTTPException(status.HTTP_404_NOT_FOUND,
                              'Order not found')
