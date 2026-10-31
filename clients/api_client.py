import os
import re
import requests


class OrangeHrmApiClient:
    """API client for orangehrm platform"""

    def __init__(self, base_url=None, username=None, password=None):
        # initialize configuration from environment variables or defaults
        self.base_url = (base_url or os.getenv("ORANGEHRM_BASE_URL", "https://opensource-demo.orangehrmlive.com")).rstrip("/")
        self.username = username or os.getenv("ORANGEHRM_USERNAME", "Admin")
        self.password = password or os.getenv("ORANGEHRM_PASSWORD", "admin123")
        self.session = requests.Session()
        user_agent = os.getenv(
            "ORANGEHRM_USER_AGENT",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        self.session.headers.update({
            "User-Agent": user_agent,
            "Accept": "application/json, text/plain, */*"
        })
        self._is_authenticated = False

    def authenticate(self):
        # fetch login page to retrieve csrf token
        login_url = f"{self.base_url}/web/index.php/auth/login"
        resp = self.session.get(login_url, timeout=15)

        # parse csrf token from html response
        token_match = re.search(r':token=\"&quot;([^&]+)&quot;\"', resp.text)
        if not token_match:
            token_match = re.search(r'name="_token"\s+value="([^"]+)"', resp.text)
        token = token_match.group(1) if token_match else ""

        # post credentials to validation endpoint
        validate_url = f"{self.base_url}/web/index.php/auth/validate"
        login_resp = self.session.post(
            validate_url,
            data={
                "_token": token,
                "username": self.username,
                "password": self.password
            },
            timeout=15
        )
        self._is_authenticated = True
        return login_resp

    def request(self, method, endpoint, **kwargs):
        # ensure session is authenticated before request execution
        if not self._is_authenticated:
            self.authenticate()

        # format full url path
        if endpoint.startswith("http://") or endpoint.startswith("https://"):
            url = endpoint
        else:
            url = f"{self.base_url}{endpoint if endpoint.startswith('/') else '/' + endpoint}"

        # set default timeout if not specified
        kwargs.setdefault("timeout", 15)
        return self.session.request(method, url, **kwargs)

    def get(self, endpoint, **kwargs):
        # send http get request
        return self.request("GET", endpoint, **kwargs)

    def post(self, endpoint, **kwargs):
        # send http post request
        return self.request("POST", endpoint, **kwargs)

    def delete(self, endpoint, **kwargs):
        # send http delete request
        return self.request("DELETE", endpoint, **kwargs)

    def put(self, endpoint, **kwargs):
        # send http put request
        return self.request("PUT", endpoint, **kwargs)

    def get_users(self, limit=10, offset=0):
        # retrieve user records with pagination
        endpoint = "/web/index.php/api/v2/admin/users"
        return self.get(endpoint, params={"limit": limit, "offset": offset})

    def create_employee(self, payload):
        # create employee record via pim api
        endpoint = "/web/index.php/api/v2/pim/employees"
        return self.post(endpoint, json=payload)

    def get_employee(self, emp_number):
        # retrieve employee details by empnumber
        endpoint = f"/web/index.php/api/v2/pim/employees/{emp_number}"
        return self.get(endpoint)

    def delete_employees(self, ids):
        # delete list of employees by id array
        endpoint = "/web/index.php/api/v2/pim/employees"
        return self.delete(endpoint, json={"ids": ids})

    def close(self):
        # close underlying requests session
        self.session.close()
