from django.db import models

# Create your models here.


class Resource(models.Model):
    type = models.CharField(max_length=200)
    num = models.IntegerField(default=0)


class Development(models.Model):
    type = models.CharField(max_length=200)
    num = models.IntegerField(default=0)


class Bank(models.Model):
    resource_cards = models.ManyToManyField(Resource)
    development_cards = models.ManyToManyField(Development)


class Dice(models.Model):
    left = models.PositiveIntegerField(default=1)
    right = models.PositiveIntegerField(default=1)

    def sum(self):
        return self.left + self.right


class CantanMap(models.Model):
    map_id = models.AutoField(primary_key=True)
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    dice = models.ForeignKey(Dice, on_delete=models.CASCADE)


class Game(models.Model):
    SETTLE = 'ST'
    MAIN = 'MA'
    END = 'ED'
    GAME_STATUS = [
        (SETTLE, 'Settle'),
        (MAIN, 'Main'),
        (END, 'End'),
    ]

    map_name = models.CharField(max_length=200)
    turn_id = models.IntegerField(default=0)
    status = models.CharField(
        max_length=2,
        choices=GAME_STATUS,
        default=MAIN)
    number_of_player = models.PositiveIntegerField(default=2)
    current_player_id = models.IntegerField()


class Player(models.Model):
    score = models.IntegerField(default=0)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    resource_cards = models.ManyToManyField(Resource)
    development_cards = models.ManyToManyField(Development)


class Position(models.Model):
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    z = models.IntegerField(default=0)


class Node(models.Model):
    map = models.ForeignKey(CantanMap, on_delete=models.CASCADE)
    pos = models.OneToOneField(Position, on_delete=models.CASCADE)
    knighted = models.BooleanField(default=False)


class Vertex(models.Model):
    node = models.ForeignKey(Node, on_delete=models.CASCADE)
    # there are totally 6 vertices
    idx = models.IntegerField(default=0)
    # -1 for nothing, 0 for settlement and 1 for town
    status = models.IntegerField(default=-1)


class Edge(models.Model):
    node = models.ForeignKey(Node, on_delete=models.CASCADE)
    # there are totally 6 edges
    idx = models.IntegerField(default=0)
    road = models.BooleanField(default=False)


