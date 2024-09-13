# Program to scrap Instagram data and see if your followers follow you back
import instaloader
import numpy

class InstaScraper:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.profile = None

    def create_session(self):
        L = instaloader.Instaloader()
        try:
            L.login(self.username, self.password) # Login or load session
            self.profile = instaloader.Profile.from_username(L.context, self.username)
        except instaloader.exceptions.LoginRequiredException:
            print("Login failed!")
        except instaloader.exceptions.ConnectionException:
            print("Connection issue!")
        except Exception as e:
            print(f"An error occurred: {e}")

    def get_follower_list(self):
        return [follower.username for follower in self.profile.get_followers()]

    def get_followee_list(self):
        return [followee.username for followee in self.profile.get_followees()]

    def get_enemies_list(self): # Enemies are people who you follow but they do not return the favour
        unfollow_list = numpy.setdiff1d(self.get_followee_list(), self.get_follower_list())
        filename = "unfollowers_" + self.username + ".txt"
        with open(filename, "w") as file:
            for person in unfollow_list:
                file.write(person + "\n")
        print(f"Unfollowers list saved to {filename}")

    def main(self):
        self.create_session()
        self.get_enemies_list()

if __name__ == "__main__":
    username = input("Enter your name: ") # can also just delete inputs and replace it with "username" 
    password = input("Enter your password: ")
    my_object = InstaScraper(username, password)
    my_object.main()
