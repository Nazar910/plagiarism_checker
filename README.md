# Development
Prerequisites:
- set up virtual env
```bash
python3 -m venv plagiarism_checker_env
source ./plagiarism_checker_env/bin/activate
```
Note: to deactivate enter:
```bash
deactivate
```
- install deps
```
pip3 install --no-cache-dir -r requirements.txt
pip3 install --no-cache-dir -r requirements_dev.txt
```
- run unit tests
```
python3 -m unittest discover
```
- run one test
```
python3 -m unittest test.string_comparer.test_simhash.TestSimhash.test_return_true_when_similar
```
