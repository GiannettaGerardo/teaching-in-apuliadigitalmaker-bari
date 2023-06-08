from my_firebase_client import FirebaseClient

def print_auth_menu():
  print(" ||----------------------------------------------------||")
  print(" || Welcome to ...                                     ||")
  print(" ||----------------------------------------------------||")
  print(" ||                        Menù                        ||")
  print(" || Enter a number to choose an action.                ||")
  print(" || [1] Exit                                           ||")
  print(" || [2] Sign Up                                        ||")
  print(" || [3] Sign In                                        ||")
  print(" ||----------------------------------------------------||")

def print_action_menu(username: str):
  print("    Welcome " + username)
  print(" ||----------------------------------------------------||")
  print(" ||                        Menù                        ||")
  print(" || Enter a number to choose an action.                ||")
  print(" || [1] Exit                                           ||")
  print(" || [2] Logout                                         ||")
  print(" ||----------------------------------------------------||")

def print_menu(client: FirebaseClient):
  if client.isLoggedIn():
    print_action_menu("User")
  else:
    print_auth_menu()

def parse_input(client: FirebaseClient, value: int):
  if value == 1:
    print("Exit in progress...")
    exit()
  if client.isLoggedIn():
    pass

def main():
  client = FirebaseClient()
  while True:
    try:
      print_menu(client)
      print(">> ", end="")
      value = int(input())
      parse_input(client, value)
    except ValueError:
      print("Invalid number. Retry...")
    print("")
  #client.signUp(email="giannettagerry90@gmail.com", password="f1rebaseTest_")

if __name__ == "__main__":
  main()