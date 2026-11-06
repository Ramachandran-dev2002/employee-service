import json
from urllib.error import HTTPError
from urllib.request import Request, urlopen


class Response:
	def __init__(self, status_code, body):
		self.status_code = status_code
		self.body = body

	def json(self):
		return json.loads(self.body)

	def raise_for_status(self):
		if self.status_code >= 400:
			raise RuntimeError(f"HTTP error: {self.status_code}")


def request(method, url, json_body=None):
	data = None if json_body is None else json.dumps(json_body).encode("utf-8")
	headers = {"Content-Type": "application/json"} if data is not None else {}
	request = Request(url, data=data, headers=headers, method=method)
	try:
		with urlopen(request) as response:
			return Response(response.status, response.read().decode("utf-8"))
	except HTTPError as error:
		return Response(error.code, error.read().decode("utf-8"))


class requests:
	get = staticmethod(lambda url: request("GET", url))
	post = staticmethod(lambda url, json: request("POST", url, json))
	put = staticmethod(lambda url, json: request("PUT", url, json))
	patch = staticmethod(lambda url, json: request("PATCH", url, json))
	delete = staticmethod(lambda url: request("DELETE", url))


BASE_URL = "https://jsonplaceholder.typicode.com"


def explain_status(code):
	messages = {
		200: "OK",
		201: "Created",
		400: "Bad request",
		401: "Unauthorized",
		404: "Not found",
		500: "Internal server error",
	}
	return messages.get(code, "Unknown status")


def main():
	users_response = requests.get(f"{BASE_URL}/users")
	users_response.raise_for_status()
	for user in users_response.json()[:5]:
		print(f"{user['id']} - {user['name']} - {user['email']}")

	post_response = requests.post(
		f"{BASE_URL}/posts",
		json={"title": "Example", "body": "Example post", "userId": 1},
	)
	print(f"POST: {post_response.status_code}, id: {post_response.json()['id']}")

	put_response = requests.put(
		f"{BASE_URL}/posts/1",
		json={"id": 1, "title": "Updated", "body": "Updated post", "userId": 1},
	)
	patch_response = requests.patch(
		f"{BASE_URL}/posts/1", json={"title": "Patched"}
	)
	delete_response = requests.delete(f"{BASE_URL}/posts/1")
	print(
		f"PUT: {put_response.status_code} | PATCH: {patch_response.status_code} "
		f"| DELETE: {delete_response.status_code}"
	)

	missing_response = requests.get(f"{BASE_URL}/posts/9999")
	print(
		f"GET /posts/9999 -> {missing_response.status_code} "
		f"{explain_status(missing_response.status_code)}"
	)


if __name__ == "__main__":
	main()
