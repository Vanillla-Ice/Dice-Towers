import random

class Dice:
    def __init__(self):
        self.value = random.randint(1, 6)
        self.color = random.choice(('black', 'white'))

    def __lt__(self, obj):
        less = self.value < obj.value
        return less if self.color == obj.color else not less

    def __gt__(self, obj):
        greater = self.value > obj.value
        return greater if self.color == obj.color else not greater
    
    def __eq__(self, obj):
        return self.value == obj.value
    
    def __repr__(self):
        return f'{self.color} {self.value}'

class Tower:
    def __init__(self, max_height: int):
        self.max_height = max_height
        self.height = 0
        self.dices = []
    
    def put_dice(self, dice: Dice):
        """Разместить кубик в своей башне."""
        if self.height < self.max_height:
            self.dices.append(dice)
            self.height += 1
            return self.dices
    
    def put_enemy_dice(self, dice: Dice):
        """Разместить кубик в башне чужой кубик."""
        if self.height < self.max_height:
            self.dices = [d for d in self.dices if not (d == dice)]
            self.height = len(self.dices)
            return self.put_dice(dice)
        
    def __repr__(self):
        return str(self.dices)

class DiceTowerGame:
    max_height = 5

    def __init__(self):
        self.player_tower = Tower(self.max_height)
        self.ai_tower = Tower(self.max_height)

    @staticmethod
    def roll_dice():
        """Бросить два кубика."""
        return Dice(), Dice()
    
    def player_move(self, dices: list, player_commit: list, ai_commit: int):
        """Сделать ход игрока по его инструкции."""
        if ai_commit:
            self.ai_tower.put_enemy_dice(dices[ai_commit])
        for dice_index in player_commit:
            self.player_tower.put_dice(dices[dice_index])
    
    def ai_move(self, dice1, dice2):
        """Сделать ход за ИИ c базовой стратегией"""

        # Попытка атаковать игрока первым кубиком
        if self.player_tower.height < self.max_height:
            self.player_tower.put_enemy_dice(dice1)
        # Если атаковать нельзя, ставим кубик в башню ИИ
        else:
            self.ai_tower.put_dice(dice1)

        # Попытка разместить у себя второй кубик
        self.ai_tower.put_dice(dice2)
    
    def compare_towers(self):
        """Сравнение кубиков в башнях на каждом уровне."""
        player_score = 0
        ai_score = 0
        
        for i in range(self.max_height):
            player_dice = self.player_tower.dices[i]
            ai_dice = self.ai_tower.dices[i]
            
            if player_dice < ai_dice:
                ai_score += 1
            elif player_dice > ai_dice:
                player_score += 1
        
        return player_score, ai_score

    def play(self):
        """Основной цикл игры."""
        while self.player_tower.height < self.max_height or self.ai_tower.height < self.max_height:
            # Ход игрока
            dice1, dice2 = DiceTowerGame.roll_dice()
            print(f"Вы бросили кубики: {dice1} и {dice2}")
            
            player_move = input("Ваш ход: ")
            player_commit, ai_commit = player_move.split(",")
            player_commit = list(map(int, player_commit.split()))
            ai_commit = int(ai_commit) if ai_commit else None
            self.player_move([dice1, dice2], player_commit, ai_commit)

            # ход AI
            dice1, dice2 = DiceTowerGame.roll_dice()
            self.ai_move(dice1, dice2)
            
            print(f"Ваша башня: {self.player_tower}")
            print(f"Башня AI: {self.ai_tower}")
            print("-" * 30)

        # Игра завершена, сравниваем башни
        player_score, ai_score = self.compare_towers()
        print(f"Ваш счёт: {player_score}")
        print(f"Счёт AI: {ai_score}")

        if player_score > ai_score:
            print("Вы победили!")
        elif ai_score > player_score:
            print("AI победил!")
        else:
            print("Ничья!")

if __name__ == "__main__":
    game = DiceTowerGame()
    game.play()
