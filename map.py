

# import streamlit as st
# import requests
# import folium
# from streamlit_folium import folium_static

# def get_coordinates(address):
#     url = "https://google-maps-geocoding.p.rapidapi.com/geocode/json"
#     headers = {
#         "X-RapidAPI-Key": "b850a85650msh0e6357b70677354p1b0904jsn73acf7bda544",
#         "X-RapidAPI-Host": "google-maps-geocoding.p.rapidapi.com"
#     }
#     params = {"address": address, "language": "en"}
#     try:
#         response = requests.get(url, headers=headers, params=params)
#         response.raise_for_status()  # Raise an exception for bad status codes
#         data = response.json()
#         if data["status"] == "OK":
#             location = data["results"][0]["geometry"]["location"]
#             return location["lat"], location["lng"]
#         else:
#             st.error("Geocoding failed. Please check the address and try again.")
#             return None, None
#     except requests.exceptions.RequestException as e:
#         st.error(f"Error fetching geocoding data: {e}")
#         return None, None

# def main():
#     st.title("Map Display")

#     # Input destination address
#     address = st.text_input("Enter Destination Address:")

#     if st.button("Get Coordinates"):
#         if address:
#             # Fetch coordinates
#             lat, lng = get_coordinates(address)
#             if lat is not None and lng is not None:
#                 st.success(f"Coordinates for {address}: Latitude - {lat}, Longitude - {lng}")
#                 # Display map using Folium
#                 m = folium.Map(location=[lat, lng], zoom_start=12)
#                 folium.Marker([lat, lng], popup=address).add_to(m)
#                 folium_static(m)
#             else:
#                 st.error("Failed to fetch coordinates.")
#         else:
#             st.warning("Please enter a destination address.")

# if __name__ == "__main__":
#     main()

import openai
import os
from dotenv import find_dotenv, load_dotenv
import time
import logging
from datetime import datetime
import requests
import json
import streamlit as st
import folium
from streamlit_folium import folium_static

load_dotenv()
openai.api_key = os.environ.get("OPENAI_API_KEY")

import requests
import json
import time
import streamlit as st

class AssistantManager:
    thread_id = "thread_dLVUxAboknZy46QjKPIBQ0W9"
    assistant_id = "asst_uI9Iq6NdKivEUMbl7eaKnTiq"

    def __init__(self, client):
        self.client = client
        self.assistant = None
        self.thread = None
        self.run = None
        self.summary = None

        if AssistantManager.assistant_id:
            self.assistant = self.client.beta.assistants.retrieve(
                assistant_id=AssistantManager.assistant_id
            )
        if AssistantManager.thread_id:
            self.thread = self.client.beta.threads.retrieve(
                thread_id=AssistantManager.thread_id
            )

    def create_assistant(self, name, instructions, tools):
        if not self.assistant:
            assistant_obj = self.client.beta.assistants.create(
                name=name, instructions=instructions, tools=tools
            )
            AssistantManager.assistant_id = assistant_obj.id
            self.assistant = assistant_obj
            print(f"AssisID:::: {self.assistant.id}")

    def create_thread(self):
        if not self.thread:
            thread_obj = self.client.beta.threads.create()
            AssistantManager.thread_id = thread_obj.id
            self.thread = thread_obj
            print(f"ThreadID::: {self.thread.id}")

    def add_message_to_thread(self, role, content):
        if self.thread:
            self.client.beta.threads.messages.create(
                thread_id=self.thread.id, role=role, content=content
            )

    def run_assistant(self, instructions):
        if self.thread and self.assistant:
            self.run = self.client.beta.threads.runs.create(
                thread_id=self.thread.id,
                assistant_id=self.assistant.id,
                instructions=instructions,
            )

    def process_message(self):
        if self.thread:
            messages = self.client.beta.threads.messages.list(thread_id=self.thread.id)
            summary = []

            last_message = messages.data[0]
            role = last_message.role
            response = last_message.content[0].text.value
            summary.append(response)

            self.summary = "\n".join(summary)
            print(f"SUMMARY-----> {role.capitalize()}: ==> {response}")

    def call_required_functions(self, required_actions):
        if not self.run:
            return
        tool_outputs = []

        for action in required_actions["tool_calls"]:
            func_name = action["function"]["name"]
            arguments = json.loads(action["function"]["arguments"])

            # Here you can add more functions if needed
            raise ValueError(f"Unknown function: {func_name}")

        print("Submitting outputs back to the Assistant...")
        self.client.beta.threads.runs.submit_tool_outputs(
            thread_id=self.thread.id, run_id=self.run.id, tool_outputs=tool_outputs
        )

    def get_summary(self):
        return self.summary

    def wait_for_completion(self):
        if self.thread and self.run:
            while True:
                time.sleep(5)
                run_status = self.client.beta.threads.runs.retrieve(
                    thread_id=self.thread.id, run_id=self.run.id
                )
                print(f"RUN STATUS:: {run_status.model_dump_json(indent=4)}")

                if run_status.status == "completed":
                    self.process_message()
                    break
                elif run_status.status == "requires_action":
                    print("FUNCTION CALLING NOW...")
                    self.call_required_functions(
                        required_actions=run_status.required_action.submit_tool_outputs.model_dump()
                    )

    def run_steps(self):
        run_steps = self.client.beta.threads.runs.steps.list(
            thread_id=self.thread.id, run_id=self.run.id
        )
        print(f"Run-Steps::: {run_steps}")
        return run_steps.data

def get_coordinates(address):
    url = "https://google-maps-geocoding.p.rapidapi.com/geocode/json"
    headers = {
        "X-RapidAPI-Key": "b850a85650msh0e6357b70677354p1b0904jsn73acf7bda544",
        "X-RapidAPI-Host": "google-maps-geocoding.p.rapidapi.com"
    }
    params = {"address": address, "language": "en"}
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        if data["status"] == "OK":
            location = data["results"][0]["geometry"]["location"]

            lat = location["lat"]
            lng = location["lng"]
            return lat, lng
        else:
            print("Error: Unable to fetch coordinates.")
            return None, None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching coordinates: {str(e)}")
        return None, None

def display_locations_on_map(locations):
    # Create a map centered around the first location
    map_center = get_coordinates(locations[0])
    m = folium.Map(location=map_center, zoom_start=10)

    # Add markers for each location
    for location in locations:
        lat, lng = get_coordinates(location)
        if lat is not None and lng is not None:
            folium.Marker([lat, lng], popup=location).add_to(m)

    # Display the map
    folium_static(m)

def main():
    openai_client = openai.Client(api_key=os.environ.get("OPENAI_API_KEY"))
    manager = AssistantManager(client=openai_client)

    st.title("ITINERARY GENERATOR")
    st.image('bg.jpg')
    location_name = st.text_input("Enter location name:")
    submit_button = st.button(label="Run Assistant")

    if submit_button:
        manager.create_assistant(
            name="Assistant Application",
            instructions="You are a personal travel Assistant.Your job is to generate itineraries based on user destination. Generate the itinerary day wise for each of the input",
            tools=[
                {
                    "type": "function",
                    "function": {
                        "name": "get_tripadvisor_data",  # You can remove this line if not needed
                        "description": "Fetch data for a given location.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "location_name": {
                                    "type": "string",
                                    "description": "The name of the location.",
                                }
                            },
                            "required": ["location_name"],
                        },
                    },
                }
            ],
        )
        manager.create_thread()

        manager.add_message_to_thread(
            role="user", content=f"fetch data for location with name: {location_name}"
        )
        manager.run_assistant(instructions="Fetch data")

        manager.wait_for_completion()

        summary = manager.get_summary()

        st.write(summary)

        st.text("Run steps")
def get_coordinates(address):
    url = "https://google-maps-geocoding.p.rapidapi.com/geocode/json"
    headers = {
        "X-RapidAPI-Key": "b850a85650msh0e6357b70677354p1b0904jsn73acf7bda544",
        "X-RapidAPI-Host": "google-maps-geocoding.p.rapidapi.com"
    }
    params = {"address": address, "language": "en"}
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        if data["status"] == "OK":
            location = data["results"][0]["geometry"]["location"]

            lat = location["lat"]
            lng = location["lng"]
            return lat, lng
        else:
            print("Error: Unable to fetch coordinates.")
            return None, None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching coordinates: {str(e)}")
        return None, None

def display_locations_on_map(locations):
    # Create a map centered around the first location
    map_center = get_coordinates(locations[0])
    m = folium.Map(location=map_center, zoom_start=10)

    # Add markers for each location
    for location in locations:
        lat, lng = get_coordinates(location)
        if lat is not None and lng is not None:
            folium.Marker([lat, lng], popup=location).add_to(m)

    # Display the map
    folium_static(m)

def main():
    openai_client = openai.Client(api_key=os.environ.get("OPENAI_API_KEY"))
    manager = AssistantManager(client=openai_client)

    st.title("ITINERARY GENERATOR")
    st.image('bg.jpg')
    location_name = st.text_input("Enter location name:")
    submit_button = st.button(label="Run Assistant")

    if submit_button:
        manager.create_assistant(
            name="Assistant Application",
            instructions="You are a personal travel Assistant.Your job is to generate itineraries based on user destination. Generate the itinerary day wise for each of the input",
            tools=[
                {
                    "type": "function",
                    "function": {
                        "name": "get_tripadvisor_data",  # You can remove this line if not needed
                        "description": "Fetch data for a given location.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "location_name": {
                                    "type": "string",
                                    "description": "The name of the location.",
                                }
                            },
                            "required": ["location_name"],
                        },
                    },
                }
            ],
        )
        manager.create_thread()

        manager.add_message_to_thread(
            role="user", content=f"fetch data for location with name: {location_name}"
        )
        manager.run_assistant(instructions="Fetch data")

        manager.wait_for_completion()

        summary = manager.get_summary()

        st.write(summary)

        st.text("Run Steps:")
        st.code(manager.run_steps(), language="json")

        # Extract locations from the summary
        locations = [location.strip() for location in summary.split("\n")]

        # Display locations on the map
        display_locations_on_map(locations)

        # Add download button
        st.download_button('Download Itinerary', summary, file_name='itinerary.txt')

if __name__ == "__main__":
    main()



