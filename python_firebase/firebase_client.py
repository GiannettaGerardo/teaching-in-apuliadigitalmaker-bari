import requests
import time
import json as jsonModule

class Token:
  """Represents and manage a Firebase Reponse Token."""
  def __init__(self, json, email: str=None):
    """With email is for refresh token endpoint, without
       is for signUp and signIn endpoint."""
    if email == None:
      self.creationTime = int(time.time())
      self.expiresIn = int(json.get("expiresIn"))
      self.idToken = json.get("idToken")
      self.email = json.get("email")
      self.refreshToken = json.get("refreshToken")
      self.localId = json.get("localId")
    else:
      self.creationTime = int(time.time())
      self.expiresIn = int(json.get("expires_in"))
      self.idToken = json.get("id_token")
      self.refreshToken = json.get("refresh_token")
      self.localId = json.get("user_id")
      self.email = email

  def isUsable(self) -> bool:
    """The token is usable if there is more than a minute left until expiration."""
    return ((self.creationTime + self.expiresIn) - int(time.time())) > 60


class FirebaseClient:
  """Represents a simple Firebase client that use the Firebase REST API."""
  def __init__(self, configFile: str):
    with open(configFile) as jsonConfigFile:
      self.firebaseConfig = jsonModule.load(jsonConfigFile)
    self.token = None


  def _checkRefreshToken(self):
    if self.token == None:
      raise Exception("No token json object...")
    if self.token.isUsable():
      return
    url = "https://securetoken.googleapis.com/v1/token?key=" + self.firebaseConfig["apiKey"]
    headers = {"content-type": "application/json; charset=UTF-8"}
    data = {
      "grant_type": "refresh_token",
      "refresh_token": self.token.refreshToken
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 200:
      self.token = None
      raise Exception("Error: response returned " + response.status_code + " with body: \n" + response.json())
    self.token = Token(response.json(), self.token.email)


  def signUp(self, email: str, password: str):
    url = "https://identitytoolkit.googleapis.com/v1/accounts:signUp?key=" + self.firebaseConfig["apiKey"]
    headers = {"content-type": "application/json; charset=UTF-8"}
    data = {
      "email": email,
      "password": password,
      "returnSecureToken": "true"
    }
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code != 200:
      self.token = None
      raise Exception("Error: response returned " + response.status_code + " with body: \n" + response.json())
    self.token = Token(response.json())

    
  def signIn(self, email: str, password: str):
    url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=" + self.firebaseConfig["apiKey"]
    headers = {"content-type": "application/json; charset=UTF-8"}
    data = {
      "email": email,
      "password": password,
      "returnSecureToken": "true"
    }
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code != 200:
      self.token = None
      raise Exception("Error: response returned " + response.status_code + " with body: \n" + response.json())
    self.token = Token(response.json())

  def logout(self):
    self.token = None
  
  def isLoggedIn(self) -> bool:
    return self.token != None 
  
  def getUserId(self) -> str:
    return self.token.localId
