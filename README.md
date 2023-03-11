# Tarkov Items API
Tarkov Items API is an API that extracts data from Escape from Tarkov, a popular online multiplayer first-person shooter game, and provides access to detailed information on items found in the game. This API is designed to allow developers and gamers to easily access the most up-to-date information on items in the game, without the need for manual data entry.

# Features
The Tarkov Items API provides access to a wide range of information on items in the game, including so far:

Item name
Item trader price
Item flea price

# Integration with RaidVoice
Tarkov Items API is planned to be integrated with RaidVoice, a speech recognition application that can tell you real-time prices of items you request. Designed specifically for hardcore Escape From Tarkov players. This integration allows for faster and more efficient access to item data, as it can now be retrieved and shared in real-time during gameplay.

By simply using the RaidVoice overlay during gameplay, you can easily access detailed information on any item in the game without having to leave the game or switch to another application. This integration saves time and increases efficiency, allowing you to focus on your gameplay without distractions.

The API is regularly updated every 8 hours, so you can be sure that you are always accessing the most current data on items in the game.

# Endpoints
The Tarkov Items API plans to include several endpoints, each providing access to different types of data. These endpoints will include:

/items - Returns a list of all items in the game, with basic information such as name and type.
/items/{item-id} - Returns detailed information on a specific item, including its description, image, price, rarity, and more.
/items/quest/{quest-name} - Returns a list of all items required for a specific quest in the game, along with their details.
/items/trader/{trader-name} - Returns a list of all items that can be bought or sold by a specific trader in the game, along with their prices and level requirements.
Getting Started
To get started using the Tarkov Items API, simply make a request to one of the API endpoints using your preferred programming language. The API response will be returned in JSON format, making it easy to parse and use in your own applications.

# Authentication
The Tarkov Items API does not currently require authentication, meaning that anyone can access the API endpoints and retrieve item data.
