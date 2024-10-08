from fastapi import APIRouter


router = APIRouter(tags=['orders'], prefix='/orders')


@router.post('/')
async def create_order():
    pass


@router.get('/{order_id}')
async def get_order_by_id():
    pass


@router.patch('/{order_id}')
async def edit_order():
    pass


@router.delete('/{order_id}')
async def delete_order():
    pass


@router.get('/mine_orders')
async def get_mine_orders():
    pass


@router.post('/{order_id}/purchase')
async def purchase_order():
    pass
