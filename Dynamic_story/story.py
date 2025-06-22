import json
import os
from typing import Dict, List

class StoryNode:
    def __init__(self, node_id: str, text: str, options: List[Dict[str, str]]):
        self.node_id = node_id
        self.text = text
        self.options = options  # List of {"text": "...", "next_node": "..."}
    
    def display(self):
        print("\n" + self.text + "\n")
        for i, option in enumerate(self.options, 1):
            print(f"{i}. {option['text']}")
    
    def get_next_node(self, choice: int):
        if 1 <= choice <= len(self.options):
            return self.options[choice - 1]['next_node']
        return None

class Story:
    def __init__(self, title: str, start_node: str, nodes: Dict[str, StoryNode]):
        self.title = title
        self.start_node = start_node
        self.nodes = nodes
        self.current_node = start_node
        self.visited_nodes = set()
    
    def start(self):
        self.current_node = self.start_node
        self.play()
    
    def play(self):
        while self.current_node:
            node = self.nodes[self.current_node]
            self.visited_nodes.add(self.current_node)
            node.display()
            
            if not node.options:  # Ending node
                print("\n[The End]")
                break
            
            try:
                choice = int(input("\nYour choice (1-" + str(len(node.options)) + "): "))
                next_node = node.get_next_node(choice)
                if next_node:
                    self.current_node = next_node
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Please enter a number.")

class StoryManager:
    def __init__(self):
        self.stories = {}
        self.current_story = None
        self.save_file = "story_save.json"
    
    def add_story(self, story_data: dict):
        nodes = {}
        for node_id, node_data in story_data['nodes'].items():
            nodes[node_id] = StoryNode(node_id, node_data['text'], node_data['options'])
        story = Story(story_data['title'], story_data['start_node'], nodes)
        self.stories[story.title] = story
    
    def list_stories(self):
        print("\nAvailable Stories:")
        for i, title in enumerate(self.stories.keys(), 1):
            print(f"{i}. {title}")
    
    def select_story(self, choice: int):
        titles = list(self.stories.keys())
        if 1 <= choice <= len(titles):
            self.current_story = self.stories[titles[choice - 1]]
            return True
        return False
    
    def save_progress(self):
        if self.current_story:
            data = {
                "story_title": self.current_story.title,
                "current_node": self.current_story.current_node,
                "visited_nodes": list(self.current_story.visited_nodes)
            }
            with open(self.save_file, 'w') as f:
                json.dump(data, f)
            print("Progress saved!")
    
    def load_progress(self):
        if os.path.exists(self.save_file):
            with open(self.save_file, 'r') as f:
                data = json.load(f)
            if data['story_title'] in self.stories:
                self.current_story = self.stories[data['story_title']]
                self.current_story.current_node = data['current_node']
                self.current_story.visited_nodes = set(data['visited_nodes'])
                print("Progress loaded!")
                return True
        print("No save file found or story not available.")
        return False

def load_sample_story(story_manager: StoryManager):
    sample_story = {
        "title": "The Mysterious Cave",
        "start_node": "start",
        "nodes": {
            "start": {
                "text": "You find yourself at the entrance of a dark cave. A cold wind blows from within. What do you do?",
                "options": [
                    {"text": "Enter the cave cautiously", "next_node": "enter_cave"},
                    {"text": "Look around the entrance first", "next_node": "look_around"},
                    {"text": "Decide it's too dangerous and leave", "next_node": "leave"}
                ]
            },
            "enter_cave": {
                "text": "As you step inside, the cave becomes pitch black. You hear strange noises ahead.",
                "options": [
                    {"text": "Light a torch if you have one", "next_node": "light_torch"},
                    {"text": "Continue forward in the dark", "next_node": "continue_dark"},
                    {"text": "Turn back and exit the cave", "next_node": "turn_back"}
                ]
            },
            "look_around": {
                "text": "Near the entrance, you find an old backpack containing a torch and some rope.",
                "options": [
                    {"text": "Take the backpack and enter the cave", "next_node": "enter_with_items"},
                    {"text": "Ignore the backpack and enter the cave", "next_node": "enter_cave"},
                    {"text": "Take the backpack but decide not to enter", "next_node": "take_and_leave"}
                ]
            },
            "leave": {
                "text": "You decide the cave isn't worth the risk and return home. Life goes on as usual.",
                "options": []
            },
            "light_torch": {
                "text": "The torch illuminates the cave walls covered in ancient drawings. A path splits left and right.",
                "options": [
                    {"text": "Take the left path", "next_node": "left_path"},
                    {"text": "Take the right path", "next_node": "right_path"}
                ]
            },
            "continue_dark": {
                "text": "Blind in the darkness, you trip and fall into a deep pit. Unable to climb out, your adventure ends here.",
                "options": []
            },
            "turn_back": {
                "text": "You exit the cave, shaken but unharmed. Perhaps another day you'll return.",
                "options": []
            },
            "enter_with_items": {
                "text": "With the torch lighting your way, you enter confidently. The cave splits in two directions.",
                "options": [
                    {"text": "Take the left path", "next_node": "left_path"},
                    {"text": "Take the right path", "next_node": "right_path"}
                ]
            },
            "take_and_leave": {
                "text": "You take the backpack and decide to return home. The items might be useful someday.",
                "options": []
            },
            "left_path": {
                "text": "The left path leads to a underground lake. In the center is a small island with a chest.",
                "options": [
                    {"text": "Use the rope to swing across", "next_node": "swing_to_island"},
                    {"text": "Try to swim across", "next_node": "swim"},
                    {"text": "Decide not to risk it and turn back", "next_node": "turn_back_from_lake"}
                ]
            },
            "right_path": {
                "text": "The right path leads to a chamber filled with glittering crystals. In the center stands a pedestal with a strange artifact.",
                "options": [
                    {"text": "Take the artifact", "next_node": "take_artifact"},
                    {"text": "Examine the crystals instead", "next_node": "examine_crystals"},
                    {"text": "Leave the chamber", "next_node": "leave_chamber"}
                ]
            },
            "swing_to_island": {
                "text": "You successfully swing across and open the chest to find a treasure hoard! You're rich!",
                "options": []
            },
            "swim": {
                "text": "Halfway across, something pulls you under. You never surface again.",
                "options": []
            },
            "turn_back_from_lake": {
                "text": "You return to the cave entrance, having explored but not risked too much.",
                "options": []
            },
            "take_artifact": {
                "text": "As you touch the artifact, you're transported to another world full of wonders!",
                "options": []
            },
            "examine_crystals": {
                "text": "The crystals contain magical energy. Studying them makes you a renowned scientist.",
                "options": []
            },
            "leave_chamber": {
                "text": "You leave the chamber and eventually exit the cave, wondering what might have been.",
                "options": []
            }
        }
    }
    story_manager.add_story(sample_story)

def main():
    manager = StoryManager()
    load_sample_story(manager)
    
    print("Interactive Story Generator")
    print("--------------------------")
    
    while True:
        print("\nMain Menu:")
        print("1. List available stories")
        print("2. Start a new story")
        print("3. Load saved progress")
        print("4. Exit")
        
        try:
            choice = int(input("Your choice (1-4): "))
            
            if choice == 1:
                manager.list_stories()
            elif choice == 2:
                manager.list_stories()
                story_choice = int(input("Select a story (number): "))
                if manager.select_story(story_choice):
                    manager.current_story.start()
            elif choice == 3:
                if manager.load_progress():
                    manager.current_story.play()
            elif choice == 4:
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a number.")

if __name__ == "__main__":
    main()