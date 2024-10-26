from django.db import models

# Create your models here.
class Users(models.Model):
    username=models.CharField(max_length=100,primary_key=True)
    password=models.CharField(max_length=50)

class Game(models.Model):
    group_name=models.CharField(max_length=100)
    username=models.ForeignKey(Users,on_delete=models.CASCADE)
    cards_list=models.CharField(max_length=100,default="")
    created = models.DateTimeField(auto_now_add=True)
    game_starting_player=models.CharField(max_length=100)
    start_distribution=models.CharField(max_length=100)

    def __str__(self):
        return f"{self.username} - {self.group_name}"
    
class CardContainer(models.Model):
    group_name=models.ForeignKey(Game,on_delete=models.CASCADE)
    playing_card=models.CharField(max_length=100)
    card_done=models.BooleanField(default=False)
    username=models.ForeignKey(Users,on_delete=models.CASCADE)