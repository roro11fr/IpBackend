# IpBackend  
Steps to run this project:  
git clone https://github.com/roro11fr/IpBackend.git  
cd myProject  
python -m venv myVEnv # create virtual environment -only once  
source myVEnv/bin/activate  # Linux/macOS  
myVEnv\Scripts\activate     # Windows - activate environment  
pip install -r requirements.txt # install all libraries  
to run: python manage.py runserver  

Steps to connect project to the data base:   
download mysql and install from:  
1. Download and install MySQL Installer:  
  
Go to the official MySQL download page:  
https://dev.mysql.com/downloads/installer/ (choose version 8.xx)  
Install MySQL:  
Run the downloaded installer (mysql-installer-community-x.x.x.msi).  
In the setup type selection, choose Developer Default to install:  
MySQL Server  
MySQL Workbench  
Additional utilities like MySQL Shell and Router.  
Proceed with the installation, and follow these key steps during the process:  
Set up the MySQL Server (use default port 3306).  
Choose Standalone MySQL Server unless a custom configuration is needed.  
Set a root password (save it securely).  
Complete the installation. 

2. Set Environment Variables  
Go to Control Panel > System > Advanced system settings.  
Click Environment Variables, then edit the Path variable under System Variables.  
Add the MySQL bin folder path (e.g., C:\Program Files\MySQL\MySQL Server 8.0\bin).  
Restart the Command Prompt and verify:  
mysql -- version  

3. Create a New Database Schema  
Open MySQL Workbench.  
Connect to your local MySQL server (using the root user and password).  
Create a new database schema:  
Go to the Schemas tab.  
Right-click and choose Create Schema.  
Name the schema bazaip.  
Click Apply to save.  

4. Import the Provided SQL File  
In MySQL Workbench, open your schema (bazaip).  
Go to File > Open SQL Script.  
Select the SQL file you received.  
Execute the script using the lightning bolt icon.  

5. Configure Your Django Project  
Update settings.py for Database Connection  
In the myProject/settings.py file, update the DATABASES section with your MySQL credentials: 
DATABASES = {  
    'default': {  
        'ENGINE': 'django.db.backends.mysql',  
        'NAME': 'bazaip',        # Replace with your schema name  
        'USER': 'root',          # MySQL username  
        'PASSWORD': 'your_password',  # Replace with your root password  
        'HOST': '127.0.0.1',  
        'PORT': '3306',  
    }  
}  

6. Apply Django Migrations  
Run the following commands to set up your database tables:  
python manage.py makemigrations  
python manage.py migrate  

7. Run the Django Development Server  
Start your project server:  
python manage.py runserver  