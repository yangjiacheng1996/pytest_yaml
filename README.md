# pytest_yaml
get data from yaml and excute automatic tests

# Quick Start
## run cases
git clone https://github.com/yangjiacheng1996/pytest_yaml.git <br>
pip install -r requirements.txt  <br>
python run.py test -t sample.yml  <br>
## generate report
Please follow the output.  <br>
here give you a example  <br>
To generate report,install java then use command:  <br>
        D:\project\pytest_yaml\tools\allure\bin\allure generate D:\project\pytest_yaml\result -o D:\project\pytest_yaml\result\report --clean  <br>
To show report in browser,use command:  <br>
        D:\project\pytest_yaml\tools\allure\bin\allure open D:\project\pytest_yaml\result\report  <br>
