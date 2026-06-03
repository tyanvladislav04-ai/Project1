import logging
import os

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))

logger = logging.getLogger("masks")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(os.path.join(ROOT_DIR, "logs/masks.log"), "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_mask_card_number(card_number: str) -> str:
    """Функция, которая принимает на вход номер карты и возвращает ее маску."""
    logger.info("Ввод номера карты клиента")
    if len(card_number) != 16 or card_number.isdigit() is False:
        logger.error("Введен некорректный номер карты")
        mask_card_number = "Введен некорректный номер карты"
    else:
        card_number_str = str(card_number)
        mask_card_number = f"{card_number_str[:4]} {card_number_str[4:6]}** **** {card_number_str[-4:]}"
        logger.info("Маска создана")
    return mask_card_number


def get_mask_account(account: str) -> str:
    """Функция, которая принимает на вход номер счета и возвращает его маску."""
    logger.info("Ввод номера счета клиента")
    if len(account) != 20 or not account.isdigit():
        logger.error("Введен некорректный номер счета")
        mask_account = "Введен некорректный номер счета"
    else:
        account_str = str(account)
        mask_account = f"**{account_str[-4:]}"
        logger.info("Маска создана")
    return mask_account
