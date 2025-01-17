import os

from box import Box
from restfly.session import APISession

from pyzscaler import __version__

from .devices import DevicesAPI
from .secrets import SecretsAPI
from .session import AuthenticatedSessionAPI


class ZCC(APISession):
    """
    A Controller to access Endpoints in the Zscaler Mobile Admin Portal API.

    The ZCC object stores the session token and simplifies access to CRUD options within the ZCC Portal.

    Attributes:
        client_id (str): The ZCC Client ID generated from the ZCC Portal.
        client_secret (str): The ZCC Client Secret generated from the ZCC Portal.
        company_id (str):
            The ZCC Company ID. There seems to be no easy way to obtain this at present. See the note
            at the top of this page for information on how to retrieve the Company ID.

    """

    _vendor = "Zscaler"
    _product = "Zscaler Mobile Admin Portal"
    _backoff = 3
    _build = __version__
    _box = True
    _box_attrs = {"camel_killer_box": True}
    _env_base = "ZCC"
    _env_cloud = "zscaler"
    _url = "https://api-mobile.zscaler.net/papi"

    def __init__(self, **kw):
        self._client_id = kw.get("client_id", os.getenv(f"{self._env_base}_CLIENT_ID"))
        self._client_secret = kw.get("client_secret", os.getenv(f"{self._env_base}_CLIENT_SECRET"))
        self.company_id = kw.get("company_id", os.getenv(f"{self._env_base}_COMPANY_ID"))
        self.conv_box = True
        super(ZCC, self).__init__(**kw)

    def _build_session(self, **kwargs) -> Box:
        """Creates a ZCC API session."""
        super(ZCC, self)._build_session(**kwargs)
        self._auth_token = self.session.create_token(client_id=self._client_id, client_secret=self._client_secret)
        return self._session.headers.update({"auth-token": f"{self._auth_token}"})

    @property
    def devices(self):
        """The interface object for the :ref:`ZCC Devices interface <zcc-devices>`."""
        return DevicesAPI(self)

    @property
    def secrets(self):
        """The interface object for the :ref:`ZCC Secrets interface <zcc-secrets>`."""
        return SecretsAPI(self)

    @property
    def session(self):
        """The interface object for the :ref:`ZCC Authenticated Session interface <zcc-session>`."""
        return AuthenticatedSessionAPI(self)
