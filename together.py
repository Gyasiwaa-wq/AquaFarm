import streamlit as st
from PIL import Image
import random
import cv2
import numpy as np
import base64
import sqlite3
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, VideoTransformerBase



# Connect to SQLite database
conn = sqlite3.connect("users.db")
c = conn.cursor()

# Create users table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS users
             (username TEXT PRIMARY KEY, password TEXT, profile_picture BLOB)''')


# Helper functions for user authentication
def create_user(username, password):
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()

def authenticate_user(username, password):
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    result = c.fetchone()
    return result is not None

# Function to load CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Sign-up form
def sign_up():
    # Load the CSS file for styling
    local_css("style/auth.css")

    st.write("## Sign Up")
    new_username = st.text_input("Username")
    new_password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if new_password != confirm_password:
        st.error("Password and Confirm Password do not match.")
        return

    if st.button("Register"):
        create_user(new_username, new_password)
        st.success("Registration successful. Please sign in.")

# Sign-in form
def sign_in():
    # Load the CSS file for styling
    local_css("style/auth.css")
    
    st.write("## Sign In")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Log In"):
        if authenticate_user(username, password):
            st.success("Authentication successful!")
            # Return True and username to indicate successful login
            return True, username
        else:
            st.error("Invalid username or password")
            # Return False and None to indicate unsuccessful login
            return False, None
    else:
        # Return False and None to indicate login form hasn't been submitted yet
        return False, None
 

def init_session_state():
    if "user_progress" not in st.session_state:
        st.session_state.user_progress = {}

# Helper function to save user progress to session state
def save_user_progress(username, data):
    st.session_state.user_progress[username] = data

# Helper function to load user progress from session state
def load_user_progress(username):
    return st.session_state.user_progress.get(username, None)


def show_main_page(username,):
   # Set page width and layout
    st.set_page_config(layout="wide")

    init_session_state()
    
     # Get user progress from cookie
    user_progress = load_user_progress(username)
    # Navigation bar    
    st.markdown('<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css" rel="stylesheet">', unsafe_allow_html=True)   
    
    st.sidebar.markdown(f"""
        <style>

        .sidebar-content {{
            width: 100%;
        }}              

        .user-welcome{{
            font-family: 'Mulish', sans-serif;
            font-size: 20px;
            text-align: center; 
            color: #067eff;
            font-weight: bold;                                   
        }}
                        
        .pages a{{
        text-decoration: none;
        color: #626262;
        font-weight: 600;
        font-size: 18px;
        font-family: 'Mulish', sans-serif;
        }}

        .pages li{{
        list-style-type: none;
        margin-bottom: 1rem;
        padding: 5px;
        border-left: 1.8px solid #067eff;
        border-radius: 5px;
        }}

        .pages li:hover{{
        background-color: #e4f4fc;
        border-radius: 5px;
        border-left: 2.5px solid #3E8EDE;
        }}

        .css-6qob1r.e1fqkh3o3{{
        background: #fff;
       box-shadow:  0 2px 4px -1px #293066;
        }}

        .sidebar-icon{{
        margin-right: 7px; 
        color: #626262;
        }}

        .logo {{
        font-size: 30px;
        cursor: pointer;
        font-family: 'Mulish', sans-serif;
        font-weight: 800;
        color: #067eff;
        }}


        .fish {{
        font-style: normal;
        font-family: fontawesome;
        background: -webkit-linear-gradient(225deg, rgb(251, 175, 21), rgb(251, 21, 242),             
        rgb(21, 198, 251)) 0% 0% / 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: 2s ease 0s infinite normal none running fontgradient;
        -webkit-animation: fontgradient 2s ease infinite;
        -moz-animation: fontgradient 2s ease infinite;
        animation: fontgradient 2s ease infinite;  
        }}
        @-webkit-keyframes fontgradient {{
        0%{{background-position:0% 92%}}
        50%{{background-position:100% 9%}}
        100%{{background-position:0% 92%}}
        }}
        @-moz-keyframes fontgradient {{
        0%{{background-position:0% 92%}}
        50%{{background-position:100% 9%}}
        100%{{background-position:0% 92%}}
        }}
        @keyframes fontgradient {{
        0%{{background-position:0% 92%}}
        50{{background-position:100% 9%}}
        100%{{background-position:0% 92%}}
        }} 
        }}

        /* Add a style for the logout button */
        .logout-button {{
            margin-left: 80%;
            margin-top: 10px;
            font-size: 18px;
            padding: 5px 14px;
            background-color: transparent;
            color:  #067eff;
            border: 1.5px solid #067eff;
            border-radius: 5px;
            cursor: pointer;
        }}                
        
        </style>

        <div class="sidebar-content">
            <div class="sidebar-section">
                <p class="logo"><span class="sidebar-icon fish"><i class="fas fa-fish"></i></span>AquaFarm</p>
                <!-- Display the user welcome part -->
                <p class="user-welcome">Welcome, {username}!</p>
                <ul class="pages">    
                    <li ><span class="sidebar-icon"><i class="fas fa-home"></i></span><a href="#home">Home</a></li>
                    <li><span class="sidebar-icon"><i class="fas fa-info-circle"></i></span><a href="#about">About Us</a></li>
                    <li><span class="sidebar-icon"><i class="fas fa-user"></i></span><a href="#dashboard">Dashboard</a></li>
                    <li><span class="sidebar-icon"><i class="fa fa-hourglass-start" aria-hidden="true"></i></span><a href="#start">Get Started</a></li>
                    <li><span class="sidebar-icon"><i class="fas fa-envelope"></i></span><a href="#about">Contact Us</a></li>
                </ul>              
            </div>
        </div>
        """, unsafe_allow_html=True)
    # Logout button
    if st.sidebar.button("Logout"):
        # Clear the login status and username in the session state
        st.session_state.login_status = False
        st.session_state.username = None
        # Clear the user progress from the session state
        st.session_state.user_progress = {}
        # Show the authentication forms again
        st.experimental_rerun()
    
# Dashboard--------------------------
    st.markdown("""
        <style>
            .css-1vbkxwb.e16nr0p34 p {
                color: #067eff;
            }
            .css-1vbkxwb.e16nr0p34:hover{
                border-color: #067eff;
            }

        
        </style>
    """, unsafe_allow_html=True)
    

    # Hero section
    st.markdown(
        """
        <style>
        
        
        .hero-container {
            display: flex;
            flex-direction: row;
            justify-content: center;
            align-items: center;
            height: 75vh;
        }
        
        .hero-text {
            width: 50%;
            padding: 1rem;
            text-align: center;
            margin-right: 28px;
        }
        .hero-text h1{
            font-size: 75px;
            font-family: 'Montserrat', sans-serif;
            font-weight: 700;
            filter: drop-shadow(0px 2.5px 1.5px black);
            color: #067eff;
            margin-bottom: 0;
        }
        
        .summary p{
            color: #626262;
            font-size: 18px;
            font-weight: 600;
            font-family: 'Mulish', sans-serif;
        }
        .species{
            color: #626262;
            align-items: center;
            display: flex;
            flex-direction: column;
            font-size: 18px;
            font-family: 'Mulish', sans-serif;
            font-weight: 500;
        }

        .fish_species{
            display: flex;
            
        }

        .fish_species li{
            margin-right: 23px;
            font-weight: 600;
        }

        .hero-image {
            width: 50%;
            padding: 2rem;
            text-align: center;
            margin-top: 0;
        }
        .hero-image img {
            max-width: 100%;
            height: auto;
            border-radius: 10px;
            filter: drop-shadow(8px 8px 15px black);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    image_path = "images/fish_2.jpg"
    image = Image.open(image_path)

    

    st.markdown(
        """
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Mulish&display=swap" rel="stylesheet">
        <div class="hero-container"  id="home">
            <div class="hero-text">
                <div class="left">
                    <h1>AQUAFARM</h1>
                    <div class="species">
                        Experience Automated Excellence in Aquaculture. <br> Optimized for Three Fish Classes: 
                        <ul class="fish_species">
                            <li>Catfish</li>
                            <li>Tilapia</li>
                            <li>Mudfish</li>
                        </ul>
                    </div>
                </div>
            </div>
            <div class="hero-image">
                <img src="data:image/jpeg;base64,{}" alt="Fish Image">
            </div>
        </div>
        """.format(image_to_base64(image)),
        unsafe_allow_html=True,
    )

    def display_customer_satisfaction():
    # Customer satisfaction data (sample)
        customer_reviews = [
            {
                "name": "John Mensah",
                "review": "I am extremely satisfied with the automated fish rearing system. It has made my job much easier and efficient.",
                "rating": 5,
                "image": "images/fish_1.jpg"
            },
            {
                "name": "Yaw Opoku",
                "review": "The fish rearing system has exceeded my expectations. It's user-friendly and provides excellent results.",
                "rating": 4,
                "image": "images/fish_4.jpg"
            },
            {
                "name": "Adom Boateng",
                "review": "I highly recommend the automated fish rearing system. It has helped me optimize my fish farming process.",
                "rating": 5,
                "image": "images/fish_3.jpg"
            }
        ]

        st.subheader("Customer Satisfaction")
        st.write("See what our customers have to say about our automated fish rearing system.")

        for review in customer_reviews:
            col1, col2 = st.columns([1, 4])
            with col1:
                st.image(review["image"], caption=review["name"], width=100)
            with col2:
                st.write(f"**{review['name']}**")
                st.write(f"Rating: {review['rating']} stars")
                st.write(review["review"])
            st.write("---")


    st.markdown(
        """
        <style>
        body{
            font-size: 1.2rem;
        }
        .mission_vision{
            text-align: justify;
        }
        .about_section h1 {
            font-size: 2rem;
            margin-bottom: 1rem;
            color: #566e7c;
            font-weight: bold;
            text-align: center;
            font-family: 'Mulish', sans-serif;
        }
        .mission_title, .who_title, .contact_title , .intro{
            color: #566e7c;
            font-weight: bold;
            font-family: 'Mulish', sans-serif;
            font-size: 1.8rem;
        }
        .mission_text, .who_text, .contact_subtitle, .contact_info, .introduction{
            color: #626262;
            font-family: 'Mulish', sans-serif;
            
            font-size: 18px;
        }
        .contact_title ul li{
            font-size: 18px;
        }
        .css-5rimss {
            font-family: 'Mulish', sans-serif;
            font-size: 18px;
        }
        h2 {
            font-size: 2rem;
            margin-bottom: 1.5rem;
        }
        p {
            font-size: 1.1rem;
            line-height: 1.6;
            margin-bottom: 1.2rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )



    # About Us section
    st.markdown(
        """
        <div id="about">
            <div class="about_section">
            <br><br>
                <h1>ABOUT US</h1>
                <div class="mission_vision">
                    <h2 class="intro">Introduction</h2>
                    <p class="introduction">
                        At AquaFarm, our commitment to sustainability is at the core of everything we do. We recognize the importance of responsible 
                        aquaculture practices and their impact on the environment. That's why our automation systems are designed
                        to minimize resource consumption, monitor water quality, and promote the overall health of aquatic ecosystems.
                    </p>
                    <h2 class="mission_title">Mission and Vision</h2>
                    <p class="mission_text">
                         <b>Our mission</b> is to revolutionize the fish farming industry by providing advanced 
                        automated solutions that optimize fish rearing processes and improve productivity. We aim to become the 
                        leading provider of cutting-edge technology in aquaculture.
                        <br><br>
                        <b>Our vision</b> is to empower fish farmers with innovative tools and insights, enabling sustainable and 
                        efficient fish production worldwide. We strive to enhance profitability, environmental stewardship, 
                        and global food security through our automated fish rearing systems.
                    </p>
                    <h2 class="who_title">Sustainability and Responsibility</h2>
                    <p class="who_text">
                        At AquaFarm, we understand the critical importance of sustainability in aquaculture. We are committed to promoting 
                        responsible practices that minimize environmental impact and ensure the welfare of fish populations. Our solutions are designed 
                        to conserve resources, optimize water quality, and mitigate risks, allowing fish farmers to operate in an environmentally friendly and socially responsible manner.
                    </p>
                    <h2 class="who_title">Why AquaFarm?</h2>
                    <p class="who_text">
                        <b>Data-Driven Decision Making:</b> By uploading photos, images, and videos of their fishes, users can leverage the power of data analysis to gain valuable insights. 
                        The website's analysis tools can process the visual content and provide key information about the fish population, growth rates, size distribution, behavioral patterns, 
                        and overall health. This data-driven approach allows fish farmers to make informed decisions regarding feeding strategies, environmental adjustments, or health management protocols.<br><br>
                        <b>Monitoring and Performance Evaluation:</b> The analysis provided by the website can serve as a monitoring and performance evaluation tool. By comparing data over time, 
                        fish farmers can track the progress of their fish populations, identify trends, and assess the effectiveness of their rearing practices. This continuous evaluation enables 
                        farmers to optimize their operations, make necessary adjustments, and ensure the best possible outcomes for their fishes.<br><br>
                        <b>Efficient Farm Management:</b> The website's analysis and data reporting features provide a consolidated overview of the fish population's performance and status. This information
                        streamlines farm management by centralizing key metrics and facilitating informed decision-making. Fish farmers can access comprehensive reports, graphs, and trends that provide a clear 
                        understanding of their farm's productivity, allowing them to optimize resource allocation, plan for future growth, and maximize operational efficiency.<br><br>
                        <b>Early Detection of Issues:</b> The analysis of uploaded photos, images, and videos can help identify potential issues or anomalies within the fish population. By detecting early signs of disease, 
                        stress, or suboptimal conditions, fish farmers can take prompt action to mitigate risks and prevent widespread problems. This proactive approach to fish health management can save time, resources, 
                        and, most importantly, protect the overall well-being of the fish.<br><br>
                        <b>Research and Innovation:</b> The data and analysis obtained from the website can contribute to research efforts and innovation in fish rearing practices. Aggregated data from 
                        multiple users can be anonymized and used for broader scientific studies or industry benchmarking. Researchers and innovators can leverage this collective information to develop
                        new technologies, refine existing methodologies, and advance the field of fish farming.<br>
                    </p>
                    <br>
                </div>           
            </div>
        </div>
        """,
        unsafe_allow_html=True,        
    )
    # Customer satisfaction
    display_customer_satisfaction()
    
    
    # Use save_user_progress to save user progress
    save_user_progress(username, user_progress)


# Get Started Section
    st.markdown("""
    <style>
        .started{
            font-size: 2rem;
            margin-bottom: 1rem;
            color: #566e7c;
            font-weight: bold;
            text-align: center;
            font-family: 'Mulish', sans-serif;
        }
    </style>

    <div id="start">
        <h1 class="started">Getting Started</h1>
    </div>

    """, unsafe_allow_html=True)
        # Function to process the uploaded video
    def process_video(uploaded_video):
        # Perform analysis on the video using the machine learning model
        # Replace this with your own machine learning model code
        
        # Sample code to display the video
        video = cv2.VideoCapture(uploaded_video.name)
        while video.isOpened():
            ret, frame = video.read()
            if not ret:
                break
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            st.image(frame, channels="RGB")
        video.release()

    # Function to process the uploaded photo
    def process_photo(uploaded_photo):
        # Perform analysis on the photo using the machine learning model
        # Replace this with your own machine learning model code
        
        # Sample code to display the photo
        image = Image.open(uploaded_photo)
        st.image(image, caption='Uploaded Photo', use_column_width=True)

   
    st.write('Upload or record videos and photos for analysis')

    # File uploader for video
    uploaded_video = st.file_uploader('Upload a video', type=['mp4'])
    if uploaded_video is not None:
        st.video(uploaded_video)
        process_video(uploaded_video)

    # File uploader for photo
    uploaded_photo = st.file_uploader('Upload a photo', type=['jpg', 'jpeg', 'png'])
    if uploaded_photo is not None:
        process_photo(uploaded_photo)


    # Webcam video recorder    

    # Create a checkbox to enable video recording
    record_video = st.checkbox("Record Video")

    # Check if the checkbox is checked
    if record_video:
        # Use webrtc_streamer with a custom VideoProcessor to record video frames
        webrtc_streamer(
            key="example",
            rtc_configuration={ 
                "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
    }
)

    

    # Webcam photo capture   
    capture_photo = st.checkbox("Capture Photo")
    # Initialize the session state to store captured images
    if "captured_image" not in st.session_state:
        st.session_state.captured_image = None
    # Check if the checkbox is checked
    if capture_photo:
        # Check if the user has taken a photo
        if "captured_image" not in st.session_state:
            st.session_state.captured_image = False
            image_captured = st.camera_input("Capture Image", key="firstCamera")
        else:
            image_captured = st.camera_input("Capture Image", key="firstCamera")

        # Display the captured photo
        if image_captured:
            st.session_state.captured_image = image_captured
            st.image(st.session_state.captured_image, caption="Captured Photo", use_column_width=True)

    # Check if the user has captured a photo and show the download button
    if st.session_state.captured_image:
        st.download_button("Download Photo", data=st.session_state.captured_image, file_name="captured_photo.jpg")


    # Show a message when the checkbox is not checked
    if not capture_photo:
        st.write("Enable the checkbox above to capture a photo.")


# Get user progress from session state
    user_progress = load_user_progress(username)


# Dashboard Section
    st.markdown(f"""
    <style>
        .dashboard_section h2{{
            font-size: 2rem;
            margin-bottom: 1rem;
            color: #067eff;
            font-weight: bold;
            font-family: 'Mulish', sans-serif;
        }}
        .dashboard_section h1{{
            font-size: 2rem;
            margin-bottom: 1rem;
            color: #566e7c;
            font-weight: bold;
            text-align: center;
            font-family: 'Mulish', sans-serif;
        }}
    </style>

    <div class="dashboard_section" id="dashboard">
        <h1>Dashboard</h1>        
        <h2>Hello, {username}!</h2>
    </div>
           
    """, unsafe_allow_html=True)


    # Contact Us section

    st.markdown("""

    <style>
        .column1, {
            width: 30%;
            margin-right: 10px:
        }
        .column2{
            width: 40%;
        }
        .contact-form{
            display: flex;
            margin-top: 50px;
        }
        .column2{
            margin-left: 10px:
        }
        .space{
            width:8%;
        }
    </style>


    <div class="contact-form" id="contact">
        <div class="column1">
            <h3>Contact Us</h3>
                <form action="https://formsubmit.co/emmanuellagyasiwaa55@gmail.com" method="POST">
                    <input type="hidden" name="_captcha" value="false">
                    <input type="text" name="name" placeholder="Your name" required>
                    <input type="email" name="email" placeholder="Your email" required>
                    <textarea name="message" placeholder="Your message here"></textarea>
                    <button type="submit">Send</button>
                </form>
        </div>
        <div class="space">
        </div>
        <div class="column2">
            <div>
                <i class="fa fa-phone" aria-hidden="true"></i><br>
                <h3>Call Us</h3>
                <p>
                    0557741210<br>
                    0544093313
                </p>
            </div>
            <div>
                <i class="fa fa-envelope" aria-hidden="true"></i><br>
                <h3>Email Us</h3>
                <p>
                    emmanuellagyasiwaa55@gmail.com<br>
                    timoyeb20@gmail.com
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    

    # Use Local CSS File
    def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


    local_css("style/style.css")


    # Create a footer using a container
    footer = st.container()

    with footer:
        st.markdown(
            """
            <style>
            .footer {
                position: absolute;
                left: 0;
                top: 120px;
                width: 100%;
                color: #9a9a9a;
                padding: 10px;
                text-align: center;
            }
            </style>
            <div class="footer">
                <p>Copyright &copy; 2023 - AquaFarm Website</p>
            </div>
            """,
            unsafe_allow_html=True
        )


def image_to_base64(image):
    from io import BytesIO
    import base64

    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    image_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return image_base64


def main():
# Check if the user is logged in
    if "login_status" not in st.session_state:
        st.session_state.login_status = False
    if "username" not in st.session_state:
        st.session_state.username = None

    if not st.session_state.login_status:
        # User is not logged in, show the authentication forms
        st.title("User Authentication")
        choice = st.radio("Select an action:", ("Sign Up", "Sign In"))

        if choice == "Sign Up":
            sign_up()
        elif choice == "Sign In":
            login_successful, username = sign_in()
            if login_successful:
                # Update the login status and username in the session state
                st.session_state.login_status = True
                st.session_state.username = username
                # Clear the authentication components to display the main page in a new tab
                st.experimental_rerun()
    else:
        # User is already logged in, show the main page
        show_main_page(st.session_state.username)


    # Close the connection
    conn.close()

if __name__ == "__main__":
    main()