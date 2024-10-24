import random

import factory
from app.orm_models import Client, Parking, ClientParking  # noqa
from app.main import db  # noqa


class ClientFakeFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Client
        sqlalchemy_session = db.session

    name = factory.Faker("first_name", locale="en_US")
    surname = factory.Faker("last_name", locale="en_US")
    credit_card = factory.Maybe(
        factory.Faker("boolean", chance_of_getting_true=60),
        yes_declaration=factory.Faker("credit_card_number", locale="en_US"),
        no_declaration=None,
    )
    car_number = factory.Maybe(
        factory.Faker("boolean", chance_of_getting_true=90),
        yes_declaration=factory.Faker("license_plate", locale="en_US"),
        no_declaration=None,
    )


class ClientInvalidFakeFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Client
        sqlalchemy_session = db.session

    name = factory.Maybe(
        factory.Faker("boolean", chance_of_getting_true=0),
        yes_declaration=factory.Faker("first_name", locale="en_US"),
        no_declaration=None,
    )
    surname = factory.Maybe(
        factory.Faker("boolean", chance_of_getting_true=25),
        yes_declaration=factory.Faker("last_name", locale="en_US"),
        no_declaration=None,
    )
    credit_card = factory.Maybe(
        factory.Faker("boolean", chance_of_getting_true=55),
        yes_declaration=factory.Faker("credit_card_number", locale="en_US"),
        no_declaration=None,
    )
    car_number = factory.Maybe(
        factory.Faker("boolean", chance_of_getting_true=55),
        yes_declaration=factory.Faker("license_plate", locale="en_US"),
        no_declaration=None,
    )


class ParkingFakeFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Parking
        sqlalchemy_session = db.session

    address = factory.Faker("address", locale="en_US")
    opened = factory.Maybe(
        factory.Faker("boolean", chance_of_getting_true=50),
        yes_declaration=factory.Faker("boolean", chance_of_getting_true=70),
        no_declaration=None,
    )
    count_places = factory.Faker("random_number", digits=2)
    count_available_places = factory.LazyAttribute(
        lambda c: random.randrange(c.count_places)
    )


class ParkingInvalidFakeFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Parking
        sqlalchemy_session = db.session

    address = factory.Maybe(
        factory.Faker("boolean", chance_of_getting_true=0),
        yes_declaration=factory.Faker("address", locale="en_US"),
        no_declaration=None,
    )
    opened = factory.Maybe(
        factory.Faker("boolean", chance_of_getting_true=90),
        yes_declaration=factory.Faker("boolean", chance_of_getting_true=70),
        no_declaration=None,
    )
    count_places = factory.Maybe(
        factory.Faker("boolean", chance_of_getting_true=100),
        yes_declaration=factory.Faker("random_number", digits=2),
        no_declaration=None,
    )
    count_available_places = factory.LazyAttribute(
        lambda c: random.randrange(c.count_places)
    )


class ClientParkingFakeFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = ClientParking
        sqlalchemy_session = db.session

    client_id = factory.SubFactory(ClientFakeFactory)
    parking_id = factory.SubFactory(ParkingFakeFactory)
    time_in = factory.Faker(
        "date_time_between", start_date="-1d", end_date="now", tzinfo=None
    )
    time_out = factory.Maybe(
        factory.Faker("boolean", chance_of_getting_true=50),
        yes_declaration=factory.Faker(
            "date_time_between", start_date="now", end_date="+1d", tzinfo=None
        ),
        no_declaration=None,
    )
