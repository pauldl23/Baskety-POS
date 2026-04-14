# Baskety-POS

Welcome to **Baskety**, a comprehensive mini mart grocery store inventory configuration and point-of-sale (POS) management system! This Django-based application is designed to streamline product tracking, manage grocery stock, and facilitate fast sales transactions efficiently.

## Project Overview

Baskety provides a centralized solution for managing a mini mart's daily operations. It features a user-friendly dashboard for quick insights, a robust product management module, and a complete POS system tailored for fast-paced retail environments.

### Key Features

*   **Dashboard Analytics:** Get a bird's-eye view of your inventory and sales performance with interactive charts and summaries.
*   **Product Management:** Easily add, edit, view, and delete products in the system.
*   **Inventory Control:** Track stock levels, adjust quantities, and monitor low-stock items to ensure you never run out of essential supplies.
*   **Point of Sale (POS):** A dedicated interface for processing sales quickly and accurately, including a modern customer-facing display.
*   **Reporting:** Generate comprehensive reports on sales, inventory status, and other key metrics to inform decision-making.
*   **User Accounts & Roles:** Secure authentication system with different access levels to protect sensitive data.

---

## Getting Started (For Collaborators)

This section provides instructions for group members on how to set up the project locally and start contributing.

### Prerequisites

Before you begin, ensure you have the following installed on your machine:
*   [Python 3.x](https://www.python.org/downloads/)
*   [Git](https://git-scm.com/downloads)
*   [pip](https://pip.pypa.io/en/stable/installation/) (Python package installer)

### 1. Clone the Repository
First, clone the Baskety repository to your local machine:
```bash
git clone https://github.com/yanellebryan/Baskety.git
cd Baskety
```

### 2. Set Up a Virtual Environment
It is highly recommended to use a virtual environment to manage project dependencies and avoid conflicts with other Python projects.

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
Once the virtual environment is activated, install the required packages using `pip`:
```bash
pip install -r requirements.txt
```
*(Note: If `requirements.txt` is missing, the core dependency is `django`. Other dependencies may be added as the project evolves.)*

### 4. Apply Database Migrations
Initialize your local database by running the Django migrations:
```bash
python manage.py migrate
```

### 5. Create a Superuser (Optional but Recommended)
To access the Django admin panel, you'll need a superuser account:
```bash
python manage.py createsuperuser
```
Follow the prompts to set up your admin credentials.

### 6. Run the Development Server
Start the local server to see the project in action:
```bash
python manage.py runserver
```
Open your web browser and navigate to `http://127.0.0.1:8000/`.

---

## Workflow for Collaboration

To keep our codebase clean and organized, please follow this workflow when making contributions:

1.  **Always pull the latest changes** from the `main` branch before starting new work:
    ```bash
    git checkout main
    git pull origin main
    ```
2.  **Create a new branch** for your feature or bug fix. Give it a descriptive name:
    ```bash
    git checkout -b feature/your-feature-name
    ```
    *(e.g., `git checkout -b feature/add-new-reports`)*
3.  **Make your changes and test them locally.**
4.  **Commit your changes** with clear and concise messages:
    ```bash
    git add .
    git commit -m "Add new reporting feature for daily sales"
    ```
5.  **Push your branch** to the remote repository on GitHub:
    ```bash
    git push origin feature/your-feature-name
    ```
6.  **Open a Pull Request (PR)** on GitHub. Navigate to the repository, select your branch, and click "Compare & pull request". Provide a clear description of your changes and request a review from your groupmates.

Happy coding! Let's build something great together.
