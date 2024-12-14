import unittest
# Red Phase

class TestAdvancedPaymentOptions(unittest.TestCase):
    def test_split_payment(self):
        # 测试分账功能
        pass

    def test_gift_card_payment(self):
        # 测试礼品卡支付
        pass

# Green Phase
class PaymentProcessor1:
    def split_payment(self, total, split):
        # 简单分账逻辑
        return [total / split for _ in range(split)]

    def gift_card_payment(self, total, gift_card_balance):
        if total <= gift_card_balance:
            return gift_card_balance - total
        return "Insufficient balance"


# Refactor Phase
class PaymentProcessor2:
    def split_payment(self, total, split):
        if split <= 0:
            raise ValueError("Split must be greater than zero")
        share = total / split
        return [share] * split

    def gift_card_payment(self, total, gift_card_balance):
        if gift_card_balance < total:
            raise ValueError("Insufficient gift card balance")
        return gift_card_balance - total