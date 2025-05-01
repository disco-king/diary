# diary

Install in an env:
```
python3 -m venv venv
source ./venv/bin/activate
pip install --editable .
```

Install  systemwide (requires `pipx`):
```
pipx install --editable .
```

Run:
```
diary
```

Enable shell completion in bash:
```
echo 'eval "$(_DIARY_COMPLETE=bash_source diary)"' >> ~/.bashrc
```

