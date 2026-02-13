import customtkinter as ctk
from tkinter import messagebox
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

#ML Model training
training_comments = [
    "What is the price?",
    "How much does it cost?",
    "Is this available?",
    "Is it in stock?",
    "Amazing product",
    "I love this"
]
training_labels = [
    "price",
    "price",
    "availability",
    "availability",
    "positive",
    "positive"
]

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(training_comments)

model = MultinomialNB()
model.fit(X, training_labels)

#window work
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Social Media Manager Agent")
app.geometry("700x750")
ctk.set_appearance_mode('dark')

scheduled_posts = []

#Functions
def schedule_post():
    platform = platform_entry.get().strip()
    content = content_text.get("1.0", "end").strip()

    if not platform or not content:
        messagebox.showwarning("Error", "Please fill all fields")
        return

    post = f"Platform: {platform} | Content: {content}"
    scheduled_posts.append(post)
    posts_box.insert("end", post)

    platform_entry.delete(0, "end")
    content_text.delete("1.0", "end")

    messagebox.showinfo("Success", "Post Scheduled Successfully!")


def generate_caption():
    topic = topic_entry.get().lower().strip()

    if topic == "product":
        caption = "🚀 Check out our latest product! #NewLaunch"
    elif topic == "offer":
        caption = "🔥 Limited time offer! Grab it now!"
    elif topic == "festival":
        caption = "🎉 Celebrate with us! Special festive deals inside!"
    else:
        caption = "📢 Stay connected with us for updates!"

    caption_output.configure(text=caption)


def auto_reply():
    comment = comment_entry.get().strip()

    if not comment:
        messagebox.showwarning("Error", "Please enter a comment")
        return

    transformed = vectorizer.transform([comment])
    prediction = model.predict(transformed)[0]

    if prediction == "price":
        reply = "Please DM us for pricing details."
    elif prediction == "availability":
        reply = "Yes, it is available in stock."
    else:
        reply = "Thank you for your positive feedback!"

    reply_output.configure(text=reply)


def clear_posts():
    posts_box.delete("0.0", "end")
    scheduled_posts.clear()


#Scroll bar
main_frame = ctk.CTkScrollableFrame(app, width=650, height=700)
main_frame.pack(pady=10, padx=10, fill="both", expand=True)

header = ctk.CTkLabel(main_frame, text="Social Media Manager Agent", font=("Arial", 22, "bold"))
header.pack(pady=20)

#Schedule Frame
schedule_frame = ctk.CTkFrame(main_frame)
schedule_frame.pack(pady=10, padx=20, fill="both")

ctk.CTkLabel(schedule_frame, text="Schedule Post", font=("Arial", 16, "bold")).pack(pady=10)

platform_entry = ctk.CTkEntry(schedule_frame, width=500, placeholder_text="Enter Platform Name")
platform_entry.pack(pady=5)

content_text = ctk.CTkTextbox(schedule_frame, width=500, height=80)
content_text.pack(pady=5)

ctk.CTkButton(schedule_frame, text="Schedule Post", command=schedule_post).pack(pady=5)

#Posts Textbox with Scrollbar (Enabled by default in CTkTextbox)
posts_box = ctk.CTkTextbox(schedule_frame, width=500, height=120)
posts_box.pack(pady=5)

ctk.CTkButton(schedule_frame, text="Clear All Posts", fg_color="red", command=clear_posts).pack(pady=5)

#Caption
caption_frame = ctk.CTkFrame(main_frame)
caption_frame.pack(pady=10, padx=20, fill="both")

ctk.CTkLabel(caption_frame, text="Caption Generator", font=("Arial", 16, "bold")).pack(pady=10)

topic_entry = ctk.CTkEntry(caption_frame, width=500, placeholder_text="Enter topic (product/offer/festival)")
topic_entry.pack(pady=5)

ctk.CTkButton(caption_frame, text="Generate Caption", command=generate_caption).pack(pady=5)

caption_output = ctk.CTkLabel(caption_frame, text="")
caption_output.pack(pady=5)

#Auto Reply Frame
reply_frame = ctk.CTkFrame(main_frame)
reply_frame.pack(pady=10, padx=20, fill="both")

ctk.CTkLabel(reply_frame, text="Auto Reply (ML Based)", font=("Arial", 16, "bold")).pack(pady=10)

comment_entry = ctk.CTkEntry(reply_frame, width=500, placeholder_text="Enter user comment")
comment_entry.pack(pady=5)

ctk.CTkButton(reply_frame, text="Generate Reply", command=auto_reply).pack(pady=5)

reply_output = ctk.CTkLabel(reply_frame, text="")
reply_output.pack(pady=5)

app.mainloop()