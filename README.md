# github_instructions
instructions on how to configure pythonanywhere for github

# Setup creds on pythonanywhere:
git config --global user.name "astaroth"
git config --global user.email "jules3313@gmail.com"

# Change your remote URL from HTTPS to SSH:

git remote add origin git@github.com:viralkiller/DAMI.git


git remote set-url origin git@github.com:viralkiller/DAMI.git

# Generate SSH on pythonanywhere
ssh-keygen -t ed25519 -C "your_email@example.com"
[add to github]

# Pull then push, pull issues can be resolved with:
git pull origin master --allow-unrelated-histories
[Choose option in VIM]
[ZZ to quit VIM]

ChatGPT:

If you'd like to push your PythonAnywhere Flask app directory to a new GitHub repository without installing anything on your local machine, you can do it directly from PythonAnywhere using the command line in your browser. Here are the steps:

1. **Set Up Git on PythonAnywhere**:
   - Log in to your PythonAnywhere account.
   - Open a Bash console from the Dashboard.
   - Configure Git with your username and email if you haven't already:
     ```
     git config --global user.name "Your Name"
     git config --global user.email "your_email@example.com"
     ```

2. **Create a New Repository on GitHub**:
   - Go to [GitHub](https://github.com) in your web browser.
   - Sign into your account.
   - Click on the "+" icon in the upper-right corner and select "New repository".
   - Fill out the form to create a new repository (don't initialize with a README if you're pushing an existing project).
   - Click "Create repository".

3. **Prepare Your Flask App**:
   - Make sure your Flask app does not contain sensitive data like secret keys or passwords; if it does, remove them or use environment variables.
   - On PythonAnywhere, navigate to your Flask app directory in the Bash console.
   - Create a `.gitignore` file to exclude files or directories that should not be uploaded to GitHub (like `__pycache__`, virtual environment directories, etc.).

4. **Initialize Your Local Repository on PythonAnywhere**:
   - In the Bash console, navigate to your Flask app directory (`cd path/to/your/flask_app`).
   - Initialize the directory as a Git repository with `git init`.

5. **Commit Your Flask App**:
   - Add all your files to the staging area with `git add .` (make sure your `.gitignore` is set up correctly).
   - Commit the changes with `git commit -m "Initial commit"`.

6. **Link Your Local Repository to Your GitHub Repository**:
   - Go back to your GitHub repository page to get the remote repository URL (it should be provided after you create the repo).
   - In the Bash console on PythonAnywhere, link your local repository to the GitHub repository with:
     ```
     git remote add origin YOUR_GITHUB_REPOSITORY_URL
     ```

7. **Push Your Code to GitHub**:
   - Push your commit to GitHub with:
     ```
     git push -u origin master
     ```
     or
     ```
     git push -u origin main
     ```
     (depending on the name of the branch you're pushing to, which is typically 'main' for new repositories).

After completing these steps, your code will be pushed from PythonAnywhere to your GitHub repository.

Please replace `YOUR_GITHUB_REPOSITORY_URL` with the actual URL of your GitHub repository, and `path/to/your/flask_app` with the actual path to your Flask application on PythonAnywhere.
