#pip install requests
#pip install git+https://github.com/ozgur/python-firebasefrom firebase import firebase

firebase = firebase.FirebaseApplication('https://userdatabasesports-default-rtdb.firebaseio.com', None)

def scan():
        import cv2
        import webbrowser
        cap = cv2.VideoCapture(0)
        detector = cv2.QRCodeDetector()
        while True:
            _, img = cap.read() #qrs have unique ids
            uid, bbox, _ = detector.detectAndDecode(img) 
            if uid:
                return str(uid)
            cv2.waitKey(0)
            
def verify(): # at entry and check points
           
    uid = scan()
    if uid in firebase.get('/Users/', ''):
        print('Verified User! Welcome.',firebase.get('/Users/'+uid+'/Type/', ''))
    else:
        print('Unverified User! Registration required.')


def buy(product): # at food and shopping stalls 
    
    uid = str(782830)
    current=firebase.get('/Users/'+uid+'/Bill','')
    name=firebase.get('/Users/'+uid+'/Name','')
    if product in firebase.get('/Shop',''):
        cost=firebase.get('/Shop/'+product+'/Price', '')
        print(cost)
        firebase.put('/Users/'+uid,'Bill',current+cost)
        print("Thank you for shopping! Price added to virtual wallet.")
    else: 
        print('Invalid product. Please try again.')
        
fun=input("Enter V (Verifying User or Employee), B (Billing): ")

if fun=='V': #Verify
    verify()

if fun=='B': #Buy
    prod=input('Enter Product: ')
    buy(prod)
