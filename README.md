# RealTime-TaskDeliverySystem
This is a working example of RealTime Task delivery system. Through this system, a manager can create a new Task and in the realtime delivery, agents can accept the task. A task can be created with 3 different priority level:-
* HIGH 
* MEDIUM 
* LOW.

Each time a new task created with higher priority will replace the existing low priority task shown to the delivery agents in realtime.
Once a task is accepted by a delivery agent it will be removed from all other delivery agents portal in the real-time.

# Technologies used
* Django
* Web-sockets
* RabbitMQ (For realtime Task delivery)
* AWS (For deployment)
* PostgreSQL

# Demo Login
| Username  | Password  | User Type  |
|---|---|---|
| akshat |akshat@1234|StoreManager|
| akshat1|akshat@1234|Delivery Agent|
| akshat2|akshat@1234|Delivery Agent|

# Deployment URL
http://35.168.60.242:8000

# Project in Action
https://drive.google.com/file/d/1Gs8OnlPqrbn_HLiMHUxOUrWfW1EmozRz/view?usp=sharing Please watch this video for better understanding of the project

# Support
Please feel free to contact me for any kind of Questions/Suggestions about the project.
<br>Mail ID : akshat.khanna@st.niituniversity.in 
