from typing import Dict


class Room:
    def __init__(self, room_id: int | None, floor: int, guest_num: int, beds: int, price: int):
        self.roomId = room_id if room_id else None
        self.floor = floor
        self.guest_num = guest_num
        self.beds = beds
        self.price = price

    def return_data(self) -> Dict:
        return {
            "roomId": self.roomId,
            "floor": self.floor,
            "guestNum": self.guest_num,
            "beds": self.beds,
            "price": self.price
        }
