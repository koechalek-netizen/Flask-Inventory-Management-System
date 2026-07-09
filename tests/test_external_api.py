from unittest.mock import patch, Mock
import external_api

@patch("external_api.requests.get")
def test_get_product_by_barcode_success(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "status": 1,
        "product": {"product_name": "Nutella", "brands": "Ferrero"}
    }
    mock_get.return_value = mock_response

    result = external_api.get_product_by_barcode("3017620422003")
    assert result["product_name"] == "Nutella"

@patch("external_api.requests.get")
def test_get_product_by_barcode_not_found(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"status": 0}
    mock_get.return_value = mock_response

    result = external_api.get_product_by_barcode("000000000000")
    assert result is None

@patch("external_api.requests.get")
def test_get_product_by_barcode_bad_status(mock_get):
    mock_response = Mock()
    mock_response.status_code = 403
    mock_get.return_value = mock_response

    result = external_api.get_product_by_barcode("123")
    assert result is None

@patch("external_api.requests.get")
def test_search_product_by_name_success(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "products": [{"product_name": "Nutella"}, {"product_name": "Nutella B-Ready"}]
    }
    mock_get.return_value = mock_response

    result = external_api.search_product_by_name("nutella")
    assert len(result) == 2
    assert result[0]["product_name"] == "Nutella"

@patch("external_api.requests.get")
def test_search_product_by_name_no_results(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"products": []}
    mock_get.return_value = mock_response

    result = external_api.search_product_by_name("xyzxyzxyz")
    assert result is None

@patch("external_api.requests.get")
def test_network_failure(mock_get):
    import requests
    mock_get.side_effect = requests.exceptions.RequestException("Network error")

    result = external_api.get_product_by_barcode("3017620422003")
    assert result is None