import cv2
from firebase import firebase
import tkinter as tk
from tkinter import simpledialog, messagebox

firebase = firebase.FirebaseApplication('https://userdatabasesports-default-rtdb.firebaseio.com', None)

def scan():
    cap = cv2.VideoCapture(0)
    detector = cv2.QRCodeDetector()
    while True:
        _, img = cap.read()  # qrs have unique ids
        uid, bbox, _ = detector.detectAndDecode(img)
        if uid:
            cap.release()
            cv2.destroyAllWindows()
            return str(uid)
        cv2.imshow("QR Code Scanner", img)
        if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit the scanner
            cap.release()
            cv2.destroyAllWindows()
            break

def verify():
    uid = scan()
    if uid in firebase.get('/Users/', ''):
        user_type = firebase.get(f'/Users/{uid}/Type/', '')
        messagebox.showinfo('Verification', f'Verified User! Welcome. User Type: {user_type}')
    else:
        messagebox.showwarning('Verification', 'Unverified User! Registration required.')

def buy(product):
    uid = simpledialog.askstring('User ID', 'Enter User ID for Billing:')
    if not uid:
        messagebox.showwarning('Error', 'User ID cannot be empty!')
        return

    if uid in firebase.get('/Users/', ''):
        if product in firebase.get('/Shop', ''):
            cost = firebase.get(f'/Shop/{product}/Price', '')
            current = firebase.get(f'/Users/{uid}/Bill', 0)
            firebase.put('/Users/' + uid, 'Bill', current + cost)
            messagebox.showinfo('Billing', f'Thank you for shopping, {uid}! Price added to virtual wallet.')
        else:
            messagebox.showwarning('Invalid Product', 'Invalid product. Please try again.')
    else:
        messagebox.showwarning('Invalid User', 'User ID not found in database. Please try again.')

def on_button_verify():
    verify()

def on_button_buy():
    product = simpledialog.askstring('Product', 'Enter Product:')
    if product:
        buy(product)

root = tk.Tk()
root.title('QR Code Verification and Billing')

frame = tk.Frame(root)
frame.pack(padx=20, pady=20)

button_verify = tk.Button(frame, text='Verify User', command=on_button_verify)
button_verify.pack(fill=tk.X, padx=10, pady=5)

button_buy = tk.Button(frame, text='Buy Product', command=on_button_buy)
button_buy.pack(fill=tk.X, padx=10, pady=5)

root.mainloop()
