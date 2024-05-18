### Install Scoop (Run in Windows Terminal)
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
Invoke-RestMethod -Uri https://get.scoop.sh | Invoke-Expression
```
reference : [Scoop](https://scoop.sh/)


### Install pipx
```bash
scoop install pipx
pipx ensurepath
```
reference : [pipx documentation](https://pipx.pypa.io/stable/installation/)

### Install Python Poetry
```bash
pipx install poetry
```
reference : [poetry documentation](https://python-poetry.org/docs/#installing-with-pipx)

