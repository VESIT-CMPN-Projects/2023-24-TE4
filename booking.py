

import streamlit as st

# def generate_booking_url(destination, checkin_date, checkout_date, guests, budget):
#     base_url = "https://www.booking.com"
#     parameters = {
#         "ss": destination,          # 'ss' parameter represents the destination
#         "checkin_monthday": checkin_date[-2:],  # 'checkin_monthday' parameter represents the check-in day
#         "checkin_month": checkin_date[5:7],     # 'checkin_month' parameter represents the check-in month
#         "checkin_year": checkin_date[:4],        # 'checkin_year' parameter represents the check-in year
#         "checkout_monthday": checkout_date[-2:], # 'checkout_monthday' parameter represents the check-out day
#         "checkout_month": checkout_date[5:7],    # 'checkout_month' parameter represents the check-out month
#         "checkout_year": checkout_date[:4],      # 'checkout_year' parameter represents the check-out year
#         "group_adults": guests,                 # 'group_adults' parameter represents the number of guests
#         "group_children": 0,                    # 'group_children' parameter represents the number of children
#         "price_filter": budget                  # 'price_filter' parameter represents the budget category
#     }
#     encoded_parameters = "&".join([f"{key}={value}" for key, value in parameters.items()])
#     booking_url = f"{base_url}/searchresults.html?{encoded_parameters}"
#     return booking_url

def generate_booking_url(destination, checkin_date, checkout_date, guests, budget):
    base_url = "https://www.booking.com"
    parameters = {
        "ss": destination,
        "checkin": checkin_date,
        "checkout": checkout_date,
        "group_adults": guests,
        "group_children": 0,
        "price_filter": budget
    }
    encoded_parameters = "&".join([f"{key}={value}" for key, value in parameters.items()])
    booking_url = f"{base_url}/searchresults.html?{encoded_parameters}"
    return booking_url


def main():
    st.title("Hotel Booking")

    # Input fields
    destination = st.text_input("Destination", "Pune")
    checkin_date = st.date_input("Check-in Date", value=None)
    checkout_date = st.date_input("Check-out Date", value=None)
    guests = st.number_input("Number of Guests", min_value=1, value=1)
    accommodation_types = ["Entire homes & apartments", "Apartments", "Hotels", "Holiday homes", "Homestays", 
                           "Guest houses", "Hostels", "Villas", "Motels", "Resorts", "Bed and breakfasts"]
    accommodation_type = st.selectbox("Accommodation Type", accommodation_types, index=0)
    review_scores = ["Superb: 9+", "Very good: 8+", "Good: 7+", "Pleasant: 6+"]
    review_score = st.selectbox("Review Score", review_scores, index=0)
    budget_options = ["Any", "Low", "Medium", "High"]
    budget = st.selectbox("Budget Category", budget_options, index=0)

    # Generate booking URL on button click
    if st.button("Generate Booking URL"):
        if checkin_date and checkout_date:
            checkin_str = checkin_date.strftime("%Y-%m-%d")
            checkout_str = checkout_date.strftime("%Y-%m-%d")
            booking_url = generate_booking_url(destination, checkin_str, checkout_str, guests, budget)
            st.write("Booking URL:", booking_url)
        else:
            st.error("Please select both check-in and check-out dates.")

if __name__ == "__main__":
    main()


# def main():
#     st.title("Booking.com URL Generator")

#     # Input fields
#     destination = st.text_input("Destination", "Pune")
#     checkin_date = st.date_input("Check-in Date", value=None)
#     checkout_date = st.date_input("Check-out Date", value=None)
#     guests = st.number_input("Number of Guests", min_value=1, value=1)
#     budget_options = ["Any", "Low", "Medium", "High"]
#     budget = st.selectbox("Budget Category", budget_options, index=0)

#     # Generate booking URL on button click
#     if st.button("Generate Booking URL"):
#         if checkin_date and checkout_date:
#             checkin_str = checkin_date.strftime("%Y-%m-%d")
#             checkout_str = checkout_date.strftime("%Y-%m-%d")
#             booking_url = generate_booking_url(destination, checkin_str, checkout_str, guests, budget)
#             st.write("Booking URL:", booking_url)
#         else:
#             st.error("Please select both check-in and check-out dates.")

# if __name__ == "__main__":
#     main()


# def main():
#     st.title("Booking.com URL Generator")

#     # Input fields
#     destination = st.text_input("Destination", "New York")
#     checkin_date = st.date_input("Check-in Date", value=None)
#     checkout_date = st.date_input("Check-out Date", value=None)
#     guests = st.number_input("Number of Guests", min_value=1, value=1)
#     budget_options = ["Any", "Low", "Medium", "High"]
#     budget = st.selectbox("Budget Category", budget_options, index=0)

#     # Generate booking URL on button click
#     if st.button("Generate Booking URL"):
#         if checkin_date and checkout_date:
#             checkin_str = checkin_date.strftime("%Y-%m-%d")
#             checkout_str = checkout_date.strftime("%Y-%m-%d")
#             booking_url = generate_booking_url(destination, checkin_str, checkout_str, guests, budget)
#             st.write("Booking URL:", booking_url)
#         else:
#             st.error("Please select both check-in and check-out dates.")

# if __name__ == "__main__":
#     main()




import streamlit as st

def generate_flight_booking_url(origin_city, destination_city, depart_date, return_date, adults):
    base_url = "https://www.booking.com/flights/index.en-gb.html"
    parameters = {
        "origin": origin_city,                 # Origin city name
        "destination": destination_city,       # Destination city name
        "depart_date": depart_date,           # Departure date in YYYY-MM-DD format
        "return_date": return_date,           # Return date in YYYY-MM-DD format
        "adults": adults                      # Number of adults
    }
    encoded_parameters = "&".join([f"{key}={value}" for key, value in parameters.items()])
    booking_url = f"{base_url}?{encoded_parameters}"
    return booking_url

def main():
    st.title("Flight Booking ")

    # Input fields
    origin_city = st.text_input("Origin City", "Mumbai")
    destination_city = st.text_input("Destination City", "Delhi")
    depart_date = st.date_input("Departure Date", value=None)

    trip_type = st.radio("Select Trip Type", ["One way", "Round trip"])

    if trip_type == "Round trip":
        return_date = st.date_input("Return Date", value=None)
    else:
        return_date = None

    adults = st.number_input("Number of Adults", min_value=1, value=1)

    # Generate flight booking URL on button click
    if st.button("Generate Flight Booking URL"):
        if depart_date:
            depart_date_str = depart_date.strftime("%Y-%m-%d")
            return_date_str = return_date.strftime("%Y-%m-%d") if return_date else None
            booking_url = generate_flight_booking_url(origin_city, destination_city, depart_date_str, return_date_str, adults)
            st.markdown(f"Flight Booking URL: [{booking_url}]({booking_url})")
        else:
            st.error("Please select departure date.")

if __name__ == "__main__":
    main()


# import streamlit as st

# def generate_car_rental_url(destination):
#     base_url = "https://www.booking.com/cars/index.en-gb.html"
#     parameters = {
#         "aid": "304142",
#         "label": "gen173nr-1FEg1mbGlnaHRzX2luZGV4KIICQgVpbmRleEgJWARobIgBAZgBCbgBF8gBDNgBAegBAfgBA4gCAagCA7gCA0gCuqYGwBsACAeNzc5MmVjMmMtMTk3My00MWU4LThhOTktYjMwZmY0NTJmODTgAgXgAgE",
#         "sid": "aab3055d5652b78bccf80f82492c9b96",
#         "keep_landing": 1,
#         "ss": destination,  # 'ss' parameter represents the destination
#     }
#     encoded_parameters = "&".join([f"{key}={value}" for key, value in parameters.items()])
#     rental_url = f"{base_url}?{encoded_parameters}"
#     return rental_url

# def main():
#     st.title("Car Rental URL Generator")

#     # Input field
#     with st.form("destination_form"):
#         destination = st.text_input("Destination", "Enter destination")
#         submitted = st.form_submit_button("Generate Car Rental URL")

#     # Generate car rental URL on button click
#     if submitted:
#         if destination:
#             car_rental_url = generate_car_rental_url(destination)
#             st.markdown(f"Car Rental URL: [{car_rental_url}]({car_rental_url})")
#         else:
#             st.error("Please enter a destination.")

# if __name__ == "__main__":
#     main()
