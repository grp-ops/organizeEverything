## organizeEverything

[Automate folder structure creation]
[Sort folders, drives and directories]

#### createPrjDirectory.py

Creates a master folder with internal subfolders for new projects.

**Requirements**

```
pip install tkinter
```


#### Use either as a .bat file or shell alias

**Windows**

Create .bat file by opening notepad:
```
@echo off 
python C:\path\to\createPrjDirectory.py
pause
```

Save as createPrjDirectory.bat in an easily accessible location to create project tree.


**Linux / MacOs**

Add as an alias in zshrc:

```
echo 'alias newprj="python3 createPrjDirectory.py"' | tee -a >> .zshrc
```

Add as an alias in bashrc:

```
echo 'alias newprj="python3 createPrjDirectory.py"' | tee -a >> .bashrc
```

Close & reopen your shell or:

```
source .zshrc
```

```
source .bashrc
```
