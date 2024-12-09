# from flask import Flask, request, jsonify, render_template
# import pickle
# import os
# import smtplib
#
# app = Flask(__name__)
#
# # Load the model
# model = pickle.load(open("model.pkl", "rb"))
#
# print(f"Template folder path: {os.path.abspath('templates')}")
#
# @app.route("/")
# def home():
#     return render_template("index.html")
#
# @app.route("/predict", methods=["POST"])
# @app.route("/predict", methods=["POST"])
# def predict():
#     try:
#         # Parse input features from the form
#         square_feet = float(request.form["square_feet"])  # Convert to float
#         rooms = int(request.form["rooms"])  # Convert to integer
#         age = int(request.form["age"])  # Convert to integer
#         location = int(request.form["location"])  # Convert to integer
#
#         # Create input array for prediction
#         input_features = [[square_feet, rooms, age, location]]
#
#         # Predict using the model
#         prediction = model.predict(input_features)
#
#         return render_template("result.html", prediction=prediction[0])
#
#     except ValueError as e:
#         # Handle ValueError explicitly
#         return f"Input Error: {str(e)}"
#
#     except Exception as e:
#         # Handle any other errors
#         return f"Error: {str(e)}"
#
#
# def send_email(to_email, message):
#     # Simple SMTP logic (for demo purposes)
#     print(f"Sending email to {to_email}: {message}")
#
# if __name__ == "__main__":
#     app.run(debug=True)


from flask import Flask, request, jsonify, render_template
import pickle
import os
import smtplib

app = Flask(__name__)

# Load the model
model = pickle.load(open("model.pkl", "rb"))

@app.route("/")
def home():
    """
    Route for the home page.
    """
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
@app.route("/predict", methods=["POST"])
def predict():
    """
    Route for making predictions.
    """
    try:
        # Parse input features from the form
        square_feet = float(request.form["square_feet"])  # Convert to float
        rooms = int(request.form["rooms"])  # Convert to integer
        age = int(request.form["age"])  # Convert to integer
        location = request.form["location"].strip()  # Get location as a string

        # Map location string to numeric encoding
        location_mapping = {
            "Electronic City Phase II": 0,
            "Chikka Tirupathi": 1,
            "Uttarahalli": 2,
            "Lingadheeranahalli": 3,
            "Kothanur": 4,
            "Whitefield": 5,
            "Old Airport Road": 6,
            "Rajaji Nagar": 7,
            "Marathahalli": 8,
            "Gandhi Bazar": 9,
            "7th Phase JP Nagar": 10,
            "Gottigere": 11,
            "Sarjapur": 12,
            "Mysore Road": 13,
            "Bisuvanahalli": 14,
            "Raja Rajeshwari Nagar": 15,
            "Ramakrishnappa Layout": 16,
            "Manayata Tech Park": 17,
            "Kengeri": 18,
            "Binny Pete": 19,
            "Thanisandra": 20,
            "Bellandur": 21,
            "Mangammanapalya": 22,
            "Ramagondanahalli": 23,
            "Yelahanka": 24,
            "Hebbal": 25,
            "Kasturi Nagar": 26,
            "Kanakpura Road": 27,
            "Electronics City Phase 1": 28,
            "Kundalahalli": 29,
            "Chikkalasandra": 30,
            "Murugeshpalya": 31,
            "Ganga Nagar": 32,
            "HSR Layout": 33,
            "Doddathoguru": 34,
            "KR Puram": 35,
            "Himagiri Meadows": 36,
            "Adarsh Nagar": 37,
            "Lakshminarayana Pura": 38,
            "Begur Road": 39,
            "Devanahalli": 40,
            "Govindaraja Nagar Ward": 41,
            "Tharabanahalli": 42,
            "Varthur": 43,
            "Bommanahalli": 44,
            "Gunjur": 45,
            "Devarachikkanahalli": 46,
            "Double Road": 47,
            "Hegde Nagar": 48,
            "Haralur Road": 49,
            "Kalena Agrahara": 50,
            "Cholanayakanahalli": 51,
            "Kaval Byrasandra": 52,
            "ISRO Layout": 53,
            "Kodanda Reddy Layout": 54,
            "Garudachar Palya": 55,
            "EPIP Zone": 56,
            "Dasanapura": 57,
            "Kasavanhalli": 58,
            "Sanjay nagar": 59,
            "Mysore Highway": 60,
            "Domlur": 61,
            "Sarjapura - Attibele Road": 62,
            "Devasthanagalu": 63,
            "T Dasarahalli": 64,
            "Yeshwanthpur": 65,
            "Chandapura": 66,
            "Green View Layout": 67,
            "Shantiniketan Layout": 68,
            "Peenya": 69,
            "Nagarbhavi": 70,
            "Jalahalli West": 71,
            "Lakshmiamma Garden": 72,
            "Byatarayanapura": 73,
            "Ramamurthy Nagar": 74,
            "Kadugodi": 75,
            "LB Shastri Nagar": 76,
            "Vajarahalli": 77,
            "Hormavu": 78,
            "Vishwapriya Layout": 79,
            "Shampura": 80,
            "Akshaya Nagar": 81,
            "Shree Ananth Nagar Layout": 82,
            "Horamavu Agara": 83,
            "MCECHS layout": 84,
            "Coffee Board Layout": 85,
            "Ambedkar Nagar": 86,
            "Malleswaram": 87,
            "Nagasandra": 88,
            "Langford Town": 89,
            "Kudlu Gate": 90,
            "Akshaya Vana": 91,
            "Giri Nagar": 92,
            "Kogilu": 93,
            "Panathur": 94,
            "Nagondanahalli": 95,
            "Padmanabhanagar": 96,
            "1st Block Jayanagar": 97,
            "Kammasandra": 98,
            "Tala Cauvery Layout": 99,
            "Magadi Road": 100,
            "Ngef Layout": 101,
            "Koramangala": 102,
            "Lakshminarayanapura, Electronic City Phase 2": 103,
            "Muthurayya Swamy Layout": 104,
            "8th Phase JP Nagar": 105,
            "Budigere": 106,
            "Dodda Nekkundi Extension": 107,
            "Mylasandra": 108,
            "Kalyan nagar": 109,
            "Dr Shivarama Karantha Nagar": 110,
            "Bank Of Baroda Colony": 111,
            "Kullappa Colony": 112,
            "Mukkutam Nagar": 113,
            "Ashwath Nagar": 114,
            "Ncpr Industrial Layout": 115,
            "Muttarahalli": 116,
            "Maruthi Sevanagar": 117,
            "RMV 2nd Stage": 118,
            "Singasandra": 119,
            "Somasundara Palya": 120,
            "Muneshwara Nagar": 121,
            "Basaveshwara Nagar": 122,
            "Bull Temple Road": 123,
            "Kodihalli": 124,
            "Narayanapura": 125,
            "Binny Mills Employees Colony": 126
        }

        location_code = location_mapping.get(location, -1)

        if location_code == -1:
            return f"Error: Location '{location}' is not recognized. Please enter a valid location."

        # Debugging: Print parsed input
        print(f"Inputs: Square Feet={square_feet}, Rooms={rooms}, Age={age}, Location={location_code}")

        # Create input array for prediction
        input_features = [[square_feet, rooms, age, location_code]]

        # Predict using the model
        prediction = round(model.predict(input_features)[0], 2)  # Extract the first prediction
        print(prediction)

        # Render the result.html template and pass the prediction
        return render_template("result.html", result=prediction)

    except ValueError as e:
        # Handle ValueError explicitly
        return f"Input Error: {str(e)}"

    except Exception as e:
        # Handle any other errors
        return f"Error: {str(e)}"


# @app.route("/send_email", methods=["POST"])
# def send_email():
#     """
#     Route for sending email.
#     """
#     try:
#         # Parse email and message from the form
#         to_email = request.form["email"]  # User's email
#         location = request.form["location"]  # Example: Sending location details
#         message = f"The location you are interested in is: {location}"
#
#         # For demonstration, just print instead of sending an email
#         print(f"Sending email to {to_email}: {message}")
#
#         # Add actual email-sending logic if required (e.g., using SMTP)
#         # Uncomment below for real email functionality (you'll need SMTP credentials)
#         """
#         smtp_server = "smtp.example.com"
#         smtp_port = 587
#         sender_email = "your_email@example.com"
#         sender_password = "your_password"
#
#         with smtplib.SMTP(smtp_server, smtp_port) as server:
#             server.starttls()
#             server.login(sender_email, sender_password)
#             server.sendmail(sender_email, to_email, message)
#         """
#
#         return jsonify({"message": "Email sent successfully!", "to_email": to_email})
#
#     except Exception as e:
#         return jsonify({"error": str(e)})


if __name__ == "__main__":
    # Run the app
    app.run(debug=True)
