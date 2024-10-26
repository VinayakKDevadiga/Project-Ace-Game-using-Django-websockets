from channels.generic.websocket import JsonWebsocketConsumer
from .models import *
from asgiref.sync import async_to_sync


# for game operatins
from .card_distribute import cardlist
import random

class MyJsonAsyncConsumer(JsonWebsocketConsumer):
      
    def connect(self):
        self.groupname = self.scope['url_route']['kwargs']['GroupName']
        print("WebSocket connected...",self.groupname)
        self.cardlist = cardlist.copy()
        async_to_sync(self.channel_layer.group_add)(
            self.groupname,
            self.channel_name
        )
        self.accept()

    def disconnect(self, code):
        all_users = Game.objects.filter(group_name=self.groupname).select_related('username').values('username__username')
        # If only one object/player is there in group and he is disconnected then delete his object in database
        if len(all_users)==1:
             Game.objects.filter(group_name=self.groupname).delete()
        
        print("WebSocket disconnected...", code)
        # Query Game model again to get updated data
        all_users = Game.objects.filter(group_name=self.groupname).select_related('username').values('username__username')
        all_usernames = [user['username__username'] for user in all_users]

        # Send updated data to the group
        async_to_sync(self.channel_layer.group_send)(
            self.groupname,
            {
                'type': 'user_joined',  # Custom type for handling in consumer
                "message": "User Disconnected",
                "user_joined": all_usernames  # Send the list of usernames
            }
        )
    

    def receive_json(self, content, **kwargs):
        print("The content recieved...",content)

        # if (content['types']== 'start_actual_game'):
        #      self.username_from_actual_start=content['username']

   
        if (content['content']['types']=='start_game'):
            async_to_sync(self.channel_layer.group_send)(
            self.groupname,
            {
            'type': 'start_game',# Custom type for handling in consumer  
            'message':'game started'
            })
        else:
            print('Message received...', content['content'])
            self.groupname = content['content']['group_name1'].replace('"', '')
            self.username = content['content']['user_name1'].replace('"', '')
            self.password=  content['content']['password1'].replace('"', '')

            print("User name, password.....",self.username,self.password)
            exist_user = Users.objects.filter(username=self.username, password=self.password).first()
            if exist_user:
                exist_game_user= Game.objects.filter(group_name=self.groupname, username=exist_user)
                if not exist_game_user:
                    Game_object = Game.objects.create(group_name=self.groupname, username=exist_user)
                    Game_object.save()

                all_users = Game.objects.filter(group_name=self.groupname).select_related('username').values('username__username')
                all_usernames = [user['username__username'] for user in all_users]
               
                self.send_json(
                    {
                        'message':"user_name",
                        'username':self.username
                    }
                )
                async_to_sync(self.channel_layer.group_send)(
                self.groupname,
                {
                'type': 'user_joined',# Custom type for handling in consumer
                "message": "User Found",
                "user_joined":all_usernames
                })
                
            else:
                self.send_json(
                    {
                        "message":"User Not exist" ,
                        "redirect":'home/'
                    }
                )

    def user_joined(self, event):
            #storing gameadmin in database
            # self.gameadmin=Gameadmin.objects.create(group_name)
            # Handle the message sent to the group chats every member
            self.send_json({
                'message': event['message'],
                'user_joined': event['user_joined']
            })


    def start_game(self, event):

        # Get all game objects ordered by creation date
        self.games_ordered_by_creation = Game.objects.filter(group_name=self.groupname).order_by('created')

        # Extract the usernames from the ordered games
        self.all_usernames = [game.username.username for game in self.games_ordered_by_creation]

        # Print the usernames
        print("Printing all users...", self.all_usernames)

        # Check the length of ordered games
        print("Length...", len(self.games_ordered_by_creation))

        # Randomly choose a starting player
        self.random_position = random.randint(0, len(self.all_usernames) - 1)
        self.start_DIst_player = self.random_position  # for start index of user

        # Initialize empty lists for each player
        self.playerlists = [[] for _ in range(len(self.all_usernames))]

       
        # Distribute the cards
        while self.cardlist:
            while self.random_position < len(self.all_usernames):
                if self.cardlist:
                    card_index = random.randint(0, len(self.cardlist) - 1)
                    card=self.cardlist.pop(card_index)
                    self.playerlists[self.random_position].append(card)
                    if card=='SA':
                         # player holdin 'SA'
                        self.game_starting_player_index=self.random_position
                        
                    self.random_position += 1

                    if self.random_position == len(self.all_usernames):
                        self.random_position = 0

                    if not self.cardlist:
                        break

        print("Player lists:", self.playerlists)



        # 
        self.cardlist_dict={}

        for i in range(len(self.all_usernames)):
            self.all_cards=' '.join(self.playerlists[i])
            # Retrieve the Game object for the current user
            self.game = Game.objects.get(username__username=self.all_usernames[i])
            
            # Update the cards_list field
            self.game.cards_list = self.all_cards
            print("all cards ...",self.all_cards)

            #setting ga,e starting player
            self.game.game_starting_player=self.all_usernames[self.game_starting_player_index]
            #setting start_distribution player in game
            self.game.start_distribution=self.all_usernames[self.start_DIst_player]

            # Save the updated Game object
            self.game.save()

            #insert data into self.cardlist_dict
            self.cardlist_dict[self.all_usernames[i]]=self.all_cards
      
       
        self.send_json({
                'message':"Only 10 players allowed" if len(self.all_usernames)>10 else event['message'],
                'start_card_dist_player':self.all_usernames[self.start_DIst_player],
                'start_game_player':self.all_usernames[self.game_starting_player_index],
                'cardlist':self.cardlist_dict,
           
            })
    
    
 