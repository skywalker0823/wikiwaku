# pytest test.py

# import json
# from fastapi.testclient import TestClient
# from ..main import app

# client = TestClient(app)

# def test_line_webhook():
#     payload = {
#         "events": [
#             {
#                 "type": "message",
#                 "message": {
#                     "text": "test"
#                 }

#     }
#         ]
#     }
#     response = client.post("/", json.dumps(payload))
#     assert response.status_code == 200
#     assert response.text == 'OK'