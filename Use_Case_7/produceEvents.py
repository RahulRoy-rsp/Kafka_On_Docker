from kafka import KafkaProducer # pip install kafka-python

import os
import json
import random
import time

"""
base event json structure
{
    "player_id": 12,
    "name_info": {
        "first_name": "Joe",
        "last_name": "Root"
    },
    "nationality": "England",
    "clubs": ["Yorkshire", "Trent Rockets"],
    "role": "Batsman"
}
"""

class postEventsToKafkaTopic:
    
    def __init__(self, topic_name, bootstrap_server):
        
        # defining static variables
        self.first_names = ["Joe", "Steven", "Mark", "Ricky", "Gary", "Micheal", "Eric"]
        self.last_names = ["Root", "Smith", "Holland", "Steamboat", "Sobers", "Clarke", "Rowan"]
        self.nationalities = ["England", "Australia", "Scotland", "Germany", "Spain", "Netherlands"]
        self.clubs = ["Yorkshire", "Surrey", "Sussex", "New South Wales", "Victoria", "Western Australia", "Tasmania", "Queensland", "Kent"]
        self.roles = ["Batsman", "Bowler", "All-Rounder"]

        self.topic_name = topic_name
        self.bootstrap_server = bootstrap_server

        # generating random player_id 
        self.player_id = self.__generatePlayerId()
        
        # Initialize the Kafka producer
        self.producer = KafkaProducer(
            bootstrap_servers = self.bootstrap_server,
            value_serializer = lambda x: json.dumps(x).encode('utf-8'),
            key_serializer = lambda x: str(x).encode('utf-8')
        )
    
    def __generatePlayerId(self):
        player_id_file = "player_ids.json"

        # Check if the file exists
        if not os.path.exists(player_id_file):
            # If the file doesn't exist, create it with an initial structure
            print(f"{player_id_file} does not exist. Creating it with an initial structure.")
            with open(player_id_file, "w") as f:
                json.dump({"player_ids": []}, f)

        # Read the player_ids from the file
        with open(player_id_file, "r") as f:
            data = json.load(f)
            existing_player_ids = data["player_ids"]

        # Generate a random player ID (between 1 to 100) and ensure it doesn't already exist
        while True:
            new_player_id = random.randint(1, 100)
            if new_player_id not in existing_player_ids:
                # Add the new player ID to the list and save it
                existing_player_ids.append(new_player_id)
                with open(player_id_file, "w") as f:
                    json.dump({"player_ids": existing_player_ids}, f)
                print(f"Generated new unique player ID: {new_player_id}")
                return new_player_id
            else:
                print(f"Player ID {new_player_id} already exists, generating a new one.")

        
    def eventGenerator(self):
        print(f"Generating an event for {self.player_id}")

        # Generate the event JSON
        self.generated_event = {
            "player_id": self.player_id,
            "name_info": {
                "first_name": random.choice(self.first_names),
                "last_name": random.choice(self.last_names)
            },
            "nationality": random.choice(self.nationalities),
            "clubs": random.sample(self.clubs, random.randint(1, 3)),  # Random number of clubs between 1 and 3
            "role": random.choice(self.roles)
        }

        print(f"Event generated for player {self.player_id}")
        print(self.generated_event)
        
        # Send the event to Kafka
        return self.__sendEvent(self.generated_event)
    
    def __sendEvent(self, event_data):
        print("Preparing to send event to Kafka topic:", self.topic_name)
        
        try:
            # Produce the event to the Kafka topic
            key = str(self.player_id).encode('utf-8')  # You can use the player_id as the key
            self.producer.send(self.topic_name, key=key, value=event_data)
            self.producer.flush()  # Ensure the event is sent immediately
            print(f"Event sent successfully for player {self.player_id}")
        except Exception as e:
            print(f"Error sending event for player {self.player_id}: {e}")
        finally:
            self.producer.close()  # Close the producer after sending the event

if __name__ == "__main__":
    
    topic_name = ""  # enter the Kafka topic name where the data will be produced
    bootstrap_server = ""  # Kafka server address

    eventsToPass = 2 # number of events to be passed at a time
    while eventsToPass > 0:
        obj = postEventsToKafkaTopic(topic_name, bootstrap_server)
        obj.eventGenerator()
        time.sleep(2)
        eventsToPass -= 1
    
