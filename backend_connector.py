from pocketbase import PocketBase  # Client also works the same
from pocketbase.utils import ClientResponseError

from logzero import logger


async def save_data(agent: str, utter: str, conversation_id: str):
    pb = PocketBase("http://127.0.0.1:8090")

    auth_data = pb.admins.auth_with_password("admin@admin.de", "adminadmin")
    # after the above you can also access the auth data from the authStore
    # print(pb.auth_store.is_valid)
    # print(pb.auth_store.token)
    # print(pb.auth_store.model.id)

    # check if admin token is valid
    logger.debug(f"{auth_data.is_valid=}")
    logger.debug(f"{auth_data.token=}")

    data = {
        "dialogstep": 2,
        "agent": agent,
        "utter": utter,
        "date": "2022-01-01 10:00:00.123Z",
        "conversation_id": conversation_id,
    }

    record = pb.collection("conversations").create(data)
    logger.info(f"{record=}")
    # records = pb.collection("conversations").get_full_list()
    # print(records)

    # "logout" the last authenticated account
    pb.auth_store.clear()


async def is_conv_id_unique(conv_id: str) -> bool:
    pb = PocketBase("http://127.0.0.1:8090")

    auth_data = pb.admins.auth_with_password("admin@admin.de", "adminadmin")

    try:
        pb.collection("conversations").get_first_list_item(
            f'conversation_id="{conv_id}"'
        )
        pb.auth_store.clear()
        return False
    except ClientResponseError as e:
        logger.debug("conv_id is unique")
        pb.auth_store.clear()
        return True
