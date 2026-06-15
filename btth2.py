import logging

from pos_logic import (
    DRINK_MENU,
    add_to_order,
    calculate_total,
    ItemNotFoundError,
    InvalidQuantityError
)

logging.basicConfig(
    level=logging.INFO,
    format=(
        "%(asctime)s - "
        "%(levelname)s - "
        "%(message)s"
    )
)


def display_menu():
    """
    Display main menu.
    """

    print("\n========== HIGHLANDS MINI POS ==========")
    print("1. Xem thực đơn")
    print("2. Thêm món vào giỏ")
    print("3. Xem giỏ hàng & Tính tổng tiền")
    print("4. Thanh toán & Xóa giỏ hàng")
    print("5. Thoát ca làm việc")
    print("========================================")


def view_drink_menu():
    """
    Display menu.
    """

    print(
        "\n--- THỰC ĐƠN HIGHLANDS COFFEE ---"
    )

    for code, item in DRINK_MENU.items():
        print(
            f"[{code}] - "
            f"{item['name']} - "
            f"{item['price']:,} VNĐ"
        )


def view_order(current_order):
    """
    Display order.
    """

    if not current_order:
        print(
            "Giỏ hàng trống, "
            "vui lòng chọn món "
            "(Chức năng 2)."
        )
        return

    print(
        "\n--- GIỎ HÀNG HIỆN TẠI ---"
    )

    print(
        "Mã SP | Tên đồ uống"
        " | Đơn giá | "
        "Số lượng | Thành tiền"
    )

    print("-" * 70)

    for item in current_order:
        code = item["code"]
        quantity = item["quantity"]

        drink = DRINK_MENU[code]

        subtotal = (
            drink["price"] * quantity
        )

        print(
            f"{code:<5} | "
            f"{drink['name']:<18} | "
            f"{drink['price']:,} | "
            f"{quantity:<8} | "
            f"{subtotal:,} VNĐ"
        )

    print("-" * 70)

    total = calculate_total(
        current_order
    )

    print(
        f"Tổng tiền cần thanh toán: "
        f"{total:,} VNĐ"
    )


def checkout(current_order):
    """
    Checkout order.
    """

    if not current_order:
        print(
            "Giỏ hàng trống, "
            "vui lòng chọn món "
            "(Chức năng 2)."
        )
        return

    total = calculate_total(
        current_order
    )

    print("\n--- THANH TOÁN ---")

    print(
        f"Tổng tiền cần thanh toán: "
        f"{total:,} VNĐ"
    )

    confirm = input(
        f"Xác nhận thanh toán "
        f"{total:,} VNĐ? (y/n): "
    ).lower()

    if confirm == "y":
        logging.info(
            "Checkout successful"
        )

        current_order.clear()

        print(
            "Thanh toán thành công."
        )

        print(
            "Giỏ hàng đã được "
            "làm trống."
        )

    elif confirm == "n":
        print(
            "Đã hủy thao tác "
            "thanh toán."
        )

    else:
        print(
            "Lựa chọn không hợp lệ. "
            "Thanh toán đã bị hủy."
        )


def add_item_menu(current_order):
    """
    Add item workflow.
    """

    print(
        "\n--- THÊM MÓN VÀO GIỎ ---"
    )

    try:
        drink_code = input(
            "Nhập mã đồ uống: "
        )

        quantity = int(
            input("Nhập số lượng: ")
        )

        add_to_order(
            current_order,
            drink_code,
            quantity
        )

        code = (
            drink_code
            .strip()
            .upper()
        )

        print(
            f"Đã thêm {quantity} x "
            f"{DRINK_MENU[code]['name']} "
            f"vào giỏ hàng."
        )

    except ValueError:
        logging.error(
            "ValueError - "
            "Invalid quantity input"
        )

        print(
            "Vui lòng nhập số lượng "
            "là một số nguyên!"
        )

    except ItemNotFoundError as error:
        logging.warning(
            "ItemNotFoundError "
            "- Code: %s",
            error
        )

        print(
            "Mã đồ uống không hợp lệ, "
            "vui lòng kiểm tra lại "
            "thực đơn!"
        )

    except InvalidQuantityError as error:
        logging.warning(
            "InvalidQuantityError "
            "- Quantity: %s",
            error
        )

        print(
            "Số lượng phải lớn hơn 0!"
        )


def main():
    """
    Main program.
    """

    current_order = []

    while True:
        display_menu()

        choice = input(
            "Chọn chức năng (1-5): "
        )

        match choice:
            case "1":
                view_drink_menu()

            case "2":
                add_item_menu(
                    current_order
                )

            case "3":
                view_order(
                    current_order
                )

            case "4":
                checkout(
                    current_order
                )

            case "5":
                logging.info(
                    "Cashier logged out. "
                    "System shutdown."
                )

                print(
                    "Đã thoát ca làm việc. "
                    "Hẹn gặp lại!"
                )

                break

            case _:
                print(
                    "Lựa chọn không hợp lệ."
                )


if __name__ == "__main__":
    main()