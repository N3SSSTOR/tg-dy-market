import asyncio 
import uuid 
import time 

from AaioAsync import AaioAsync 

from config import AAIO_API_KEY, AAIO_SHOP_ID, AAIO_SECRET_KEY_1


async def test() -> None:
    aaio = AaioAsync(
        apikey=AAIO_API_KEY,
        shopid=AAIO_SHOP_ID,
        secretkey=AAIO_SECRET_KEY_1,
    )

    # order_id = str(uuid.uuid4())
    # pay_url = await aaio.generatepaymenturl(
    #     amount=50,
    #     order_id=order_id,
    #     desc="Оплата товара тест",
    # )

    # print(
    #     f"OrderID: {order_id}"
    #     f"\nPayment URL: {pay_url}"
    # )

    """
    {
        'id': 'cc96c8c3-aa6c-4d64-a8db-098a88dcbf66', 
        'order_id': '78e8b1c5-d89f-40ce-a6f7-0a0993913409', 
        'merchant_id': '57809dde-f705-4a9f-95c1-eb27299f17f9', 
        'merchant_domain': 't.me/dy_market_bot', 
        'method': '', 
        'amount': 50.0, 'currency': 'RUB', 
        'profit': None, 
        'commission': None, 
        'commission_client': None, 
        'commission_type': None, 
        'email': None, 
        'status': 'in_process', 
        'date': '2024-04-16 16:09:30', 
        'expired_date': '2024-04-16 22:09:30', 
        'complete_date': None, 
        'us_vars': []
    }
    """

    """
    {
        'id': 'cc96c8c3-aa6c-4d64-a8db-098a88dcbf66', 
        'order_id': '78e8b1c5-d89f-40ce-a6f7-0a0993913409', 
        'merchant_id': '57809dde-f705-4a9f-95c1-eb27299f17f9', 
        'merchant_domain': 't.me/dy_market_bot', 
        'method': 'cards_ru', 
        'amount': 50.0, 
        'currency': 'RUB', 
        'profit': 46.25, 
        'commission': 3.75, 
        'commission_client': 0.0, 
        'commission_type': '100:0', 
        'email': 'supermagicnestor@gmail.com', 
        'status': 'hold', 
        'date': '2024-04-16 16:09:30', 
        'expired_date': '2024-04-16 16:30:26', 
        'complete_date': '2024-04-16 16:21:59', 
        'us_vars': []
    }
    """

    order_id = "78e8b1c5-d89f-40ce-a6f7-0a0993913409"
    # https://aaio.so/merchant/pay?invoice_uid=cc96c8c3-aa6c-4d64-a8db-098a88dcbf66

    order = await aaio.getorderinfo(order_id)
    print(order.model_dump())


def main() -> None:
    asyncio.run(test())


if __name__ == "__main__":
    main()