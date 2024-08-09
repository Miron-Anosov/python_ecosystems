import pytest

from flask.testing import FlaskClient
from flask import Response


class TestGetAllClients:
    @pytest.fixture(scope="class")
    def all_clients_data(self, get_all_client_response) -> list:
        return get_all_client_response.get_json()

    def test_get_all_clients_status_200(self, get_all_client_response) -> None:
        assert (
            get_all_client_response.status_code == 200
        ), "Expected status code to be 200"

    def test_get_all_clients_type_response(self, all_clients_data: list) -> None:
        assert isinstance(all_clients_data, list), "Expected response data to be a list"
        assert len(all_clients_data) == 1, "Expected response list to not be empty"

    def test_get_all_clients_response_has_correct_key(
        self, all_clients_data: list
    ) -> None:

        assert (
            "clients" in all_clients_data[0]
        ), "Expected each item to have key 'clients'"

    def test_get_all_clients_responses_key_has_list(
        self, all_clients_data: list
    ) -> None:
        assert isinstance(
            all_clients_data[0]["clients"], list
        ), "Expected 'clients' key to contain a list"

    def test_get_client_by_id_not_found(
        self, get_client_by_id_response: Response
    ) -> None:
        data = get_client_by_id_response.get_json()
        assert data is None
        assert get_client_by_id_response.status_code == 404

    def test_get_client_by_id_error_request(
        self, client_scope_only_func: FlaskClient
    ) -> None:
        response = client_scope_only_func.get("/clients/1.1")
        assert response.get_json() is None
        assert response.status_code == 404

    def test_post_client_response_error(self, client: FlaskClient) -> None:
        response = client.post("/clients")
        assert response.status_code == 500

    def test_post_client_parking_response_error_content_type(
        self, client: FlaskClient
    ) -> None:
        response = client.post("/client_parkings")
        assert response.status_code == 415

    def test_post_client_parking_response_error_400(self, client: FlaskClient) -> None:
        headers = {"Content-Type": "application/json"}
        response = client.post("/client_parkings", headers=headers)
        assert response.status_code == 400

    def test_post_client_parking_response_error_500(self, client: FlaskClient) -> None:
        headers = {"Content-Type": "application/json"}
        params = {"invalid params": None}
        response = client.post("/client_parkings", headers=headers, json=params)
        assert response.status_code == 422
