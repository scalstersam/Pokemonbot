import aiohttp  # A library for asynchronous HTTP requests
import random
import asyncio  # Diperlukan untuk menjalankan fungsi async di luar
from datetime import datetime,timezone,timedelta

class Pokemon:
    pokemons = {} # atribute kelas
    # Object initialisation (constructor)
    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer
        self.pokemon_number = random.randint(1, 1000)
        self.name = None
        self.img = None
        self.hp = random.randint(50,100)
        self.power = random.randint(300,500)
        self.last_feed_time = datetime.now()
        if pokemon_trainer not in Pokemon.pokemons:
            Pokemon.pokemons[pokemon_trainer] = self
        else:
            self = Pokemon.pokemons[pokemon_trainer]

    async def get_name(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'  
        async with aiohttp.ClientSession() as session:  
            async with session.get(url) as response:  
                if response.status == 200:
                    data = await response.json()  
                    return data['forms'][0]['name']  
                else:
                    return "Pikachu"  

    async def info(self):
        if not self.name:
            self.name = await self.get_name()  
        return f"""The name of your Pokémon: {self.name}
                Your Pokemon's power: {self.power}
                Your Pokemon's HP: {self.hp}"""
    
    async def show_img(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'  
        async with aiohttp.ClientSession() as session:  
            async with session.get(url) as response:  
                if response.status == 200:
                    data = await response.json()  
                    return data['sprites']['other']['showdown']['front_default']  
                else:
                    return None  

    async def attack(self, enemy):
        if isinstance(enemy, wizard):  
            turns = random.randint(1,5)
            if turns == 1:
                return "Pokemon penyihir menggunakan perisai dalam pertarungan"
        if enemy.hp > self.power:
            enemy.hp -= self.power
            return f"Pertarungan @{self.pokemon_trainer} dengan @{enemy.pokemon_trainer}"
        else:
            enemy.hp = 0
            return f"@{self.pokemon_trainer} menang melawan @{enemy.pokemon_trainer}!"

    async def feed(self, feed_interval = 20, hp_increase = 10 ):
            current_time = datetime.now()  
            delta_time = timedelta(seconds=feed_interval)  
            if (current_time - self.last_feed_time) > delta_time:
                self.hp += hp_increase
                self.last_feed_time = current_time
                return f"Kesehatan Pokemon dipulihkan. HP saat ini: {self.hp}"
            else:
                return f"Kalian dapat memberi makan Pokémon kalian di: {current_time+delta_time}"

class wizard(Pokemon):
    async def feed(self):
        return super().feed(hp_increase=20)

class fighter(Pokemon):
    async def attack(self, enemy):
        superpower = random.randint(5,15)
        self.power += superpower
        hasil = await super().attack(enemy)
        self.power -= superpower
        return hasil + f"\nPetarung menggunakan serangan super dengan kekuatan:{superpower} "

    async def feed(self):
        return super().feed(feed_interval=10)


# ==========================================
# TEMPAT MENAMBAHKAN KODE UJI COBA (MAIN)
# ==========================================
async def main():
    # Perhatikan perubahan huruf kecil/besar (wizard -> wizard, fighter -> fighter)
    my_wizard = wizard("username1")
    my_fighter = fighter("username2")

    # Karena info() dan attack() adalah fungsi async, gunakan await
    print(await my_wizard.info())
    print()
    print(await my_fighter.info())
    print()
    print(await my_fighter.attack(my_wizard))

if __name__ == '__main__':
    asyncio.run(main())