import os
from pathlib import Path

import requests
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"
GITIGNORE_FILE = BASE_DIR / ".gitignore"


def prepare_environment():
	# Create the requested demo .env without replacing an existing one.
	if not ENV_FILE.exists():
		ENV_FILE.write_text("API_KEY=demo-key-123\n", encoding="utf-8")

	# Keep the environment file out of Git.
	ignored_entries = (
		GITIGNORE_FILE.read_text(encoding="utf-8").splitlines()
		if GITIGNORE_FILE.exists()
		else []
	)
	if ".env" not in ignored_entries:
		with GITIGNORE_FILE.open("a", encoding="utf-8") as gitignore:
			if ignored_entries and not GITIGNORE_FILE.read_text(encoding="utf-8").endswith("\n"):
				gitignore.write("\n")
			gitignore.write(".env\n")

	load_dotenv(ENV_FILE)


def safe_get(url):
	"""GET a URL, retrying up to three times after a timeout."""
	for attempt in range(4):
		try:
			response = requests.get(url, timeout=5)
			response.raise_for_status()
			return response
		except requests.exceptions.Timeout:
			if attempt == 3:
				print("Request timed out after retries")
		except requests.exceptions.ConnectionError:
			print("Connection error; please try again")
			break
		except requests.exceptions.HTTPError as error:
			print(f"HTTP error: {error}")
			break
	return None


def main():
	prepare_environment()
	api_key = os.getenv("API_KEY")

	if api_key:
		try:
			response = requests.get(
				"https://httpbin.org/headers",
				headers={"X-API-Key": api_key},
				timeout=5,
			)
			response.raise_for_status()
			received_key = response.json().get("headers", {}).get("X-Api-Key")
			print(f"Server received key: {received_key}")
		except requests.exceptions.Timeout:
			print("Request timed out; please try again")
		except requests.exceptions.ConnectionError:
			print("Connection error; please try again")
		except requests.exceptions.HTTPError as error:
			print(f"HTTP error: {error}")

	try:
		requests.get("https://httpbin.org/delay/10", timeout=3).raise_for_status()
	except requests.exceptions.Timeout:
		print("Timeout after 3 seconds: please try again")
	except requests.exceptions.ConnectionError:
		print("Connection error; please try again")
	except requests.exceptions.HTTPError as error:
		print(f"HTTP error: {error}")

	try:
		response = requests.get("https://httpbin.org/status/500", timeout=5)
		response.raise_for_status()
	except requests.exceptions.HTTPError:
		print("Server error 500 handled")
	except requests.exceptions.Timeout:
		print("Request timed out; please try again")
	except requests.exceptions.ConnectionError:
		print("Connection error; please try again")

	response = safe_get("https://httpbin.org/json")
	if response is not None:
		slideshow = response.json().get("slideshow", {})
		result = {
			"title": slideshow.get("title"),
			"author": slideshow.get("author"),
		}
		(BASE_DIR / "result.json").write_text(
			__import__("json").dumps(result, indent=2), encoding="utf-8"
		)


if __name__ == "__main__":
	main()
