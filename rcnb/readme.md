# RAISE Centre for Nanobiotechnology Web Application

Welcome to the official repository for the RAISE Centre for Nanobiotechnology's web application\! 🔬

This is a comprehensive **Django web application** designed to serve as the digital hub for the Centre. It provides a platform for managing products, events, and a directory of startups, all while being configured for seamless deployment on **Railway**.

-----

## ✨ Key Features

This application is packed with features to support the Centre's operations and community engagement:

  * **User Authentication**: Secure and robust user registration and login system, allowing for personalized user experiences.
  * **Product Management**: A complete system for administrators to add, edit, and remove products offered by the Centre.
  * **E-commerce Functionality**:
      * **Shopping Cart**: A fully functional, intuitive shopping cart for a smooth purchasing process.
      * **Order Management**: A system for both users and administrators to track and manage orders.
      * **Favorites**: Allows users to save products they are interested in for later.
  * **Startup Directory**: A curated and searchable directory of startups associated with the Centre, showcasing their work and contact information.
  * **Events Calendar**: Keep the community informed about upcoming workshops, seminars, and other events.

-----

## 🚀 Setup and Installation

To get this project up and running on your local machine, follow these steps.

### 1\. Clone the Repository

First, clone this repository to your local machine using git:

```bash
git clone https://github.com/sterneesr/raise-nano.git
cd raise-nano/rcnb
```

### 2\. Install Dependencies

Install all the required Python packages using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### 3\. Configure Environment Variables

You'll need to set up your environment variables. Create a `.env` file in the `rcnb` directory. Copy the following content into the file and replace the placeholder values with your actual keys and credentials.

**.env file:**

```env
# Admin User Details
ADMIN_USER=your_admin_username
ADMIN_PASS=your_admin_password
ADMIN_EMAIL=your_admin_email

# Django Settings
SECRET_KEY=your_super_secret_django_key
DEBUG=True
DJANGO_ENV=development

# Database URL (e.g., for PostgreSQL)
DATABASE_URL=postgres://USER:PASSWORD@HOST:PORT/DATABASE_NAME

# Cloudinary API for Media Storage
CLOUDINARY_CLOUD_NAME=your_cloudinary_cloud_name
CLOUDINARY_API_KEY=your_cloudinary_api_key
CLOUDINARY_API_SECRET=your_cloudinary_api_secret

# Email Settings (using SendGrid)
EMAIL_HOST_USER=your_email_host_user
SENDGRID_API_KEY=your_sendgrid_api_key
```

**Note**: These keys are essential for the application to function correctly, especially for database connections, media file storage, and sending emails.

### 4\. Run Database Migrations

Apply the database schema by running the migrations:

```bash
python manage.py migrate
```

### 5\. Start the Development Server

You're all set\! Start the Django development server:

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`.

-----

## ☁️ Deployment on Railway

This application is pre-configured for easy deployment on the [Railway](https://railway.app/) platform. The `Procfile` and `build.sh` script included in the repository handle the build and deployment process.

When deploying on Railway, make sure to add the environment variables listed above to your Railway project's settings.

-----

## 🤝 Contributing & Contributors

This project was made possible by the hard work and dedication of a talented team. We welcome contributions from the community\! If you'd like to contribute, please fork the repository and submit a pull request.

### Project Contributors:

  * **Sternee**: [LinkedIn Profile](https://www.linkedin.com/in/sternee-sr-154990322/)
  * **Anu**: [LinkedIn Profile](https://www.google.com/search?q=https://www.linkedin.com/in/anu-selvam-17122a270)
  * **Maria**: [LinkedIn Profile](https://www.google.com/search?q=https://www.linkedin.com/in/maria-mistica-9b241a367)
  * **Ehasni**: [LinkedIn Profile](https://www.google.com/search?q=https://www.linkedin.com/in/ehasni-r-330021312)