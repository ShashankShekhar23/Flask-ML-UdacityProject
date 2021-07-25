# Flask-ML-UdacityProject
This is a repo for Udacity Project - Deploy Flask Machine Learning Application on Azure App Service

# Steps to run this project #

* Create a Github Repo
* Clone github repo through Azure Cloud Shell

`git clone <SSH-REPO-LINK>`
* Create scaffolding for project (if not created)
  * Makefile
  ```
  setup:
	python3 -m venv ~/.flask-ml-azure
	#source ~/.flask-ml-azure/bin/activate
	
  install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt
    
  test:
	#python -m pytest -vv --cov=myrepolib tests/*.py
	#python -m pytest --nbval notebook.ipynb
  
  lint:
	#hadolint Dockerfile #uncomment to explore linting Dockerfiles
	pylint --disable=R,C,W1203 app.py
  
  all: install lint test
  ```
  
  * requirements.txt
  ```
  Flask==1.0.2
  pandas==0.24.2
  scikit-learn==0.20.3
  ```
  
  * app.py
  ```
  from flask import Flask, request, jsonify
  from flask.logging import create_logger
  import logging
  
  import pandas as pd
  from sklearn.externals import joblib
  from sklearn.preprocessing import StandardScaler
  app = Flask(__name__)
  LOG = create_logger(app)
  LOG.setLevel(logging.INFO)

  def scale(payload):
    """Scales Payload"""

  LOG.info("Scaling Payload: %s payload")
  scaler = StandardScaler().fit(payload)
  scaled_adhoc_predict = scaler.transform(payload)
  return scaled_adhoc_predict

  @app.route("/")
  def home():
    html = "<h3>Sklearn Prediction Home</h3>"
    return html.format(format)

  # TO DO:  Log out the prediction value
  @app.route("/predict", methods=['POST'])
  def predict():
    """Performs an sklearn prediction
    input looks like:
            {
    "CHAS":{
      "0":0
    },
    "RM":{
      "0":6.575
    },
    "TAX":{
      "0":296.0
    },
    "PTRATIO":{
       "0":15.3
    },
    "B":{
       "0":396.9
    },
    "LSTAT":{
       "0":4.98
    }
    result looks like:
    { "prediction": [ 20.35373177134412 ] }
    """

    try:
        clf = joblib.load("boston_housing_prediction.joblib")
    except:
        LOG.info("JSON payload: %s json_payload")
        return "Model not loaded"

    json_payload = request.json
    LOG.info("JSON payload: %s json_payload")
    inference_payload = pd.DataFrame(json_payload)
    LOG.info("inference payload DataFrame: %s inference_payload")
    scaled_payload = scale(inference_payload)
    prediction = list(clf.predict(scaled_payload))
    return jsonify({'prediction': prediction})

  if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
    ```
    
    * Create `make_predict.sh` and `make_predict_azure_app.sh`
    
    make_predict.sh
    ```
    #!/usr/bin/env bash

    PORT=5000
    echo "Port: $PORT"

    # POST method predict
    curl -d '{  
   "CHAS":{  
      "0":0
   },
   "RM":{  
      "0":6.575
   },
   "TAX":{  
      "0":296.0
   },
   "PTRATIO":{  
      "0":15.3
   },
   "B":{  
      "0":396.9
   },
   "LSTAT":{  
      "0":4.98
   }
  }'\
     -H "Content-Type: application/json" \
     -X POST http://localhost:$PORT/predict
    ```
    
    make_predict_azure_app.sh
    ```
    #!/usr/bin/env bash

    PORT=443
    echo "Port: $PORT"

    # POST method predict
    curl -d '{
   "CHAS":{
      "0":0
   },
   "RM":{
      "0":6.575
   },
   "TAX":{
      "0":296.0
   },
   "PTRATIO":{
      "0":15.3
   },
   "B":{
      "0":396.9
   },
   "LSTAT":{
      "0":4.98
   }
  }'\
     -H "Content-Type: application/json" \
     -X POST https://<yourappname>.azurewebsites.net:$PORT/predict 
     #your application name <yourappname>goes here
    ```
    
* Create a python virtual environment and source it if not created
```
python3 -m venv ~/.<your-repo-name>
source ~/.<your-repo-name>/bin/activate
```
* Run `make all` which will install, lint and test code.
* Create an app service and initially deploy your app in Cloud Shell
`az webapp up -n <your-appservice-name>`
![FlaskMLAppService](https://user-images.githubusercontent.com/86247520/126907532-3197799b-ca81-4aa6-8797-823fce387bd0.PNG)
* Verify the deployed application works by browsing to the deployed url
`https://<your-appservice>.azurewebsites.net/`
![FlaskMLAppServiceURL](https://user-images.githubusercontent.com/86247520/126907571-4f70ce5b-7ae8-40cd-a764-d667ebd526e6.PNG)
* To make Prediction, change the line in `make_predict_azure_app.sh` to match the deployed prediction
`-X POST https://<your-appservice-name>.azurewebsites.net:$PORT/predict`
![PredictionAppService](https://user-images.githubusercontent.com/86247520/126907629-24b77722-4e16-4d16-8440-6d2a3a06c1c5.PNG)
* To check Logs for your running application, browse the URL:
`https://<your-appservice-name>.scm.azurewebsites.net/api/logs/docker`
![FlaskMLAppLog](https://user-images.githubusercontent.com/86247520/126907710-d15e7744-7fe7-4294-b265-c6b06f0ab806.PNG)
* Go to [Azure DevOps](https://dev.azure.com/) URL and create a new project
* Navigate to **Project Settings** >> **Service Connections**
* **Create a new service connection** via **Azure Resource Manager** (Take scope level as **Subscription**)
* Navigate to **Pipelines** and create a new one
* Create the **GitHub** Integration
* Configure **Python to Linux Web App on Azure**
* **Validate and configure** the pipeline
* The pipeline will build the Azure application. Once all the test pass, it will look like:
![FlaskMLAzurePipeline](https://user-images.githubusercontent.com/86247520/126907989-373c746e-92f9-4530-90bd-f46b2713bb7a.PNG)
