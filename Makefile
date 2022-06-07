# ----------------------------------
#          INSTALL & TEST
# ----------------------------------
install_requirements:
	@pip install -r requirements.txt

check_code:
	@flake8 scripts/* deep-pv/*.py

black:
	@black scripts/* deep-pv/*.py

test:
	@coverage run -m pytest tests/*.py
	@coverage report -m --omit="${VIRTUAL_ENV}/lib/python*"

ftest:
	@Write me

clean:
	@rm -f */version.txt
	@rm -f .coverage
	@rm -fr */__pycache__ */*.pyc __pycache__
	@rm -fr build dist
	@rm -fr deep-pv-*.dist-info
	@rm -fr deep-pv.egg-info

install:
	@pip install . -U

all: clean install test black check_code

count_lines:
	@find ./ -name '*.py' -exec  wc -l {} \; | sort -n| awk \
        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''
	@find ./scripts -name '*-*' -exec  wc -l {} \; | sort -n| awk \
		        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''
	@find ./tests -name '*.py' -exec  wc -l {} \; | sort -n| awk \
        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''

# ----------------------------------
#      UPLOAD PACKAGE TO PYPI
# ----------------------------------

PYPI_USERNAME=<AUTHOR>
build:
	@python setup.py sdist bdist_wheel

pypi_test:
	@twine upload -r testpypi dist/* -u $(PYPI_USERNAME)

pypi:
	@twine upload dist/* -u $(PYPI_USERNAME)

# ----------------------------------
#             GCP set-up and upload
# ----------------------------------
PROJECT_ID=deeppv-351812
BUCKET_NAME=wagon-data-907-deeppv
BUCKET_FOLDER=train_data

REGION=europe-west1
PACKAGE_NAME=DEEP-PV

MODULE=get_data
PACKAGE_NAME=deep_pv
LOCAL_PATH= /Users/ivanthung/code/ivanthung/deep-pv/models/trained_weights
BUCKET_FILE_NAME=$(shell basename ${LOCAL_PATH})

set_project:
	@gcloud config set project ${PROJECT_ID}

create_bucket:
	@gsutil mb -l ${REGION} -p ${PROJECT_ID} gs://${BUCKET_NAME}

upload_data:
	@gsutil cp -r ${LOCAL_PATH} gs://${BUCKET_NAME}/${BUCKET_FOLDER}/${BUCKET_FILE_NAME}

upload_weights:
	@gsutil cp -r ${LOCAL_PATH} gs://${BUCKET_NAME}/${BUCKET_FOLDER}/${BUCKET_FILE_NAME}

run_locally:
	@python -m ${PACKAGE_NAME}.${FILENAME}

get_predict_image_gcp:
	@python -m ${PACKAGE_NAME}.${MODULE}


### GCP AI Platform - - - - - - - - - - - - - - - - - - - -
##### Machine configuration - - - - - - - - - - - - - - - -

REGION=europe-west1
PYTHON_VERSION=3.7
FRAMEWORK=tensorflow
RUNTIME_VERSION=1.15
BUCKET_TRAINING_FOLDER=training_folder # non-existing
FILENAME=train.py # non-existing

gcp_submit_training:
	gcloud ai-platform jobs submit training ${JOB_NAME} \
		--job-dir gs://${BUCKET_NAME}/${BUCKET_TRAINING_FOLDER} \
		--package-path ${PACKAGE_NAME} \
		--module-name ${PACKAGE_NAME}.${FILENAME} \
		--python-version=${PYTHON_VERSION} \
		--runtime-version=${RUNTIME_VERSION} \
		--region ${REGION} \
		--stream-logs

# ----------------------------------
#             USE API
# ----------------------------------

run_api:
	uvicorn api.fast:app --reload

# ----------------------------------
#          HEROKU COMMANDS
# ----------------------------------

streamlit:
	-@streamlit run app.py

streamlit_test:
	-@streamlit run app_test.py

heroku_login:
	-@heroku login

heroku_create_app:
	-@heroku create ${APP_NAME}

deploy_heroku:
	-@git push heroku master
	-@heroku ps:scale web=1
