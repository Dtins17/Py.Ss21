import logging
import re

logging.basicConfig(
    filename="momo_transactions.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

balance = 0


class InvalidAmountError(Exception):
    pass


class InsufficientBalanceError(Exception):
    pass


def deposit(amount):
    global balance

    if amount <= 0:
        raise InvalidAmountError(amount)

    balance += amount

    logging.info(
        "Deposit successful: +%s VND. Current Balance: %s",
        amount,
        balance
    )


def transfer(phone, amount):
    global balance

    if amount <= 0:
        raise InvalidAmountError(amount)

    if amount > balance:
        raise InsufficientBalanceError(amount)

    if amount >= 10000000:
        logging.warning(
            "High value transaction detected: %s VND to %s",
            amount,
            phone
        )

    balance -= amount

    logging.info(
        "Transfer successful: -%s VND to %s. Current Balance: %s",
        amount,
        phone,
        balance
    )


def get_balance():

    logging.info(
        "Balance checked. Current Balance: %s",
        balance
    )

    return balance


def validate_phone(phone):

    return bool(
        re.fullmatch(r"\d{10}", phone)
    )


def display_menu():

    print("\n========== VÍ MOMO GIẢ LẬP ==========")
    print("1. Nạp tiền vào ví")
    print("2. Chuyển tiền")
    print("3. Xem số dư hiện tại")
    print("4. Thoát chương trình")
    print("=====================================")


while True:

    display_menu()

    choice = input(
        "Chọn chức năng (1-4): "
    )

    if choice == "1":

        print("\n--- NẠP TIỀN VÀO VÍ ---")

        while True:

            try:

                amount = int(
                    input("Nhập số tiền cần nạp: ")
                )

                deposit(amount)

                print(
                    f"\nNạp tiền thành công: +{amount:,} VND"
                )

                print(
                    f"Số dư hiện tại: {balance:,} VND"
                )

                break

            except ValueError:

                logging.error(
                    "ValueError: Invalid numeric input for deposit."
                )

                print(
                    "Lỗi: Vui lòng nhập số tiền hợp lệ."
                )

            except InvalidAmountError as error:

                logging.error(
                    "InvalidAmountError: Attempted to process %s VND.",
                    error
                )

                print(
                    "Lỗi: Số tiền giao dịch phải lớn hơn 0."
                )

                break

    elif choice == "2":

        print("\n--- CHUYỂN TIỀN ---")

        phone = input(
            "Nhập số điện thoại người nhận: "
        )

        if not validate_phone(phone):

            print(
                "Số điện thoại không hợp lệ."
            )

            continue

        try:

            amount = int(
                input("Nhập số tiền cần chuyển: ")
            )

            transfer(phone, amount)

            print(
                f"\nChuyển tiền thành công tới số điện thoại {phone}."
            )

            print(
                f"Số tiền đã chuyển: {amount:,} VND"
            )

            print(
                f"Số dư còn lại: {balance:,} VND"
            )

        except ValueError:

            logging.error(
                "ValueError: Invalid numeric input for transfer."
            )

            print(
                "Lỗi: Vui lòng nhập số tiền hợp lệ."
            )

        except InvalidAmountError as error:

            logging.error(
                "InvalidAmountError: Attempted to process %s VND.",
                error
            )

            print(
                "Lỗi: Số tiền giao dịch phải lớn hơn 0."
            )

        except InsufficientBalanceError as error:

            logging.error(
                "InsufficientBalanceError: Attempted to transfer "
                "%s VND with balance %s VND.",
                error,
                balance
            )

            print(
                "Giao dịch thất bại: Số dư của bạn không đủ."
            )

            print(
                f"Số dư hiện tại: {balance:,} VND"
            )

    elif choice == "3":

        print("\n--- SỐ DƯ VÍ MOMO ---")

        print(
            f"Số dư hiện tại: {get_balance():,} VND"
        )

    elif choice == "4":

        logging.info(
            "System shutdown"
        )

        print(
            "Cảm ơn bạn đã sử dụng dịch vụ."
        )

        break

    else:

        print(
            "Lựa chọn không hợp lệ."
        )