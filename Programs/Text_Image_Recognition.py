from base64 import b64encode
import googleapiclient.discovery
from oauth2client.client import GoogleCredentials
from tkinter import *
from tkinter.filedialog import *
import subprocess

# Launches Interface & Sets Dimensions
root = Tk()
root.title("Text Image Recognition")
root.geometry("800x480")

# Declares the text results variable to be used for displaying image recognition results
global _results
_results = StringVar()

# Declares the text location variable to be used for displaying the location on the image where the text was detected
global _location
_location = StringVar()

# Declares the browse file method that declares a filename variable which is defined by the askopenfilename method
def browseFile():
    global _filename
    _filename = askopenfilename()

# Declares the callToGoogleAPI method which sends the IMAGE_FILE variable off to the Google Cloud Vision API and
# collects the sent back results
def callToGoogleAPI():

    # Response back from request to the Google Cloud Vision API
    global response

    # Both the selected image file and the credentials file to the Google Cloud Vision API
    IMAGE_FILE = _filename
    CREDENTIALS_FILE = "credentials.json"

    # Used to connect to the Google Cloud-ML Service
    credentials = GoogleCredentials.from_stream(CREDENTIALS_FILE)
    service = googleapiclient.discovery.build('vision', 'v1', credentials=credentials)

    # Reads through the file and convert it to a base64 encoding
    with open(IMAGE_FILE, "rb") as f:
        image_data = f.read()
        encoded_image_data = b64encode(image_data).decode('UTF-8')

    # Creates the request object for the Google Cloud Vision API
    batch_request = [{
        'image': {
            'content': encoded_image_data
        },
        'features': [
            {
                'type': 'TEXT_DETECTION'
            }
        ]
    }]
    request = service.images().annotate(body={'requests': batch_request})

    # Sends the request object to Google to be executed
    response = request.execute()

    # Checks for an error, in the case of an error, the response will be set to the error that is retrieved
    if 'error' in response:
        raise RuntimeError(response['error'])
    printResults()

# Declares the printResults method, which takes the response and prints out the results to the console and program.
def printResults():

    # Extracts the text from the response
    extracted_texts = response['responses'][0]['textAnnotations']

    # Extracts the first piece of text found in the image
    extracted_text = extracted_texts[0]

    # Sets the _results variable value to the extracted text
    _results.set(extracted_text['description'])

    # Sets the _location variable value to the the location on the image where the text was detected
    _location.set(extracted_text['boundingPoly'])

    # Prints the extract text to the console
    print(extracted_text['description'])

    # Prints the location on the image where the text was detected to the console
    print(extracted_text['boundingPoly'])


# Declares the main frame of the program which contains all the elements inside it
mainFrame = Frame(root)
mainFrame.pack()

# Declares the HowTo Label Element
txtHowTo = Label(mainFrame, text="HOW TO USE")
txtHowTo.pack()

# Declares the Step1 Label Element
txtStep1 = Label(mainFrame, text="Step #1: Press 'Choose Image'")
txtStep1.pack()

# Declares the Step2 Label Element
txtStep2 = Label(mainFrame, text="Step #2: Select your image from the file explorer")
txtStep2.pack()

# Declares the Step3 Label Element
txtStep3 = Label(mainFrame, text="Step #3: Press 'Run'")
txtStep3.pack()

# Declares the Step4 Label Element
txtStep4 = Label(mainFrame, text="Step #4: The text detected from your image will be displayed")
txtStep4.pack()

# Declares the Choose Image Button Element, which initiates the browseFile method
btnChooseImage = Button(mainFrame, text="Choose Image", fg="red", command=browseFile)
btnChooseImage.pack(fill=X)

# Declares the Run Button Element, which initiates the callToGoogleAPI method
btnRun = Button(mainFrame, text="Run", fg="green", command=callToGoogleAPI)
btnRun.pack(fill=X)

# Declares the Results Label Element, which displays the value of the _results variable
txtResults = Label(mainFrame, textvariable = _results)
txtResults.pack(fill=X)

# Declares the Location Label Element, which displays the value of the _location variable
txtLocation = Label(mainFrame, textvariable = _location)
txtLocation.pack(fill=X, side=BOTTOM)

root.mainloop()

