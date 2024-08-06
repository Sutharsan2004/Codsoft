"""

user=input("Hi! Enter your prompt...")
if user == "What is your name?":
    print("I'm a predefined ChatBot model. Ask me anything you need to discuss....")
    input("Hi! Enter your prompt...")
    print("Here the topics to discuss-> 1.AI 2.Weather 3.Local News 4.Latest Technology 5.Sports")
    user = input("Enter your choice...")
    if user == "AI":
      print("")

else:
    print("Sorry.. Can't able to interpret your request....")