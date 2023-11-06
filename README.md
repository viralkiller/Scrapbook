# github_instructions
instructions on how to configure pythonanywhere for github


# Change your remote URL from HTTPS to SSH:
git remote set-url origin git@github.com:username/repo.git

# Generate SSH on pythonanywhere
ssh-keygen -t ed25519 -C "your_email@example.com"
[add to github]

# Pull then push, pull issues can be resolved with:
git pull origin master --allow-unrelated-histories
[Choose option in VIM]
[ZZ to quit VIM]

